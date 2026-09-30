//! The dense order (docs/representation.md §3): a battle as a free-fall frame.
//!
//! [`frame`] is the frame: the Clohessy–Wiltshire tide as integer velocity kicks at fixed
//! epochs, with error-feedback carries. It runs the lattice law's two evaluation orders
//! through the `Kickable` hook on the steppers: lockstep (`emergent_lattice::chronon::Chronon`)
//! and sparse (`emergent_lattice_event::EventCore`, the epochs being scheduled events of the
//! frame that the core advances to). Both give identical bits ([`frame::Outcome`]).
//! [`anchor`] is re-anchoring: the frame recentres on its members' centre of mass, moves its
//! reference circle to the tube's guiding centre and hands members out of the size rule, as
//! events of the law, bit-identical in both orders. [`scenes`] are the seeded battles the
//! tests and cost probes use.
pub mod anchor;
pub mod frame;
pub mod scenes;

pub use anchor::{recentre, AnchorPolicy, AnchorReport, Handoff, Recentred, Tube};
pub use frame::{Battle, BattleStats, Frame, FrameError, Outcome, Weight};
