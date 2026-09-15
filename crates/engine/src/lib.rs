//! Deterministic spacetime compiler for the inertial causal laboratory.
//! It compiles generators, certificates, responses and families rather than
//! stepping entities through ticks. Canonical laboratory law and experimental
//! gravity are deliberately versioned separately.
pub const LAW_ID: &str = "es-inertial-causal-v1";
pub mod archive;
pub mod authority;
pub mod composition;
pub mod coupled_adapter;
pub mod geometry;
pub mod math;
pub mod policy;
pub mod population;
pub mod propagator;
pub mod response;
pub mod runtime;
pub mod scenario;
pub mod scheduler;
pub mod storage;
pub use archive::{ArchiveManifest, HistoryChunk, HistoryRemainder, LiveArchive};
pub use composition::ReceptionIndex;
pub use policy::{
    compile_policy, evaluate_policy, evaluate_policy_bytecode, Broadcast, BroadcastReception, Guard,
    OmniscientDiagnostic, PolicyAction, PolicyBytecode, PolicyOutcome, PolicyProgram, PolicyRule,
    ReceivedKnowledge,
};
pub use runtime::{
    AdvanceResult, Command, Engine, EngineError, EventRecord, Observation, ObserveResult, WorkBudget,
};
pub use scheduler::{CompositionScheduler, IncomingInfluence, Region};
