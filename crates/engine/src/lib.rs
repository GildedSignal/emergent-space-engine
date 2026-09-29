//! The dense order (docs/representation.md §3): a battle as a free-fall frame.
//!
//! [`frame`] is the frame: the Clohessy–Wiltshire tide as integer velocity kicks at fixed
//! epochs, with error-feedback carries. It runs the lattice law's two evaluation orders
//! through the `Kickable` hook on the steppers: lockstep (`emergent_lattice::chronon::Chronon`)
//! and sparse (`emergent_lattice_event::EventCore`, the epochs being scheduled events of the
//! frame that the core advances to). Both give identical bits ([`frame::Outcome`]).
//! [`scenes`] are the seeded battles the tests and cost probes use.
pub mod frame;
pub mod scenes;

pub use frame::{Battle, BattleStats, Frame, FrameError, Outcome, Weight};
