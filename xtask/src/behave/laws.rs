//! The laws the judge can meet without a physics core. `echo` answers with the oracle, so every
//! gate must pass. Each planted law has one flaw and must fail exactly the gate that guards it:
//! together they prove the judge can fail (a test that cannot fail is a control).
use super::restricted::{self, Model, Restricted, RTOL};
use super::belt::{Belt, BeltSpec, Flaw, ProgramBelt, SampleBelt};
use super::kerr::Fate;
use super::rotating::{self, KerrAnswer, KerrQuery, Sense};
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
    fn kerr(&self, chi: f64, query: &KerrQuery) -> Option<KerrAnswer> {
        Some(rotating::oracle_answer(chi, query))
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
    /// B13: a surface 50% too wide: a ship whose path passes within 1.5 planet radii of the planet's centre is
    /// destroyed (no answer), though the reference passes above the real surface (the oracle's domain begins at 1.0).
    Swollen,
    /// B9: bands spaced a sixteenth of the periapsis radius apart in r (linear, not logarithmic): the
    /// count grows with r_apo/r_peri instead of its logarithm. The old gate's median over e < 0.7 passes it.
    Linear,
    /// B14: a moon bound to the planet precesses 20% too fast; its distances (so its class) are the reference's.
    Apsides,
    /// B16: the static memo: the lens's own deflection at its own impact parameter, with no aberration.
    Static,
    /// B16: the composition with the sign of the aberration flipped (the lens moves at −β).
    Flipped,
    /// B12 (probe P2 of the Opus motion memo, 6 October; a control that must PASS): echo plus an error that is bounded and depends only on
    /// the current state, never on the history: the Jacobi constant moved by 10⁻⁷·(a − a₀)/(R_H/sep) of its value, a the ship's semimajor
    /// axis about the star in separations (a₀ at t = 0), by scaling the velocity as the planet's frame sees it. A law whose error never
    /// compounds, so B12 must not call it growth; if it does, B12's statistic is miscalibrated (it reads a chaotic ship's diffusion in a).
    Bounded,
    /// B12 (the other side of probe P2, a control that must FAIL): echo plus a compounding error: each time the ship comes within 3 R_H of the
    /// planet (a sample inside after one outside) the Jacobi constant takes a random step of 10⁻⁷ of its value (uniform, unit variance, from the
    /// ship's own start), and the error is the sum of the steps so far: a random walk in the number of encounters, with a memory.
    Compound,
    /// B12 v2 (must FAIL): echo plus a random walk in the handoffs: at each crossing of the doll's edge (seen at the samples) the Jacobi constant takes a random step of
    /// 10⁻⁷ of its value (uniform, unit variance, from the ship's own start). The ensemble's ships are bound to the planet, so they cross the edge and never leave 3 R_H.
    Crossing,
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
    /// B18 belt (red-team F1): every e above its 1 - 1e-4 quantile pulled 15% toward that quantile.
    BeltCrush,
    /// B18 belt (F2): p clipped from below at its 1e-4 quantile.
    BeltInnerClip,
    /// B18 belt (F3): the deepest e-tail bodies take their omega from one 1/32 of the circle.
    BeltAligned,
    /// B18 belt (F4): a 4 MB one-level quantile table in the store, declared as information.
    BeltTable20,
    /// B19: no frame dragging: Schwarzschild (χ = 0) answers every spin.
    NoDrag,
    /// B19: Schwarzschild everywhere, with the Kerr ISCO and photon orbit bolted onto the circular orbits.
    IscoFudge,
    /// B19: a Penrose split whose forward photon carries 10⁻³ more energy than conservation allows.
    PenroseLeak,
    /// B19: correct for prograde orbits only: retrograde questions are answered as their prograde mirror.
    ProgradeOnly,
    /// B19: right everywhere except that light of χ = 0.998 against the spin at |b| in (5.2, 6.2) (inside b₋ = −7.0, captured) is
    /// said to scatter: a band between the four-point probes of criterion 2(d), which only the dense capture family sees.
    RetroCapture,
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
            Fault::Swollen => {
                let mut it = restricted::Integrator::new(scene, Model::Full, RTOL, ship).conserving().tracking();
                let states = times.iter().map(|&t| it.advance(t)).collect::<Option<Vec<_>>>();
                states.filter(|_| it.closest() >= SWOLLEN * scene.planet_radius)
            }
            Fault::Apsides => Echo.restricted(scene, ship, times).map(|states| skew_apsides(scene, ship, times, states)),
            Fault::Bounded => Echo.restricted(scene, ship, times).map(|states| plant_bounded(scene, ship, times, states)),
            Fault::Compound => Echo.restricted(scene, ship, times).map(|states| plant_compound(scene, ship, times, states)),
            Fault::Crossing => Echo.restricted(scene, ship, times).map(|states| plant_crossing(scene, ship, times, &states, BOUNDED)),
            Fault::Averaged if resonance::is_scene(scene) => resonance::averaged(scene, ship, times),
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
            Fault::BeltCrush => Flaw::Crush,
            Fault::BeltInnerClip => Flaw::InnerClip,
            Fault::BeltAligned => Flaw::Aligned,
            Fault::BeltTable20 => Flaw::Table20,
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
    fn kerr(&self, chi: f64, query: &KerrQuery) -> Option<KerrAnswer> {
        match self.0 {
            Fault::NoDrag => Echo.kerr(0.0, query),
            Fault::IscoFudge => match *query {
                // The headline Kerr numbers, copied: circular orbits exist outside the photon orbit and are stable outside the ISCO.
                KerrQuery::Circular { .. } => Echo.kerr(chi, query),
                _ => Echo.kerr(0.0, query),
            },
            Fault::PenroseLeak => match Echo.kerr(chi, query)? {
                KerrAnswer::Split { forward: (e, l), backward } => Some(KerrAnswer::Split { forward: (e + PENROSE_LEAK, l), backward }),
                other => Some(other),
            },
            Fault::ProgradeOnly => Echo.kerr(chi, &prograde_mirror(query)),
            Fault::RetroCapture => match *query {
                KerrQuery::PhotonFate { b } if chi == 0.998 && (-6.2..-5.2).contains(&b) => Some(KerrAnswer::Fate(Fate::Scattered)),
                _ => Echo.kerr(chi, query),
            },
            _ => Echo.kerr(chi, query),
        }
    }
}
/// The planted leak: energy the forward photon carries beyond conservation.
const PENROSE_LEAK: f64 = 1e-3;
/// A retrograde question asked as its prograde mirror (the law knows only one sense of rotation).
fn prograde_mirror(query: &KerrQuery) -> KerrQuery {
    match *query {
        KerrQuery::Cycle { p, e, .. } => KerrQuery::Cycle { p, e, sense: Sense::Pro },
        KerrQuery::Circular { r, .. } => KerrQuery::Circular { r, sense: Sense::Pro },
        KerrQuery::Fate { energy, angular } => KerrQuery::Fate { energy, angular: angular.abs() },
        KerrQuery::PhotonFate { b } => KerrQuery::PhotonFate { b: b.abs() },
        KerrQuery::Deflection { b } => KerrQuery::Deflection { b: b.abs() },
        KerrQuery::Tube { energy, angular, r } => KerrQuery::Tube { energy, angular: angular.abs(), r },
        KerrQuery::Split { energy, angular, r } => KerrQuery::Split { energy, angular: angular.abs(), r },
        KerrQuery::Clock { .. } => *query,
    }
}

/// B18 belt's third control: a program whose e comes from a two-level dyadic quantile table (2^12 cells in each octave of the
/// probability, at both ends). Dyadic tables do not clip a tail if they are dyadic in the probability's octaves at that end;
/// this one passes.
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
/// The surface of `Fault::Swollen`, in planet radii.
const SWOLLEN: f64 = 1.5;
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

/// `planted-bounded`: the relative Jacobi error per unit of (a − a₀)/(R_H/sep).
const BOUNDED: f64 = 1e-7;
/// The semimajor axis (in separations) past which `planted-bounded` stops reading it: an ejected ship's error stays bounded too.
const AXIS_CAP: f64 = 10.0;

/// The ship's semimajor axis about the star, in separations, from its barycentric state at t (capped at AXIS_CAP; an unbound ship has the cap).
pub(super) fn star_axis(scene: &Restricted, t: f64, s: &[f64; 4]) -> f64 {
    let (energy, _) = scene.heliocentric(t, s);
    if energy < 0.0 { ((1.0 - scene.mu) / (-2.0 * energy) / scene.sep).min(AXIS_CAP) } else { AXIS_CAP }
}

/// Each state's velocity, as the planet's frame (the frame in which the Jacobi constant is 2Ũ − |u|²) sees it, is scaled by κ so that the constant
/// moves by −`shift[i]`: C = 2Ũ − |u|², so scaling u by κ moves C by −|u|²(κ² − 1). Where |u|² is too small to carry the shift (a zero-velocity
/// point) the velocity is set to the frame's and the shift is what |u|² can carry.
pub(super) fn lay(scene: &Restricted, states: Vec<[f64; 4]>, shift: &[f64]) -> Vec<[f64; 4]> {
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

/// `planted-bounded`: the constant moves by BOUNDED·(a − a₀)/(R_H/sep) of |C₀|, where a is the semimajor axis of the same state. The shift depends on
/// that one state and nothing before it, so the error is bounded and has no memory.
fn plant_bounded(scene: &Restricted, ship: [f64; 4], times: &[f64], states: Vec<[f64; 4]>) -> Vec<[f64; 4]> {
    let (a0, c0, unit) = (star_axis(scene, 0.0, &ship), scene.jacobi(0.0, &ship).abs(), scene.hill() / scene.sep);
    let shift: Vec<f64> = times.iter().zip(&states).map(|(&t, s)| BOUNDED * (star_axis(scene, t, s) - a0) / unit * c0).collect();
    lay(scene, states, &shift)
}

/// `planted-compound`: the constant moves by 10⁻⁷ of |C₀| times the sum of one unit-variance random step per encounter so far (the ship at a
/// sample within 3 R_H of the planet after a sample outside). The sum is a memory: the error is a random walk in the encounter count.
fn plant_compound(scene: &Restricted, ship: [f64; 4], times: &[f64], states: Vec<[f64; 4]>) -> Vec<[f64; 4]> {
    let c0 = scene.jacobi(0.0, &ship).abs();
    let mut rng = super::sample::Rng(ship.iter().fold(0x5EED, |h, x| h.rotate_left(17) ^ x.to_bits()));
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

/// `planted-crossing`: the Jacobi constant moves by `amp`·|C₀| times the sum of one unit-variance random step per crossing of the doll's edge so far.
pub(super) fn plant_crossing(scene: &Restricted, ship: [f64; 4], times: &[f64], states: &[[f64; 4]], amp: f64) -> Vec<[f64; 4]> {
    let c0 = scene.jacobi(0.0, &ship).abs();
    let mut rng = super::sample::Rng(ship.iter().fold(0x5EED, |h, x| h.rotate_left(17) ^ x.to_bits()));
    let (mut sum, mut inside) = (0.0, None);
    let shift: Vec<f64> = times
        .iter()
        .zip(states)
        .map(|(&t, s)| {
            let now = scene.planet_distance(t, s) < scene.soi();
            if inside.is_some_and(|b| b != now) {
                sum += (rng.unit() - 0.5) * 12f64.sqrt();
            }
            inside = Some(now);
            amp * sum * c0
        })
        .collect();
    lay(scene, states.to_vec(), &shift)
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
        "planted-swollen" => Box::new(Planted(Fault::Swollen)),
        "planted-linear" => Box::new(Planted(Fault::Linear)),
        "planted-apsides" => Box::new(Planted(Fault::Apsides)),
        "planted-static" => Box::new(Planted(Fault::Static)),
        "planted-flipped" => Box::new(Planted(Fault::Flipped)),
        "planted-average" => Box::new(Planted(Fault::Averaged)),
        "planted-bounded" => Box::new(Planted(Fault::Bounded)),
        "planted-compound" => Box::new(Planted(Fault::Compound)),
        "planted-crossing" => Box::new(Planted(Fault::Crossing)),
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
        "planted-belt-crush" => Box::new(Planted(Fault::BeltCrush)),
        "planted-belt-innerclip" => Box::new(Planted(Fault::BeltInnerClip)),
        "planted-belt-aligned" => Box::new(Planted(Fault::BeltAligned)),
        "planted-belt-table20" => Box::new(Planted(Fault::BeltTable20)),
        "iid-blocks" => Box::new(IidBlocks),
        "dyadic-belt" => Box::new(DyadicBelt),
        "planted-nodrag" => Box::new(Planted(Fault::NoDrag)),
        "planted-isco" => Box::new(Planted(Fault::IscoFudge)),
        "planted-penrose" => Box::new(Planted(Fault::PenroseLeak)),
        "planted-proonly" => Box::new(Planted(Fault::ProgradeOnly)),
        "planted-rcapture" => Box::new(Planted(Fault::RetroCapture)),
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

#[cfg(test)]
mod tests {
    use super::*;
    use crate::behave::handoff::{coarse_times, kept};
    use crate::behave::restricted::JUPITER;

    #[test]
    fn planted_bounded_answers_each_time_from_that_states_alone() {
        // The error is a function of the one state it is laid on: planting a single sample gives the word the whole run gives, bit for bit.
        let (scene, times) = (JUPITER, coarse_times(&JUPITER));
        let ship = kept()[0].ship;
        let truth = Echo.restricted(&scene, ship, &times).unwrap();
        let all = plant_bounded(&scene, ship, &times, truth.clone());
        for j in [0, 1, 17, 800, 1600] {
            assert_eq!(plant_bounded(&scene, ship, &times[j..=j], vec![truth[j]]), vec![all[j]], "sample {j}");
        }
        assert_eq!(all[0], truth[0], "no error where a = a₀");
        assert!(all.iter().zip(&truth).any(|(p, t)| p != t));
    }
}
