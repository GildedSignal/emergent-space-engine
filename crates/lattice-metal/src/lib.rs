//! Chronon mode on Metal for the lattice law (step 5 of docs/work-allocation-design.md §7).
//!
//! [`MetalChronon`] reproduces [`emergent_lattice::chronon::Chronon`] bit for bit under both
//! laws: world digest, log digest, and the `ops`, `predicates`, `fired`, `batches` and
//! `max_batch` metrics (the GPU tests exactly the candidate pairs the reference grid tests,
//! unless the GPU consumed-contact table overflows, see [`Stats::table_overflows`]). `units`
//! and `max_unit_ops` follow its own slicing.
//!
//! The chronon loop lives on the GPU (shaders.metal): up to 64 chronons per command buffer,
//! each one the reference's cell side from the exact max|k_c|, a counting sort into a
//! spatially ordered torus of buckets, the pair scan with the exact bin predicate, the advance
//! and wall set, and, under the Newtonian law, the response: the batch splits into connected
//! components (they commute, law.rs) and each is resolved by `law::resolve`'s rule in i64,
//! consumed and logged. The CPU hashes the event log while the next buffer runs. A chronon
//! holding a component the GPU may not resolve exactly (the relativistic law, a guard, a full
//! table row or log, a component too large to follow) stops the buffer; the CPU resolves those
//! components with `law::respond` in i128 (in parallel) and the loop resumes.
//!
//! # 64-bit exactness
//! The GPU evaluates `law::hit` in i64. Let C be the cell side, K = max|k_c| over bodies and
//! R = reach_max ≤ C. Pairs are only tested between adjacent cells, so |d_c| < 2C, |w_c| ≤ 2K,
//! reach ≤ R, and 2K ≤ C. Hence dd < 8C², |dw| < 8CK, ww ≤ 8K², rr·ww ≤ 8C²K², cross² < 64C²K²
//! and |d + w|² < 18C². Before every chronon the GPU checks **C·(K + 1) ≤ 2^28**, which puts
//! every product below 2^62 and lets velocities travel as i16 (K < 2^14), positions relative
//! to their cell as u32 and radii in 28 bits; the CPU checks that **cell coordinates fit i32**
//! for the whole buffer (max|x_c| is tracked as a bound). Otherwise the chronon runs on the
//! CPU path, the reference grid in i128. The GPU response hands any component whose impulse
//! arithmetic might leave i64 to the CPU (|k_c| < 2^18, |d_c| < 2^30, carries < 2^60, float
//! bounds below 2^60 on the rounding denominator and numerators); full pair buffers are
//! regrown and the chronon rerun. Nothing is ever rounded.
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
    /// Resolve contact components on the GPU (Newtonian law); false leaves every response
    /// to the CPU.
    pub gpu_response: bool,
}

impl Default for Options {
    fn default() -> Self {
        Options { max_batch: 64, pair_capacity: 0, cpu_every: 0, par_min: 512, threads: 0, gpu_response: true }
    }
}

/// Where the chronons went (not part of the canonical outcome).
#[derive(Clone, Debug, Default)]
pub struct Stats {
    /// Chronons detected on the GPU (responded there, or on the CPU after a halt).
    pub gpu_chronons: u64,
    /// Chronons run entirely on the CPU path (precondition, `cpu_every`, empty worlds).
    pub cpu_chronons: u64,
    pub command_buffers: u64,
    /// Chronons encoded, including those skipped after a halt in their buffer.
    pub encoded: u64,
    /// Command buffers that stopped for a CPU response.
    pub halts: u64,
    /// Contacts resolved on the GPU and on the CPU.
    pub gpu_contacts: u64,
    pub cpu_contacts: u64,
    /// Chronons rerun because the pair buffer was full.
    pub pair_overflows: u64,
    /// Consumed contacts the GPU table could not hold (the CPU still filters them exactly;
    /// only the predicate count can then exceed the reference's).
    pub table_overflows: u64,
    /// GPU hits the CPU dropped as already consumed.
    pub filtered: u64,
    /// Wall time from commit to completion of command buffers.
    pub gpu_wait: Duration,
    /// GPU execution time of those command buffers (GPUStartTime to GPUEndTime).
    pub gpu_busy: Duration,
    /// Wall time in CPU responses after halts.
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
