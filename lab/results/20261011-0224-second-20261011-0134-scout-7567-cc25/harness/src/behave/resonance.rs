//! B17 resonance (docs/law.md; r4 v3's cases, as `restricted` scenes). Where the restricted
//! three-body problem is not hierarchical, a body near a mean-motion resonance with the planet
//! pumps its eccentricity and its resonant angle librates. Orbit-averaged kicks, even to first order
//! in the planet's mass, lose both (r4 v1 and v2: they over-pump by 2x and the angle circulates),
//! so a law must keep the resonance's phase feedback. This gate asks the law for it.
//!
//! - The scene: a star of mass 1 − μ and a planet of mass μ on a circle (`Restricted`, the same
//!   circular restricted three-body problem and reference as B12-B14), and a massless ship inside the
//!   planet's orbit, started on a Kepler orbit about the star with eccentricity 0.02.
//! - Resonant cases: the first-order resonances j+1:j, 2:1 and 3:2 (the planet's period against the
//!   ship's), at planet mass μ = 3e-5, 3e-4 and 3e-3, each at three detunings of the period ratio
//!   (exact, and ±1/3 of the resonance half-width W = 2.5·μ^(2/3)), each from two phases: the
//!   ship's mean anomaly 4° (libration-prone) and 172° (circulation-prone). The resonant angle is
//!   φ = (j+1)·λ_planet − j·λ_ship − ϖ_ship.
//! - Controls, far from resonance: period ratios 5.0, 2.55 and 2.15 at μ = 3e-4 (eccentricity 0.05),
//!   and 5.0 and 2.55 at μ = 3e-3 (eccentricity 0.1). Nothing resonant happens, so the ship's
//!   eccentricity stays within a narrow band: a law that invents a pump fails them.
//! - Each case runs 200 synodic periods and the law is asked for the ship's state every eighth of
//!   its orbital period. From the states (the law's and the reference's, by the same function)
//!   come the eccentricity e(t) about the star and the resonant angle φ(t), unwrapped.
//!
//! The metrics (r4 v3's, over the law's samples against the reference):
//! - e-pump ratio: the law's largest e over the reference's, per resonant case, in [0.8, 1.25].
//! - Regime: φ librates iff its unwrapped excursion (largest minus smallest) over the run is
//!   under 2π, and circulates otherwise. Where the reference's excursion is within 20% of 2π
//!   the finite run cannot tell the two apart; those cases are not asked for regime or
//!   amplitude and are reported. Elsewhere the regimes must match in every case.
//! - Libration amplitude ratio: where the reference librates, the law's excursion over the
//!   reference's, symmetrized to min(r, 1/r), at least 0.8 in every case.
//! - Controls: the law's smallest and largest e each within 20% of the reference's, in every control.
//!
//! The reference is converged or the case is not asked: the metrics must agree between the tolerances
//! 1e-12 and 1e-13 and under a 1e-9 relative change of the ship's semi-major axis (e within 1e-3,
//! excursion within 1%). More than 10% of the cases not converged fails the gate. A law that does not
//! answer a case, or answers states that leave the star's bound orbit, fails it.
use super::restricted::{self, Restricted, RTOL, RTOL_FINE};
use super::{Gate, Law};
use std::f64::consts::{PI, TAU};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::OnceLock;

/// The star-planet separation of every scene: the scene of B12-B14 (5.27e8 M, 5.2 AU of the Sun). The reference is
/// Newtonian, so the scene must sit where GR is negligible (docs/law.md, oracle domain, 6 October). At the old
/// separation of 100 M the ship was at 34-54 M, where GR moves the apse by 0.35-0.55 rad per orbit (the Opus motion memo),
/// and at 10^4 M the apse still moves by 3/(a(1 - e^2)) = 5e-4 of the mean motion, which shifts a resonance's detuning by
/// 0.2 of the half-width at mu = 3e-5 (W = 2.4e-3). At 10^6 M that shift is 0.002 W, and at 5.27e8 M it is 4e-6 W. The reference
/// is scale-free (G = M = 1), so its answers do not change; the plane's own cadence is what a weak-field scene finally tests
/// (its default cadence costs more than 60 s here; see `--plane-step`).
pub const SEP: f64 = restricted::JUPITER.sep;
pub const MASS_RATIOS: [f64; 3] = [3e-5, 3e-4, 3e-3];
/// Whether `scene` is one of this gate's (B12-B14's scene has the same separation and a mass ratio of 1e-3, which is none of these).
/// The planted law of this gate answers only these.
pub fn is_scene(scene: &Restricted) -> bool {
    scene.sep == SEP && MASS_RATIOS.contains(&scene.mu)
}
/// Detunings of the period ratio, in units of the resonance half-width.
pub const DETUNINGS: [f64; 3] = [-1.0 / 3.0, 0.0, 1.0 / 3.0];
/// The resonance half-width of the period ratio, relative: 2.5·μ^(2/3).
pub fn half_width(mu: f64) -> f64 {
    2.5 * mu.powf(2.0 / 3.0)
}
/// The ship's initial mean anomalies, radians (4° and 172°).
pub const PHASES: [f64; 2] = [4.0 * PI / 180.0, 172.0 * PI / 180.0];
pub const E_RESONANT: f64 = 0.02;
pub const SYNODIC_PERIODS: f64 = 200.0;
pub const SAMPLES_PER_ORBIT: f64 = 8.0;
pub const PUMP_MIN: f64 = 0.8;
pub const PUMP_MAX: f64 = 1.25;
pub const AMPLITUDE_MIN: f64 = 0.8;
pub const CONTROL_TOL: f64 = 0.2;
/// The reference's excursion within this fraction of 2π is borderline.
pub const BORDERLINE: f64 = 0.2;
pub const EXCLUDED_MAX: f64 = 0.1;

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Kind {
    /// The first-order resonance j+1:j.
    Resonant(u32),
    Control,
}

/// One case: the scene, the period ratio P_planet/P_ship, and the ship's eccentricity and mean anomaly.
#[derive(Clone, Debug)]
pub struct Case {
    pub name: String,
    pub kind: Kind,
    pub scene: Restricted,
    pub ratio: f64,
    pub e0: f64,
    pub m0: f64,
}

pub fn cases() -> Vec<Case> {
    let scene = |mu: f64| Restricted { mu, sep: SEP, planet_radius: 1e-3 * SEP };
    let mut out = Vec::new();
    for (j, exact) in [(1u32, 2.0), (2, 1.5)] {
        for &mu in &MASS_RATIOS {
            for d in DETUNINGS {
                for (k, &m0) in PHASES.iter().enumerate() {
                    let ratio = exact * (1.0 + d * half_width(mu));
                    out.push(Case { name: format!("{}:{} mu {mu:.0e} detune {d:+.2} phase {k}", j + 1, j), kind: Kind::Resonant(j), scene: scene(mu), ratio, e0: E_RESONANT, m0 });
                }
            }
        }
    }
    for (ratio, mu, e0) in [(5.0, 3e-4, 0.05), (2.55, 3e-4, 0.05), (2.15, 3e-4, 0.05), (5.0, 3e-3, 0.1), (2.55, 3e-3, 0.1)] {
        out.push(Case { name: format!("control {ratio} mu {mu:.0e}"), kind: Kind::Control, scene: scene(mu), ratio, e0, m0: PHASES[0] });
    }
    out
}

pub fn wrap(x: f64) -> f64 {
    let y = x % TAU;
    if y > PI {
        y - TAU
    } else if y < -PI {
        y + TAU
    } else {
        y
    }
}

/// The ship's period about the star (mean motion n₁ = ratio·Ω).
fn orbital_period(c: &Case) -> f64 {
    TAU / (c.ratio * c.scene.omega())
}

/// The sample times: every eighth of the ship's period, for `SYNODIC_PERIODS` synodic periods.
pub fn times(c: &Case) -> Vec<f64> {
    let (p1, p2) = (orbital_period(c), c.scene.period());
    let synodic = 1.0 / (1.0 / p1 - 1.0 / p2);
    let dt = p1 / SAMPLES_PER_ORBIT;
    let n = (SYNODIC_PERIODS * synodic / dt).ceil() as usize;
    (1..=n).map(|k| k as f64 * dt).collect()
}

/// The ship's barycentric state at t = 0: the Kepler orbit about the star with semi-major axis from the
/// period ratio, eccentricity e0 and mean anomaly m0, periapsis along +x (where the planet is at t = 0).
pub fn start(c: &Case) -> [f64; 4] {
    let s = &c.scene;
    let n1 = c.ratio * s.omega();
    let a = ((1.0 - s.mu) / (n1 * n1)).cbrt();
    let e = c.e0;
    let mut ea = c.m0;
    for _ in 0..50 {
        ea -= (ea - e * ea.sin() - c.m0) / (1.0 - e * ea.cos());
    }
    let (se, ce) = ea.sin_cos();
    let (px, py) = (a * (ce - e), a * (1.0 - e * e).sqrt() * se);
    let f = n1 * a / (1.0 - e * ce);
    let (vx, vy) = (-f * se, f * (1.0 - e * e).sqrt() * ce);
    let (p, v) = s.star(0.0);
    [p[0] + px, p[1] + py, v[0] + vx, v[1] + vy]
}

/// The heliocentric elements of a barycentric state at t: (a, e, ϖ, λ), about the star's mass 1 − μ.
pub fn elements(scene: &Restricted, t: f64, s: &[f64; 4]) -> (f64, f64, f64, f64) {
    let (p, v) = scene.star(t);
    let (x, y, vx, vy) = (s[0] - p[0], s[1] - p[1], s[2] - v[0], s[3] - v[1]);
    let gm = 1.0 - scene.mu;
    let (r, v2, rv) = ((x * x + y * y).sqrt(), vx * vx + vy * vy, x * vx + y * vy);
    let k = v2 - gm / r;
    let (ex, ey) = ((k * x - rv * vx) / gm, (k * y - rv * vy) / gm);
    let e = ex.hypot(ey);
    let varpi = ey.atan2(ex);
    let a = 1.0 / (2.0 / r - v2 / gm);
    let (ce, se) = ((1.0 - r / a) / e, rv / (e * (gm * a).sqrt()));
    let m = se.atan2(ce) - e * se;
    (a, e, varpi, varpi + m)
}

/// What the metrics read from one run: the smallest and largest e, and the excursion of φ (0 for a control).
#[derive(Clone, Copy, Debug)]
pub struct Track {
    pub e_min: f64,
    pub e_max: f64,
    pub excursion: f64,
}

/// The track of `states` at `times`. None: a state is not on a bound orbit about the star (e not in
/// (0, 1)), or the count is wrong.
pub fn track(c: &Case, times: &[f64], states: &[[f64; 4]]) -> Option<Track> {
    if states.len() != times.len() || times.is_empty() {
        return None;
    }
    let j = if let Kind::Resonant(j) = c.kind { j as f64 } else { 0.0 };
    let (mut e_min, mut e_max, mut lo, mut hi, mut prev, mut un) = (f64::INFINITY, 0.0f64, f64::INFINITY, f64::NEG_INFINITY, 0.0, 0.0);
    for (i, (&t, s)) in times.iter().zip(states).enumerate() {
        let (a, e, varpi, lam) = elements(&c.scene, t, s);
        if !(a > 0.0 && e > 0.0 && e < 1.0 && lam.is_finite() && varpi.is_finite()) {
            return None;
        }
        let phi = wrap((j + 1.0) * c.scene.phase(t) - j * lam - varpi);
        un = if i == 0 { phi } else { un + wrap(phi - prev) };
        prev = phi;
        (e_min, e_max, lo, hi) = (e_min.min(e), e_max.max(e), lo.min(un), hi.max(un));
    }
    Some(Track { e_min, e_max, excursion: hi - lo })
}

/// The regime of an excursion: Some(true) librates, Some(false) circulates, None borderline.
pub fn librates(excursion: f64) -> Option<bool> {
    ((excursion - TAU).abs() > BORDERLINE * TAU).then_some(excursion < TAU)
}

/// The reference for one case: its track, and whether it is converged (the metrics agree between
/// tolerances and under a nudge).
#[derive(Clone, Copy, Debug)]
pub struct Truth {
    pub track: Track,
    pub converged: bool,
}

fn run(c: &Case, rtol: f64, nudge: f64) -> Option<Track> {
    let times = times(c);
    let mut ship = start(c);
    if nudge != 0.0 {
        // A relative change of the semi-major axis: the heliocentric radius scales as a, the speed as a^(-1/2).
        let (p, v) = c.scene.star(0.0);
        let s = 1.0 + nudge;
        ship = [p[0] + (ship[0] - p[0]) * s, p[1] + (ship[1] - p[1]) * s, v[0] + (ship[2] - v[0]) / s.sqrt(), v[1] + (ship[3] - v[1]) / s.sqrt()];
    }
    let states = restricted::reference(&c.scene, ship, &times, rtol)?;
    track(c, &times, &states)
}

fn close(a: &Track, b: &Track) -> bool {
    (a.e_max - b.e_max).abs() <= 1e-3 * a.e_max && (a.e_min - b.e_min).abs() <= 1e-3 * a.e_max && (a.excursion - b.excursion).abs() <= 1e-2 * a.excursion.max(1.0)
}

/// The reference's verdict on case `c`, with the two convergence runs. None: the reference gave up.
pub fn assess(c: &Case) -> Option<Truth> {
    let track = run(c, RTOL, 0.0)?;
    let converged = [run(c, RTOL_FINE, 0.0), run(c, RTOL, 1e-9)].iter().all(|r| r.as_ref().is_some_and(|r| close(&track, r)));
    Some(Truth { track, converged })
}

/// The reference's truth for every case, computed once per process on up to four threads (the
/// answer does not depend on the schedule).
pub fn truths() -> &'static Vec<Option<Truth>> {
    static TRUTHS: OnceLock<Vec<Option<Truth>>> = OnceLock::new();
    TRUTHS.get_or_init(|| {
        let (all, next) = (cases(), AtomicUsize::new(0));
        let threads = std::thread::available_parallelism().map_or(1, |n| n.get()).min(4);
        let mut done: Vec<(usize, Option<Truth>)> = std::thread::scope(|scope| {
            let workers: Vec<_> = (0..threads)
                .map(|_| {
                    scope.spawn(|| {
                        let mut mine = Vec::new();
                        loop {
                            let i = next.fetch_add(1, Ordering::Relaxed);
                            if i >= all.len() {
                                return mine;
                            }
                            mine.push((i, assess(&all[i])));
                        }
                    })
                })
                .collect();
            workers.into_iter().flat_map(|w| w.join().expect("a resonance case's reference panicked")).collect()
        });
        done.sort_by_key(|d| d.0);
        done.into_iter().map(|d| d.1).collect()
    })
}

/// How one case fared against the reference.
#[derive(Clone, Copy, Debug, Default)]
pub struct Verdict {
    /// The law's largest e over the reference's (resonant cases).
    pub pump: Option<f64>,
    /// Both librate or both circulate (None: borderline, or not a resonant case).
    pub regime: Option<bool>,
    /// min(r, 1/r) of the excursions' ratio, where the reference librates.
    pub amplitude: Option<f64>,
    /// The control's envelope is within tolerance (controls).
    pub control: Option<bool>,
}

pub fn verdict(c: &Case, truth: &Truth, law: &Track) -> Verdict {
    let t = &truth.track;
    let mut v = Verdict::default();
    match c.kind {
        Kind::Resonant(_) => {
            v.pump = Some(law.e_max / t.e_max);
            if let Some(lib) = librates(t.excursion) {
                v.regime = Some((law.excursion < TAU) == lib);
                if lib {
                    let r = law.excursion / t.excursion;
                    v.amplitude = Some(r.min(1.0 / r));
                }
            }
        }
        Kind::Control => v.control = Some((law.e_min / t.e_min - 1.0).abs() <= CONTROL_TOL && (law.e_max / t.e_max - 1.0).abs() <= CONTROL_TOL),
    }
    v
}

/// The extreme of a series, NaN if any is NaN (a failure must show).
fn extreme(xs: impl Iterator<Item = f64>, start: f64, pick: fn(f64, f64) -> f64) -> f64 {
    xs.fold(start, |m, x| if m.is_nan() || x.is_nan() { f64::NAN } else { pick(m, x) })
}

pub fn b17(law: &dyn Law) -> Gate {
    let _quiet = super::scale::QUIET.read().unwrap_or_else(|e| e.into_inner());
    let all = cases();
    let truths = truths();
    let mut rows: Vec<(usize, Verdict)> = Vec::new();
    let (mut unconverged, mut unanswered) = (0, 0);
    for (i, (c, truth)) in all.iter().zip(truths).enumerate() {
        let Some(truth) = truth.filter(|t| t.converged) else {
            unconverged += 1;
            continue;
        };
        let ts = times(c);
        match law.restricted(&c.scene, start(c), &ts).and_then(|s| track(c, &ts, &s)) {
            Some(l) => rows.push((i, verdict(c, &truth, &l))),
            None => unanswered += 1,
        }
    }
    let kind = |k: fn(&Kind) -> bool| rows.iter().filter(|r| k(&all[r.0].kind)).collect::<Vec<_>>();
    let resonant = kind(|k| matches!(k, Kind::Resonant(_)));
    let controls = kind(|k| *k == Kind::Control);
    let pumps: Vec<f64> = resonant.iter().filter_map(|r| r.1.pump).collect();
    let (pump_lo, pump_hi) = (extreme(pumps.iter().copied(), f64::INFINITY, f64::min), extreme(pumps.iter().copied(), 0.0, f64::max));
    let asked: Vec<&&(usize, Verdict)> = resonant.iter().filter(|r| r.1.regime.is_some()).collect();
    let regime_ok = asked.iter().filter(|r| r.1.regime == Some(true)).count();
    let amplitudes: Vec<f64> = resonant.iter().filter_map(|r| r.1.amplitude).collect();
    let amp_min = extreme(amplitudes.iter().copied(), f64::INFINITY, f64::min);
    let control_ok = controls.iter().filter(|r| r.1.control == Some(true)).count();
    let borderline = resonant.len() - asked.len();
    let failing: Vec<&str> = rows
        .iter()
        .filter(|(_, v)| {
            v.pump.is_some_and(|p| !(PUMP_MIN..=PUMP_MAX).contains(&p)) || v.amplitude.is_some_and(|a| a < AMPLITUDE_MIN || a.is_nan()) || v.regime == Some(false) || v.control == Some(false)
        })
        .map(|r| all[r.0].name.as_str())
        .collect();
    let pass = unanswered == 0
        && unconverged as f64 <= EXCLUDED_MAX * all.len() as f64
        && !resonant.is_empty()
        && !controls.is_empty()
        && pumps.iter().all(|p| (PUMP_MIN..=PUMP_MAX).contains(p))
        && amplitudes.iter().all(|&a| a >= AMPLITUDE_MIN)
        && regime_ok == asked.len()
        && control_ok == controls.len();
    let detail = format!(
        "resonance: e-pump ratio [{pump_lo:.6}, {pump_hi:.6}] over {} resonant cases (needs [{PUMP_MIN}, {PUMP_MAX}]); libration amplitude ratio {amp_min:.3} min over {} librating (needs {AMPLITUDE_MIN}); regime {regime_ok}/{} matched ({borderline} borderline, not asked); controls {control_ok}/{}; {unanswered} unanswered, {unconverged} of {} not converged",
        resonant.len(),
        amplitudes.len(),
        asked.len(),
        controls.len(),
        all.len()
    ) + &if failing.is_empty() { String::new() } else { format!("; {} cases fail a leg, among them {}", failing.len(), failing.iter().take(4).copied().collect::<Vec<_>>().join(", ")) };
    Gate { id: "B17", pass, detail, secs: 0.0 }
}

/// The Laplace coefficient b^(1)_{3/2}(α) = (1/π)∫₀^{2π} cos ψ·(1 − 2α cos ψ + α²)^(−3/2) dψ, by the
/// trapezoid rule (exponentially accurate for a periodic integrand).
pub fn laplace_b(alpha: f64) -> f64 {
    let n = 4096;
    (0..n)
        .map(|k| {
            let psi = TAU * k as f64 / n as f64;
            psi.cos() / (1.0 - 2.0 * alpha * psi.cos() + alpha * alpha).powf(1.5)
        })
        .sum::<f64>()
        * 2.0
        / n as f64
}

/// The law of `planted-average`: the first-order orbit average (Laplace-Lagrange) of the planet's pull
/// on a ship inside its orbit. Averaged over both mean longitudes, the planet's pull leaves the ship's
/// semi-major axis and eccentricity as they were, turns its periapsis at A = (n/4)·μ/(1 − μ)·α²·b^(1)_{3/2}(α)
/// (α = a/a_planet), and the mean longitude advances at the Kepler rate n. Nothing resonant survives
/// the average, which is what r4 v1 and v2 found fails. The ship's states are the precessing ellipse.
pub fn averaged(scene: &Restricted, ship: [f64; 4], times: &[f64]) -> Option<Vec<[f64; 4]>> {
    let (a, e, varpi0, lam0) = elements(scene, 0.0, &ship);
    if !(a > 0.0 && e > 0.0 && e < 1.0) {
        return None;
    }
    let gm = 1.0 - scene.mu;
    let n = (gm / (a * a * a)).sqrt();
    let alpha = a / scene.sep;
    let precession = 0.25 * n * scene.mu / gm * alpha * alpha * laplace_b(alpha);
    Some(
        times
            .iter()
            .map(|&t| {
                let (varpi, m) = (varpi0 + precession * t, wrap(lam0 - varpi0 + n * t));
                let mut ea = m;
                for _ in 0..50 {
                    ea -= (ea - e * ea.sin() - m) / (1.0 - e * ea.cos());
                }
                let (se, ce) = ea.sin_cos();
                let (root, f) = ((1.0 - e * e).sqrt(), n * a / (1.0 - e * ce));
                let (px, py, vx, vy) = (a * (ce - e), a * root * se, -f * se, f * root * ce);
                let (sv, cv) = varpi.sin_cos();
                let (x, y) = (cv * px - sv * py, sv * px + cv * py);
                // the velocity of the ellipse at fixed elements, plus the turning of the whole ellipse
                let (u, w) = (cv * vx - sv * vy - precession * y, sv * vx + cv * vy + precession * x);
                let (star, star_v) = scene.star(t);
                [star[0] + x, star[1] + y, star_v[0] + u, star_v[1] + w]
            })
            .collect(),
    )
}


#[cfg(test)]
mod tests {
    use super::super::laws::{Echo, Events, Fault, Planted, Silent};
    use super::*;

    fn truth(name: &str) -> Truth {
        let i = cases().iter().position(|c| c.name == name).unwrap_or_else(|| panic!("no case {name}"));
        truths()[i].unwrap()
    }
    fn events(restricted: impl Fn(&Restricted, [f64; 4], &[f64]) -> Option<Vec<[f64; 4]>> + 'static) -> Events {
        Events { binary: Box::new(Some), restricted: Box::new(restricted) }
    }
    fn tr(e_min: f64, e_max: f64, excursion: f64) -> Track {
        Track { e_min, e_max, excursion }
    }

    #[test]
    fn the_cases_are_r4_v3s_two_resonances_three_masses_three_detunings_two_phases_and_five_controls() {
        let all = cases();
        let resonant: Vec<&Case> = all.iter().filter(|c| matches!(c.kind, Kind::Resonant(_))).collect();
        assert_eq!((all.len(), resonant.len()), (41, 36));
        for (j, exact) in [(1, 2.0), (2, 1.5)] {
            for mu in MASS_RATIOS {
                let ratios: Vec<f64> = resonant.iter().filter(|c| c.kind == Kind::Resonant(j) && c.scene.mu == mu).map(|c| c.ratio).collect();
                assert_eq!(ratios.len(), 6);
                // exact, and ±1/3 of the half-width 2.5·μ^(2/3) away, each twice (two phases)
                assert!(ratios.iter().filter(|&&r| r == exact).count() == 2 && ratios.iter().filter(|&&r| (r / exact - 1.0 - half_width(mu) / 3.0).abs() < 1e-12).count() == 2);
            }
        }
        assert!((half_width(3e-3) - 0.052).abs() < 1e-3 && (half_width(3e-5) - 0.0024).abs() < 1e-4);
        let controls: Vec<f64> = all.iter().filter(|c| c.kind == Kind::Control).map(|c| c.ratio).collect();
        assert_eq!(controls, [5.0, 2.55, 2.15, 5.0, 2.55]);
        assert!(all.iter().all(|c| c.scene.sep == SEP && c.scene.planet_radius > 0.0));
        // Each case runs 200 synodic periods and is sampled every eighth of the ship's period.
        for c in &all {
            let ts = times(c);
            let synodic = 1.0 / (1.0 / orbital_period(c) - 1.0 / c.scene.period());
            assert!(*ts.last().unwrap() >= SYNODIC_PERIODS * synodic && ts[1] - ts[0] - orbital_period(c) / 8.0 < 1e-9, "{}", c.name);
        }
    }

    #[test]
    fn a_ship_starts_on_the_kepler_orbit_the_case_names_about_the_star() {
        for c in cases().iter().step_by(7) {
            let (a, e, varpi, lam) = elements(&c.scene, 0.0, &start(c));
            let n1 = c.ratio * c.scene.omega();
            assert!((a / ((1.0 - c.scene.mu) / (n1 * n1)).cbrt() - 1.0).abs() < 1e-12 && (e - c.e0).abs() < 1e-12 && varpi.abs() < 1e-9 && wrap(lam - c.m0).abs() < 1e-9, "{}: {a} {e} {varpi} {lam}", c.name);
        }
    }

    #[test]
    fn the_reference_pumps_and_librates_at_the_resonance_and_leaves_the_controls_alone() {
        // 2:1 at μ = 3e-3, exact, from the libration-prone phase: e grows seven-fold and φ librates; from the other phase it circulates.
        let (lib, circ) = (truth("2:1 mu 3e-3 detune +0.00 phase 0"), truth("2:1 mu 3e-3 detune +0.00 phase 1"));
        assert!(lib.track.e_max > 6.0 * E_RESONANT && librates(lib.track.excursion) == Some(true), "{lib:?}");
        assert!(circ.track.e_max > 6.0 * E_RESONANT && librates(circ.track.excursion) == Some(false), "{circ:?}");
        // The pump scales with the mass: 3e-5 hardly moves e, 3e-3 multiplies it.
        let weak = truth("2:1 mu 3e-5 detune +0.00 phase 0");
        assert!(weak.track.e_max < 2.0 * E_RESONANT && weak.track.e_max < lib.track.e_max / 3.0, "{weak:?}");
        // Far from resonance e stays within 20% of its start, and φ (undefined there) is not a number to read.
        for c in cases().iter().filter(|c| c.kind == Kind::Control) {
            let t = truth(&c.name).track;
            assert!(t.e_max < 1.2 * c.e0 && t.e_min > 0.8 * c.e0 && t.e_max > 0.99 * c.e0, "{}: {t:?}", c.name);
        }
    }

    #[test]
    fn only_the_cases_the_reference_converges_on_are_asked_and_a_chaotic_one_is_dropped_and_counted() {
        let ts = truths();
        assert_eq!(ts.len(), 41);
        let bad: Vec<usize> = (0..41).filter(|&i| !ts[i].is_some_and(|t| t.converged)).collect();
        // 3:2 at μ = 3e-3, detuned inward, from the circulation-prone phase: the ship scatters off the planet (e up to 0.7).
        assert_eq!(bad.iter().map(|&i| cases()[i].name.clone()).collect::<Vec<_>>(), ["3:2 mu 3e-3 detune -0.33 phase 1"]);
        assert!(bad.len() as f64 <= EXCLUDED_MAX * 41.0);
        assert!(close(&tr(0.02, 0.1, 5.0), &tr(0.02, 0.10005, 5.04)) && !close(&tr(0.02, 0.1, 5.0), &tr(0.02, 0.102, 5.0)) && !close(&tr(0.02, 0.1, 5.0), &tr(0.02, 0.1, 5.2)));
    }

    #[test]
    fn the_regimes_are_librating_below_two_pi_circulating_above_and_borderline_within_a_fifth_of_it() {
        assert_eq!(librates(1.0), Some(true));
        assert_eq!(librates(4.9), Some(true));
        assert_eq!(librates(5.2), None);
        assert_eq!(librates(TAU), None);
        assert_eq!(librates(7.4), None);
        assert_eq!(librates(7.7), Some(false));
        assert_eq!(librates(80.0), Some(false));
    }

    #[test]
    fn the_verdicts_are_r4_v3s_metrics_with_their_thresholds() {
        let resonant = &cases()[14]; // 2:1, μ = 3e-3, exact, phase 0
        assert_eq!(resonant.kind, Kind::Resonant(1));
        let truth = Truth { track: tr(0.014, 0.139, 2.5), converged: true };
        let v = verdict(resonant, &truth, &tr(0.014, 0.139, 2.5));
        assert_eq!((v.pump, v.regime, v.amplitude), (Some(1.0), Some(true), Some(1.0)));
        // Pump is the ratio of the largest e; the amplitude ratio is symmetrized; a circulating law against a librating truth mismatches.
        let v = verdict(resonant, &truth, &tr(0.014, 0.0556, 2.0));
        assert!((v.pump.unwrap() - 0.4).abs() < 1e-9 && (v.amplitude.unwrap() - 0.8).abs() < 1e-12 && v.regime == Some(true));
        let v = verdict(resonant, &truth, &tr(0.014, 0.2, 3.125));
        assert!((v.pump.unwrap() - 1.4388).abs() < 1e-3 && (v.amplitude.unwrap() - 0.8).abs() < 1e-12);
        let v = verdict(resonant, &truth, &tr(0.014, 0.139, 40.0));
        assert_eq!((v.regime, v.amplitude.map(|a| a < 0.07)), (Some(false), Some(true)));
        // A circulating truth has no libration amplitude; a borderline one is not asked for either.
        let circ = Truth { track: tr(0.014, 0.139, 70.0), converged: true };
        let v = verdict(resonant, &circ, &tr(0.014, 0.139, 3.0));
        assert_eq!((v.regime, v.amplitude), (Some(false), None));
        let v = verdict(resonant, &Truth { track: tr(0.014, 0.139, 6.0), converged: true }, &tr(0.014, 0.139, 3.0));
        assert_eq!((v.regime, v.amplitude), (None, None));
        // A control: each end of the envelope within 20%.
        let control = &cases()[36];
        assert_eq!(control.kind, Kind::Control);
        let t = Truth { track: tr(0.0485, 0.0500, 0.0), converged: true };
        assert_eq!(verdict(control, &t, &tr(0.0485, 0.0500, 0.0)).control, Some(true));
        assert_eq!(verdict(control, &t, &tr(0.05, 0.05, 0.0)).control, Some(true));
        assert_eq!(verdict(control, &t, &tr(0.0485, 0.0625, 0.0)).control, Some(false));
        assert_eq!(verdict(control, &t, &tr(0.0380, 0.0500, 0.0)).control, Some(false));
    }

    #[test]
    fn the_laplace_coefficient_and_the_averaged_precession_are_right_where_averaging_is_right() {
        // b^(1)_{3/2}(α) = 3α(1 + 15α²/8 + 175α⁴/64 + ...)
        let a = 0.1;
        assert!((laplace_b(a) / (3.0 * a * (1.0 + 15.0 * a * a / 8.0 + 175.0 * a.powi(4) / 64.0 + 3675.0 * a.powi(6) / 1024.0)) - 1.0).abs() < 1e-6);
        // Far from resonance the planted law's periapsis precession is the reference's: control 5.0 at μ = 3e-3.
        let c = &cases()[39];
        assert_eq!((c.ratio, c.scene.mu), (5.0, 3e-3));
        let (ts, ship) = (times(c), start(c));
        // The slope of the unwrapped periapsis longitude over the run.
        let slope = |states: &[[f64; 4]]| {
            let (mut un, mut prev) = (0.0, elements(&c.scene, ts[0], &states[0]).2);
            for (&t, s) in ts.iter().zip(states) {
                let v = elements(&c.scene, t, s).2;
                un += wrap(v - prev);
                prev = v;
            }
            un / (ts.last().unwrap() - ts[0])
        };
        let truth = restricted::reference(&c.scene, ship, &ts, RTOL).unwrap();
        let planted = averaged(&c.scene, ship, &ts).unwrap();
        let (a_truth, a_law) = (slope(&truth), slope(&planted));
        assert!((a_law / a_truth - 1.0).abs() < 0.05, "reference {a_truth:e}, first-order average {a_law:e} rad per unit time");
        // And its states are an ellipse of the same shape: a and e are the osculating ones at the start.
        let (a0, e0, _, _) = elements(&c.scene, 0.0, &ship);
        let (a1, e1, _, _) = elements(&c.scene, ts[100], &planted[100]);
        assert!((a1 / a0 - 1.0).abs() < 1e-3 && (e1 / e0 - 1.0).abs() < 5e-3);
    }

    #[test]
    fn echo_is_the_reference_to_a_part_in_ten_thousand_on_every_leg_and_the_first_order_average_fails_the_resonance_and_not_the_controls() {
        let g = b17(&Echo);
        assert!(g.pass && g.detail.contains("35 resonant cases") && g.detail.contains("controls 5/5") && g.detail.contains("1 of 41 not converged"), "{}", g.detail);
        let pumps: Vec<f64> = g.detail.split("[").nth(1).unwrap().split("]").next().unwrap().split(", ").map(|x| x.parse().unwrap()).collect();
        assert!(pumps.iter().all(|p| (p - 1.0).abs() < 1e-4), "{}", g.detail);
        // The planted first-order average: e stays where it began (pump ratio 0.1 at the strong resonances), φ drifts
        // instead of librating or circulating the way the truth does, and the quiet controls pass.
        let g = b17(&Planted(Fault::Averaged));
        assert!(!g.pass && g.detail.contains("controls 5/5") && g.detail.contains("libration amplitude ratio 0.0"), "{}", g.detail);
        let pump_lo: f64 = g.detail.split("[").nth(1).unwrap().split(", ").next().unwrap().parse().unwrap();
        assert!(pump_lo < 0.2, "{}", g.detail);
        // Silence fails.
        assert!(!b17(&Silent).pass);
    }

    #[test]
    fn a_law_that_does_not_answer_a_case_or_leaves_the_stars_orbit_fails_whatever_else_it_gets_right() {
        // Echo on every case but the first, which it does not answer.
        let first = std::cell::Cell::new(true);
        let g = b17(&events(move |s, ship, ts| if first.replace(false) { None } else { Echo.restricted(s, ship, ts) }));
        assert!(!g.pass && g.detail.contains("1 unanswered"), "{}", g.detail);
        // States that are unbound about the star (a free particle) do not have an eccentricity below one.
        let g = b17(&events(|s, ship, ts| Some(ts.iter().map(|&t| s.barycentric(t, &[ship[0] + 1e3 * t, ship[1], ship[2] + 10.0, ship[3]])).collect())));
        assert!(!g.pass && g.detail.contains("unanswered"), "{}", g.detail);
        // The wrong number of states.
        assert!(!b17(&events(|s, ship, ts| Echo.restricted(s, ship, &ts[1..]))).pass);
    }
}
