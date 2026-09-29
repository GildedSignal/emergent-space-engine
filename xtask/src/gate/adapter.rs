//! ADAPTER FROM THE CANONICAL CRATE `emergent-geodesic` TO THE GATE. NOT WIRED YET (a stub).
//!
//! `cargo run --release -p xtask -- gravity-gate` uses this evaluator by default. While it is
//! unwired the gate stops at once with GATES FAIL and says so. The integrator wires it when
//! `crates/geodesic` is merged. Steps:
//!
//! 1. `xtask/Cargo.toml`: add `emergent-geodesic = { path = "../crates/geodesic", features = ["test-support"] }`
//!    (the feature only exposes test controls; it must never replace the canonical schedule).
//! 2. Replace the `impl Evaluator for CrateEvaluator` below with the code in the block after
//!    these steps, and make `wired()` return true.
//! 3. The crate must provide what G2.2 compares (the harness reports missing ones as failures,
//!    never as skipped): `static_clock_rate` and `circular_clock_rate` in `Orbit`, and a
//!    `shapiro_delay(r1, r2)` method (see `Body::shapiro_delay` for the exact definition);
//!    `deflection` and the periods are already in the crate's `Orbit`.
//! 4. The reduced schedule (16, 32, 64 bits) is the crate's own test control; call it in
//!    `new_body_reduced`. Everything else is a field-by-field copy.
//!
//! ```ignore
//! use emergent_geodesic as g;
//! struct Wrap(g::Geodesic);
//! fn convert(r: Result<g::Geodesic, g::AnchorError>) -> Built {
//!     r.map(|x| Box::new(Wrap(x)) as Box<dyn Body>).map_err(|e| AnchorError(e.to_string()))
//! }
//! impl Body for Wrap {
//!     fn position(&self, t: i128) -> At {
//!         match self.0.position(t) {
//!             g::At::Free(x) => At::Free(x),
//!             g::At::Absorbed { chronon } => At::Absorbed { chronon },
//!             g::At::OutOfRange { chronon } => At::OutOfRange { chronon },
//!             g::At::Before => At::Before,
//!         }
//!     }
//!     fn proper_time(&self, t: i128) -> f64 { self.0.proper_time(t) }
//!     fn orbit(&self) -> Orbit {
//!         let o = self.0.orbit();
//!         Orbit { energy: o.energy, angular_momentum: o.angular_momentum, p: o.p, e: o.e, radial_period: o.radial_period,
//!             proper_radial_period: o.proper_radial_period, periapsis_advance: o.periapsis_advance, deflection: o.deflection,
//!             static_clock_rate: o.static_clock_rate, circular_clock_rate: o.circular_clock_rate,
//!             class: match o.class { g::OrbitClass::Bound => OrbitClass::Bound, g::OrbitClass::Unbound => OrbitClass::Unbound,
//!                 g::OrbitClass::Marginal => OrbitClass::Marginal, g::OrbitClass::Plunging => OrbitClass::Plunging,
//!                 g::OrbitClass::Radial => OrbitClass::Radial, g::OrbitClass::Circular => OrbitClass::Circular,
//!                 g::OrbitClass::Separatrix => OrbitClass::Separatrix } }
//!     }
//!     fn shapiro_delay(&self, r1: f64, r2: f64) -> Option<f64> { Some(self.0.shapiro_delay(r1, r2)) }
//! }
//! impl Evaluator for CrateEvaluator {
//!     fn name(&self) -> String { "emergent-geodesic".into() }
//!     fn new_body(&self, f: Field, q: i128, a: Anchor, m: Motion) -> Built {
//!         convert(g::Geodesic::new(g::Field { m: f.m }, q, g::Anchor { t: a.t, x: a.x, k: a.k },
//!             match m { Motion::Timelike => g::Motion::Timelike, Motion::Null => g::Motion::Null }))
//!     }
//!     fn new_body_reduced(&self, f: Field, q: i128, a: Anchor, m: Motion, schedule: &[u32]) -> Option<Built> {
//!         // The test-support constructor with the schedule [16, 32, 64] (its name is the crate's to choose).
//!         Some(convert(g::Geodesic::new_with_test_schedule(g::Field { m: f.m }, q, g::Anchor { t: a.t, x: a.x, k: a.k },
//!             match m { Motion::Timelike => g::Motion::Timelike, Motion::Null => g::Motion::Null }, schedule)))
//!     }
//! }
//! ```
use super::types::*;

pub struct CrateEvaluator;

impl Evaluator for CrateEvaluator {
    fn name(&self) -> String {
        "emergent-geodesic (adapter not wired)".into()
    }
    fn wired(&self) -> bool {
        false
    }
    fn new_body(&self, _f: Field, _q: i128, _a: Anchor, _m: Motion) -> Built {
        Err(AnchorError("the crate adapter is not wired: see xtask/src/gate/adapter.rs".into()))
    }
}
