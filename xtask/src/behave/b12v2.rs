//! B12 v2 (candidate of 6 October; not frozen and not in the judge's list: `cargo test --release -p xtask b12v2`, and the ignored `a_named_law_through_the_gate`).
//!
//! The requirement (principle 13): a law's Jacobi error is a function of the ship's state and never of how long the law has been running, so it cannot compound.
//! The 200-period exponent of one chaotic ship cannot see that: a bounded error that depends on the state reads 0.3-0.6 there (the ship's state diffuses), a random
//! walk reads about the same, and the reference itself reads 1.2-1.8 above its float floor (the red-team of 6 October). So the object tested is changed:
//! - **An ensemble, not a trajectory.** The 16 ships are iid draws from the invariant measure of the flow on one energy surface: the planet's confined region at
//!   C = C_L1·(1 + ε_c), where the zero-velocity curve closes around the planet and the measure is uniform in (x, y, direction of the rotating-frame velocity). For
//!   an error that is a function of the state, e_i(t) = f(s_i(t)) − f(s_i(0)) then has mean zero at every t and increments whose mean square D(L) is flat in the
//!   lag L beyond a decorrelation time (about one period; measured on known state functions of the reference's own trajectories). A leak moves the mean, a random
//!   walk makes D(L) grow like L, a leak like L². The ships that cross the doll edge 20 times are the busy ones (27% of draws); their indices are frozen.
//! - **Two tests across the ships, each with a derived critical value.** M: the ensemble mean of the ships' slopes of e in t is zero (Student's t, two-sided). V: the
//!   mean over ships of γ, the slope of ln D on ln L over T/2 ... T/16, is zero (Student's t, one-sided): 0 for a bounded error, 1 a walk, 2 a leak. The false-alarm
//!   probability of a run is ALPHA = 10⁻³, split between them; the power is 0.9.
//! - **ε_c** is half of the largest margin at which the confined region still reaches the doll edge (ε* = 7.3·10⁻⁵): a law whose error stays under it cannot open the
//!   neck, so it is also the cap on |e| (the old 10⁻⁴ cannot be kept: the region would not reach the edge).
//! - **What it can see.** The smallest steady leak (Jacobi error per planet period) the run sees with power 0.9 is λ = (t_c + t_p)·s_β/√N, s_β the ships' own scatter
//!   of slopes: between A/(5T) and A/(12T) on the three bounded plants (A their rms amplitude, T = 200 periods), about 8 times better than the amplitude/horizon limit A/T
//!   because the error decorrelates every orbit and the ships are independent. It reaches ε_c after H = ε_c/λ ≈ 8·T·ε_c/A periods. A random walk is seen when it grows to about the amplitude within half the run.
//!   To certify by observation the 10 Gyr of the test ladder (8×10⁸ periods of a Jupiter-like planet) a law's own bounded error would have to be under about 7·10⁻¹¹.
//! - **Machine independence.** No reference runs in the gate: the initial states come from the integer stream and + − × / √ only (sine and cosine by a fixed series),
//!   the law's own states are the only trajectories, and no ship is assessed, excluded or replaced. A chaotic ship leaves its twin on another machine within tens of
//!   periods, so the decision is a statistic over iid ships and is tested to be the same with every initial state nudged by one ulp.
use super::restricted::{Restricted, JUPITER};
use super::resonance::elements;
use super::{sample, Law};

/// Periods run and samples per period (the law is asked for its state every P/8).
pub const PERIODS: usize = 200;
pub const COARSE: usize = 8;
/// Ships judged.
pub const SHIPS: usize = 16;
/// Hill radius over separation, (μ/3)^(1/3) for μ = 10⁻³, as a literal (the gate's initial states use only + − × / and √, which every IEEE machine rounds alike).

/// The scene: B12-B14's, with the planet a point (radius 10⁻³ of Jupiter's): B12 asks about the Jacobi constant under handoffs, and the oracle is a point mass.
pub fn scene() -> Restricted {
    Restricted { planet_radius: JUPITER.planet_radius * 1e-3, ..JUPITER }
}

/// Hill radius and sphere-of-influence radius over the separation for μ = 10⁻³, (μ/3)^(1/3) and μ^(2/5), as literals: the ensemble's initial states may use only
/// + − × / √ and literals, which every IEEE-754 machine rounds alike (libm's cbrt, powf, sin and cos differ in the last bit between machines).
pub const HILL_OVER_SEP: f64 = 0.06933612743506347;
pub const SOI_OVER_SEP: f64 = 0.06309573444801933;

/// Ω = sep^(−3/2) from a square root and a division.
pub fn omega(scene: &Restricted) -> f64 {
    1.0 / (scene.sep * scene.sep.sqrt())
}

/// sin and cos by Taylor series with fixed operation order (libm's differ in the last bit between machines).
pub fn sin_cos(x: f64) -> (f64, f64) {
    let (mut s, mut c, mut ts, mut tc) = (0.0, 0.0, x, 1.0);
    for n in 0..40 {
        let m = (2 * n) as f64;
        s += ts;
        c += tc;
        ts = -ts * (x * x) / ((m + 2.0) * (m + 3.0));
        tc = -tc * (x * x) / ((m + 1.0) * (m + 2.0));
    }
    (s, c)
}

/// The effective potential Ũ = (1−μ)/r₁ + μ/r₂ + ½Ω²ρ² at the barycentric position (x, y) (the star at (−sep·μ, 0), the planet at (sep·(1−μ), 0)), so that the
/// Jacobi constant is 2Ũ − |u|² with u the velocity in the rotating frame.
pub fn potential(scene: &Restricted, x: f64, y: f64) -> f64 {
    let w = omega(scene);
    let r1 = ((x + scene.sep * scene.mu) * (x + scene.sep * scene.mu) + y * y).sqrt();
    let r2 = ((x - scene.sep * (1.0 - scene.mu)) * (x - scene.sep * (1.0 - scene.mu)) + y * y).sqrt();
    (1.0 - scene.mu) / r1 + scene.mu / r2 + 0.5 * w * w * (x * x + y * y)
}

/// The L1 point's x on the star-planet axis (bisection, fixed 200 steps) and its Jacobi constant 2Ũ.
pub fn l1(scene: &Restricted) -> (f64, f64) {
    let (mu, sep, w) = (scene.mu, scene.sep, omega(scene));
    let d = |x: f64| {
        let (a, b) = (x + sep * mu, sep * (1.0 - mu) - x);
        -(1.0 - mu) / (a * a) + mu / (b * b) + w * w * x
    };
    let h = HILL_OVER_SEP * sep;
    let (mut lo, mut hi) = (sep * (1.0 - mu) - 1.5 * h, sep * (1.0 - mu) - 0.5 * h);
    for _ in 0..200 {
        let m = 0.5 * (lo + hi);
        if d(lo) * d(m) <= 0.0 {
            hi = m
        } else {
            lo = m
        }
    }
    let x = 0.5 * (lo + hi);
    (x, 2.0 * potential(scene, x, 0.0))
}

/// The confinement margin ε_c. Every ship has the Jacobi constant C_L1·(1 + ε_c), just above L1's, so the zero-velocity curve closes the region around the planet
/// and nothing enters or leaves: the energy surface is bounded and the flow's invariant measure is uniform on it. The region must still reach the doll edge on
/// the L1 side, which it does for ε_c below ε* = 2Ũ(planet − R_SOI)/C_L1 − 1 (7.3·10⁻⁵ here); ε_c is half of it. A law whose Jacobi error stays under ε_c cannot
/// open the neck, so ε_c is also the largest error the gate allows.
pub fn margin(scene: &Restricted) -> f64 {
    let (_, cl1) = l1(scene);
    let edge = scene.sep * (1.0 - scene.mu) - SOI_OVER_SEP * scene.sep;
    0.5 * (2.0 * potential(scene, edge, 0.0) / cl1 - 1.0)
}

/// Candidate `n` of the ensemble: a point uniform in the planet's confined region, the rotating-frame velocity of the size the Jacobi constant fixes and a uniform
/// direction (the invariant measure of a Hamiltonian flow on its energy surface is uniform in (x, y, direction)). Draws that miss the region are rejected, so the
/// n-th candidate is a function of the integer stream and IEEE arithmetic only.
pub fn candidates(scene: &Restricted, n: usize) -> Vec<[f64; 4]> {
    let (xl1, cl1) = l1(scene);
    let c = cl1 * (1.0 + margin(scene));
    let (px, w) = (scene.sep * (1.0 - scene.mu), omega(scene));
    let rmax = px - xl1;
    let mut rng = sample::Rng(ENSEMBLE_SEED);
    let mut out = Vec::new();
    while out.len() < n {
        let (dx, dy) = (rmax * (2.0 * rng.unit() - 1.0), rmax * (2.0 * rng.unit() - 1.0));
        let th = std::f64::consts::TAU * rng.unit();
        if dx * dx + dy * dy >= rmax * rmax {
            continue;
        }
        let (x, y) = (px + dx, dy);
        let u2 = 2.0 * potential(scene, x, y) - c;
        if u2 < 0.0 {
            continue;
        }
        let (sn, cs) = sin_cos(th - std::f64::consts::PI);
        let (sn, cs) = (-sn, -cs);
        let u = u2.sqrt();
        out.push([x, y, u * cs - w * y, u * sn + w * x]);
    }
    out
}
pub const ENSEMBLE_SEED: u64 = 20261006;

/// The indices of the candidates the ensemble keeps: those whose reference (echo's integrator at 10⁻¹²) crosses the doll edge at least `CROSSINGS_MIN` times in
/// 200 periods counted at P/256, as B12's contract asks, the first `SHIPS` of them. Found once by the ignored test `search` and frozen here: the gate reads this
/// list and never assesses a ship with a reference, so no run depends on a machine's chaos.
pub const KEPT: [usize; SHIPS] = [4, 6, 15, 18, 20, 21, 24, 32, 35, 38, 44, 48, 49, 55, 58, 70];
pub const CROSSINGS_MIN: usize = 20;

/// The kept ships.
pub fn ensemble(scene: &Restricted) -> Vec<[f64; 4]> {
    let all = candidates(scene, KEPT.iter().max().map_or(0, |m| m + 1));
    KEPT.iter().map(|&i| all[i]).collect()
}

pub fn times(scene: &Restricted) -> Vec<f64> {
    (0..=PERIODS * COARSE).map(|j| j as f64 * scene.period() / COARSE as f64).collect()
}

// ---------------------------------------------------------------------------------------------------------------------------------------------
// Student's t, from its definition (the regularized incomplete beta function by Lentz's continued fraction), so that every critical value below is derived.

fn ln_gamma(x: f64) -> f64 {
    // Lanczos, g = 7, n = 9
    const C: [f64; 9] = [0.999_999_999_999_809_9, 676.520_368_121_885_1, -1_259.139_216_722_402_8, 771.323_428_777_653_1, -176.615_029_162_140_6, 12.507_343_278_686_905, -0.138_571_095_265_720_12, 9.984_369_578_019_572e-6, 1.505_632_735_149_311_6e-7];
    let x = x - 1.0;
    let t = x + 7.5;
    let a: f64 = C[0] + (1..9).map(|i| C[i] / (x + i as f64)).sum::<f64>();
    0.5 * (std::f64::consts::TAU).ln() + (x + 0.5) * t.ln() - t + a.ln()
}

fn beta_inc(a: f64, b: f64, x: f64) -> f64 {
    if x <= 0.0 {
        return 0.0;
    }
    if x >= 1.0 {
        return 1.0;
    }
    let front = (ln_gamma(a + b) - ln_gamma(a) - ln_gamma(b) + a * x.ln() + b * (1.0 - x).ln()).exp();
    let cf = |a: f64, b: f64, x: f64| {
        let tiny = 1e-300;
        let (mut c, mut d) = (1.0, 1.0 - (a + b) * x / (a + 1.0));
        if d.abs() < tiny {
            d = tiny;
        }
        d = 1.0 / d;
        let mut h = d;
        for m in 1..400 {
            let m = m as f64;
            for k in 0..2 {
                let num = if k == 0 { m * (b - m) * x / ((a + 2.0 * m - 1.0) * (a + 2.0 * m)) } else { -(a + m) * (a + b + m) * x / ((a + 2.0 * m) * (a + 2.0 * m + 1.0)) };
                d = 1.0 + num * d;
                if d.abs() < tiny {
                    d = tiny;
                }
                c = 1.0 + num / c;
                if c.abs() < tiny {
                    c = tiny;
                }
                d = 1.0 / d;
                h *= d * c;
            }
        }
        h
    };
    if x < (a + 1.0) / (a + b + 2.0) {
        front * cf(a, b, x) / a
    } else {
        1.0 - (ln_gamma(a + b) - ln_gamma(a) - ln_gamma(b) + b * (1.0 - x).ln() + a * x.ln()).exp() * cf(b, a, 1.0 - x) / b
    }
}

/// P(T ≤ t) for Student's t with `dof` degrees of freedom.
pub fn t_cdf(t: f64, dof: f64) -> f64 {
    let tail = 0.5 * beta_inc(0.5 * dof, 0.5, dof / (dof + t * t));
    if t > 0.0 { 1.0 - tail } else { tail }
}

/// The p-quantile of Student's t (p in (0.5, 1)), by bisection.
pub fn t_quantile(p: f64, dof: f64) -> f64 {
    let (mut lo, mut hi) = (0.0, 1e4);
    for _ in 0..200 {
        let m = 0.5 * (lo + hi);
        if t_cdf(m, dof) < p {
            lo = m
        } else {
            hi = m
        }
    }
    0.5 * (lo + hi)
}

/// What the gate reads of one sample of one ship: the signed relative Jacobi error, the semimajor axis (in separations) and the eccentricity about the
/// star, and the distance from the planet (in Hill radii).
#[derive(Clone, Copy, Debug)]
pub struct Row {
    pub err: f64,
    pub a: f64,
    pub e: f64,
    pub r2: f64,
}

/// The law's samples of `ship` at `times`, or None where it does not answer.
pub fn series(scene: &Restricted, law: &dyn Law, ship: [f64; 4], times: &[f64]) -> Option<Vec<Row>> {
    let states = law.restricted(scene, ship, times).filter(|s| s.len() == times.len())?;
    let c0 = scene.jacobi(0.0, &ship);
    Some(
        times
            .iter()
            .zip(&states)
            .map(|(&t, s)| {
                let (a, e, _, _) = elements(scene, t, s);
                Row { err: (scene.jacobi(t, s) - c0) / c0, a: a / scene.sep, e, r2: scene.planet_distance(t, s) / scene.hill() }
            })
            .collect(),
    )
}

/// The law's signed relative Jacobi errors on every ship of the ensemble (None where a ship has no answer), the ships on up to four threads (the answer does not
/// depend on the schedule: each ship is run alone).
pub fn errors(law: &(dyn Law + Sync)) -> Option<Vec<Vec<f64>>> {
    use std::sync::atomic::{AtomicUsize, Ordering};
    let (scene, times) = (scene(), times(&scene()));
    let ships = ensemble(&scene);
    let (next, threads) = (AtomicUsize::new(0), std::thread::available_parallelism().map_or(1, |n| n.get()).min(4));
    let mut done: Vec<(usize, Option<Vec<f64>>)> = std::thread::scope(|sc| {
        let workers: Vec<_> = (0..threads)
            .map(|_| {
                sc.spawn(|| {
                    let mut mine = Vec::new();
                    loop {
                        let i = next.fetch_add(1, Ordering::Relaxed);
                        if i >= ships.len() {
                            return mine;
                        }
                        mine.push((i, series(&scene, law, ships[i], &times).map(|rows| rows.iter().map(|r| r.err).collect())));
                    }
                })
            })
            .collect();
        workers.into_iter().flat_map(|w| w.join().expect("a ship's run panicked")).collect()
    });
    done.sort_by_key(|d| d.0);
    done.into_iter().map(|d| d.1).collect()
}

// ---------------------------------------------------------------------------------------------------------------------------------------------
// The statistic.
//
// The requirement (principle 13): the Jacobi error is a function of the state and never of how long the law has been running. The ensemble makes that testable
// without a reference and without waiting for a chaotic ship to come back: the ships are iid draws from the invariant measure of the flow on one energy surface.
// Then for any error that is a function of the state, e_i(t) = f(s_i(t)) − f(s_i(0)) has mean zero at every t (both ends are draws from the same measure), and so do
// its increments e_i(t + L) − e_i(t), whose mean square D(L) rises with the lag L only until the ship has forgotten its state and is flat after that. An error with a
// memory is not so: a leak moves the mean, a random walk makes D(L) grow like L (a leak like L²). Two tests, each across the iid ships, so each has a derived
// critical value and none is fitted:
//   M: the ensemble mean of the ships' least-squares slopes of e in t is zero (Student's t);
//   V: the exponent γ of D(L) over the lags T/2 ... T/16, ship by ship, has mean zero (Student's t over the ships): the error type, 0 bounded, 1 a walk, 2 a leak.

/// The false-alarm probability of one run of the gate, split between its two tests.
pub const ALPHA: f64 = 1e-3;
/// The power with which a leak of the detectable size is seen.
pub const POWER: f64 = 0.9;
/// The Jacobi constant's evaluation noise, relative: 16 units in the last place (the terms of 2Ũ − |u|² cancel by a factor of a few).
pub const NOISE: f64 = 16.0 * f64::EPSILON;
/// A Jupiter-like planet's year, in years (sep = 5.2 AU).
pub const YEAR: f64 = 11.86;
/// The lags of V, in periods: T/2 down by halves to T/16. The increments of a state function are flat in the lag from about one period (measured on the placebo state functions); the
/// smallest lag is a dozen of those, because a shorter one reads the slow tail of the decorrelation as growth (0.01 in the exponent, with a standard error of 0.005).
pub const LAGS: [f64; 4] = [100.0, 50.0, 25.0, 12.5];

/// Everything the gate says about a law.
#[derive(Clone, Debug)]
pub struct Verdict {
    pub pass: bool,
    /// The largest |e| over every ship and sample, and the margin it must stay under.
    pub worst: f64,
    pub margin: f64,
    /// The root mean square of e over every ship and sample: the amplitude of what the law's error does.
    pub rms: f64,
    /// M: the t statistic of the mean slope (two-sided) and its critical value.
    pub t_mean: f64,
    pub t_mean_crit: f64,
    /// V: the exponent of the increments' mean square in the lag, its jackknife t statistic (one-sided) and the critical value.
    pub gamma: f64,
    pub t_gamma: f64,
    pub t_gamma_crit: f64,
    /// The smallest steady leak (Jacobi error per planet period) the run sees with `POWER`, and the horizon (planet periods) at which it reaches the margin.
    pub leak_min: f64,
    pub horizon: f64,
    /// Why it failed (empty if it passed).
    pub why: String,
}

fn mean(x: &[f64]) -> f64 {
    x.iter().sum::<f64>() / x.len() as f64
}

/// The least-squares slope of y on x.
fn slope(x: &[f64], y: &[f64]) -> f64 {
    let (mx, my) = (mean(x), mean(y));
    x.iter().zip(y).map(|(a, b)| (a - mx) * (b - my)).sum::<f64>() / x.iter().map(|a| (a - mx) * (a - mx)).sum::<f64>()
}

/// The one-sample t statistic of `x` against zero, and the sample standard deviation.
fn t_stat(x: &[f64]) -> (f64, f64) {
    let (n, m) = (x.len() as f64, mean(x));
    let sd = (x.iter().map(|a| (a - m) * (a - m)).sum::<f64>() / (n - 1.0)).sqrt();
    (if sd > 0.0 { m / (sd / n.sqrt()) } else if m == 0.0 { 0.0 } else { f64::INFINITY.copysign(m) }, sd)
}

/// The mean square of the increments of `e` over `k` samples, over every start.
fn increments(e: &[f64], k: usize) -> f64 {
    (0..e.len() - k).map(|j| (e[j + k] - e[j]) * (e[j + k] - e[j])).sum::<f64>() / (e.len() - k) as f64
}

/// One ship's exponent γ: the slope of ln D(L) on ln L over `lags`, D the mean square of that ship's increments (0 for a ship whose error is exactly zero).
fn ship_exponent(e: &[f64], lags: &[f64]) -> f64 {
    let d: Vec<f64> = lags.iter().map(|&l| increments(e, (l * COARSE as f64).round() as usize)).collect();
    if d.iter().all(|&y| y == 0.0) {
        return 0.0;
    }
    if d.iter().any(|&y| !(y > 0.0)) {
        return f64::NAN;
    }
    slope(&lags.iter().map(|l| l.ln()).collect::<Vec<_>>(), &d.iter().map(|y| y.ln()).collect::<Vec<_>>())
}

/// V for one series per ship (`x[i][j]`, samples P/`COARSE` apart): the mean of the ships' exponents and its t statistic against zero.
pub fn growth(x: &[Vec<f64>]) -> (f64, f64) {
    growth_over(x, &LAGS)
}

pub fn growth_over(x: &[Vec<f64>], lags: &[f64]) -> (f64, f64) {
    let gs: Vec<f64> = x.iter().map(|e| ship_exponent(e, lags)).collect();
    (mean(&gs), t_stat(&gs).0)
}

/// Judges the ensemble: `errs[i][j]` is ship i's signed relative Jacobi error at sample j; `margin` is the confinement margin.
pub fn judge(errs: &[Vec<f64>], margin: f64) -> Verdict {
    let n = errs.len();
    let mut v = Verdict { pass: false, worst: 0.0, margin, rms: 0.0, t_mean: 0.0, t_mean_crit: 0.0, gamma: 0.0, t_gamma: 0.0, t_gamma_crit: 0.0, leak_min: f64::NAN, horizon: f64::NAN, why: String::new() };
    let len = PERIODS * COARSE + 1;
    if n < 2 || errs.iter().any(|e| e.len() != len || e.iter().any(|x| !x.is_finite())) {
        v.why = "a ship has no answer, or a junk one".into();
        return v;
    }
    v.worst = errs.iter().flatten().fold(0.0f64, |m, e| m.max(e.abs()));
    v.rms = (errs.iter().flatten().map(|e| e * e).sum::<f64>() / (n * len) as f64).sqrt();
    let dof = (n - 1) as f64;
    let (m_crit, g_crit) = (t_quantile(1.0 - ALPHA / 4.0, dof), t_quantile(1.0 - ALPHA / 2.0, dof));
    (v.t_mean_crit, v.t_gamma_crit) = (m_crit, g_crit);
    let t: Vec<f64> = (0..len).map(|j| j as f64 / COARSE as f64).collect();
    let betas: Vec<f64> = errs.iter().map(|e| slope(&t, e)).collect();
    let (tm, sd_beta) = t_stat(&betas);
    v.t_mean = tm;
    (v.gamma, v.t_gamma) = growth(errs);
    // the detectable leak: the mean slope that the mean test sees with `POWER`, given the ships' own scatter of slopes (never below the evaluation noise)
    let big_t = PERIODS as f64;
    v.leak_min = ((m_crit + t_quantile(POWER, dof)) * sd_beta / (n as f64).sqrt()).max(NOISE / big_t);
    v.horizon = margin / v.leak_min;
    let mut why = Vec::new();
    if v.worst > margin {
        why.push(format!("worst |e| {:.1e} is past the confinement margin {margin:.1e}", v.worst));
    }
    if v.t_mean.abs() > m_crit || v.t_mean.is_nan() {
        why.push(format!("the ensemble's mean error drifts (t = {:+.1}, critical {m_crit:.1})", v.t_mean));
    }
    if v.t_gamma > g_crit || v.t_gamma.is_nan() {
        why.push(format!("the error's increments grow with the lag (exponent {:.2}, t = {:+.1}, critical {g_crit:.1})", v.gamma, v.t_gamma));
    }
    v.pass = why.is_empty();
    v.why = why.join("; ");
    v
}

/// The gate's one line: the verdict and the evidence.
pub fn line(v: &Verdict) -> String {
    let years = v.horizon * YEAR;
    format!(
        "handoffs v2: worst |e| {:.1e}, rms {:.1e} (margin {:.1e}); mean drift t = {:+.1} (critical {:.1}); increments' exponent {:+.3}, t = {:+.1} (critical {:.1}); detectable leak {:.1e} per period, reaching the margin after {:.1e} periods ({:.1e} years of a 12-year orbit){}",
        v.worst,
        v.rms,
        v.margin,
        v.t_mean,
        v.t_mean_crit,
        v.gamma,
        v.t_gamma,
        v.t_gamma_crit,
        v.leak_min,
        v.horizon,
        years,
        if v.why.is_empty() { String::new() } else { format!("; FAILS: {}", v.why) }
    )
}

pub fn b12v2(law: &(dyn Law + Sync)) -> super::Gate {
    let _quiet = super::scale::QUIET.read().unwrap_or_else(|e| e.into_inner());
    match errors(law) {
        Some(errs) => {
            let v = judge(&errs, margin(&scene()));
            super::Gate { id: "B12v2", pass: v.pass, detail: line(&v), secs: 0.0 }
        }
        None => super::Gate { id: "B12v2", pass: false, detail: "handoffs v2: the law has no answer on a ship of the ensemble".into(), secs: 0.0 },
    }
}

#[cfg(test)]
mod tests {
    use super::super::laws::{lay, plant_crossing, star_axis, Echo, Fault, Planted};
    use super::*;

    #[test]
    fn the_series_functions_are_right() {
        for x in [-2.6, -1.0, 0.0, 0.3, 2.62] {
            let (s, c) = sin_cos(x);
            assert!((s - f64::sin(x)).abs() < 1e-15 && (c - f64::cos(x)).abs() < 1e-15, "{x}");
        }
    }

    fn g_a(scene: &Restricted, t: f64, s: &[f64; 4]) -> f64 {
        star_axis(scene, t, s) / (scene.hill() / scene.sep)
    }
    fn g_r(scene: &Restricted, t: f64, s: &[f64; 4]) -> f64 {
        (scene.hill() / scene.planet_distance(t, s)).min(5.0)
    }
    /// Planetocentric Kepler energy in units of μ/R_H, floored at −20.
    fn g_p(scene: &Restricted, t: f64, s: &[f64; 4]) -> f64 {
        let w = scene.relative(t, s);
        ((0.5 * (w[2] * w[2] + w[3] * w[3]) - scene.mu / w[0].hypot(w[1])) / (scene.mu / scene.hill())).max(-20.0)
    }
    type Plant = Box<dyn Fn(&Restricted, &[f64; 4], &[f64], &[[f64; 4]]) -> Vec<[f64; 4]> + Sync>;
    fn plants() -> Vec<(&'static str, Plant)> {
        let jac = |scene: &Restricted, ship: &[f64; 4]| scene.jacobi(0.0, ship).abs();
        let bounded = |amp: f64, g: fn(&Restricted, f64, &[f64; 4]) -> f64| -> Plant {
            Box::new(move |scene, ship, times, truth| {
                let (g0, c0) = (g(scene, 0.0, ship), scene.jacobi(0.0, ship).abs());
                let shift: Vec<f64> = times.iter().zip(truth).map(|(&t, s)| amp * (g(scene, t, s) - g0) * c0).collect();
                lay(scene, truth.to_vec(), &shift)
            })
        };
        let leak = move |rate: f64| -> Plant {
            Box::new(move |scene, ship, times, truth| {
                let c0 = jac(scene, ship);
                let shift: Vec<f64> = times.iter().map(|&t| rate * t / scene.period() * c0).collect();
                lay(scene, truth.to_vec(), &shift)
            })
        };
        let leak_v = |rate: f64| -> Plant {
            Box::new(move |scene, _, times, truth| truth.iter().zip(times).map(|(st, &t)| { let f = 1.0 + rate * t / scene.period(); [st[0], st[1], st[2] * f, st[3] * f] }).collect())
        };
        let scaled = |eps: f64| -> Plant { Box::new(move |_, _, _, truth| truth.iter().map(|st| [st[0], st[1], st[2] * (1.0 + eps), st[3] * (1.0 + eps)]).collect()) };
        let walk = |amp: f64| -> Plant { Box::new(move |scene, ship, times, truth| plant_crossing(scene, *ship, times, truth, amp)) };
        vec![
            ("echo", Box::new(|_, _, _, truth| truth.to_vec())),
            ("scaled", scaled(1e-11)),
            ("bounded_a", bounded(1e-7, g_a)),
            ("bounded_r", bounded(1e-7, g_r)),
            ("bounded_p", bounded(1e-7, g_p)),
            ("walk", walk(1e-7)),
            ("clock", Box::new(|scene, ship, times, truth| {
                // a bounded error that tracks absolute time, not the state: 1e-7·sin(2πt/100P)
                let c0 = scene.jacobi(0.0, ship).abs();
                let shift: Vec<f64> = times.iter().map(|&t| 1e-7 * (std::f64::consts::TAU * t / (100.0 * scene.period())).sin() * c0).collect();
                lay(scene, truth.to_vec(), &shift)
            })),
            ("walk8", walk(1e-8)),
            ("leak10", leak(1e-10)),
            ("leak9", leak(1e-9)),
            ("leak11", leak(1e-11)),
            ("leakv9", leak_v(1e-9)),
        ]
    }

    /// Echo's states on a ship, computed once per process (the planted laws below all lay their errors on them).
    fn truth(scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
        use std::collections::HashMap;
        use std::sync::{Mutex, OnceLock};
        static CACHE: OnceLock<Mutex<HashMap<([u64; 4], usize), Vec<[f64; 4]>>>> = OnceLock::new();
        let key = (ship.map(f64::to_bits), times.len());
        if let Some(hit) = CACHE.get_or_init(Default::default).lock().unwrap().get(&key) {
            return Some(hit.clone());
        }
        let states = Echo.restricted(scene, ship, times)?;
        CACHE.get_or_init(Default::default).lock().unwrap().insert(key, states.clone());
        Some(states)
    }

    /// A planted law: echo's states with the plant laid on them.
    struct Applied(Plant);
    impl Law for Applied {
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
        fn restricted(&self, scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
            let t = truth(scene, ship, times)?;
            Some((self.0)(scene, &ship, times, &t))
        }
    }
    fn applied(name: &str) -> Applied {
        Applied(plants().into_iter().find(|p| p.0 == name).unwrap_or_else(|| panic!("no plant {name}")).1)
    }

    fn verdict(law: &(dyn Law + Sync)) -> Verdict {
        judge(&errors(law).expect("the law answers"), margin(&scene()))
    }

    /// The bounded state-only plant of the old P2 (1e-7·(a − a₀)/(R_H/sep)) with a steady leak laid on it.
    fn bounded_and_leak(rate: f64) -> Applied {
        Applied(Box::new(move |scene, ship, times, truth| {
            let (g0, c0) = (g_a(scene, 0.0, ship), scene.jacobi(0.0, ship).abs());
            let shift: Vec<f64> = times.iter().zip(truth).map(|(&t, s)| (1e-7 * (g_a(scene, t, s) - g0) + rate * t / scene.period()) * c0).collect();
            lay(scene, truth.to_vec(), &shift)
        }))
    }

    #[test]
    fn the_ensemble_is_the_planets_confined_region_at_one_energy() {
        let s = scene();
        let (xl1, cl1) = l1(&s);
        let reach = s.sep * (1.0 - s.mu) - xl1;
        let c = cl1 * (1.0 + margin(&s));
        // the margin is half of ε*, about 3.6e-5
        assert!((margin(&s) - 3.635e-5).abs() < 2e-8, "{}", margin(&s));
        let ships = ensemble(&s);
        assert_eq!(ships.len(), SHIPS);
        for ship in &ships {
            let (j, d) = (s.jacobi(0.0, ship), s.planet_distance(0.0, ship));
            assert!((j / c - 1.0).abs() < 1e-9, "the Jacobi constant {j} against {c}");
            assert!(d < reach, "inside the neck: {} R_H", d / s.hill());
        }
        // distinct, ascending, drawn from the stream
        assert!(KEPT.windows(2).all(|w| w[0] < w[1]));
        // the literals are the scene's own
        assert!((HILL_OVER_SEP * s.sep / s.hill() - 1.0).abs() < 1e-15 && (SOI_OVER_SEP * s.sep / s.soi() - 1.0).abs() < 1e-15 && (omega(&s) / s.omega() - 1.0).abs() < 1e-15);
    }

    #[test]
    #[ignore = "re-derives the frozen ensemble's placebo (about 10 s)"]
    fn the_ensemble_is_stationary_under_the_reference() {
        // Known state functions of echo's own trajectories have mean-zero changes and increments flat in the lag: the premise of both tests, measured.
        let (s, times) = (scene(), times(&scene()));
        let ships = ensemble(&s);
        let rows: Vec<Vec<Row>> = ships.iter().map(|&sh| series(&s, &Echo, sh, &times).unwrap()).collect();
        for (name, f) in [("r2", (|r: &Row| r.r2.min(5.0)) as fn(&Row) -> f64), ("a", |r: &Row| r.a.clamp(-5.0, 5.0)), ("e", |r: &Row| r.e.min(5.0))] {
            let x: Vec<Vec<f64>> = rows.iter().map(|rs| rs.iter().map(|r| f(r) - f(&rs[0])).collect()).collect();
            let t: Vec<f64> = (0..x[0].len()).map(|j| j as f64 / COARSE as f64).collect();
            let (tm, _) = t_stat(&x.iter().map(|e| slope(&t, e)).collect::<Vec<_>>());
            let (g, tg) = growth(&x);
            println!("{name}: mean t {tm:+.2}, exponent {g:+.3} t {tg:+.2}");
            assert!(tm.abs() < t_quantile(1.0 - ALPHA / 4.0, 15.0) && tg < t_quantile(1.0 - ALPHA / 2.0, 15.0), "{name}");
        }
    }

    #[test]
    fn echo_scaled_and_every_state_only_error_pass() {
        for (name, law) in [("echo", applied("echo")), ("scaled", applied("scaled")), ("bounded a", applied("bounded_a")), ("bounded r", applied("bounded_r")), ("bounded p", applied("bounded_p"))] {
            let v = verdict(&law);
            println!("{name}: {}", line(&v));
            assert!(v.pass, "{name}: {}", line(&v));
        }
        let v = verdict(&Planted(Fault::Bounded));
        assert!(v.pass, "{}", line(&v));
    }

    #[test]
    fn a_walk_a_leak_a_drift_and_a_kick_fail_and_each_by_its_own_test() {
        let m = margin(&scene());
        // a walk (1e-7 a crossing): the increments grow like the lag, the mean does not move
        let v = verdict(&applied("walk"));
        println!("walk: {}", line(&v));
        assert!(!v.pass && v.t_mean.abs() < v.t_mean_crit && v.t_gamma > v.t_gamma_crit && v.gamma > 0.5 && v.worst < m, "{}", line(&v));
        // a steady leak: the mean moves, and the increments grow like the lag squared
        let v = verdict(&applied("leak9"));
        println!("leak: {}", line(&v));
        assert!(!v.pass && v.t_mean.abs() > v.t_mean_crit && v.gamma > 1.5, "{}", line(&v));
        // the harness's leak (the speeds grow): the increments hide it under the state's oscillation, the mean does not
        let v = verdict(&applied("leakv9"));
        println!("leak in the speeds: {}", line(&v));
        assert!(!v.pass && v.t_mean.abs() > v.t_mean_crit && v.t_gamma < v.t_gamma_crit, "{}", line(&v));
        // the reference's own drift (no projection), and the planted kick
        for (name, fault) in [("drift", Fault::Drift), ("kick", Fault::Kick), ("crossing walk", Fault::Crossing)] {
            let v = verdict(&Planted(fault));
            println!("{name}: {}", line(&v));
            assert!(!v.pass, "{name}: {}", line(&v));
        }
    }

    #[test]
    fn a_bounded_error_that_tracks_the_clock_is_flagged() {
        // The red-team's F3: 1e-7·sin(2πt/100P) is bounded and passes the old exponent, but it is not a function of the state: every ship carries the same one, so the
        // ensemble's mean moves with time. The gate calls that a clock bug (a law whose error tracks absolute time), which a law with no history does not have.
        let v = verdict(&applied("clock"));
        assert!(!v.pass && v.t_mean.abs() > v.t_mean_crit && v.worst < v.margin, "{}", line(&v));
    }

    #[test]
    fn a_leak_of_twice_the_detectable_size_fails_and_a_quarter_of_it_does_not() {
        // The limit is the gate's own: it reports the smallest leak it sees with power 0.9 (a bounded law's own scatter of slopes sets it). At that size the run's
        // realization decides (it fails in 10 of 10 ensembles in the ignored calibration); at twice it is always seen; at a quarter, never.
        let v = verdict(&applied("bounded_a"));
        let lam = v.leak_min;
        println!("bounded a: detectable {lam:.2e} per period, {:.2e} periods to the margin", v.horizon);
        let at = verdict(&bounded_and_leak(lam));
        println!("at the size: {}", line(&at));
        let twice = verdict(&bounded_and_leak(2.0 * lam));
        assert!(!twice.pass && twice.t_mean.abs() > twice.t_mean_crit, "{}", line(&twice));
        let below = verdict(&bounded_and_leak(lam / 4.0));
        assert!(below.pass, "{}", line(&below));
    }

    #[test]
    fn the_decisions_do_not_depend_on_the_last_bit() {
        // A chaotic ship reaches no common state on two machines after a few tens of periods; the decision must not care. Every initial x nudged by one ulp.
        let (s, times) = (scene(), times(&scene()));
        let nudged: Vec<[f64; 4]> = ensemble(&s).into_iter().map(|mut sh| { sh[0] = f64::from_bits(sh[0].to_bits() + 1); sh }).collect();
        let errs = |law: &Applied| -> Vec<Vec<f64>> { nudged.iter().map(|&sh| series(&s, law, sh, &times).unwrap().iter().map(|r| r.err).collect()).collect() };
        for (name, want) in [("echo", true), ("bounded_a", true), ("walk", false), ("leak9", false), ("leakv9", false)] {
            let v = judge(&errs(&applied(name)), margin(&s));
            assert_eq!(v.pass, want, "{name}: {}", line(&v));
        }
    }

    /// The first 160 candidates (of the same stream) that cross the doll edge 20 times: ten ensembles of 16 for the null's calibration.
    const CALIBRATION: [usize; 160] = [4, 6, 15, 18, 20, 21, 24, 32, 35, 38, 44, 48, 49, 55, 58, 70, 76, 81, 83, 84, 86, 89, 92, 96, 105, 106, 107, 114, 118, 134, 139, 152, 153, 154, 158, 164, 167, 169, 170, 178, 182, 196, 198, 199, 202, 204, 208, 209, 218, 235, 237, 241, 242, 249, 258, 263, 269, 274, 276, 292, 303, 307, 309, 313, 315, 317, 318, 320, 322, 331, 341, 342, 344, 347, 349, 356, 358, 363, 368, 369, 373, 376, 381, 384, 399, 400, 405, 407, 408, 417, 425, 428, 431, 434, 438, 447, 448, 450, 457, 458, 465, 468, 474, 482, 484, 485, 490, 498, 506, 511, 515, 520, 528, 532, 535, 538, 546, 555, 556, 560, 562, 578, 582, 596, 603, 604, 605, 606, 612, 625, 629, 636, 639, 642, 644, 647, 648, 656, 657, 660, 675, 684, 685, 687, 690, 694, 700, 710, 722, 724, 739, 749, 755, 758, 769, 775, 787, 797, 808, 813];

    #[test]
    #[ignore = "the null over ten independent ensembles (about 1 minute)"]
    fn the_statistics_follow_their_null_on_ten_independent_ensembles() {
        // Ten disjoint ensembles of 16 busy ships; the laws whose error is a function of the state or nothing at all. Under the null each t statistic is Student's with 15
        // degrees of freedom, so the largest of 50 should sit near the 98th percentile (t = 2.6) and none should pass the critical values.
        let (s, times) = (scene(), times(&scene()));
        let all = candidates(&s, CALIBRATION.iter().max().unwrap() + 1);
        std::thread::scope(|sc| {
            for chunk in CALIBRATION.chunks(40) {
                let (all, times, s) = (&all, &times, &s);
                sc.spawn(move || chunk.iter().for_each(|&i| drop(truth(s, all[i], times))));
            }
        });
        let (mut worst_m, mut worst_g) = (0.0f64, f64::NEG_INFINITY);
        for name in ["echo", "scaled", "bounded_a", "bounded_r", "bounded_p"] {
            let law = applied(name);
            let (mut tm, mut tg) = (Vec::new(), Vec::new());
            for group in CALIBRATION.chunks(16) {
                let errs: Vec<Vec<f64>> = group.iter().map(|&i| series(&s, &law, all[i], &times).unwrap().iter().map(|r| r.err).collect()).collect();
                let v = judge(&errs, margin(&s));
                assert!(v.pass, "{name}: {}", line(&v));
                (tm.push(v.t_mean), tg.push(v.t_gamma));
            }
            println!("{name}: t_mean {:?} t_gamma {:?}", tm.iter().map(|x| (x * 10.0).round() / 10.0).collect::<Vec<_>>(), tg.iter().map(|x| (x * 10.0).round() / 10.0).collect::<Vec<_>>());
            worst_m = tm.iter().fold(worst_m, |m, x| m.max(x.abs()));
            worst_g = tg.iter().fold(worst_g, |m, &x| m.max(x));
        }
        println!("largest |t_mean| {worst_m:.2}, largest t_gamma {worst_g:.2} (critical {:.2} and {:.2})", t_quantile(1.0 - ALPHA / 4.0, 15.0), t_quantile(1.0 - ALPHA / 2.0, 15.0));
        // and the other side: how many of the ten ensembles fail each law that must fail (the leak is laid on the bounded a-law, at the size the gate itself reports for it)
        let lam = verdict(&applied("bounded_a")).leak_min;
        let laws: Vec<(String, Applied)> = vec![("crossing walk 1e-7".into(), applied("walk")), ("leak in the speeds 1e-9".into(), applied("leakv9")), ("Jacobi leak 1e-9".into(), applied("leak9")), ("bounded a + leak at the detectable size".into(), bounded_and_leak(lam)), ("bounded a + half of it".into(), bounded_and_leak(lam / 2.0)), ("bounded a + a quarter".into(), bounded_and_leak(lam / 4.0))];
        for (name, law) in &laws {
            let mut caught = 0;
            for group in CALIBRATION.chunks(16) {
                let errs: Vec<Vec<f64>> = group.iter().map(|&i| series(&s, law, all[i], &times).unwrap().iter().map(|r| r.err).collect()).collect();
                caught += !judge(&errs, margin(&s)).pass as usize;
            }
            println!("{name}: failed in {caught} of 10 ensembles");
        }
    }

    #[test]
    #[ignore = "a named law through the gate: B12V2_LAW=plane|planted-kick|... (B12V2_STEP for the plane's cadence)"]
    fn a_named_law_through_the_gate() {
        use super::super::plane::Plane;
        let name = std::env::var("B12V2_LAW").unwrap_or_else(|_| "plane".into());
        let t0 = std::time::Instant::now();
        let g = if name == "plane" {
            b12v2(&Plane { step_log2: std::env::var("B12V2_STEP").ok().and_then(|v| v.parse().ok()).unwrap_or(7) })
        } else {
            match name.as_str() {
                "echo" => b12v2(&Echo),
                "planted-bounded" => b12v2(&Planted(Fault::Bounded)),
                "planted-compound" => b12v2(&Planted(Fault::Compound)),
                "planted-crossing" => b12v2(&Planted(Fault::Crossing)),
                "planted-drift" => b12v2(&Planted(Fault::Drift)),
                "planted-kick" => b12v2(&Planted(Fault::Kick)),
                _ => panic!("no law {name}"),
            }
        };
        println!("{name}: {} {} [{:.1} s]", if g.pass { "PASS" } else { "FAIL" }, g.detail, t0.elapsed().as_secs_f64());
    }

    #[test]
    #[ignore = "experiment"]
    fn placebo_by_crossings() {
        let (s, times) = (scene(), times(&scene()));
        let all = candidates(&s, CALIBRATION.iter().max().unwrap() + 1);
        std::thread::scope(|sc| {
            for chunk in CALIBRATION.chunks(40) {
                let (all, times, s) = (&all, &times, &s);
                sc.spawn(move || chunk.iter().for_each(|&i| drop(truth(s, all[i], times))));
            }
        });
        let mut rows = Vec::new();
        for &i in CALIBRATION.iter() {
            let rs = series(&s, &applied("echo"), all[i], &times).unwrap();
            let cross = rs.windows(2).filter(|w| (w[0].r2 * s.hill() < s.soi()) != (w[1].r2 * s.hill() < s.soi())).count();
            let g = |f: fn(&Row) -> f64| { let x: Vec<f64> = rs.iter().map(|r| f(r) - f(&rs[0])).collect(); ship_exponent(&x, &LAGS) };
            rows.push((cross, g(|r| r.r2.min(5.0)), g(|r| r.a.clamp(-5.0, 5.0)), g(|r| r.e.min(5.0)), mean(&rs.iter().map(|r| r.r2.min(5.0)).collect::<Vec<_>>())));
        }
        rows.sort_by_key(|r| r.0);
        for chunk in rows.chunks(40) {
            println!("crossings {}..{}: mean gamma r2 {:+.3} a {:+.3} e {:+.3}; mean r2 {:.2}", chunk[0].0, chunk[chunk.len() - 1].0, mean(&chunk.iter().map(|r| r.1).collect::<Vec<_>>()), mean(&chunk.iter().map(|r| r.2).collect::<Vec<_>>()), mean(&chunk.iter().map(|r| r.3).collect::<Vec<_>>()), mean(&chunk.iter().map(|r| r.4).collect::<Vec<_>>()));
        }
    }

    #[test]
    #[ignore = "first n busy candidates"]
    fn search_many() {
        use super::super::restricted::{Integrator, Model, RTOL};
        let n: usize = std::env::var("B12V2_N").ok().and_then(|v| v.parse().ok()).unwrap_or(160);
        let s = scene();
        let all = candidates(&s, 8 * n);
        let kept: Vec<usize> = std::thread::scope(|sc| {
            let all = &all;
            let chunks: Vec<_> = all.chunks(80).enumerate().map(|(c, ch)| sc.spawn(move || {
                let mut out = Vec::new();
                for (k, ship) in ch.iter().enumerate() {
                    let mut it = Integrator::new(&s, Model::Full, RTOL, *ship).conserving();
                    let (mut inside, mut cross) = (None, 0);
                    for j in 0..=PERIODS * 256 {
                        let t = j as f64 * s.period() / 256.0;
                        let Some(st) = it.advance(t) else { break };
                        let now = s.planet_distance(t, &st) < s.soi();
                        cross += inside.is_some_and(|b| b != now) as usize;
                        inside = Some(now);
                    }
                    if cross >= CROSSINGS_MIN { out.push(c * 80 + k); }
                }
                out
            })).collect();
            let mut v = Vec::new();
            for (c, h) in chunks.into_iter().enumerate() { v.extend(h.join().unwrap()); if v.len() >= n { let _ = c; break; } }
            v
        });
        println!("MANY = {:?}", &kept[..n.min(kept.len())]);
    }

    #[test]
    fn student_t_is_the_tables() {
        // 15 degrees of freedom: 0.975 -> 2.131, 0.995 -> 2.947, 0.9995 -> 4.073; 1 dof (Cauchy): 0.9 -> 3.078; the normal limit: 0.975 -> 1.960
        for (p, dof, want) in [(0.975, 15.0, 2.1314), (0.995, 15.0, 2.9467), (0.9995, 15.0, 4.0728), (0.9, 1.0, 3.0777), (0.975, 1e5, 1.9600)] {
            assert!((t_quantile(p, dof) - want).abs() < 2e-3, "{p} {dof}: {}", t_quantile(p, dof));
        }
        assert!((t_cdf(0.0, 7.0) - 0.5).abs() < 1e-12 && (t_cdf(1.3, 9.0) + t_cdf(-1.3, 9.0) - 1.0).abs() < 1e-12);
    }

    #[test]
    fn l1_is_where_the_books_say() {
        let s = JUPITER;
        let (x, c) = l1(&s);
        // μ = 1e-3: L1 at 0.9766 R_H from the planet, 2Ũ = 3.03995 in units where sep = Ω = 1
        let scale = 1.0 / s.sep; // lengths in separations
        assert!(((s.sep * (1.0 - s.mu) - x) / s.hill() - 0.97659).abs() < 1e-4, "{}", (s.sep * (1.0 - s.mu) - x) / s.hill());
        assert!((c * s.sep / 3.039948774974589 - 1.0).abs() < 1e-9, "{}", c * s.sep);
        let _ = scale;
    }

    #[test]
    #[ignore = "re-derives the frozen ensemble (about 1 minute)"]
    fn search() {
        use super::super::restricted::{Integrator, Model, RTOL};
        let s = scene();
        let (mut kept, mut tried) = (Vec::new(), 0);
        for (i, ship) in candidates(&s, 400).into_iter().enumerate() {
            tried += 1;
            let mut it = Integrator::new(&s, Model::Full, RTOL, ship).conserving();
            let (mut inside, mut cross) = (None, 0);
            for j in 0..=PERIODS * 256 {
                let t = j as f64 * s.period() / 256.0;
                let Some(st) = it.advance(t) else { break };
                let now = s.planet_distance(t, &st) < s.soi();
                cross += inside.is_some_and(|b| b != now) as usize;
                inside = Some(now);
            }
            if cross >= CROSSINGS_MIN {
                kept.push(i);
            }
            if kept.len() == SHIPS {
                break;
            }
        }
        println!("KEPT = {kept:?} after {tried} candidates");
    }
}
