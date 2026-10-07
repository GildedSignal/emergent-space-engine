//! The B12 control laws, verbatim from xtask/src/behave/laws.rs and the gate's own tests
//! (handoff.rs `scaled`, `a_slow_leak_far_inside_the_bound_fails_on_the_exponent`): Echo,
//! the smooth bounded `scaled`, `planted-bounded`, `planted-compound`, `planted-drift`
//! and the 1e-12-per-period leak. Only the trait is the local `LawR`.
use crate::handoff::LawR;
use crate::restricted::{self, Restricted, RTOL};
use crate::sample::Rng;

/// `echo`'s restricted arm, verbatim.
pub struct Echo;
impl LawR for Echo {
    fn restricted(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        restricted::conserving_reference(scene, ship, times, RTOL)
    }
}

/// The gate's `scaled(eps)` test law: every speed scaled by 1 + eps (smooth bounded error ~2.7·eps).
pub struct Scaled(pub f64);
impl LawR for Scaled {
    fn restricted(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        Some(Echo.restricted(scene, ship, times)?.into_iter().map(|st| [st[0], st[1], st[2] * (1.0 + self.0), st[3] * (1.0 + self.0)]).collect())
    }
}

/// The gate's slow-leak test law: speeds grow by 1e-12 per planet period.
pub struct LeakPeriod;
impl LawR for LeakPeriod {
    fn restricted(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        let s = Echo.restricted(scene, ship, times)?;
        Some(s.iter().zip(times).map(|(st, &t)| [st[0], st[1], st[2] * (1.0 + 1e-12 * t / scene.period()), st[3] * (1.0 + 1e-12 * t / scene.period())]).collect())
    }
}

/// `planted-drift`'s restricted arm, verbatim: the reference without conservation.
pub struct Drift;
impl LawR for Drift {
    fn restricted(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        restricted::reference(scene, ship, times, RTOL)
    }
}

const BOUNDED: f64 = 1e-7;
const AXIS_CAP: f64 = 10.0;

/// Verbatim `star_axis`.
fn star_axis(scene: &Restricted, t: f64, s: &[f64; 4]) -> f64 {
    let (energy, _) = scene.heliocentric(t, s);
    if energy < 0.0 { ((1.0 - scene.mu) / (-2.0 * energy) / scene.sep).min(AXIS_CAP) } else { AXIS_CAP }
}

/// Verbatim `lay`.
fn lay(scene: &Restricted, states: Vec<[f64; 4]>, shift: &[f64]) -> Vec<[f64; 4]> {
    let w = scene.omega();
    states
        .into_iter()
        .zip(shift)
        .map(|(s, &want)| {
            let (ux, uy) = (s[2] + w * s[1], s[3] - w * s[0]);
            let k = (1.0 + want / (ux * ux + uy * uy)).max(0.0).sqrt();
            [s[0], s[1], s[2] + (k - 1.0) * ux, s[3] + (k - 1.0) * uy]
        })
        .collect()
}

/// Verbatim `plant_bounded`.
fn plant_bounded(scene: &Restricted, ship: [f64; 4], times: &[f64], states: Vec<[f64; 4]>) -> Vec<[f64; 4]> {
    let (a0, c0, unit) = (star_axis(scene, 0.0, &ship), scene.jacobi(0.0, &ship).abs(), scene.hill() / scene.sep);
    let shift: Vec<f64> = times.iter().zip(&states).map(|(&t, s)| BOUNDED * (star_axis(scene, t, s) - a0) / unit * c0).collect();
    lay(scene, states, &shift)
}

/// Verbatim `plant_compound`.
fn plant_compound(scene: &Restricted, ship: [f64; 4], times: &[f64], states: Vec<[f64; 4]>) -> Vec<[f64; 4]> {
    let c0 = scene.jacobi(0.0, &ship).abs();
    let mut rng = Rng(ship.iter().fold(0x5EED, |h, x| h.rotate_left(17) ^ x.to_bits()));
    let (mut sum, mut inside) = (0.0, false);
    let shift: Vec<f64> = times
        .iter()
        .zip(&states)
        .map(|(&t, s)| {
            let now = scene.planet_distance(t, s) < 3.0 * scene.hill();
            if now && !inside {
                sum += (rng.unit() - 0.5) * 12f64.sqrt();
            }
            inside = now;
            BOUNDED * sum * c0
        })
        .collect();
    lay(scene, states, &shift)
}

/// `Planted(Fault::Bounded)` restricted arm, verbatim.
pub struct PlantedBounded;
impl LawR for PlantedBounded {
    fn restricted(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        Echo.restricted(scene, ship, times).map(|states| plant_bounded(scene, ship, times, states))
    }
}

/// `Planted(Fault::Compound)` restricted arm, verbatim.
pub struct PlantedCompound;
impl LawR for PlantedCompound {
    fn restricted(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        Echo.restricted(scene, ship, times).map(|states| plant_compound(scene, ship, times, states))
    }
}
