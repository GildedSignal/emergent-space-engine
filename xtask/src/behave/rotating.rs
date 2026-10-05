//! B19 rotating holes (docs/law.md, "Rotating holes"; Julien, 5 October: "especially rotating black holes", "I want gr for all of
//! its interesting effects that are weird"). A doll has a spin χ = a/M; the plane is the hole's equator, where Kerr geodesics stay.
//! The oracle is `kerr.rs` (equatorial Kerr geodesics in float64, cross-checked against mpmath); this file is the gate: the
//! questions the judge asks a law (one method, `Law::kerr`), the frozen seeds, and the six criteria of the row, exactly as written.
//!
//! Questions (`KerrQuery`) and answers (`KerrAnswer`), G = c = M = 1, χ in [0, 1) spinning towards +φ. `None` from `Law::kerr` is
//! "not implemented" and fails every criterion that asks; `Some(KerrAnswer::Absent)` is the law's statement that there is no such
//! orbit, observer or tube.
//!
//! 1. **Cycles.** χ ∈ {0.5, 0.9, 0.998} × {prograde, retrograde} × 256 seeds: Darwin (p, e) with e uniform in [0, 0.7] and p
//!    log-uniform from 1.1 times the separatrix p_s(e) to 1000 (the separatrix is the ISCO at e = 0 and moves out with e). The law
//!    answers the periapsis advance beyond 2π (in the direction of motion), the radial period in coordinate and in proper time.
//!    PASS iff, in every cell of 256, at least 99% have the advance within 1% and at least 99% the periods within 0.1% (the rule of
//!    G1 and G2; the row writes no percentage, so this reading is for the integrator to confirm).
//! 2. **Fates.** Exactly as the oracle, with no allowance, in every (χ, sense): (a) circular orbits at r = r_isco + g·(r_isco − r_ph),
//!    g ∈ {−0.5, −0.1, −0.02, +0.02, +0.1, +0.5, 2}: stable iff g > 0 ("no stable bound cycle inside the ISCO of its sense"), and none
//!    at all between the horizon and the photon orbit; (b) E = 1 from infinity at L = x·L_mb (the marginally bound orbit's angular
//!    momentum of the sense), x ∈ {0.9, 0.97, 1.03, 1.1}: captured iff x < 1; (c) bound or plunge: at the separatrix's angular
//!    momentum L_s of e ∈ {0.2, 0.4, 0.6}, a quarter of the bound window W (between the barrier's energy E_s and the stable circular
//!    orbit's) below E_s is bound and above it plunges (a body started at its outer turning point); and every E < 1 with L at 0.9
//!    and 0.5 of the ISCO's plunges; (d) light at b = x·b_c, x ∈ {0.9, 0.97, 1.03, 1.1}, with b_c the critical impact parameter of the
//!    sense (b₊ prograde, b₋ retrograde): captured iff x < 1.
//! 3. **Frame dragging.** 128 states per χ inside the ergosphere (r between the horizon and 2, ZAMO-frame velocities up to rapidity 4
//!    in every direction), as tubes with constants (E, L): the law must answer them all (not Absent) with dφ/dt > 0 — also for L < 0 —
//!    and rates equal to the oracle's within 1e-6 (an addition to the row: positivity alone could be faked by a constant); and
//!    outside the ergosphere the static clock √(1 − 2/r) and the ZAMO's lapse within 1e-12 (B7's tolerance) at 32 radii per χ, with no
//!    static clock at all (Absent) at 16 radii between the horizon and 2 ("every timelike tube has dφ/dt > 0": a static one has 0).
//! 4. **Negative energy and the Penrose process.** The row says "negative-energy cycles". No *bound* future-directed equatorial orbit has
//!    E < 0 (kerr.rs scans for one: the solutions with E < 0 are all time-reversed), so the judge asks for negative-energy *tubes*, the
//!    arcs that exist: (a) the tubes of (3) with E < 0 must be answered; (b) the same (E, L) forged at r' in (2.2, 30), outside the
//!    ergosphere, must be refused (Absent): nowhere else; (c) the Penrose split of a unit-mass body at a radial turning point into two
//!    photons moving along ±φ̂ in the ZAMO frame: r at the horizon + {1/4, 1/2, 3/4} of the way to 2, v_φ ∈ {0.3, 0.6, 0.9} (the
//!    canonical case is the middle of each: r half way, v = 0.6), conserving E and L to 8 rounding errors, returning more energy than it
//!    took in (E_forward > E₀, E_backward < 0), and equal to the oracle within 1e-6; and the same splits at r ∈ {2.5, 4, 8}, which gain
//!    nothing (E_backward > 0).
//! 5. **Light.** 64 impact parameters per (χ, sense), |b| log-uniform from 1.05·|b_c| to 300: the deflection within 1% for at least 99%.
//! 6. **χ = 0 is Schwarzschild, bit for bit.** The law's own Schwarzschild methods (`advance_per_cycle`, `deflection`, `captured`,
//!    `photon_captured`, `static_clock_rate`) on G1's first 64 orbits, G3's 64 impacts, G4's cases and B7's first 32 radii, hashed;
//!    the same seeds asked of `kerr(0, ·)` in both senses (spin zero cannot tell them apart) hash to the same digest.
//!
//! The oracle's own error is measured against mpmath (`kerr_mpmath.py`) and printed on the line; the thresholds are read against it.
use super::kerr::{self, Fate, Kerr, ERGOSPHERE};
use super::sample::{self, Rng};
use super::{oracle, Gate, Law};

/// The spins judged.
pub const CHI: [f64; 3] = [0.5, 0.9, 0.998];
const CYCLE_SEEDS: usize = 256;
const LIGHT_SEEDS: usize = 64;
const TUBE_SEEDS: usize = 128;
const CLOCK_SEEDS: usize = 32;
const INSIDE_SEEDS: usize = 16;
const FORGED_PER_NEGATIVE: usize = 1;
/// The separatrix margin of criterion 1: p starts at this times p_s(e).
pub const SEPARATRIX_MARGIN: f64 = 1.1;
pub const ADVANCE_TOL: f64 = 1e-2;
pub const PERIOD_TOL: f64 = 1e-3;
pub const DEFLECTION_TOL: f64 = 1e-2;
/// B7's tolerance: the clock formulas are closed forms.
pub const CLOCK_TOL: f64 = 1e-12;
/// An addition to the row (see the module docs): the tube's rates within this of the oracle's.
pub const RATE_TOL: f64 = 1e-6;
/// The split's fragments within this (of |E₀| + |L₀|) of the oracle's.
pub const SPLIT_TOL: f64 = 1e-6;
/// Conservation is exact: the sum of the fragments equals the body within this many rounding errors.
pub const CONSERVE_ULPS: f64 = 8.0;
/// The margin below which a seed's allowed-region verdict is within the oracle's own rounding: the seed is dropped.
const MARGIN: f64 = 1e-6;

/// Which way round the hole an orbit goes: with its spin (L > 0) or against it (L < 0).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Sense {
    Pro,
    Retro,
}
impl Sense {
    pub fn sign(self) -> f64 {
        match self {
            Sense::Pro => 1.0,
            Sense::Retro => -1.0,
        }
    }
}
/// A clock the law is asked to read: one that stays at fixed r and φ (impossible inside the ergosphere), or the zero-angular-momentum observer.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Observer {
    Static,
    Zamo,
}

/// What the judge asks of a law about a hole of spin χ (`Law::kerr`).
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum KerrQuery {
    /// One radial cycle of the stable bound orbit with Darwin (p, e) and a sense: the advance, the periods.
    Cycle { p: f64, e: f64, sense: Sense },
    /// The circular orbit at r: does it exist (Absent otherwise), and is it stable?
    Circular { r: f64, sense: Sense },
    /// A unit-mass body with constants (E, L), started at its outer turning point (E < 1) or at infinity (E >= 1).
    Fate { energy: f64, angular: f64 },
    /// Light with impact parameter b = L/E (negative: against the spin), from infinity.
    PhotonFate { b: f64 },
    /// The deflection of light at b, from and to infinity: |Δφ| − π (Absent if it is captured).
    Deflection { b: f64 },
    /// dτ/dt of a static or a ZAMO observer at r (Absent where there is none).
    Clock { r: f64, observer: Observer },
    /// The tube of a unit-mass body with constants (E, L) through radius r: its dφ/dt and dτ/dt. Absent if no future-directed
    /// body with these constants can be at r.
    Tube { energy: f64, angular: f64, r: f64 },
    /// The Penrose split of a unit-mass body at its radial turning point r (constants E, L) into two photons moving along +φ̂ and −φ̂
    /// in the ZAMO frame; the answer is the constants of each. Absent if the body cannot be there.
    Split { energy: f64, angular: f64, r: f64 },
}

/// A law's answer (`Law::kerr`).
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum KerrAnswer {
    Cycle { advance: f64, period: f64, proper_period: f64 },
    Circular { stable: bool },
    Fate(Fate),
    Angle(f64),
    Rate(f64),
    Tube { phi_rate: f64, clock_rate: f64 },
    /// ((E, L) of the +φ̂ photon, (E, L) of the −φ̂ photon).
    Split { forward: (f64, f64), backward: (f64, f64) },
    /// There is no such thing here.
    Absent,
}

/// The oracle's answer to a query: what `echo` answers. At χ = 0 it is the existing Schwarzschild oracle's (`oracle.rs`) wherever
/// that has an answer, so that the bit-for-bit criterion compares the same functions; the general Kerr code agrees with it to 1e-9
/// (kerr.rs tests).
pub fn oracle_answer(chi: f64, q: &KerrQuery) -> KerrAnswer {
    let k = Kerr::new(chi);
    let schwarzschild = chi == 0.0;
    match *q {
        KerrQuery::Cycle { p, e, sense } => {
            if schwarzschild {
                return if p > 6.0 + 2.0 * e && e < 1.0 {
                    let (t, tau) = oracle::radial_periods(p, e);
                    KerrAnswer::Cycle { advance: oracle::periapsis_advance(p, e), period: t, proper_period: tau }
                } else {
                    KerrAnswer::Absent
                };
            }
            k.cycle(p, e, sense.sign()).map_or(KerrAnswer::Absent, |c| KerrAnswer::Cycle { advance: c.advance, period: c.period, proper_period: c.proper_period })
        }
        KerrQuery::Circular { r, sense } => {
            let s = sense.sign();
            k.circular(r, s).map_or(KerrAnswer::Absent, |_| KerrAnswer::Circular { stable: r >= k.isco(s) })
        }
        KerrQuery::Fate { energy, angular } => {
            if schwarzschild && energy >= 1.0 {
                let captured = angular.abs() < oracle::capture_angular(energy);
                return KerrAnswer::Fate(if captured { Fate::Captured } else { Fate::Scattered });
            }
            KerrAnswer::Fate(k.fate(energy, angular))
        }
        KerrQuery::PhotonFate { b } => {
            if schwarzschild {
                return KerrAnswer::Fate(if b.abs() < oracle::photon_critical_b() { Fate::Captured } else { Fate::Scattered });
            }
            KerrAnswer::Fate(k.photon_fate(b))
        }
        KerrQuery::Deflection { b } => {
            if schwarzschild {
                return if b.abs() < oracle::photon_critical_b() { KerrAnswer::Absent } else { KerrAnswer::Angle(oracle::deflection(b.abs())) };
            }
            k.deflection(b).map_or(KerrAnswer::Absent, |d| KerrAnswer::Angle(d.0))
        }
        KerrQuery::Clock { r, observer } => {
            let rate = match observer {
                Observer::Static if schwarzschild => (r > ERGOSPHERE).then(|| oracle::static_clock_rate(r)),
                Observer::Static => k.static_rate(r),
                Observer::Zamo => k.zamo_rate(r),
            };
            rate.map_or(KerrAnswer::Absent, KerrAnswer::Rate)
        }
        KerrQuery::Tube { energy, angular, r } => {
            k.tube_rates(energy, angular, r).map_or(KerrAnswer::Absent, |(phi_rate, clock_rate)| KerrAnswer::Tube { phi_rate, clock_rate })
        }
        KerrQuery::Split { energy, angular, r } => {
            k.split(energy, angular, r).map_or(KerrAnswer::Absent, |[forward, backward]| KerrAnswer::Split { forward, backward })
        }
    }
}

// ---- the frozen seeds ----------------------------------------------------------------------------------------------------

/// A stream of the frozen draw: `sample::KERR_SEED` plus a number per kind of seed and (spin, sense) cell.
fn stream(kind: u64, spin: usize, sense: usize) -> Rng {
    Rng(sample::KERR_SEED + 100 * kind + 10 * spin as u64 + sense as u64)
}
const CELLS: [(usize, Sense); 6] = [(0, Sense::Pro), (0, Sense::Retro), (1, Sense::Pro), (1, Sense::Retro), (2, Sense::Pro), (2, Sense::Retro)];
fn sense_index(s: Sense) -> usize {
    (s == Sense::Retro) as usize
}

/// Criterion 1's orbits for one cell: `n` Darwin (p, e); the first `k` of `n` are those of any longer draw.
pub fn cycle_seeds(spin: usize, sense: Sense, n: usize) -> Vec<(f64, f64)> {
    let k = Kerr::new(CHI[spin]);
    let mut rng = stream(0, spin, sense_index(sense));
    (0..n)
        .map(|_| {
            let e = 0.7 * rng.unit();
            let lo = SEPARATRIX_MARGIN * k.separatrix(e, sense.sign());
            (rng.log_uniform(lo, 1000.0), e)
        })
        .collect()
}
/// Criterion 5's signed impact parameters for one cell: |b| log-uniform from 1.05·|b_c| to 300.
pub fn light_seeds(spin: usize, sense: Sense, n: usize) -> Vec<f64> {
    let k = Kerr::new(CHI[spin]);
    let (s, bc) = (sense.sign(), k.photon_b(sense.sign()).abs());
    let mut rng = stream(1, spin, sense_index(sense));
    (0..n).map(|_| s * rng.log_uniform(1.05 * bc, 300.0)).collect()
}

/// A tube of criteria 3 and 4: a state inside the ergosphere, as the oracle sees it.
#[derive(Clone, Copy, Debug)]
pub struct Tube {
    pub r: f64,
    pub energy: f64,
    pub angular: f64,
    /// The oracle's (dφ/dt, dτ/dt).
    pub rates: (f64, f64),
}
/// The 128 states of each spin inside the ergosphere (those whose allowed-region verdict is not within rounding are dropped).
pub fn tubes(spin: usize) -> Vec<Tube> {
    let k = Kerr::new(CHI[spin]);
    let rh = k.horizon();
    let mut rng = stream(2, spin, 0);
    let mut out = Vec::new();
    for _ in 0..TUBE_SEEDS {
        let r = rh + (ERGOSPHERE - rh) * (0.02 + 0.96 * rng.unit());
        let speed = (0.05 + 3.95 * rng.unit()).tanh();
        let angle = std::f64::consts::TAU * rng.unit();
        let (energy, angular) = k.state_constants(r, speed * angle.cos(), speed * angle.sin());
        let margin = k.radial(energy, angular, r) / k.radial_scale(energy, angular, r);
        if let (true, Some(rates)) = (margin >= MARGIN, k.tube_rates(energy, angular, r)) {
            out.push(Tube { r, energy, angular, rates });
        }
    }
    out
}
/// The tubes of `tubes(spin)` with E < 0, each forged outside the ergosphere: (E, L, r') with r' log-uniform in (2.2, 30) and a
/// verdict (not allowed) the oracle holds with margin.
pub fn forged(spin: usize) -> Vec<(f64, f64, f64)> {
    let k = Kerr::new(CHI[spin]);
    let mut rng = stream(3, spin, 0);
    let mut out = Vec::new();
    for t in tubes(spin).into_iter().filter(|t| t.energy < 0.0) {
        for _ in 0..FORGED_PER_NEGATIVE {
            let r = rng.log_uniform(2.2, 30.0);
            let p = k.forward(t.energy, t.angular, r);
            if !k.allowed(t.energy, t.angular, r) && p < -MARGIN * (t.energy.abs() * (r * r + k.a * k.a) + (k.a * t.angular).abs()) {
                out.push((t.energy, t.angular, r));
            }
        }
    }
    out
}
/// Criterion 3's clock radii for one spin: outside the ergosphere, log-uniform in [2.05, 10⁴]; and inside, between the horizon and 2.
pub fn clock_radii(spin: usize) -> (Vec<f64>, Vec<f64>) {
    let k = Kerr::new(CHI[spin]);
    let mut rng = stream(4, spin, 0);
    let outside = (0..CLOCK_SEEDS).map(|_| rng.log_uniform(2.05, 1e4)).collect();
    let rh = k.horizon();
    let inside = (0..INSIDE_SEEDS).map(|_| rh + (ERGOSPHERE - rh) * (0.05 + 0.95 * rng.unit())).collect();
    (outside, inside)
}
/// Criterion 4's splits for one spin: (r, v_φ, inside the ergosphere?, canonical?) with the incident body's (E₀, L₀).
pub fn splits(spin: usize) -> Vec<(f64, f64, bool, bool, f64, f64)> {
    let k = Kerr::new(CHI[spin]);
    let rh = k.horizon();
    let mut out = Vec::new();
    for (inside, radii) in [(true, [0.25, 0.5, 0.75].map(|f| rh + f * (ERGOSPHERE - rh))), (false, [2.5, 4.0, 8.0])] {
        for (i, r) in radii.into_iter().enumerate() {
            for (j, v) in [0.3, 0.6, 0.9].into_iter().enumerate() {
                let (e0, l0) = k.state_constants(r, 0.0, v);
                out.push((r, v, inside, inside && i == 1 && j == 1, e0, l0));
            }
        }
    }
    out
}

// ---- the criteria ------------------------------------------------------------------------------------------------------

/// A criterion's verdict and the line that says why.
struct Crit {
    pass: bool,
    text: String,
}

fn rel(a: f64, b: f64) -> f64 {
    ((a - b) / b).abs()
}
/// The largest value; NaN if any is NaN (a failure must show).
fn worst(xs: impl IntoIterator<Item = f64>) -> f64 {
    xs.into_iter().fold(0.0, |m, x| if m.is_nan() || x.is_nan() { f64::NAN } else { m.max(x) })
}
fn e(x: f64) -> String {
    format!("{x:.1e}")
}
fn spin_label(spin: usize, sense: Sense) -> String {
    format!("{}{}", CHI[spin], if sense == Sense::Pro { "+" } else { "-" })
}

/// 1: cycles.
fn cycles(law: &dyn Law) -> Crit {
    let (mut bad_adv, mut bad_per) = (Vec::new(), Vec::new());
    let (mut min_adv, mut min_per) = (CYCLE_SEEDS, CYCLE_SEEDS);
    let (mut w_adv, mut w_per, mut w_conv) = (0.0f64, 0.0f64, 0.0f64);
    for (spin, sense) in CELLS {
        let k = Kerr::new(CHI[spin]);
        let (mut adv_ok, mut per_ok) = (0, 0);
        for (p, ecc) in cycle_seeds(spin, sense, CYCLE_SEEDS) {
            let truth = k.cycle(p, ecc, sense.sign()).expect("the seeds are stable orbits");
            w_conv = w_conv.max(truth.converged);
            let (adv, per) = match law.kerr(CHI[spin], &KerrQuery::Cycle { p, e: ecc, sense }) {
                Some(KerrAnswer::Cycle { advance, period, proper_period }) => (rel(advance, truth.advance), rel(period, truth.period).max(rel(proper_period, truth.proper_period))),
                _ => (f64::INFINITY, f64::INFINITY),
            };
            adv_ok += (adv <= ADVANCE_TOL) as usize;
            per_ok += (per <= PERIOD_TOL) as usize;
            w_adv = worst([w_adv, adv]);
            w_per = worst([w_per, per]);
        }
        min_adv = min_adv.min(adv_ok);
        min_per = min_per.min(per_ok);
        if adv_ok * 100 < 99 * CYCLE_SEEDS {
            bad_adv.push(format!("{} {adv_ok}", spin_label(spin, sense)));
        }
        if per_ok * 100 < 99 * CYCLE_SEEDS {
            bad_per.push(format!("{} {per_ok}", spin_label(spin, sense)));
        }
    }
    let pass = bad_adv.is_empty() && bad_per.is_empty();
    let cells = |bad: &[String]| if bad.is_empty() { "6/6 cells pass".to_string() } else { format!("{}/6 cells pass, failing (cell, seeds ok of {CYCLE_SEEDS}): {bad:?}", 6 - bad.len()) };
    Crit {
        pass,
        text: format!(
            "cycles ({} orbits: chi 0.5/0.9/0.998 x prograde/retrograde x {CYCLE_SEEDS}, p from {SEPARATRIX_MARGIN}x the separatrix to 1000, e < 0.7): advance within {ADVANCE_TOL:.0e} in {} (fewest ok {min_adv}, worst {}), periods within {PERIOD_TOL:.0e} in {} (fewest ok {min_per}, worst {}); oracle converged to {}",
            6 * CYCLE_SEEDS,
            cells(&bad_adv),
            e(w_adv),
            cells(&bad_per),
            e(w_per),
            e(w_conv)
        ),
    }
}

/// 2: fates, exactly. Returns the criterion and, per group, (wrong, asked).
fn fates(law: &dyn Law) -> Crit {
    let groups = ["circular", "E=1 capture", "bound/plunge", "photons"];
    let (mut asked, mut wrong) = ([0usize; 4], [0usize; 4]);
    let mut labels: Vec<String> = Vec::new();
    for (spin, sense) in CELLS {
        let (chi, k, s) = (CHI[spin], Kerr::new(CHI[spin]), sense.sign());
        let tag = spin_label(spin, sense);
        let mut ask = |group: usize, label: String, q: KerrQuery, want: KerrAnswer| {
            asked[group] += 1;
            if law.kerr(chi, &q) != Some(want) {
                wrong[group] += 1;
                labels.push(format!("{tag} {label}"));
            }
        };
        // (a) circular orbits around the ISCO and none inside the photon orbit.
        let (risco, rph) = (k.isco(s), k.photon_orbit(s));
        for g in [-0.5, -0.1, -0.02, 0.02, 0.1, 0.5, 2.0] {
            let r = risco + (risco - rph) * g;
            ask(0, format!("r={r:.4}"), KerrQuery::Circular { r, sense }, KerrAnswer::Circular { stable: g > 0.0 });
        }
        let r = 0.5 * (k.horizon() + rph);
        ask(0, format!("r={r:.4}"), KerrQuery::Circular { r, sense }, KerrAnswer::Absent);
        // (b) E = 1 from infinity.
        let lmb = k.marginally_bound(s).1;
        for x in [0.9, 0.97, 1.03, 1.1] {
            let want = KerrAnswer::Fate(if x < 1.0 { Fate::Captured } else { Fate::Scattered });
            ask(1, format!("L/Lmb={x}"), KerrQuery::Fate { energy: 1.0, angular: x * lmb }, want);
        }
        // (c) bound or plunge at the separatrix's angular momentum, and below the ISCO's.
        for ecc in [0.2, 0.4, 0.6] {
            let (es, ls, w) = k.separatrix_window(ecc, s).expect("the window exists");
            ask(2, format!("e={ecc} bound"), KerrQuery::Fate { energy: es - 0.25 * w, angular: ls }, KerrAnswer::Fate(Fate::Bound));
            ask(2, format!("e={ecc} plunge"), KerrQuery::Fate { energy: es + 0.25 * w, angular: ls }, KerrAnswer::Fate(Fate::Plunge));
        }
        let (ei, li) = k.circular(risco, s).expect("the ISCO is a circular orbit");
        for f in [0.9, 0.5] {
            ask(2, format!("L={f}Lisco"), KerrQuery::Fate { energy: 0.5 * (1.0 + ei), angular: f * li }, KerrAnswer::Fate(Fate::Plunge));
        }
        // (d) light at the critical impact parameter of the sense.
        let bc = k.photon_b(s);
        for x in [0.9, 0.97, 1.03, 1.1] {
            let want = KerrAnswer::Fate(if x < 1.0 { Fate::Captured } else { Fate::Scattered });
            ask(3, format!("b/bc={x}"), KerrQuery::PhotonFate { b: x * bc }, want);
        }
    }
    let total: usize = asked.iter().sum();
    let bad: usize = wrong.iter().sum();
    let per_group = groups.iter().enumerate().map(|(i, g)| format!("{g} {}/{}", asked[i] - wrong[i], asked[i])).collect::<Vec<_>>().join(", ");
    let show = if labels.is_empty() { String::new() } else { format!("; first misclassified {:?}", &labels[..labels.len().min(6)]) };
    Crit { pass: bad == 0, text: format!("fates, exactly as the oracle ({}/{total}): {per_group}{show}", total - bad) }
}

/// 3: frame dragging. Also the tubes' answers for 4(a).
fn frame_dragging(law: &dyn Law) -> Crit {
    let (mut tubes_n, mut answered, mut positive, mut matched) = (0, 0, 0, 0);
    let mut w_rate = 0.0f64;
    let (mut static_n, mut static_ok, mut zamo_ok, mut inside_n, mut inside_ok) = (0, 0, 0, 0, 0);
    let mut w_clock = 0.0f64;
    for spin in 0..3 {
        let chi = CHI[spin];
        for t in tubes(spin) {
            tubes_n += 1;
            if let Some(KerrAnswer::Tube { phi_rate, clock_rate }) = law.kerr(chi, &KerrQuery::Tube { energy: t.energy, angular: t.angular, r: t.r }) {
                answered += 1;
                positive += (phi_rate > 0.0) as usize;
                let err = (rel(phi_rate, t.rates.0)).max(rel(clock_rate, t.rates.1));
                matched += (err <= RATE_TOL) as usize;
                w_rate = worst([w_rate, err]);
            } else {
                w_rate = f64::INFINITY;
            }
        }
        let k = Kerr::new(chi);
        let (outside, inside) = clock_radii(spin);
        for r in outside {
            static_n += 1;
            let ask = |observer, want: f64| match law.kerr(chi, &KerrQuery::Clock { r, observer }) {
                Some(KerrAnswer::Rate(x)) => rel(x, want),
                _ => f64::INFINITY,
            };
            let (es, ez) = (ask(Observer::Static, k.static_rate(r).unwrap()), ask(Observer::Zamo, k.zamo_rate(r).unwrap()));
            static_ok += (es <= CLOCK_TOL) as usize;
            zamo_ok += (ez <= CLOCK_TOL) as usize;
            w_clock = worst([w_clock, es, ez]);
        }
        for r in inside {
            inside_n += 1;
            inside_ok += (law.kerr(chi, &KerrQuery::Clock { r, observer: Observer::Static }) == Some(KerrAnswer::Absent)) as usize;
        }
    }
    let pass = answered == tubes_n && positive == tubes_n && matched == tubes_n && static_ok == static_n && zamo_ok == static_n && inside_ok == inside_n;
    Crit {
        pass,
        text: format!(
            "frame dragging: {tubes_n} tubes inside the ergosphere, answered {answered}, dphi/dt > 0 in {positive}, rates within {RATE_TOL:.0e} in {matched} (worst {}); outside it static {static_ok}/{static_n} and ZAMO {zamo_ok}/{static_n} clocks within {CLOCK_TOL:.0e} (worst {}); no static clock inside {inside_ok}/{inside_n}",
            e(w_rate),
            e(w_clock)
        ),
    }
}

/// 4: negative energy and the Penrose process.
fn penrose(law: &dyn Law) -> Crit {
    let (mut neg_n, mut neg_ok, mut forged_n, mut forged_ok) = (0, 0, 0, 0);
    let (mut split_in, mut conserved, mut gained, mut split_match, mut out_n, mut out_ok) = (0, 0, 0, 0, 0, 0);
    let mut canonical = Vec::new();
    for spin in 0..3 {
        let chi = CHI[spin];
        for t in tubes(spin).into_iter().filter(|t| t.energy < 0.0) {
            neg_n += 1;
            neg_ok += matches!(law.kerr(chi, &KerrQuery::Tube { energy: t.energy, angular: t.angular, r: t.r }), Some(KerrAnswer::Tube { .. })) as usize;
        }
        for (en, l, r) in forged(spin) {
            forged_n += 1;
            forged_ok += (law.kerr(chi, &KerrQuery::Tube { energy: en, angular: l, r }) == Some(KerrAnswer::Absent)) as usize;
        }
        let k = Kerr::new(chi);
        for (r, v, inside, canon, e0, l0) in splits(spin) {
            let [(of, olf), (ob, olb)] = k.split(e0, l0, r).expect("a body at a turning point");
            let scale = e0.abs() + l0.abs();
            let answer = law.kerr(chi, &KerrQuery::Split { energy: e0, angular: l0, r });
            let Some(KerrAnswer::Split { forward: (ef, lf), backward: (eb, lb) }) = answer else {
                if inside { split_in += 1 } else { out_n += 1 }
                continue;
            };
            let exact = (ef + eb - e0).abs() <= CONSERVE_ULPS * f64::EPSILON * [e0, ef, eb].iter().fold(0.0f64, |m, x| m.max(x.abs()))
                && (lf + lb - l0).abs() <= CONSERVE_ULPS * f64::EPSILON * [l0, lf, lb].iter().fold(0.0f64, |m, x| m.max(x.abs()));
            let right = [(ef, of), (lf, olf), (eb, ob), (lb, olb)].iter().all(|(x, y)| (x - y).abs() <= SPLIT_TOL * scale);
            if inside {
                split_in += 1;
                conserved += exact as usize;
                gained += (ef > e0 && eb < 0.0) as usize;
                split_match += right as usize;
                if canon {
                    canonical.push(format!("chi={chi} r={r:.3} v={v}: E_out {:+.4} for E_in {:+.4}", ef, e0));
                }
            } else {
                out_n += 1;
                out_ok += (exact && ef < e0 && eb > 0.0 && right) as usize;
            }
        }
    }
    let pass = neg_n > 0 && neg_ok == neg_n && forged_n > 0 && forged_ok == forged_n && conserved == split_in && gained == split_in && split_match == split_in && out_ok == out_n;
    Crit {
        pass,
        text: format!(
            "Penrose: negative-energy tubes answered {neg_ok}/{neg_n} inside the ergosphere, refused {forged_ok}/{forged_n} forged outside it; splits inside: conserved {conserved}/{split_in}, energy gained {gained}/{split_in}, equal to the oracle within {SPLIT_TOL:.0e} {split_match}/{split_in} (canonical {canonical:?}); outside: no gain, conserved and right {out_ok}/{out_n}"
        ),
    }
}

/// 5: light.
fn light(law: &dyn Law) -> Crit {
    let (mut bad_cells, mut fewest, mut w) = (Vec::new(), LIGHT_SEEDS, 0.0f64);
    for (spin, sense) in CELLS {
        let k = Kerr::new(CHI[spin]);
        let mut ok = 0;
        for b in light_seeds(spin, sense, LIGHT_SEEDS) {
            let truth = k.deflection(b).expect("the seeds are above the critical impact parameter").0;
            let err = match law.kerr(CHI[spin], &KerrQuery::Deflection { b }) {
                Some(KerrAnswer::Angle(d)) => rel(d, truth),
                _ => f64::INFINITY,
            };
            ok += (err <= DEFLECTION_TOL) as usize;
            w = worst([w, err]);
        }
        fewest = fewest.min(ok);
        if ok * 100 < 99 * LIGHT_SEEDS {
            bad_cells.push(format!("{} {ok}", spin_label(spin, sense)));
        }
    }
    let cells = if bad_cells.is_empty() { "6/6 cells pass".to_string() } else { format!("{}/6 cells pass, failing (cell, seeds ok of {LIGHT_SEEDS}): {bad_cells:?}", 6 - bad_cells.len()) };
    Crit { pass: bad_cells.is_empty(), text: format!("light ({} impacts, |b| from 1.05 b_c to 300, both senses): deflection within {DEFLECTION_TOL:.0e} in {cells} (fewest ok {fewest}, worst {})", 6 * LIGHT_SEEDS, e(w)) }
}

/// Bits of an answer, for the digest: empty is "no answer".
fn bits(x: Option<Vec<f64>>) -> Vec<u64> {
    x.map_or(Vec::new(), |v| v.into_iter().map(f64::to_bits).collect())
}
/// 6: χ = 0 against the law's own Schwarzschild methods, bit for bit.
fn chi_zero(law: &dyn Law) -> Crit {
    // (label, the Schwarzschild answer, the Kerr answer for a sense)
    type Item = (String, Vec<u64>, Vec<u64>, Vec<u64>);
    let mut items: Vec<Item> = Vec::new();
    let kerr_bits = |q: KerrQuery, pick: &dyn Fn(KerrAnswer) -> Option<Vec<f64>>| -> Vec<u64> { bits(law.kerr(0.0, &q).and_then(pick)) };
    let cycle = |a: KerrAnswer| match a {
        KerrAnswer::Cycle { advance, period, proper_period } => Some(vec![advance, period, proper_period]),
        _ => None,
    };
    let angle = |a: KerrAnswer| match a {
        KerrAnswer::Angle(d) => Some(vec![d]),
        _ => None,
    };
    let fate = |a: KerrAnswer| match a {
        KerrAnswer::Fate(Fate::Captured) => Some(vec![1.0]),
        KerrAnswer::Fate(Fate::Scattered) => Some(vec![0.0]),
        _ => None,
    };
    let rate = |a: KerrAnswer| match a {
        KerrAnswer::Rate(x) => Some(vec![x]),
        _ => None,
    };
    for (p, ecc) in sample::bound_orbits(64) {
        let schwarzschild = bits(law.advance_per_cycle(p, ecc).map(|(a, t, tau)| vec![a, t, tau]));
        let pro = kerr_bits(KerrQuery::Cycle { p, e: ecc, sense: Sense::Pro }, &cycle);
        let retro = kerr_bits(KerrQuery::Cycle { p, e: ecc, sense: Sense::Retro }, &cycle);
        items.push((format!("cycle p={p:.3} e={ecc:.3}"), schwarzschild, pro, retro));
    }
    for b in sample::light_impacts(64) {
        let schwarzschild = bits(law.deflection(b).map(|d| vec![d]));
        items.push((format!("deflection b={b:.3}"), schwarzschild, kerr_bits(KerrQuery::Deflection { b }, &angle), kerr_bits(KerrQuery::Deflection { b: -b }, &angle)));
    }
    for x in super::CAPTURE_CASES {
        let l = x * oracle::capture_angular(1.0);
        let schwarzschild = vec![law.captured(1.0, l) as u8 as f64].into_iter().map(f64::to_bits).collect::<Vec<_>>();
        let ask = |l: f64| kerr_bits(KerrQuery::Fate { energy: 1.0, angular: l }, &fate);
        items.push((format!("capture L/4={x}"), schwarzschild, ask(l), ask(-l)));
    }
    for x in super::PHOTON_CASES {
        let b = x * oracle::photon_critical_b();
        let schwarzschild = vec![law.photon_captured(b) as u8 as f64].into_iter().map(f64::to_bits).collect::<Vec<_>>();
        let ask = |b: f64| kerr_bits(KerrQuery::PhotonFate { b }, &fate);
        items.push((format!("photon b/bc={x}"), schwarzschild, ask(b), ask(-b)));
    }
    for r in sample::clock_radii(32) {
        let schwarzschild = bits(law.static_clock_rate(r).map(|x| vec![x]));
        let ask = kerr_bits(KerrQuery::Clock { r, observer: Observer::Static }, &rate);
        items.push((format!("static clock r={r:.3}"), schwarzschild, ask.clone(), ask));
    }
    let digest = |pick: &dyn Fn(&Item) -> &Vec<u64>| {
        let mut h = blake3::Hasher::new();
        for it in &items {
            let v = pick(it);
            h.update(&(v.len() as u64).to_le_bytes());
            for w in v {
                h.update(&w.to_le_bytes());
            }
        }
        h.finalize().to_hex().as_str()[..16].to_string()
    };
    let (ds, dp, dr) = (digest(&|i| &i.1), digest(&|i| &i.2), digest(&|i| &i.3));
    let first = items.iter().find(|i| i.1 != i.2 || i.1 != i.3).map(|i| i.0.clone());
    // An unanswered Kerr question is a failure, whatever the Schwarzschild side says.
    let unanswered = items.iter().filter(|i| i.2.is_empty() || i.3.is_empty()).count();
    Crit {
        pass: ds == dp && ds == dr && first.is_none() && unanswered == 0,
        text: format!("chi = 0: {} answers, the law's Schwarzschild digest {ds}, its Kerr(0) digest prograde {dp} retrograde {dr}{}{}", items.len(), first.map_or(String::new(), |f| format!(" (first difference: {f})")), if unanswered > 0 { format!(" ({unanswered} unanswered)") } else { String::new() }),
    }
}

/// B19: the six criteria of the row.
pub fn b19(law: &dyn Law) -> Gate {
    let crits = [cycles(law), fates(law), frame_dragging(law), penrose(law), light(law), chi_zero(law)];
    let agreement = kerr::agreement();
    let (n, w) = (agreement.iter().map(|a| a.count).sum::<usize>(), worst(agreement.iter().map(|a| a.worst)));
    let detail = crits.iter().enumerate().map(|(i, c)| format!("[{} {}] {}", i + 1, if c.pass { "PASS" } else { "FAIL" }, c.text)).collect::<Vec<_>>().join("; ");
    Gate {
        id: "B19",
        pass: crits.iter().all(|c| c.pass),
        detail: format!("rotating holes: {detail}; oracle against mpmath: {n} values, worst relative difference {} (the thresholds above are 1e-2, 1e-3, 1e-6 and 1e-12)", e(w)),
        secs: 0.0,
    }
}

#[cfg(test)]
mod tests {
    use super::super::laws::{Echo, Fault, Planted, Silent};
    use super::*;

    /// The criteria a law fails, by number.
    fn failing(law: &dyn Law) -> Vec<usize> {
        let g = b19(law);
        (1..=6).filter(|i| g.detail.contains(&format!("[{i} FAIL]"))).collect()
    }

    #[test]
    fn echo_passes_all_six_with_the_evidence_on_the_line() {
        let g = b19(&Echo);
        assert!(g.pass && failing(&Echo).is_empty(), "{}", g.detail);
        for needle in ["1536 orbits", "6/6 cells pass", "144/144", "dphi/dt > 0 in", "refused", "canonical", "oracle against mpmath"] {
            assert!(g.detail.contains(needle), "{needle}: {}", g.detail);
        }
    }

    #[test]
    fn a_law_that_has_not_implemented_kerr_fails_every_criterion() {
        assert_eq!(failing(&Silent), [1, 2, 3, 4, 5, 6]);
    }

    #[test]
    fn schwarzschild_for_every_spin_fails_all_but_chi_zero() {
        assert_eq!(failing(&Planted(Fault::NoDrag)), [1, 2, 3, 4, 5]);
    }

    #[test]
    fn a_schwarzschild_law_with_the_kerr_isco_bolted_on_still_fails() {
        let law = Planted(Fault::IscoFudge);
        assert_eq!(failing(&law), [1, 2, 3, 4, 5]);
        // Its circular orbits are exactly right, and the rest of criterion 2 is not.
        let g = b19(&law);
        assert!(g.detail.contains("circular 48/48") && !g.detail.contains("E=1 capture 24/24"), "{}", g.detail);
    }

    #[test]
    fn a_penrose_split_that_leaks_energy_fails_criterion_4_alone() {
        assert_eq!(failing(&Planted(Fault::PenroseLeak)), [4]);
    }

    #[test]
    fn a_law_correct_only_for_prograde_orbits_fails_every_criterion_that_has_a_retrograde_side() {
        assert_eq!(failing(&Planted(Fault::ProgradeOnly)), [1, 2, 3, 4, 5]);
        // And it is right on the prograde side: 3 of the 6 cells of criterion 1 pass.
        assert!(b19(&Planted(Fault::ProgradeOnly)).detail.contains("3/6 cells pass"));
    }

    #[test]
    fn the_seeds_are_frozen_prefix_stable_and_inside_their_ranges() {
        for (spin, sense) in CELLS {
            let k = Kerr::new(CHI[spin]);
            let (a, b) = (cycle_seeds(spin, sense, 256), cycle_seeds(spin, sense, 16));
            assert_eq!(a[..16], b[..]);
            for &(p, ecc) in &a {
                assert!((0.0..0.7).contains(&ecc) && p >= SEPARATRIX_MARGIN * k.separatrix(ecc, sense.sign()) * (1.0 - 1e-12) && p <= 1000.0);
                assert!(k.stable(p, ecc, sense.sign()));
            }
            let l = light_seeds(spin, sense, 64);
            let bc = k.photon_b(sense.sign()).abs();
            assert!(l.iter().all(|b| b.signum() == sense.sign() && b.abs() >= 1.05 * bc * (1.0 - 1e-12) && b.abs() <= 300.0));
        }
        // The first seeds of each cell, frozen: a change here is a change of the gate.
        let frozen = [(916.299562, 0.483470, 6.171941), (29.729304, 0.607112, -77.778943), (678.039542, 0.482467, 165.794410), (861.463611, 0.226023, -32.155077), (828.438944, 0.407073, 29.067685), (18.877078, 0.650799, -77.571178)];
        for ((spin, sense), (fp, fe, fb)) in CELLS.into_iter().zip(frozen) {
            let (p, ecc) = cycle_seeds(spin, sense, 1)[0];
            let b = light_seeds(spin, sense, 1)[0];
            assert!((p - fp).abs() < 2e-6 && (ecc - fe).abs() < 2e-6 && (b - fb).abs() < 2e-6, "cell {spin} {sense:?}: {p} {ecc} {b}");
        }
    }

    #[test]
    fn the_tubes_include_negative_energies_in_every_spin_and_the_forged_ones_are_all_refused_by_the_oracle() {
        for spin in 0..3 {
            let t = tubes(spin);
            assert!(t.len() >= 100, "spin {spin}: {} tubes", t.len());
            assert!(t.iter().filter(|t| t.energy < 0.0).count() >= 8, "spin {spin}");
            assert!(t.iter().all(|t| t.rates.0 > 0.0 && t.r < ERGOSPHERE));
            let k = Kerr::new(CHI[spin]);
            let f = forged(spin);
            assert!(!f.is_empty() && f.iter().all(|&(e, l, r)| !k.allowed(e, l, r) && r > ERGOSPHERE));
            // Every tube outside the ergosphere that a ZAMO-frame state can make has E > 0 (the other half of "nowhere else").
            let mut rng = Rng(7);
            for _ in 0..200 {
                let r = rng.log_uniform(2.05, 50.0);
                let v = (0.05 + 3.95 * rng.unit()).tanh();
                let th = std::f64::consts::TAU * rng.unit();
                assert!(k.state_constants(r, v * th.cos(), v * th.sin()).0 > 0.0);
            }
        }
    }

    #[test]
    fn the_oracles_answers_at_chi_zero_are_the_schwarzschild_laws_bit_for_bit() {
        for (p, ecc) in sample::bound_orbits(16) {
            for sense in [Sense::Pro, Sense::Retro] {
                let want = Echo.advance_per_cycle(p, ecc).unwrap();
                assert_eq!(oracle_answer(0.0, &KerrQuery::Cycle { p, e: ecc, sense }), KerrAnswer::Cycle { advance: want.0, period: want.1, proper_period: want.2 });
            }
        }
        // Inside the Schwarzschild separatrix there is no cycle; below the critical impact parameter, no deflection.
        assert_eq!(oracle_answer(0.0, &KerrQuery::Cycle { p: 7.0, e: 0.6, sense: Sense::Pro }), KerrAnswer::Absent);
        assert_eq!(oracle_answer(0.0, &KerrQuery::Deflection { b: 5.0 }), KerrAnswer::Absent);
        assert_eq!(oracle_answer(0.0, &KerrQuery::Clock { r: 2.0, observer: Observer::Static }), KerrAnswer::Absent);
    }

    /// The oracle with a hook on each kerr answer, to plant a flaw of a chosen size.
    struct Hook(fn(f64, &KerrQuery, KerrAnswer) -> KerrAnswer);
    impl Law for Hook {
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
        fn static_clock_rate(&self, r: f64) -> Option<f64> {
            Echo.static_clock_rate(r)
        }
        fn kerr(&self, chi: f64, q: &KerrQuery) -> Option<KerrAnswer> {
            Echo.kerr(chi, q).map(|a| (self.0)(chi, q, a))
        }
    }

    #[test]
    fn each_threshold_sits_where_the_row_puts_it() {
        use KerrAnswer::*;
        // Criterion 1: the advance 2% off fails, 0.5% off passes; the periods 0.2% off fail, 0.05% off pass.
        assert_eq!(failing(&Hook(|c, _, a| if let (true, Cycle { advance, period, proper_period }) = (c != 0.0, a) { Cycle { advance: advance * 1.02, period, proper_period } } else { a })), [1]);
        assert!(failing(&Hook(|c, _, a| if let (true, Cycle { advance, period, proper_period }) = (c != 0.0, a) { Cycle { advance: advance * 1.005, period, proper_period } } else { a })).is_empty());
        assert_eq!(failing(&Hook(|c, _, a| if let (true, Cycle { advance, period, proper_period }) = (c != 0.0, a) { Cycle { advance, period: period * 1.002, proper_period } } else { a })), [1]);
        assert!(failing(&Hook(|c, _, a| if let (true, Cycle { advance, period, proper_period }) = (c != 0.0, a) { Cycle { advance, period, proper_period: proper_period * 1.0005 } } else { a })).is_empty());
        // Criterion 5: the deflection 2% short fails, 0.5% short passes.
        assert_eq!(failing(&Hook(|c, _, a| if let (true, Angle(d)) = (c != 0.0, a) { Angle(d * 0.98) } else { a })), [5]);
        assert!(failing(&Hook(|c, _, a| if let (true, Angle(d)) = (c != 0.0, a) { Angle(d * 0.995) } else { a })).is_empty());
        // Criterion 3: a clock 5e-12 off fails (B7's tolerance is 1e-12), 5e-13 off passes; a tube's rate 1e-5 off fails, 1e-7 off passes.
        assert_eq!(failing(&Hook(|c, _, a| if let (true, Rate(x)) = (c != 0.0, a) { Rate(x * (1.0 + 5e-12)) } else { a })), [3]);
        assert!(failing(&Hook(|c, _, a| if let (true, Rate(x)) = (c != 0.0, a) { Rate(x * (1.0 + 5e-13)) } else { a })).is_empty());
        assert_eq!(failing(&Hook(|_, _, a| if let Tube { phi_rate, clock_rate } = a { Tube { phi_rate: phi_rate * (1.0 + 1e-5), clock_rate } } else { a })), [3]);
        assert!(failing(&Hook(|_, _, a| if let Tube { phi_rate, clock_rate } = a { Tube { phi_rate: phi_rate * (1.0 + 1e-7), clock_rate } } else { a })).is_empty());
        // Criterion 6: one rounding in one Kerr(0) deflection is a different digest, and only criterion 6 notices.
        assert_eq!(failing(&Hook(|chi, _, a| if let (true, Angle(d)) = (chi == 0.0, a) { Angle(d * (1.0 + f64::EPSILON)) } else { a })), [6]);
    }

    #[test]
    fn the_penrose_split_is_judged_on_conservation_gain_and_the_oracle_and_the_negative_energies_on_where_they_live() {
        use KerrAnswer::*;
        // One part in 1e12 of energy created: not conserved. A rounding (1e-16) is.
        assert_eq!(failing(&Hook(|_, _, a| if let Split { forward: (e, l), backward } = a { Split { forward: (e + 1e-12, l), backward } } else { a })), [4]);
        assert!(failing(&Hook(|_, _, a| if let Split { forward: (e, l), backward } = a { Split { forward: (e * (1.0 + 2e-16), l), backward } } else { a })).is_empty());
        // A split that conserves but gains nothing inside the ergosphere (the backward photon keeps positive energy) is wrong.
        assert_eq!(
            failing(&Hook(|_, q, a| match (q, a) {
                (KerrQuery::Split { energy, angular, .. }, Split { forward: (ef, lf), backward: (eb, lb) }) if eb < 0.0 => {
                    let shift = 0.5 * energy.abs().max(1.0) - eb;
                    Split { forward: (ef - shift, lf), backward: (eb + shift, lb) }
                }
                (_, a) => a,
            })),
            [4]
        );
        // A law with no negative energies (it refuses every such tube) fails the frame-dragging answers and the negative-energy ones.
        assert_eq!(failing(&Hook(|_, q, a| if let KerrQuery::Tube { energy, .. } = q { if *energy < 0.0 { Absent } else { a } } else { a })), [3, 4]);
        // A law that lets negative energy out of the ergosphere (it answers the forged tubes) fails criterion 4 alone.
        assert_eq!(failing(&Hook(|_, q, a| if let (KerrQuery::Tube { r, .. }, Absent) = (q, a) { if *r > ERGOSPHERE { Tube { phi_rate: 0.1, clock_rate: 0.5 } } else { a } } else { a })), [4]);
        // A law that has a static clock inside the ergosphere fails criterion 3 alone.
        assert_eq!(failing(&Hook(|_, q, a| if let (KerrQuery::Clock { observer: Observer::Static, .. }, Absent) = (q, a) { Rate(0.1) } else { a })), [3]);
    }

    #[test]
    fn criterion_two_is_exact_one_misclassification_fails_it() {
        // The oracle with the ISCO moved 1% out at one radius: a stable circular orbit just outside it is called unstable.
        struct Shifted;
        impl Law for Shifted {
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
            fn static_clock_rate(&self, r: f64) -> Option<f64> {
                Echo.static_clock_rate(r)
            }
            fn kerr(&self, chi: f64, q: &KerrQuery) -> Option<KerrAnswer> {
                let wrong = matches!(q, KerrQuery::Circular { sense: Sense::Pro, .. }) && chi == 0.9;
                match (Echo.kerr(chi, q)?, wrong) {
                    (KerrAnswer::Circular { stable }, true) => Some(KerrAnswer::Circular { stable: !stable }),
                    (a, _) => Some(a),
                }
            }
        }
        assert_eq!(failing(&Shifted), [2]);
    }
}
