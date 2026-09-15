//! Deterministic spacetime compiler for the inertial causal laboratory.
//! It compiles generators, certificates, responses and families rather than
//! stepping entities through ticks. Canonical laboratory law and experimental
//! gravity are deliberately versioned separately.
pub const LAW_ID: &str = "es-inertial-causal-v1";
/// Opt-in Packet 5 law. Default [`Engine::advance`](runtime::Engine::advance)
/// remains [`LAW_ID`]. Not G2 `es-causal-compiled-spacetime-v1`.
pub const TRUNCATED_COUPLED_LAW_ID: &str = emergent_law_lab::TRUNCATED_COUPLED_LAW_ID;
pub mod geometry;
pub mod math;
pub mod population;
pub mod propagator;
pub mod response;
pub mod runtime;
pub mod scenario;
pub mod storage;
pub mod truncated_gem;
pub use runtime::{
    AdvanceResult, Command, Engine, EngineError, EventRecord, Observation, ObserveResult, WorkBudget,
};
pub use truncated_gem::{DomainStatus, GeometryView, TruncatedAdmission};
