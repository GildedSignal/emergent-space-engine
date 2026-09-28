//! Work allocation (design and rules in docs/engine.md), generic over any
//! [`emergent_lattice::Stepper`].
//!
//! **Regions.** A containerless scene is cut into islands; each island is a region: a stepper
//! with its own clock. Regions merge (union of their worlds at a common accepted tick: whole
//! bodies, consumed contacts, summed ledgers) and split through one operation, the regroup.
//!
//! **Certificate (why the union equals one stepper over the whole scene).** Time is cut into
//! windows of G chronons. With no walls the outermost body's outward velocity cannot decrease
//! (a bounce impulse on it points away from every other centre; a stop sets it to zero; Pass
//! never changes), so the extent of an isolated region over a window is exactly the hull of
//! its extents at the window's two ends: its true box, measured, never forecast. Two
//! isolated regions of one window cannot have met if their true boxes are out of reach (on
//! some axis the gap exceeds the largest reach); whichever finishes the window second checks
//! the pair. By induction on bins the joint evolution equals the union of isolated ones (the
//! response is local to batch components, a contract guarantee), and logs merge by addition.
//! Forecast boxes (tracked speed × margin, never c: evolved speeds exceed it) only plan
//! merges ahead so that conflicts are rare.
//!
//! **Scoped rollback.** A conflict in window j rolls back only the two lineages (and any
//! region sharing a snapshot with them at the window start) to that start, where they
//! restart as one region. Their later truths are re-checked against everyone's, so knock-on
//! conflicts roll back lazily, only where they happen.
//!
//! **Finality (frames never see a revised past).** Frames draw only final snapshots. The
//! global all-verified tick is final: every pair up to it has been compared. A region is
//! final beyond it only with a hard speed bound given by the law (`Config::hard_speed`): then
//! no unfinished history, from any final state grown at that speed, can reach it. The
//! elastic law has no such bound (exchanges push light bodies past c), so under it every
//! region is shown at the global tick; a relativistic law restores per-region light-cone
//! finality and with it causal slack on screen.
//!
//! **Scheduling.** Least slack first: slack = (region tick + light delay to the observer −
//! present) / time acceleration − forecast cost of its next stride (kinetic theory
//! ½·n²·σ·v̄_rel fitted online to measured ops). Regions others wait for inherit their
//! deadline. Round 3 (each behind a `Config` switch, `Config::round2` turns all off):
//! SITA lanes pin regions costing more than a fair share of the workers to performance
//! workers; per-worker least-slack queues with stealing and event-driven bookkeeping replace
//! the scan of every region under the lock; certificate strides grow by one window per
//! accepted stride and halve on a rollback (AIMD), always stopping on a sync grid so every
//! region keeps a complete snapshot there; EEVDF-style eligibility keeps a stride from
//! starting while a lagging region could still reach it; hysteresis keeps a worker on its
//! region unless another is clearly more urgent. Units are `advance(target, budget)` with the
//! budget from a measured ops→time calibration (≈ 0.5 ms). Frames never simulate: they read
//! one published pointer. Forecasts, sabotage and scheduling change speed, never results.
mod alloc;
pub mod forecast;
pub mod geom;
pub mod qos;
pub mod report;
pub mod scenes;

pub use alloc::{speculation_horizon, Allocator, Config, Factory, FrameConfig, Snap, View};
pub use report::Report;
