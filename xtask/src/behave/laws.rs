//! The laws the judge can meet without a physics core. `echo` answers with the oracle, so every
//! gate must pass. Each planted law has one flaw and must fail exactly the gate that guards it:
//! together they prove the judge can fail (a test that cannot fail is a control).
use super::restricted::{self, Model, Restricted, RTOL};
use super::{cost, oracle, scale, Law};

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
    fn static_clock_rate(&self, r: f64) -> Option<f64> {
        Some(oracle::static_clock_rate(r))
    }
    fn circular_clock_rate(&self, r: f64) -> Option<f64> {
        (r > 3.0).then(|| oracle::circular_clock_rate(r))
    }
    fn crossings_per_cycle(&self, p: f64, e: f64) -> Option<f64> {
        Some(cost::reference_crossings(p, e))
    }
    fn scene_cost(&self, n_bodies: usize, game_seconds: f64) -> Option<f64> {
        scale::echo_scene_cost(n_bodies, game_seconds)
    }
    fn binary_cycle(&self, energy: f64, angular: f64, nu: f64) -> Option<(f64, f64)> {
        Some(oracle::damour_deruelle(energy, angular, nu))
    }
    fn restricted(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        restricted::conserving_reference(scene, ship, times, RTOL)
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
    /// B7: both clock rates are off by 1e-6 relative.
    Clock,
    /// B9: every orbit costs 512 band crossings per cycle.
    Steps,
    /// B10: the scene is all pairs, so its cost grows like n².
    Quadratic,
    /// B11: Kepler's period 2π·a^(3/2) from the invariants, and no periapsis advance.
    Newton,
    /// B12, B13: the planetocentric velocity is multiplied by 1 + 1e-3 on each entry into R_SOI.
    Kick,
    /// B14: inside R_SOI the ship feels only the planet, the star's tide is dropped.
    NoTide,
    /// B12: the reference's own Jacobi drift, from Dormand-Prince at tolerance 1e-12 with nothing
    /// holding the constant.
    Drift,
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
    fn static_clock_rate(&self, r: f64) -> Option<f64> {
        let skew = if matches!(self.0, Fault::Clock) { 1.0 + 1e-6 } else { 1.0 };
        Echo.static_clock_rate(r).map(|x| x * skew)
    }
    fn circular_clock_rate(&self, r: f64) -> Option<f64> {
        let skew = if matches!(self.0, Fault::Clock) { 1.0 + 1e-6 } else { 1.0 };
        Echo.circular_clock_rate(r).map(|x| x * skew)
    }
    fn crossings_per_cycle(&self, p: f64, e: f64) -> Option<f64> {
        if matches!(self.0, Fault::Steps) {
            Some(512.0)
        } else {
            Echo.crossings_per_cycle(p, e)
        }
    }
    fn scene_cost(&self, n_bodies: usize, game_seconds: f64) -> Option<f64> {
        if matches!(self.0, Fault::Quadratic) {
            scale::quadratic_scene_cost(n_bodies, game_seconds)
        } else {
            Echo.scene_cost(n_bodies, game_seconds)
        }
    }
    fn binary_cycle(&self, energy: f64, angular: f64, nu: f64) -> Option<(f64, f64)> {
        if matches!(self.0, Fault::Newton) {
            Some((0.0, 2.0 * std::f64::consts::PI * (-2.0 * energy).powf(-1.5)))
        } else {
            Echo.binary_cycle(energy, angular, nu)
        }
    }
    fn restricted(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        match self.0 {
            Fault::Kick => restricted::integrate(scene, Model::Kick(1.0 + KICK), RTOL, ship, times),
            Fault::NoTide => restricted::integrate(scene, Model::NoTide, RTOL, ship, times),
            Fault::Drift => restricted::reference(scene, ship, times, RTOL),
            _ => Echo.restricted(scene, ship, times),
        }
    }
}
/// The planted kick: the planetocentric velocity grows by this, relative, at each entry into R_SOI.
const KICK: f64 = 1e-3;

pub fn by_name(name: &str) -> Option<Box<dyn Law>> {
    Some(match name {
        "echo" => Box::new(Echo),
        "planted-precession" => Box::new(Planted(Fault::Precession)),
        "planted-walk" => Box::new(Planted(Fault::Walk)),
        "planted-nocapture" => Box::new(Planted(Fault::NoCapture)),
        "planted-clock" => Box::new(Planted(Fault::Clock)),
        "planted-steps" => Box::new(Planted(Fault::Steps)),
        "planted-quadratic" => Box::new(Planted(Fault::Quadratic)),
        "planted-newton" => Box::new(Planted(Fault::Newton)),
        "planted-kick" => Box::new(Planted(Fault::Kick)),
        "planted-notide" => Box::new(Planted(Fault::NoTide)),
        "planted-drift" => Box::new(Planted(Fault::Drift)),
        _ => return None,
    })
}

/// A law that answers the six old gates like `echo` and none of the events layer's (B11-B14).
#[cfg(test)]
pub struct Silent;
#[cfg(test)]
impl Law for Silent {
    fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)> {
        Echo.advance_per_cycle(p, e)
    }
    fn deflection(&self, b: f64) -> Option<f64> {
        Echo.deflection(b)
    }
    fn captured(&self, energy: f64, angular: f64) -> bool {
        Echo.captured(energy, angular)
    }
    fn photon_captured(&self, b: f64) -> bool {
        Echo.photon_captured(b)
    }
    fn long_run(&self, p: f64, e: f64, cycles: usize) -> Vec<(f64, f64, f64, f64)> {
        Echo.long_run(p, e, cycles)
    }
}

/// `echo` with a hook on each events answer, to plant flaws that are not in the CLI.
#[cfg(test)]
pub struct Events {
    /// Given echo's (advance, period), what the law answers.
    pub binary: Box<dyn Fn((f64, f64)) -> Option<(f64, f64)>>,
    /// What the law answers, given the scene, the ship and the times (`Echo.restricted` is echo's answer).
    pub restricted: Box<dyn Fn(&Restricted, [f64; 4], &[f64]) -> Option<Vec<[f64; 4]>>>,
}
#[cfg(test)]
impl Law for Events {
    fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)> {
        Silent.advance_per_cycle(p, e)
    }
    fn deflection(&self, b: f64) -> Option<f64> {
        Silent.deflection(b)
    }
    fn captured(&self, energy: f64, angular: f64) -> bool {
        Silent.captured(energy, angular)
    }
    fn photon_captured(&self, b: f64) -> bool {
        Silent.photon_captured(b)
    }
    fn long_run(&self, p: f64, e: f64, cycles: usize) -> Vec<(f64, f64, f64, f64)> {
        Silent.long_run(p, e, cycles)
    }
    fn binary_cycle(&self, energy: f64, angular: f64, nu: f64) -> Option<(f64, f64)> {
        (self.binary)(Echo.binary_cycle(energy, angular, nu)?)
    }
    fn restricted(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        (self.restricted)(scene, ship, times)
    }
}
