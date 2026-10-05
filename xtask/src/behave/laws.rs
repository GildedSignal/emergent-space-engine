//! The laws the judge can meet without a physics core. `echo` answers with the oracle, so every
//! gate must pass. Each planted law has one flaw and must fail exactly the gate that guards it:
//! together they prove the judge can fail (a test that cannot fail is a control).
use super::restricted::{self, Model, Restricted, RTOL};
use super::belt::{Belt, BeltSpec, Flaw, ProgramBelt, SampleBelt};
use super::{cost, hill, lens, memory, oracle, resonance, scale, Law};

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
    fn moving_deflection(&self, lens: &lens::MovingLens) -> Option<f64> {
        Some(lens::composed(lens))
    }
    fn bytes_per_body(&self, scene: &memory::MemoryScene) -> Option<f64> {
        memory::floor_bytes(scene)
    }
    /// The exact in-judge reference belt: a SplitMix64 counter stream through an integer-reproducible Rayleigh quantile.
    fn belt_birth(&self, spec: &BeltSpec, n: u64, seed: u64) -> Option<Box<dyn Belt>> {
        Some(Box::new(ProgramBelt::birth(spec, n, seed, Flaw::None)))
    }
    fn belt_restore(&self, store: &[u8]) -> Option<Box<dyn Belt>> {
        ProgramBelt::restore(store).map(|b| Box::new(b) as Box<dyn Belt>)
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
    /// B9: bands spaced a sixteenth of the periapsis radius apart in r (linear, not logarithmic): the
    /// count grows with r_apo/r_peri instead of its logarithm. The old gate's median over e < 0.7 passes it.
    Linear,
    /// B14: a moon bound to the planet precesses 20% too fast; its distances (so its class) are the reference's.
    Apsides,
    /// B16: the static memo: the lens's own deflection at its own impact parameter, with no aberration.
    Static,
    /// B16: the composition with the sign of the aberration flipped (the lens moves at −β).
    Flipped,
    /// B17: the first-order orbit average of the planet's pull (Laplace-Lagrange), answered on B17's scenes only.
    Averaged,
    /// B18: the 16-byte tube of the contract, uncompressed, on every scene.
    Fat,
    /// B18 belt: e through the gold's 2^12-entry midpoint quantile table, so the top 1e-4 sits in one cell.
    BeltClipped,
    /// B18 belt: p and e clipped at their 1 - 1e-4 quantile (the tail count survives, the range does not).
    BeltWinsor,
    /// B18 belt: the states repeat every n/4 ordinals.
    BeltRepeat,
    /// B18 belt: one odd body in seven copies its neighbour's t_p.
    BeltSerial,
    /// B18 belt: the draw depends on a call counter shared by every thread.
    BeltThread,
    /// B18 belt: the program's store carries one more byte per body.
    BeltFat,
    /// B18 belt: an iid draw kept as 64-byte ships (over B18's iid budget).
    BeltShips,
    /// B18 belt: body i is i times a constant per column (a rank-1 lattice: perfect marginals, structure in the plane).
    BeltLattice,
    /// B18 belt: the program is right and the scars cost 40 bytes each.
    BeltFatScars,
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
        match self.0 {
            Fault::Steps => Some(512.0),
            Fault::Linear => Some(2.0 * cost::BANDS_PER_OCTAVE * (2.0 * e / (1.0 - e))),
            _ => Echo.crossings_per_cycle(p, e),
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
            Fault::Apsides => Echo.restricted(scene, ship, times).map(|states| skew_apsides(scene, ship, times, states)),
            Fault::Averaged if scene.sep == resonance::SEP => resonance::averaged(scene, ship, times),
            _ => Echo.restricted(scene, ship, times),
        }
    }
    fn moving_deflection(&self, l: &lens::MovingLens) -> Option<f64> {
        match self.0 {
            Fault::Static => Some(lens::static_memo(l)),
            Fault::Flipped => Some(lens::compose(l, oracle::deflection, -1.0)),
            _ => Echo.moving_deflection(l),
        }
    }
    fn bytes_per_body(&self, scene: &memory::MemoryScene) -> Option<f64> {
        match self.0 {
            Fault::Fat => Some(16.0),
            _ => Echo.bytes_per_body(scene),
        }
    }
    fn belt_birth(&self, spec: &BeltSpec, n: u64, seed: u64) -> Option<Box<dyn Belt>> {
        let flaw = match self.0 {
            Fault::BeltClipped => Flaw::Table12,
            Fault::BeltWinsor => Flaw::Winsor,
            Fault::BeltRepeat => Flaw::Repeat,
            Fault::BeltSerial => Flaw::Serial,
            Fault::BeltThread => Flaw::Thread,
            Fault::BeltFat => Flaw::Fat,
            Fault::BeltLattice => Flaw::Lattice,
            Fault::BeltFatScars => Flaw::FatScars,
            Fault::BeltShips => return Some(Box::new(SampleBelt::birth(spec, n, seed, true))),
            _ => return Echo.belt_birth(spec, n, seed),
        };
        Some(Box::new(ProgramBelt::birth(spec, n, seed, flaw)))
    }
    fn belt_restore(&self, store: &[u8]) -> Option<Box<dyn Belt>> {
        match self.0 {
            Fault::BeltShips => SampleBelt::restore(store).map(|b| Box::new(b) as Box<dyn Belt>),
            _ => Echo.belt_restore(store),
        }
    }
}

/// B18 belt's third control: a program whose e comes from a two-level dyadic quantile table (2^12 cells in each octave of the
/// probability). Dyadic tables do not clip the tail if they are dyadic in the probability's octaves; this one passes.
pub struct DyadicBelt;
impl Law for DyadicBelt {
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
    fn belt_birth(&self, spec: &BeltSpec, n: u64, seed: u64) -> Option<Box<dyn Belt>> {
        Some(Box::new(ProgramBelt::birth(spec, n, seed, Flaw::Dyadic)))
    }
    fn belt_restore(&self, store: &[u8]) -> Option<Box<dyn Belt>> {
        ProgramBelt::restore(store).map(|b| Box::new(b) as Box<dyn Belt>)
    }
}

/// B18 belt's second control: a belt that is an iid draw stored as packed blocks. It is judged under B18's iid floor
/// rule (bytes per body within 2x the draw entropy + 2) and passes; every other method is echo's.
pub struct IidBlocks;
impl Law for IidBlocks {
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
    fn bytes_per_body(&self, scene: &memory::MemoryScene) -> Option<f64> {
        Echo.bytes_per_body(scene)
    }
    fn belt_birth(&self, spec: &BeltSpec, n: u64, seed: u64) -> Option<Box<dyn Belt>> {
        Some(Box::new(SampleBelt::birth(spec, n, seed, false)))
    }
    fn belt_restore(&self, store: &[u8]) -> Option<Box<dyn Belt>> {
        SampleBelt::restore(store).map(|b| Box::new(b) as Box<dyn Belt>)
    }
}
/// The planted kick: the planetocentric velocity grows by this, relative, at each entry into R_SOI.
const KICK: f64 = 1e-3;
/// The planted apsides: a bound moon's periapsis longitude advances by this much more, relative.
const APSIDES_SKEW: f64 = 0.2;

/// `planted-apsides`: a ship bound to the planet at t = 0 has its planetocentric state turned, at each
/// sample, by APSIDES_SKEW times the periapsis' advance so far. A rotation about the planet keeps every
/// distance from it (so the class) and turns the apse: the rate is 1.2 times the reference's. A ship
/// that is not bound to the planet (B12's and B13's, B17's) is left as it is.
fn skew_apsides(scene: &Restricted, ship: [f64; 4], times: &[f64], states: Vec<[f64; 4]>) -> Vec<[f64; 4]> {
    let w = scene.relative(0.0, &ship);
    let bound = 0.5 * (w[2] * w[2] + w[3] * w[3]) - scene.mu / w[0].hypot(w[1]) < 0.0;
    let Some(varpi) = bound.then(|| hill::apsides_series(scene, times, &states)).flatten() else { return states };
    states
        .iter()
        .zip(times)
        .zip(&varpi)
        .map(|((s, &t), v)| {
            let (sn, c) = (APSIDES_SKEW * (v - varpi[0])).sin_cos();
            let w = scene.relative(t, s);
            scene.barycentric(t, &[c * w[0] - sn * w[1], sn * w[0] + c * w[1], c * w[2] - sn * w[3], sn * w[2] + c * w[3]])
        })
        .collect()
}

pub fn by_name(name: &str) -> Option<Box<dyn Law>> {
    Some(match name {
        "space" => Box::new(super::space::Space::default()),
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
        "planted-linear" => Box::new(Planted(Fault::Linear)),
        "planted-apsides" => Box::new(Planted(Fault::Apsides)),
        "planted-static" => Box::new(Planted(Fault::Static)),
        "planted-flipped" => Box::new(Planted(Fault::Flipped)),
        "planted-average" => Box::new(Planted(Fault::Averaged)),
        "planted-fat" => Box::new(Planted(Fault::Fat)),
        "planted-belt-clipped" => Box::new(Planted(Fault::BeltClipped)),
        "planted-belt-winsor" => Box::new(Planted(Fault::BeltWinsor)),
        "planted-belt-repeat" => Box::new(Planted(Fault::BeltRepeat)),
        "planted-belt-serial" => Box::new(Planted(Fault::BeltSerial)),
        "planted-belt-thread" => Box::new(Planted(Fault::BeltThread)),
        "planted-belt-fat" => Box::new(Planted(Fault::BeltFat)),
        "planted-belt-ships" => Box::new(Planted(Fault::BeltShips)),
        "planted-belt-lattice" => Box::new(Planted(Fault::BeltLattice)),
        "planted-belt-fatscars" => Box::new(Planted(Fault::BeltFatScars)),
        "iid-blocks" => Box::new(IidBlocks),
        "dyadic-belt" => Box::new(DyadicBelt),
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
