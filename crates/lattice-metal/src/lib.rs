//! Chronon mode on Metal for `es-lattice-elastic-v0` (step 5 of docs/work-allocation-design.md §7).
//!
//! [`MetalChronon`] reproduces [`emergent_lattice::chronon::Chronon`] bit for bit: world digest,
//! log digest, and the `ops`, `predicates`, `fired`, `batches` and `max_batch` metrics (the GPU
//! tests exactly the candidate pairs the reference grid tests, unless the GPU consumed-contact
//! table overflows, see [`Stats::table_overflows`]). `units` and `max_unit_ops` follow its own
//! slicing.
//!
//! Per chronon, on the GPU (shaders.metal): a snapshot (cells of side reach_max + 2·max|k_c|
//! as the reference, a counting sort into a spatially ordered torus of buckets, 32-byte
//! records), the 3×3-cell scan with the exact bin predicate, the advance and the wall set.
//! Contacts that form a component of their own (the common case: 96% of the 1M-ship gas)
//! are resolved on the GPU too (`settle`, `law::resolve` on one pair in i64 with overflow
//! guards; components commute, law.rs). The CPU resolves the rest with `law::resolve` in
//! i128 (components in parallel), logs, and patches the few records its response changed.
//! One-chronon command buffers also snapshot the next chronon, so each dense chronon costs one
//! GPU round trip; quiet chronons are encoded back to back and need none.
//!
//! # 64-bit exactness
//! The GPU evaluates `law::hit` in i64. Let C be the cell side, K = max|k_c| over bodies and
//! R = reach_max ≤ C. Pairs are only tested between adjacent cells, so |d_c| < 2C, |w_c| ≤ 2K,
//! reach ≤ R, and 2K ≤ C. Hence dd < 8C², |dw| < 8CK, ww ≤ 8K², rr·ww ≤ 8C²K², cross² < 64C²K²
//! and |d + w|² < 18C². Before every GPU batch the CPU checks **C·(K + 1) ≤ 2^28**, which puts
//! every product below 2^62 and lets velocities travel as i16 (K < 2^14), positions relative
//! to their cell as u32 and radii in 28 bits; and that **cell coordinates fit i32** for the
//! batch (max|x_c| is tracked as a bound). Velocities change only in responses, which end a
//! batch. Otherwise the chronon runs on the CPU path, the reference grid in i128. `settle`
//! hands any pair whose impulse arithmetic might leave i64 to the CPU (float bounds with a
//! factor 4 of slack); full pair buffers are regrown and the chronon rerun. Nothing is ever
//! rounded.
use std::time::Duration;

#[cfg(target_os = "macos")]
mod gpu;
#[cfg(target_os = "macos")]
pub use gpu::MetalChronon;

#[derive(Debug)]
pub enum MetalError {
    NoDevice,
    Shader(String),
    Law(emergent_lattice::law::LawError),
}

impl std::fmt::Display for MetalError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            MetalError::NoDevice => f.write_str("no Metal device"),
            MetalError::Shader(s) => write!(f, "Metal shader: {s}"),
            MetalError::Law(e) => write!(f, "law: {e}"),
        }
    }
}

impl std::error::Error for MetalError {}

impl From<emergent_lattice::law::LawError> for MetalError {
    fn from(e: emergent_lattice::law::LawError) -> Self {
        MetalError::Law(e)
    }
}

/// Tuning and test hooks. The outcome never depends on them.
#[derive(Clone, Debug)]
pub struct Options {
    /// Most chronons encoded in one command buffer (1..=64).
    pub max_batch: u64,
    /// Initial pair buffer capacity; 0 picks n/8 + 4096. It grows on overflow.
    pub pair_capacity: u32,
    /// Run chronon t on the CPU path when t is a multiple of this (0: only when the
    /// precondition fails). Exercises GPU/CPU hand-over.
    pub cpu_every: i64,
    /// Events per chronon from which the CPU response is spread over threads.
    pub par_min: usize,
    /// Response threads; 0 uses the available parallelism (at most 8).
    pub threads: usize,
    /// Resolve isolated contacts on the GPU (one-chronon buffers).
    pub gpu_settle: bool,
}

impl Default for Options {
    fn default() -> Self {
        Options { max_batch: 64, pair_capacity: 0, cpu_every: 0, par_min: 512, threads: 0, gpu_settle: true }
    }
}

/// Where the chronons went (not part of the canonical outcome).
#[derive(Clone, Debug, Default)]
pub struct Stats {
    pub gpu_chronons: u64,
    /// Chronons run on the CPU path (precondition, `cpu_every`, empty worlds).
    pub cpu_chronons: u64,
    pub command_buffers: u64,
    /// Chronons encoded, including those skipped after an earlier event in their buffer.
    pub encoded: u64,
    /// Chronons rerun because the pair buffer was full.
    pub pair_overflows: u64,
    /// Consumed contacts the GPU table could not hold (the CPU still filters them exactly;
    /// only the predicate count can then exceed the reference's).
    pub table_overflows: u64,
    /// Contacts resolved on the GPU (isolated pairs).
    pub settled: u64,
    /// GPU hits the CPU dropped as already consumed.
    pub filtered: u64,
    /// Next-chronon snapshots discarded because the response changed the cell side.
    pub missed: u64,
    /// Wall time from commit to completion of command buffers.
    pub gpu_wait: Duration,
    /// GPU execution time of those command buffers (GPUStartTime to GPUEndTime).
    pub gpu_busy: Duration,
    /// Wall time in CPU responses (resolve, consume, log).
    pub respond: Duration,
}

#[cfg(not(target_os = "macos"))]
pub use stub::MetalChronon;

#[cfg(not(target_os = "macos"))]
mod stub {
    use super::{MetalError, Options, Stats};
    use emergent_lattice::{law::Tick, Log, Metrics, Stepper, World};

    /// Metal exists only on Apple targets; construction always fails here.
    pub enum MetalChronon {}

    impl MetalChronon {
        pub fn new(_: World, _: bool) -> Result<Self, MetalError> {
            Err(MetalError::NoDevice)
        }
        pub fn with_options(_: World, _: bool, _: Options) -> Result<Self, MetalError> {
            Err(MetalError::NoDevice)
        }
        pub fn stats(&self) -> &Stats {
            match *self {}
        }
    }

    impl Stepper for MetalChronon {
        fn tick(&self) -> Tick {
            match *self {}
        }
        fn advance(&mut self, _: Tick, _: u64) -> Tick {
            match *self {}
        }
        fn world(&self) -> World {
            match *self {}
        }
        fn log(&self) -> &Log {
            match *self {}
        }
        fn metrics(&self) -> &Metrics {
            match *self {}
        }
    }
}
