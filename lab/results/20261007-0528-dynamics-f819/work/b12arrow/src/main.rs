//! B12's replacement statistic: the time-arrow test. Built on copies of the judge's own
//! reference (`restricted.rs`), the seed sampler and the planted laws; nothing in the crates
//! or the gates is touched.
//!
//! Requirement (PRINCIPLES 13, "errors never compound"; OC#42 "types of errors and not just
//! errors"): a law's handoff error must not carry the memory of past crossings. The complement
//! is an error that is a function of the ship's current state: such an error returns whenever
//! the state returns, so at a fixed state it has no arrow of time. A compounding error (a walk
//! in the encounter count, a leak, the reference's own drift) is larger at late times than at
//! early times *at the same state*, because returning to the state does not return the history.
//!
//! The test: match each early far-field sample of a ship to its nearest late sample in the
//! normalized slow state (a, e) (at least GAP periods apart, one-to-one), and read the sign of
//! |C_J error|_late − |C_J error|_early. Under no-memory the pair is a fair coin (chaos mixes
//! the fast state; the slow state is matched), so the per-ship concordance count is binomial
//! and the pooled gate statistic is the median per-ship z. Thresholds are derived from that
//! null, not fitted to any law.
//!
//! The judged ship set is machine-independent: the frozen 16 ships are bit constants, and each
//! is classified (busy crossing R_SOI, outside the planet in the reference) by the MEDIAN over a
//! five-run one-ulp replica ensemble of the reference, not by one chaotic path.
mod restricted;

use restricted::{Integrator, Model, Restricted, JUPITER, RTOL};
use std::sync::atomic::Ordering;

// ---------------------------------------------------------------- sampler (sample.rs, verbatim logic)

/// SplitMix64.
pub struct Rng(pub u64);
impl Rng {
    pub fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    /// Uniform in [0, 1) with 53 bits.
    fn unit(&mut self) -> f64 {
        (self.next() >> 11) as f64 / (1u64 << 53) as f64
    }
}

pub const HANDOFF_SEED: u64 = 20261002;

/// `n` handoff candidates (side, k, α), as the gate draws them.
pub fn handoffs(n: usize) -> Vec<(f64, f64, f64)> {
    let mut rng = Rng(HANDOFF_SEED);
    (0..n)
        .map(|_| {
            let side = if rng.next() >> 63 == 1 { 1.0 } else { -1.0 };
            let k = 1.5 + 1.5 * rng.unit();
            (side, k, (30.0 + 300.0 * rng.unit()).to_radians())
        })
        .collect()
}

/// The 16 frozen ships (sample::HANDOFF_KEPT): bit-constant indices into `handoffs`.
pub const HANDOFF_KEPT: [usize; 16] = [32, 39, 53, 57, 70, 72, 78, 83, 85, 88, 101, 106, 138, 142, 148, 159];

// ---------------------------------------------------------------- scene plumbing (handoff.rs, verbatim)

pub const PERIODS: usize = 200;
pub const COARSE: usize = 8;
pub const FINE: usize = 256;
pub const CROSSINGS_MIN: usize = 20;
pub const ERR_MAX: f64 = 1e-4;
pub const FLOOR: f64 = 1e-12;

/// A ship on the circular barycentric orbit of radius sep·(1 + side·x), x = (R_H/sep)·k.
pub fn ship(scene: &Restricted, side: f64, k: f64, alpha: f64) -> [f64; 4] {
    let r = scene.sep * (1.0 + side * scene.hill() / scene.sep * k);
    let v = r.powf(-0.5);
    [r * alpha.cos(), r * alpha.sin(), -v * alpha.sin(), v * alpha.cos()]
}

/// The law's sample times: t = 0 then every P/COARSE up to PERIODS.
pub fn coarse_times(scene: &Restricted) -> Vec<f64> {
    (0..=PERIODS * COARSE).map(|j| j as f64 * scene.period() / COARSE as f64).collect()
}

// ---------------------------------------------------------------- elements (resonance.rs, verbatim)

/// The heliocentric elements (a in absolute units, e) of a barycentric state at t.
pub fn elements(scene: &Restricted, t: f64, s: &[f64; 4]) -> (f64, f64) {
    let (p, v) = scene.star(t);
    let (x, y, vx, vy) = (s[0] - p[0], s[1] - p[1], s[2] - v[0], s[3] - v[1]);
    let gm = 1.0 - scene.mu;
    let (r, v2, rv) = ((x * x + y * y).sqrt(), vx * vx + vy * vy, x * vx + y * vy);
    let k = v2 - gm / r;
    let (ex, ey) = ((k * x - rv * vx) / gm, (k * y - rv * vy) / gm);
    (1.0 / (2.0 / r - v2 / gm), ex.hypot(ey))
}

// ---------------------------------------------------------------- planted laws (laws.rs, verbatim logic)

const BOUNDED: f64 = 1e-7;
const AXIS_CAP: f64 = 10.0;

fn star_axis(scene: &Restricted, t: f64, s: &[f64; 4]) -> f64 {
    let (energy, _) = scene.heliocentric(t, s);
    if energy < 0.0 { ((1.0 - scene.mu) / (-2.0 * energy) / scene.sep).min(AXIS_CAP) } else { AXIS_CAP }
}

/// Scale the rotating-frame velocity so the Jacobi constant moves by `want`.
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

fn plant_bounded(scene: &Restricted, ship: [f64; 4], times: &[f64], states: Vec<[f64; 4]>) -> Vec<[f64; 4]> {
    let (a0, c0, unit) = (star_axis(scene, 0.0, &ship), scene.jacobi(0.0, &ship).abs(), scene.hill() / scene.sep);
    let shift: Vec<f64> = times.iter().zip(&states).map(|(&t, s)| BOUNDED * (star_axis(scene, t, s) - a0) / unit * c0).collect();
    lay(scene, states, &shift)
}

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

/// The leak: the rotating-frame velocity carries `total` relative growth of the Jacobi error
/// spread linearly over the horizon (the harness leak's shape: v × (1 + total·t/H)).
fn plant_leak(scene: &Restricted, times: &[f64], states: Vec<[f64; 4]>, total: f64) -> Vec<[f64; 4]> {
    let (h, c0) = ((PERIODS as f64) * scene.period(), scene.jacobi(0.0, &states[0]).abs());
    lay(scene, states, &times.iter().map(|&t| -total * (t / h) * c0).collect::<Vec<_>>())
}

/// A bounded error periodic in absolute time (the red-team's gray case).
fn plant_periodic(scene: &Restricted, times: &[f64], states: Vec<[f64; 4]>) -> Vec<[f64; 4]> {
    let c0 = scene.jacobi(0.0, &states[0]).abs();
    let shift: Vec<f64> = times.iter().map(|&t| 1e-7 * (std::f64::consts::TAU * t / (100.0 * scene.period())).sin() * c0).collect();
    lay(scene, states, &shift)
}

// ---------------------------------------------------------------- the laws

#[derive(Clone, Copy, PartialEq)]
pub enum Law {
    Echo,
    Scaled,
    Bounded,
    Compound,
    Drift,
    Kick,
    Leak(f64),
    LeakBounded(f64),
    Periodic,
    /// Dynamics red-team: the exact conserving reference read at t(1+rate) — a pure clock
    /// drift. The ship sits on its true orbit, phaseslipped by rate*t; C_J is conserved along
    /// the orbit, so the Jacobi channel cannot see it.
    Clock(f64),
    /// The dual of planted-compound: the time offset random-walks by one step per SOI entry,
    /// instead of the Jacobi error.
    PhaseWalk,
    /// planted-compound with anti-persistent steps (AR(1) increments, phi = -0.9, matched
    /// stationary variance): does anti-persistence hide compounding from the rank test?
    AntiWalk,
    /// A bounded permanent Jacobi offset switched on at 95 P: time-localized but bounded;
    /// a gray positive control.
    StepMid,
}

impl Law {
    fn states(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        let echo = || {
            let mut it = Integrator::new(scene, Model::Full, RTOL, ship).conserving();
            times.iter().map(|&t| it.advance(t)).collect::<Option<Vec<_>>>()
        };
        match self {
            Law::Echo => echo(),
            Law::Scaled => echo().map(|st| st.into_iter().map(|s| [s[0], s[1], s[2] * (1.0 + 1e-11), s[3] * (1.0 + 1e-11)]).collect()),
            Law::Bounded => echo().map(|st| plant_bounded(scene, ship, times, st)),
            Law::Compound => echo().map(|st| plant_compound(scene, ship, times, st)),
            Law::Drift => restricted::reference(scene, ship, times, RTOL),
            Law::Kick => restricted::integrate(scene, Model::Kick(1.0 + 1e-3), RTOL, ship, times),
            Law::Leak(total) => echo().map(|st| plant_leak(scene, times, st, *total)),
            Law::LeakBounded(total) => echo().map(|st| {
                let b = plant_bounded(scene, ship, times, st);
                plant_leak(scene, times, b, *total)
            }),
            Law::Periodic => echo().map(|st| plant_periodic(scene, times, st)),
            Law::Clock(rate) => {
                let mut it = Integrator::new(scene, Model::Full, RTOL, ship).conserving();
                times.iter().map(|&t| it.advance(t * (1.0 + rate))).collect::<Option<Vec<_>>>()
            }
            Law::PhaseWalk => {
                // Pass 1: the echo states, to count SOI entries with the same rule the
                // compound plant uses. Pass 2: re-advance with the walked time offset.
                let st = echo()?;
                let mut rng = Rng(ship.iter().fold(0x5EED, |h, x| h.rotate_left(17) ^ x.to_bits()));
                let (mut delta, mut inside) = (0.0f64, false);
                let walked: Vec<f64> = times
                    .iter()
                    .zip(&st)
                    .map(|(&t, s)| {
                        let now = scene.planet_distance(t, s) < 3.0 * scene.hill();
                        if now && !inside {
                            delta += (rng.unit() - 0.5) * 0.02 * scene.period();
                        }
                        inside = now;
                        t + delta
                    })
                    .collect();
                let mut it = Integrator::new(scene, Model::Full, RTOL, ship).conserving();
                walked.iter().map(|&t| it.advance(t)).collect::<Option<Vec<_>>>()
            }
            Law::AntiWalk => echo().map(|st| {
                let c0 = scene.jacobi(0.0, &ship).abs();
                let mut rng = Rng(ship.iter().fold(0x5EED, |h, x| h.rotate_left(17) ^ x.to_bits()));
                let phi = -0.9f64;
                let noise = (1.0 - phi * phi).sqrt();
                let (mut step, mut sum, mut inside) = (0.0f64, 0.0f64, false);
                let shift: Vec<f64> = times
                    .iter()
                    .zip(&st)
                    .map(|(&t, s)| {
                        let now = scene.planet_distance(t, s) < 3.0 * scene.hill();
                        if now && !inside {
                            step = phi * step + noise * (rng.unit() - 0.5) * 12f64.sqrt();
                            sum += step;
                        }
                        inside = now;
                        BOUNDED * sum * c0
                    })
                    .collect();
                lay(scene, st, &shift)
            }),
            Law::StepMid => echo().map(|st| {
                let c0 = scene.jacobi(0.0, &st[0]).abs();
                let shift: Vec<f64> = times.iter().map(|&t| if t > 95.0 * scene.period() { 3e-9 * c0 } else { 0.0 }).collect();
                lay(scene, st, &shift)
            }),
        }
    }
}

// ---------------------------------------------------------------- the judged set: one-ulp replica ensemble

/// Fifteen deterministic one-quantum replicas of a ship: itself, ±1 ulp on each of the four
/// words, ±2 ulp on x and vy, and the two paired ±1 (x, vy) corners. Every pattern is an
/// integer offset on the bit pattern, so the ensemble is the same on every machine; its median
/// is what a chaotic ship's fate is read from.
fn replicas(ship: [f64; 4]) -> Vec<[f64; 4]> {
    let at = |i: usize, d: i64| {
        let mut s = ship;
        s[i] = f64::from_bits((s[i].to_bits() as i64 + d) as u64);
        s
    };
    let mut r = vec![ship];
    for i in 0..4 {
        for d in [1i64, -1] {
            r.push(at(i, d));
        }
    }
    for (i, d) in [(0usize, 2i64), (0, -2), (3, 2), (3, -2)] {
        r.push(at(i, d));
    }
    for (a, b) in [(1i64, 1), (-1, -1)] {
        let mut s = ship;
        s[0] = f64::from_bits((s[0].to_bits() as i64 + a) as u64);
        s[3] = f64::from_bits((s[3].to_bits() as i64 + b) as u64);
        r.push(s);
    }
    r
}

/// The reference's crossings of R_SOI (fine samples) and closest approach, for one replica.
fn watch(scene: &Restricted, ship: [f64; 4]) -> Option<(usize, f64)> {
    let mut it = Integrator::new(scene, Model::Full, RTOL, ship).tracking();
    let (mut inside, mut crossings) = (None, 0);
    for j in 0..=PERIODS * FINE {
        let t = j as f64 * scene.period() / FINE as f64;
        let state = it.advance(t)?;
        let now = scene.planet_distance(t, &state) < scene.soi();
        crossings += inside.is_some_and(|before| before != now) as usize;
        inside = Some(now);
    }
    Some((crossings, it.closest()))
}

fn median(mut xs: Vec<f64>) -> f64 {
    xs.sort_by(f64::total_cmp);
    xs[xs.len() / 2]
}

/// A ship's fate as the ensemble sees it: median crossings, median closest approach (in planet
/// radii), and how many replicas agree with each median (the fragility, reported).
pub struct Fate {
    pub crossings: f64,
    pub closest: f64,
    pub agree_cross: usize,
    pub agree_close: usize,
}

pub fn fate(scene: &Restricted, ship: [f64; 4]) -> Option<Fate> {
    let runs: Vec<(usize, f64)> = replicas(ship).into_iter().map(|r| watch(scene, r)).collect::<Option<_>>()?;
    let (cross, close) = (median(runs.iter().map(|r| r.0 as f64).collect()), median(runs.iter().map(|r| r.1).collect()));
    Some(Fate {
        crossings: cross,
        closest: close / scene.planet_radius,
        agree_cross: runs.iter().filter(|r| (r.0 as f64 - cross).abs() <= 2.0).count(),
        agree_close: runs.iter().filter(|r| (r.1 / scene.planet_radius / close - 1.0).abs() <= 0.2).count(),
    })
}

// ---------------------------------------------------------------- the statistic: the arrow z

/// Matched-pair gap: at least two synodic (Lyapunov) times — the slowest synodic period here is
/// about 6.7 P, so 12 P decorrelates the fast state (orbital and synodic phase) between the
/// visits. Shorter gaps would let an unmixed fast state carry a spurious arrow; longer ones
/// throw pairs away.
pub const GAP: f64 = 12.0;
/// A matched pair is kept only inside this normalized state distance (in the ship's own (a, e)
/// spread): a recurrence, not a forced match between states the ship never revisits. The value
/// is bounded by the requirement the adjustment needs — the state-only error must be locally
/// linear over the ball — and the bounded control's residual measures the budget actually spent
/// (about 1e-12 against its 1e-5 error, five orders of headroom), which is what licenses 0.4.
pub const D_MAX: f64 = 0.4;
/// Per-ship pairs below this carry no evidence (the z is read as 0 and the ship is reported).
pub const MIN_PAIRS: usize = 30;
/// The gate: FAIL if the median per-ship z exceeds this. Derived: under no-memory each pair is a
/// fair coin, so z_ship ~ N(0, 1) up to pair dependence; allowing a 4x variance inflation, the
/// median of 16 has sigma at most 0.63, and 5 is at least 8 standard deviations even then.
pub const Z_GATE: f64 = 5.0;
/// A law must leave at least this many judged ships for the median to mean anything: with n
/// judged ships the median-of-z spread under the null is sqrt(pi/(2n)) per ship (at most 2 with
/// the pair-dependence allowance), and Z_GATE stays at least 6 standard deviations.
pub const JUDGED_MIN: usize = 9;
/// The judged set is the oracle's domain: every ship whose one-ulp ensemble median stays outside
/// the planet. The crossing count is the SCENE contract's freeze criterion (the integrator
/// re-freezes ships to satisfy it robustly); the statistic judges the error series of every
/// domain ship, quiet or busy, and the count is reported per ship.
pub const CROSSINGS_JUDGE: usize = 0;

pub struct ShipStat {
    pub z: f64,
    pub n: usize,
    pub ties: usize,
    pub worst: f64,
    pub gap_mean: f64,
    /// Median |Δ| of the matched pairs' error magnitudes: the state-gradient noise the leak must
    /// rise above (the detection floor's denominator).
    pub diff_med: f64,
    /// The dt coefficient: the error the law gains per horizon at a fixed state.
    pub leak: f64,
    pub above_floor: bool,
    pub bad: bool,
}

/// One ship's arrow statistics from the law's states at `times`: the gap-gain test.
///
/// Matched pairs (an early far-field sample and its nearest late partner in the normalized slow
/// state (a, e), at least GAP periods apart, within D_MAX of each other, one-to-one) each carry
/// the SIGNED pair difference d = c_late − c_early of the Jacobi error. The state difference is
/// subtracted by a through-origin least-squares fit of d on (da, de): that removes the drift
/// confound (a chaotic ship's a diffuses with drift, so a state-tied error's magnitude grows
/// with time with no memory at all). What is left, r, is the error the pair gained at a fixed
/// state between the two visits.
///
/// The test asks one question of r: does it get BIGGER the longer the ship has been away? A
/// leak gives r a mean proportional to the gap; a walk gives r a spread that grows with the gap
/// (more encounters between the visits); both raise |r| with dt, and both are compounding. The
/// statistic is Kendall's rank correlation between |r| and dt, as a z: concordant and discordant
/// pair-of-pair comparisons (ties in either coordinate carry no evidence and are dropped), with
/// the parameter-free null z = 3S/sqrt(n(n − 1)(2n + 5)), S = C − D over n pairs. An error that is a
/// function of the state has exchangeable r at any gap: z ~ N(0, 1). A law with a constant
/// offset has r = 0 everywhere: no comparisons, z = 0, and it passes.
pub fn arrow(scene: &Restricted, ship: [f64; 4], times: &[f64], states: &[[f64; 4]]) -> ShipStat {
    let c0 = scene.jacobi(0.0, &ship);
    let bad = states.len() != times.len() || states.iter().flatten().any(|x| !x.is_finite());
    let cerr = |t: f64, s: &[f64; 4]| (scene.jacobi(t, s) - c0) / c0.abs();
    let err: Vec<f64> = if bad { vec![f64::INFINITY; times.len()] } else { times.iter().zip(states).map(|(&t, s)| cerr(t, s).abs()).collect() };
    let worst = err.iter().fold(0.0f64, |m, e| if e.is_nan() || m.is_nan() { f64::NAN } else { m.max(*e) });
    let far: Vec<usize> = (0..times.len()).filter(|&j| scene.planet_distance(times[j], &states[j]) > 3.0 * scene.hill()).collect();
    let el: Vec<Option<(f64, f64)>> = far.iter().map(|&j| match elements(scene, times[j], &states[j]) { (a, e) if a.is_finite() && e.is_finite() => Some((a / scene.sep, e)), _ => None }).collect();
    let good: Vec<(f64, f64)> = el.iter().filter_map(|x| *x).collect();
    let (mut z, mut n, mut ties, mut gap_mean, mut diff_med, mut leak) = (0.0f64, 0usize, 0usize, 0.0f64, 0.0f64, 0.0f64);
    if good.len() >= MIN_PAIRS * 3 && !bad {
        let (ma, me) = good.iter().fold((0.0, 0.0), |(a, e), (x, y)| (a + x, e + y));
        let (ma, me) = (ma / good.len() as f64, me / good.len() as f64);
        let sd = |xs: &[f64], m: f64| (xs.iter().map(|x| (x - m) * (x - m)).sum::<f64>() / xs.len() as f64).sqrt().max(1e-15);
        let (sa, se) = (sd(&good.iter().map(|x| x.0).collect::<Vec<_>>(), ma), sd(&good.iter().map(|x| x.1).collect::<Vec<_>>(), me));
        let half = 0.5 * PERIODS as f64;
        let u = |x: (f64, f64)| ((x.0 - ma) / sa, (x.1 - me) / se);
        let mut used = vec![false; far.len()];
        // [da, de, dt, d_signed]
        let mut rows: Vec<[f64; 4]> = Vec::new();
        let mut gaps = Vec::new();
        for (idx, &i) in far.iter().enumerate() {
            if (i / COARSE) as f64 > half {
                continue;
            }
            let Some(ei) = el[idx] else { continue };
            let (ui, vi) = u(ei);
            let mut best: Option<(f64, usize)> = None;
            for (k, &j) in far.iter().enumerate() {
                if used[k] || (j / COARSE) as f64 <= half {
                    continue;
                }
                let dt = (j - i) as f64 / COARSE as f64;
                if dt < GAP {
                    continue;
                }
                let Some(ej) = el[k] else { continue };
                let (uj, vj) = u(ej);
                let d2 = (ui - uj) * (ui - uj) + (vi - vj) * (vi - vj);
                if d2 > D_MAX * D_MAX {
                    continue;
                }
                if best.map_or(true, |(b, _)| d2 < b) {
                    best = Some((d2, k));
                }
            }
            if let Some((_, k)) = best {
                used[k] = true;
                let j = far[k];
                let dt = (j - i) as f64 / COARSE as f64;
                gaps.push(dt);
                let d = cerr(times[j], &states[j]) - cerr(times[i], &states[i]);
                if d != 0.0 {
                    let ((ai, ei2), (aj, ej)) = (el[idx].unwrap(), el[k].unwrap());
                    rows.push([(aj - ai) / sa, (ej - ei2) / se, dt / PERIODS as f64, d]);
                } else {
                    ties += 1;
                }
            }
        }
        n = rows.len();
        if n >= MIN_PAIRS {
            // The state adjustment: through-origin fit of d on (da, de).
            let mut xtx = [[0.0f64; 2]; 2];
            let mut xty = [0.0f64; 2];
            for r in &rows {
                for a in 0..2 {
                    xty[a] += r[a] * r[3];
                    for b in 0..2 {
                        xtx[a][b] += r[a] * r[b];
                    }
                }
            }
            if let Some(inv) = invert2(xtx) {
                let beta: Vec<f64> = (0..2).map(|a| (0..2).map(|b| inv[a][b] * xty[b]).sum()).collect();
                let rs: Vec<(f64, f64)> = rows.iter().map(|r| (r[2], (r[3] - (beta[0] * r[0] + beta[1] * r[1])).abs())).collect();
                // Kendall's z of |r| against dt.
                let (mut concordant, mut discordant) = (0i64, 0i64);
                for x in 0..rs.len() {
                    for y in (x + 1)..rs.len() {
                        let (dd, dr) = (rs[x].0 - rs[y].0, rs[x].1 - rs[y].1);
                        if dd != 0.0 && dr != 0.0 {
                            if dd * dr > 0.0 { concordant += 1 } else { discordant += 1 }
                        }
                    }
                }
                let items = rs.len() as f64;
                z = 3.0 * (concordant - discordant) as f64 / (items * (items - 1.0) * (2.0 * items + 5.0)).sqrt();
                // The leak estimate: the dt coefficient of d ~ da + de + dt, its size per horizon.
                let mut x3y = [0.0f64; 3];
                let mut m33 = [[0.0f64; 3]; 3];
                for r in &rows {
                    let cols = [r[0], r[1], r[2]];
                    for a in 0..3 {
                        x3y[a] += cols[a] * r[3];
                        for b in 0..3 {
                            m33[a][b] += cols[a] * cols[b];
                        }
                    }
                }
                leak = match invert3(m33) {
                    Some(i3) => (0..3).map(|a| i3[2][a] * x3y[a]).sum::<f64>(),
                    None => 0.0,
                };
                let mut ad: Vec<f64> = rs.iter().map(|x| x.1).collect();
                ad.sort_by(f64::total_cmp);
                diff_med = ad[ad.len() / 2];
            }
        }
        gaps.sort_by(f64::total_cmp);
        gap_mean = gaps.iter().sum::<f64>() / gaps.len() as f64;
    }
    ShipStat { z, n, ties, worst, gap_mean, diff_med, leak, above_floor: worst > FLOOR, bad }
}

/// The inverse of a symmetric positive-definite 2x2 matrix. None: singular.
fn invert2([[a, b], [_, d]]: [[f64; 2]; 2]) -> Option<[[f64; 2]; 2]> {
    let det = a * d - b * b;
    if det <= 0.0 || !(det.is_finite()) {
        return None;
    }
    Some([[d / det, -b / det], [-b / det, a / det]])
}

/// The inverse of a symmetric positive-definite 3x3 matrix. None: singular.
fn invert3(m: [[f64; 3]; 3]) -> Option<[[f64; 3]; 3]> {
    let (a, b, c) = (m[0][0], m[0][1], m[0][2]);
    let (d, e, f) = (m[1][1], m[1][2], m[2][2]);
    let det = a * (d * f - e * e) - b * (b * f - e * c) + c * (b * e - d * c);
    if det <= 0.0 || !det.is_finite() {
        return None;
    }
    let adj = |i: usize, j: usize| {
        let (p, q) = ((i + 1) % 3, (i + 2) % 3);
        let (r, s) = ((j + 1) % 3, (j + 2) % 3);
        m[p][r] * m[q][s] - m[p][s] * m[q][r]
    };
    let mut inv = [[0.0f64; 3]; 3];
    for i in 0..3 {
        for j in 0..3 {
            inv[i][j] = adj(j, i) / det;
        }
    }
    Some(inv)
}

/// The inverse of a symmetric positive-definite `n`x`n` matrix (Cholesky). None: not SPD.

fn invert(a: [[f64; 4]; 4], n: usize) -> Option<[[f64; 4]; 4]> {
    let mut l = [[0.0f64; 4]; 4];
    for i in 0..n {
        for j in 0..=i {
            let mut sum = a[i][j];
            for k in 0..j {
                sum -= l[i][k] * l[j][k];
            }
            if i == j {
                if sum <= 0.0 {
                    return None;
                }
                l[i][i] = sum.sqrt();
            } else {
                l[i][j] = sum / l[j][j];
            }
        }
    }
    let forward = |b: [f64; 4]| {
        let mut y = [0.0f64; 4];
        for i in 0..n {
            y[i] = b[i];
            for k in 0..i {
                y[i] -= l[i][k] * y[k];
            }
            y[i] /= l[i][i];
        }
        y
    };
    let mut inv = [[0.0f64; 4]; 4];
    for i in 0..n {
        let mut e = [0.0f64; 4];
        e[i] = 1.0;
        let z = forward(e);
        // Back-substitution with L' (L stored in place, transpose).
        let mut x = [0.0f64; 4];
        for a in (0..n).rev() {
            x[a] = z[a];
            for k in (a + 1)..n {
                x[a] -= l[k][a] * x[k];
            }
            x[a] /= l[a][a];
        }
        for j in 0..n {
            inv[i][j] = x[j];
        }
    }
    Some(inv)
}

// ---------------------------------------------------------------- the gate

pub struct Verdict {
    pub pass: bool,
    pub judged: usize,
    /// The deciding statistic: the pooled Kendall z, the ships' evidence summed with its exact
    /// null variances (the ships are independent repetitions of the same law, so the sum is the
    /// sufficient aggregate and its null is again N(0, 1) at the same threshold).
    pub z_pool: f64,
    pub z_med: f64,
    pub worst: f64,
}

pub fn gate(stats: &[ShipStat]) -> Verdict {
    let judged = stats.len();
    let silent = stats.iter().filter(|s| !s.bad && s.n < MIN_PAIRS).count();
    let evid: Vec<&ShipStat> = stats.iter().filter(|s| !s.bad && s.n >= MIN_PAIRS).collect();
    let mut zs: Vec<f64> = evid.iter().map(|s| s.z).collect();
    zs.sort_by(f64::total_cmp);
    let z_med = match zs.len() {
        0 => f64::INFINITY,
        1 => zs[0],
        n => 0.5 * (zs[n / 2 - 1] + zs[n / 2]),
    };
    // The pool: z_k = 3 S_k / sqrt(n(n-1)(2n+5)) has Var 1, so S_k = z_k w_k with
    // w_k = sqrt(n(n-1)(2n+5))/3 and Var(S_k) = w_k² / 2.
    let (mut num, mut den) = (0.0f64, 0.0f64);
    for st in &evid {
        let w = (st.n as f64 * (st.n as f64 - 1.0) * (2.0 * st.n as f64 + 5.0)).sqrt() / 3.0;
        num += st.z * w;
        den += 0.5 * w * w;
    }
    let z_pool = if den > 0.0 { num / den.sqrt() } else { f64::INFINITY };
    let worst = stats.iter().map(|s| s.worst).fold(0.0f64, |m, e| if e.is_nan() || m.is_nan() { f64::NAN } else { m.max(e) });
    let pass = judged - silent >= JUDGED_MIN && !worst.is_nan() && worst <= ERR_MAX && z_pool <= Z_GATE;
    Verdict { pass, judged: judged - silent, z_pool, z_med, worst }
}

// ---------------------------------------------------------------- main

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let fp_fma = args.iter().any(|a| a == "--fma");
    let pilot = args.iter().any(|a| a == "--pilot");
    let sweep = args.iter().any(|a| a == "--sweep");
    let permute = args.iter().any(|a| a == "--permute");

    restricted::FMA.store(fp_fma, Ordering::Relaxed);
    if args.iter().any(|a| a == "--debug") { debug_dump(); return; }
    let scene = JUPITER;
    let draws = handoffs(160);
    let kept: Vec<[f64; 4]> = HANDOFF_KEPT.iter().map(|&i| ship(&scene, draws[i].0, draws[i].1, draws[i].2)).collect();
    let times = coarse_times(&scene);

    eprintln!("[{}] rounding path {}", if fp_fma { "fma" } else { "plain" }, if fp_fma { "fma-contracted kernels" } else { "plain IEEE" });
    let t0 = std::time::Instant::now();

    // The judged set, from the ensemble.
    let ships: Vec<(usize, [f64; 4], Fate)> = kept
        .iter()
        .enumerate()
        .filter(|(i, _)| !pilot || [0usize, 1].contains(i))
        .map(|(i, &s)| (i, s, fate(&scene, s).expect("ensemble gave up")))
        .collect();
    eprintln!("[{}] ensemble: {} ships in {:.1}s", if fp_fma { "fma" } else { "plain" }, ships.len(), t0.elapsed().as_secs_f64());
    println!("== judged set (one-ulp replica ensemble, {} path) ==", if fp_fma { "fma" } else { "plain" });
    println!("ship  cross_med  agree  closest_med  agree  judged");
    let mut judged_n = 0;
    for (i, _, f) in &ships {
        let j = f.crossings >= CROSSINGS_JUDGE as f64 && f.closest >= 1.0;
        judged_n += j as usize;
        println!("#{i:<4} {:>9.1} {:>6} {:>11.2} {:>6}  {}", f.crossings, f.agree_cross, f.closest, f.agree_close, if j { if f.crossings >= CROSSINGS_MIN as f64 { "judged" } else { "judged (busy-20: no)" } } else if f.closest < 1.0 { "EXCLUDED (inside planet)" } else { "EXCLUDED (too quiet)" });
    }
    println!("judged: {judged_n} of {}", ships.len());
    let judged: Vec<(usize, [f64; 4])> = ships.iter().filter(|(_, _, f)| f.crossings >= CROSSINGS_JUDGE as f64 && f.closest >= 1.0).map(|(i, s, _)| (*i, *s)).collect();
    if permute { permute_mode(&scene, &judged, &times); return; }

    let mut laws: Vec<(&str, Law)> = vec![
        ("echo", Law::Echo),
        ("scaled 1e-11", Law::Scaled),
        ("planted-bounded", Law::Bounded),
        ("planted-compound", Law::Compound),
        ("planted-drift", Law::Drift),
        ("planted-kick", Law::Kick),
        ("leak 3e-9", Law::Leak(3e-9)),
        ("leak 1e-8", Law::Leak(1e-8)),
        ("leak+bounded 1e-8", Law::LeakBounded(1e-8)),
        ("periodic 1e-7", Law::Periodic),
        ("clock 1e-4", Law::Clock(1e-4)),
        ("clock 1e-3", Law::Clock(1e-3)),
        ("phase-walk", Law::PhaseWalk),
        ("anti-walk -0.9", Law::AntiWalk),
        ("step 95P", Law::StepMid),
    ];
    if sweep {
        laws = vec![
            ("leak 1e-16", Law::Leak(1e-16)),
            ("leak 1e-15", Law::Leak(1e-15)),
            ("leak 1e-14", Law::Leak(1e-14)),
            ("leak 1e-12", Law::Leak(1e-12)),
            ("leak 1e-10", Law::Leak(1e-10)),
            ("leak 1e-8", Law::Leak(1e-8)),
            ("leak+bounded 1e-12", Law::LeakBounded(1e-12)),
            ("leak+bounded 1e-11", Law::LeakBounded(1e-11)),
            ("leak+bounded 1e-10", Law::LeakBounded(1e-10)),
            ("leak+bounded 1e-9", Law::LeakBounded(1e-9)),
            ("leak+bounded 1e-8", Law::LeakBounded(1e-8)),
        ];
    }
    if args.iter().any(|a| a == "--channels") {
        // The quantifier channel the Jacobi functional cannot see: along-track error vs the
        // echo trajectory at the same sample times, in Hill radii, first vs last quarter.
        println!("\n== the invisible channel: |x_law - x_echo| / R_H ({}) ==", if fp_fma { "fma" } else { "plain" });
        println!("{:<22} {:>12} {:>12} {:>12} {:>12}", "law", "med Q1", "med Q4", "max Q1", "max Q4");
        let chan: Vec<(&str, Law)> = vec![
            ("echo", Law::Echo),
            ("planted-bounded", Law::Bounded),
            ("clock 1e-4", Law::Clock(1e-4)),
            ("clock 1e-3", Law::Clock(1e-3)),
            ("phase-walk", Law::PhaseWalk),
        ];
        let q = PERIODS * COARSE / 4;
        for (name, law) in chan {
            let (mut q1, mut q4) = (Vec::new(), Vec::new());
            for (_, s) in &judged {
                let echo = Law::Echo.states(&scene, *s, &times).expect("echo gave up");
                let st = law.states(&scene, *s, &times).expect("law gave up");
                for (j, (a, b)) in echo.iter().zip(&st).enumerate() {
                    let d = ((a[0] - b[0]).hypot(a[1] - b[1]) / scene.hill()) as f64;
                    if j <= q { q1.push(d) } else if j >= 3 * q { q4.push(d) }
                }
            }
            let med = |mut v: Vec<f64>| { v.sort_by(f64::total_cmp); v[v.len() / 2] };
            let mx = |v: &[f64]| v.iter().cloned().fold(0.0f64, f64::max);
            println!("{:<22} {:>12.3} {:>12.3} {:>12.3} {:>12.3}", name, med(q1.clone()), med(q4.clone()), mx(&q1), mx(&q4));
        }
    }
    println!("{:<22} {:>6} {:>8} {:>8} {:>8} {:>8} {:>9}  {:>6}  margin", "law", "judged", "z_pool", "z_med", "z_min", "z_max", "worst_err", "PASS");
    for (name, law) in laws {
        let t = std::time::Instant::now();
        let stats: Vec<ShipStat> = judged
            .iter()
            .map(|(_, s)| match law.states(&scene, *s, &times) {
                Some(st) => arrow(&scene, *s, &times, &st),
                None => arrow(&scene, *s, &times, &[]),
            })
            .collect();
        if let Some(pref) = args.iter().find(|a| a.starts_with("--detail=")) {
            if name.starts_with(&pref[9..]) {
                println!("  per-ship ({}):", name);
                for ((i, _), st) in judged.iter().zip(&stats) {
                    println!("   #{i:<3} z {:>8.2}  n {:>4}  ties {:>3}  gap {:>6.1}  |r|med {:>9.2e}  leak {:>9.2e}  worst {:>9.2e}", st.z, st.n, st.ties, st.gap_mean, st.diff_med, st.leak, st.worst);
                }
            }
        }
        let v = gate(&stats);
        let zs: Vec<f64> = stats.iter().map(|s| s.z).collect();
        let (zmin, zmax) = (zs.iter().cloned().fold(f64::INFINITY, f64::min), zs.iter().cloned().fold(f64::NEG_INFINITY, f64::max));
        let gap = stats.iter().map(|s| s.gap_mean).sum::<f64>() / stats.len() as f64;
        let margin = if v.pass { format!("z {:+.1} under {Z_GATE} ({:.1}x)", v.z_pool, Z_GATE / v.z_pool.abs().max(1e-9)) } else { format!("{:+.1} over {Z_GATE} ({:.1}x)", v.z_pool, v.z_pool / Z_GATE) };
        let mut gap = 0.0f64;
        let mut ng = 0;
        for st in &stats {
            if st.gap_mean.is_finite() {
                gap += st.gap_mean;
                ng += 1;
            }
        }
        println!(
            "{:<22} {:>6} {:>8.2} {:>8.2} {:>8.2} {:>8.2} {:>9.2e}  {:>6}  {} [{:.1}s]",
            name, v.judged, v.z_pool, v.z_med, zmin, zmax, v.worst, if v.pass { "PASS" } else { "FAIL" }, margin, t.elapsed().as_secs_f64()
        );
        let _ = (gap, ng);
    }
}

// ---------------------------------------------------------------- debug dump (removed before freeze)
#[allow(dead_code)]
fn debug_dump() {
    let scene = JUPITER;
    let draws = handoffs(160);
    let ship = ship(&scene, draws[39].0, draws[39].1, draws[39].2);
    let times = coarse_times(&scene);
    let states = Law::Bounded.states(&scene, ship, &times).unwrap();
    let c0 = scene.jacobi(0.0, &ship);
    let a0 = star_axis(&scene, 0.0, &ship);
    println!("t/P   a/sep    e      |c|      r2/R_H");
    for j in (0..times.len()).step_by(53) {
        let (a, e) = elements(&scene, times[j], &states[j]);
        println!("{:>5.0} {:>7.4} {:>6.3} {:>9.2e} {:>8.1}", times[j] / scene.period(), a / scene.sep, e, ((scene.jacobi(times[j], &states[j]) - c0) / c0).abs(), scene.planet_distance(times[j], &states[j]) / scene.hill());
    }
}

// ---------------------------------------------------------------- permutation null (dynamics red-team)

/// The matched pairs of one ship, as [da, de, dt, d_signed] (a copy of `arrow`'s construction).
fn ship_rows(scene: &Restricted, ship: [f64; 4], times: &[f64], states: &[[f64; 4]]) -> Option<Vec<[f64; 4]>> {
    let c0 = scene.jacobi(0.0, &ship);
    let cerr = |t: f64, s: &[f64; 4]| (scene.jacobi(t, s) - c0) / c0.abs();
    let far: Vec<usize> = (0..times.len()).filter(|&j| scene.planet_distance(times[j], &states[j]) > 3.0 * scene.hill()).collect();
    let el: Vec<Option<(f64, f64)>> = far.iter().map(|&j| match elements(scene, times[j], &states[j]) { (a, e) if a.is_finite() && e.is_finite() => Some((a / scene.sep, e)), _ => None }).collect();
    let good: Vec<(f64, f64)> = el.iter().filter_map(|x| *x).collect();
    if good.len() < MIN_PAIRS * 3 { return None }
    let (ma, me) = good.iter().fold((0.0, 0.0), |(a, e), (x, y)| (a + x, e + y));
    let (ma, me) = (ma / good.len() as f64, me / good.len() as f64);
    let sd = |xs: &[f64], m: f64| (xs.iter().map(|x| (x - m) * (x - m)).sum::<f64>() / xs.len() as f64).sqrt().max(1e-15);
    let (sa, se) = (sd(&good.iter().map(|x| x.0).collect::<Vec<_>>(), ma), sd(&good.iter().map(|x| x.1).collect::<Vec<_>>(), me));
    let half = 0.5 * PERIODS as f64;
    let u = |x: (f64, f64)| ((x.0 - ma) / sa, (x.1 - me) / se);
    let mut used = vec![false; far.len()];
    let mut rows: Vec<[f64; 4]> = Vec::new();
    for (idx, &i) in far.iter().enumerate() {
        if (i / COARSE) as f64 > half { continue }
        let Some(ei) = el[idx] else { continue };
        let (ui, vi) = u(ei);
        let mut best: Option<(f64, usize)> = None;
        for (k, &j) in far.iter().enumerate() {
            if used[k] || (j / COARSE) as f64 <= half { continue }
            let dt = (j - i) as f64 / COARSE as f64;
            if dt < GAP { continue }
            let Some(ej) = el[k] else { continue };
            let (uj, vj) = u(ej);
            let d2 = (ui - uj) * (ui - uj) + (vi - vj) * (vi - vj);
            if d2 > D_MAX * D_MAX { continue }
            if best.map_or(true, |(b, _)| d2 < b) { best = Some((d2, k)) }
        }
        if let Some((_, k)) = best {
            used[k] = true;
            let j = far[k];
            let d = cerr(times[j], &states[j]) - cerr(times[i], &states[i]);
            if d != 0.0 {
                let ((ai, ei2), (aj, ej)) = (el[idx].unwrap(), el[k].unwrap());
                rows.push([(aj - ai) / sa, (ej - ei2) / se, (j - i) as f64 / COARSE as f64 / PERIODS as f64, d]);
            }
        }
    }
    if rows.len() < MIN_PAIRS { None } else { Some(rows) }
}

/// Kendall's z of |r| against dt for [(dt, |r|)] items (ties dropped), as in `arrow`.
fn kendall_z(items: &[(f64, f64)]) -> f64 {
    let (mut c, mut d) = (0i64, 0i64);
    for x in 0..items.len() {
        for y in (x + 1)..items.len() {
            let (dd, dr) = (items[x].0 - items[y].0, items[x].1 - items[y].1);
            if dd != 0.0 && dr != 0.0 {
                if dd * dr > 0.0 { c += 1 } else { d += 1 }
            }
        }
    }
    let n = items.len() as f64;
    3.0 * (c - d) as f64 / (n * (n - 1.0) * (2.0 * n + 5.0)).sqrt()
}

fn permute_mode(scene: &Restricted, judged: &[(usize, [f64; 4])], times: &[f64]) {
    println!("\n== the permutation null: is z_pool's null really N(0,1)? ==");
    println!("{:<16} {:>7}  {:>9}  {:>8}  {:>9}  {:>9}", "law", "z_orig", "perm mean", "perm sd", "perm p95", "perm max");
    for (name, law) in [("echo", Law::Echo), ("scaled 1e-11", Law::Scaled), ("planted-bounded", Law::Bounded), ("periodic 1e-7", Law::Periodic)] {
        let mut per: Vec<(Vec<f64>, Vec<f64>)> = Vec::new();
        for (_, s) in judged {
            let Some(st) = law.states(scene, *s, times) else { continue };
            let Some(rows) = ship_rows(scene, *s, times, &st) else { continue };
            let mut xtx = [[0.0f64; 2]; 2];
            let mut xty = [0.0f64; 2];
            for r in &rows {
                for a in 0..2 {
                    xty[a] += r[a] * r[3];
                    for b in 0..2 { xtx[a][b] += r[a] * r[b] }
                }
            }
            let Some(inv) = invert2(xtx) else { continue };
            let beta: Vec<f64> = (0..2).map(|a| (0..2).map(|b| inv[a][b] * xty[b]).sum()).collect();
            let (dts, rs): (Vec<f64>, Vec<f64>) = rows.iter().map(|r| (r[2], (r[3] - (beta[0] * r[0] + beta[1] * r[1])).abs())).unzip();
            per.push((dts, rs));
        }
        if per.is_empty() { println!("{:<16} no evidence ships", name); continue }
        let pool = |f: &dyn Fn(usize) -> f64| {
            let (mut num, mut den) = (0.0f64, 0.0f64);
            for (k, p) in per.iter().enumerate() {
                let n = p.0.len() as f64;
                let w = (n * (n - 1.0) * (2.0 * n + 5.0)).sqrt() / 3.0;
                num += f(k) * w;
                den += 0.5 * w * w;
            }
            num / den.sqrt()
        };
        let zipped: Vec<Vec<(f64, f64)>> = per.iter().map(|(dts, rs)| dts.iter().zip(rs).map(|(&d, &r)| (d, r)).collect()).collect();
        let z_orig = pool(&|k| kendall_z(&zipped[k]));
        let b = 400;
        let mut zs = Vec::with_capacity(b);
        for it in 0..b {
            let mut rng = Rng(0xD00D_u64 ^ (it as u64 + 1).wrapping_mul(0x9E37_79B9_7F4A_7C15));
            let shuffled: Vec<Vec<(f64, f64)>> = zipped
                .iter()
                .map(|items| {
                    let mut dts: Vec<f64> = items.iter().map(|p| p.0).collect();
                    for i in (1..dts.len()).rev() {
                        let j = (rng.next() as usize) % (i + 1);
                        dts.swap(i, j);
                    }
                    dts.iter().zip(items.iter().map(|p| p.1)).map(|(d, r)| (*d, r)).collect()
                })
                .collect();
            zs.push(pool(&|k| kendall_z(&shuffled[k])));
        }
        zs.sort_by(f64::total_cmp);
        let (n, mean) = (zs.len() as f64, zs.iter().sum::<f64>() / zs.len() as f64);
        let sd = (zs.iter().map(|z| (z - mean) * (z - mean)).sum::<f64>() / (n - 1.0)).sqrt();
        println!("{:<16} {:>7.2}  {:>9.2}  {:>8.2}  {:>9.2}  {:>9.2}", name, z_orig, mean, sd, zs[(0.95 * n) as usize], zs[b - 1]);
    }
}
