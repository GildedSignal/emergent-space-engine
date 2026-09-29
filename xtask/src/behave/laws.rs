//! The laws the judge can meet without a physics core. `echo` answers with the oracle, so every
//! gate must pass. Each planted law has one flaw and must fail exactly the gate that guards it:
//! together they prove the judge can fail (a test that cannot fail is a control).
use super::{oracle, Law};

/// The oracle itself.
pub struct Echo;
impl Law for Echo {
    fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)> {
        let (t, tau) = oracle::radial_periods(p, e);
        Some((oracle::periapsis_advance(p, e), t, tau))
    }
    fn deflection(&self, b: f64) -> Option<f64> {
        Some(oracle::deflection(b))
    }
    fn captured(&self, energy: f64, angular: f64) -> bool {
        angular < oracle::capture_angular(energy)
    }
    fn photon_captured(&self, b: f64) -> bool {
        b < oracle::photon_critical_b()
    }
    fn long_run(&self, p: f64, e: f64, cycles: usize) -> Vec<(f64, f64, f64, f64)> {
        let (energy, angular) = oracle::bound_invariants(p, e);
        vec![(p / (1.0 + e), p / (1.0 - e), energy, angular); cycles]
    }
}

/// The flaws, by the gate that must catch each.
#[derive(Clone, Copy)]
pub enum Fault {
    /// G1: the periapsis advance is 2% too large.
    Precession,
    /// G5: the energy drifts like √t (a random walk's growth), the orbit's shape stays.
    Walk,
    /// G4: nothing is ever captured, massive or light.
    NoCapture,
}
/// The oracle with one planted flaw.
pub struct Planted(pub Fault);
impl Law for Planted {
    fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)> {
        let skew = if matches!(self.0, Fault::Precession) { 1.02 } else { 1.0 };
        Echo.advance_per_cycle(p, e).map(|(a, t, tau)| (a * skew, t, tau))
    }
    fn deflection(&self, b: f64) -> Option<f64> {
        Echo.deflection(b)
    }
    fn captured(&self, energy: f64, angular: f64) -> bool {
        !matches!(self.0, Fault::NoCapture) && Echo.captured(energy, angular)
    }
    fn photon_captured(&self, b: f64) -> bool {
        !matches!(self.0, Fault::NoCapture) && Echo.photon_captured(b)
    }
    fn long_run(&self, p: f64, e: f64, cycles: usize) -> Vec<(f64, f64, f64, f64)> {
        let mut run = Echo.long_run(p, e, cycles);
        if matches!(self.0, Fault::Walk) {
            for (k, cycle) in run.iter_mut().enumerate() {
                cycle.2 *= 1.0 + 1e-6 * (k as f64).sqrt();
            }
        }
        run
    }
}

pub fn by_name(name: &str) -> Option<Box<dyn Law>> {
    Some(match name {
        "space" => Box::new(super::space::Space::default()),
        "echo" => Box::new(Echo),
        "planted-precession" => Box::new(Planted(Fault::Precession)),
        "planted-walk" => Box::new(Planted(Fault::Walk)),
        "planted-nocapture" => Box::new(Planted(Fault::NoCapture)),
        _ => return None,
    })
}
