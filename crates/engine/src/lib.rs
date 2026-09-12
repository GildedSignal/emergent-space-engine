//! Deterministic, generator-native causal mechanics.
//! Canonical laboratory law and experimental gravity are deliberately versioned separately.
pub const LAW_ID: &str = "es-inertial-causal-v1";
pub mod geometry;
pub mod math;
pub mod population;
pub mod propagator;
pub mod response;
pub mod runtime;
pub mod scenario;
pub mod storage;
pub use runtime::{AdvanceResult, Command, Engine, EngineError, EventRecord, WorkBudget};
