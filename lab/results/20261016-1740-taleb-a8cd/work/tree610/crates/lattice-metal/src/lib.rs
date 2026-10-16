//! Chronon mode on Metal for the lattice law (docs/archive/engine.md).
//!
//! [`MetalChronon`] reproduces [`emergent_lattice::chronon::Chronon`] bit for bit under every
//! law: world digest, log digest, and the `ops`, `predicates`, `fired`, `batches` and
//! `max_batch` metrics (the GPU tests exactly the candidate pairs the reference grid tests,
//! unless the GPU consumed-contact table overflows, see [`Stats::table_overflows`]). `units`
//! and `max_unit_ops` follow its own slicing.
//!
//! The chronon loop lives on the GPU (shaders.metal): up to 64 chronons per command buffer,
//! each one the reference's cell side from the exact max|k_c|, a counting sort into a
//! spatially ordered torus of buckets, the pair scan with the exact bin predicate, the advance
//! and wall set, and the response: the batch splits into connected components (they commute,
//! law.rs) and each is resolved by the law's rule (`law::resolve`, `relativity::resolve_law`
//! for es-lattice-relativistic-v0 and -v1), consumed and logged. The relativistic bounce is
//! staged for every hit: the reflection while its bodies are classified, then eight threads
//! for the eight candidate 4-momenta, then the pick (isolated pairs in one thread each; larger
//! components reuse the staged work for contacts whose bodies have not bounced yet). The CPU
//! hashes the event log while the next buffer runs. A chronon holding a component the GPU may
//! not resolve exactly (a checked range left, a full table row or log, a component too large
//! to follow) stops the buffer; the CPU resolves those components with `law::respond` in i128
//! or big integers (in parallel) and the loop resumes.
//!
//! [`MetalChronon`] is also [`emergent_lattice::Kickable`] (src/gpu/kickable.rs): the free-fall frame of
//! `crates/engine` kicks and re-anchors it between chronons, with `Chronon`'s semantics, so a battle
//! runs on the GPU bit for bit as on the CPU or the event core.
//!
//! # Exactness
//! The GPU evaluates `law::hit` in i64. Let C be the cell side, K = max|k_c| over bodies and
//! R = reach_max ≤ C. Pairs are only tested between adjacent cells, so |d_c| < 2C, |w_c| ≤ 2K,
//! reach ≤ R, and 2K ≤ C. Hence dd < 8C², |dw| < 8CK, ww ≤ 8K², rr·ww ≤ 8C²K², cross² < 64C²K²
//! and |d + w|² < 18C². Before every chronon the GPU checks **C·(K + 1) ≤ 2^28**, which puts
//! every product below 2^62 and lets velocities travel as i16 (K < 2^14), positions relative
//! to their cell as u32 and radii in 28 bits; the CPU checks that **cell coordinates fit i32**
//! for the whole buffer (max|x_c| is tracked as a bound). Otherwise the chronon runs on the
//! CPU path, the reference grid in i128.
//!
//! The Newtonian bounce runs in i64 with |k_c| < 2^18, |d_c| < 2^30, carries < 2^60 and float
//! bounds below 2^60 on the rounding denominator and numerators. The relativistic bounce runs
//! in exact integer arithmetic, 128-bit values built from 64-bit halves (every operation that
//! could overflow is checked):
//! - **4-momenta.** v0: Q ≤ 2^15, so F²Q² < 2^62 and Γ < 2^31. v1: Q ≤ 2^20 (the law's whole
//!   range). Its parts are ⌊t/√s⌋ with t = 2Q³ or 2Q²|k_c| and s = Q² − |k|², found as the
//!   v with v²s ≤ t² < (v+1)²s from a float estimate: for Q ≤ 2^10 (t ≤ 2^31) the brackets are
//!   96-bit products of 32-bit limbs, first a window of two around the estimate, which settles
//!   nearly every root of a gas at Q = 2^10; above that 128-bit brackets (t² < 2^123); far off (near c)
//!   float Newton steps on the exact residual. Both versions: 4-momentum parts and carries
//!   below 2^60 (m·E < 2^59 for v1, bounded in floats).
//! - **Reflection.** The Minkowski normal's parts below 2^62, so T = N·N and S = p·N fit 126
//!   bits. The target floors ⌊Q·x/e⌋, (e, x, y) = T·p ∓ 2S·N, are decided in floats when a
//!   proven error bound (IEEE, with a factor of 3 to spare, and ratios only so nothing
//!   overflows) keeps each target inside one open unit interval; otherwise exactly, with the
//!   targets and their Q-multiples within 2^127. The filter decides nearly every floor up to
//!   Q = 2^12; it also resolves contacts whose exact targets would leave 128 bits (v1 at
//!   Q = 2^16). At Q = 2^20 a contact's normal leaves 62 bits and the CPU responds.
//! - **Pick.** |owed + e| < 2^62 for the squared scores (in 64 bits below 2^31).
//!
//! A contact outside these ranges is handed, with its whole component, to the CPU. Floats
//! only estimate: every quotient, square root and floor is verified in integers, except where
//! an IEEE error bound decides it with a wide margin (float math is compiled without
//! fast-math). Full pair buffers are regrown and the chronon rerun. Nothing is ever rounded.
use std::time::Duration;

#[cfg(target_os = "macos")]
mod gpu;
#[cfg(target_os = "macos")]
pub use gpu::MetalChronon;
#[cfg(target_os = "macos")]
#[doc(hidden)]
pub use gpu::{float_floors_probe, v1_momenta};

/// A test case for [`float_floors_probe`]: (Q, T, 2S, p, n).
#[doc(hidden)]
pub type FloorCase = (i64, i128, i128, [i64; 3], [i64; 3]);

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
    /// Resolve contact components on the GPU; false leaves every response to the CPU.
    pub gpu_response: bool,
    /// Profiling: every dispatch in a command buffer of its own, its GPU time summed per
    /// kernel in [`Stats::kernels`]. The same work in the same order (only slower).
    pub profile: bool,
}

impl Default for Options {
    fn default() -> Self {
        Options { max_batch: 64, pair_capacity: 0, cpu_every: 0, par_min: 512, threads: 0, gpu_response: true, profile: false }
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
    /// With [`Options::profile`]: GPU time and dispatches per kernel.
    pub kernels: Vec<(&'static str, Duration, u64)>,
}

#[cfg(not(target_os = "macos"))]
pub use stub::{float_floors_probe, v1_momenta, MetalChronon};

#[cfg(not(target_os = "macos"))]
mod stub {
    use super::{MetalError, Options, Stats};
    use emergent_lattice::{law::Tick, Kickable, Log, Metrics, Motion, Stepper, World};

    /// Metal exists only on Apple targets; construction always fails here.
    pub enum MetalChronon {}

    #[doc(hidden)]
    pub fn v1_momenta(_: i64, _: &[(i64, [i64; 2])]) -> Result<Vec<Option<[i64; 3]>>, MetalError> {
        Err(MetalError::NoDevice)
    }

    #[doc(hidden)]
    pub fn float_floors_probe(_: &[crate::FloorCase]) -> Result<Vec<Option<[i64; 2]>>, MetalError> {
        Err(MetalError::NoDevice)
    }

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

    impl Kickable for MetalChronon {
        fn motions(&self, _: &mut Vec<Motion>) {
            match *self {}
        }
        fn kick(&mut self, _: &[[i64; 2]]) -> Result<(), emergent_lattice::law::LawError> {
            match *self {}
        }
        fn masses(&self, _: &mut Vec<i64>) {
            match *self {}
        }
        fn rebase(&mut self, _: &[[i64; 2]], _: &[[i64; 2]]) -> Result<(), emergent_lattice::law::LawError> {
            match *self {}
        }
    }
}
