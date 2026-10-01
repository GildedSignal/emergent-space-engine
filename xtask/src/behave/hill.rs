//! B14 Hill stability (docs/law.md; principle 20: behaviours over many seeds). A moon at 0.2 to 0.9
//! Hill radii from the planet is either bound for 50 planet orbits or it escapes, and which one
//! depends on the tide: prograde moons past about half a Hill radius are lost, retrograde ones
//! last to nearly one. A law that mishandles the star's tide inside the doll gets the classes wrong.
//! A law that gets the class right can still get the apsides wrong (r9: orbit-averaged kicks keep
//! the class everywhere and the apsidal precession only below 0.17 Hill radii), so the gate judges both.
//!
//! - Seeds: 128 moons on circular planetocentric orbits, a uniform in [0.2, 0.9]·R_H, prograde for
//!   even seeds and retrograde for odd, phase uniform (the gate's first version, unchanged); then
//!   128 eccentric births, a uniform in the same range and e₀ uniform in [0, 0.3], starting at
//!   periapsis (`sample::eccentric_moons`). The moon's speed is the Kepler speed about the planet,
//!   added to the planet's.
//! - Run 50 planet periods, sampled every P/64 for the law and the reference alike. Escaped iff
//!   the distance from the planet exceeds 1.5·R_H at any sample.
//! - Judged: the reference is converged (the class is the same at tolerance 1e-13) and its class
//!   is unchanged when a is multiplied by (1 + 1e-6). The rest are chaotic, and are not asked.
//!   More than 10% of the seeds not converged fails the gate.
//! - Apsides: for a bound moon, the planetocentric periapsis longitude ϖ(t) is the direction of the
//!   Laplace-Runge-Lenz vector of the state at each sample, on the inertial axes; the precession
//!   rate is the least-squares slope of the unwrapped ϖ against time. The reference's rate is
//!   asked only where it is a rate: ϖ never jumps by more than π/2 between two samples (the apse
//!   is defined), and the rate agrees within 2% between the tolerances 1e-12 and 1e-13 and under
//!   the nudge. A law whose own ϖ jumps has no rate and misses.
//! - PASS iff at least 64 seeds are judged and at least 99% of them have the reference's class, at
//!   least 32 bound moons are judged on their apsides and at least 99% of those have a rate within
//!   10% of the reference's, and fewer than 10% of the seeds are not converged.
use super::restricted::{Integrator, Model, Restricted, JUPITER, RTOL, RTOL_FINE};
use super::{sample, Gate, Law};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::OnceLock;

/// Circular births (the first version of the gate) and eccentric births.
pub const CIRCULAR: usize = 128;
pub const ECCENTRIC: usize = 128;
pub const SEEDS: usize = CIRCULAR + ECCENTRIC;
pub const PERIODS: usize = 50;
pub const SAMPLES_PER_PERIOD: usize = 64;
/// Escaped: farther than this many Hill radii from the planet at a sample.
pub const ESCAPE_HILL: f64 = 1.5;
/// The perturbation of a that the class must survive, relative.
pub const NUDGE: f64 = 1e-6;
pub const JUDGED_MIN: usize = 64;
pub const EXCLUDED_MAX: f64 = 0.1;
/// The apsidal rate must match the reference's to this, relative.
pub const APSIDES_TOL: f64 = 0.1;
/// The reference's rate must agree between its tolerances and under the nudge to this, relative.
pub const APSIDES_STABLE: f64 = 0.02;
pub const APSIDES_MIN: usize = 32;

/// The moon on a circular orbit of radius `a` (units of M) about the
/// planet, at `phase`, prograde or retrograde, with the planet's velocity added.
#[cfg(test)]
pub fn moon(scene: &Restricted, a: f64, phase: f64, prograde: bool) -> [f64; 4] {
    birth(scene, a, phase, 0.0, prograde)
}

/// A moon born at periapsis, in direction `phase` from the planet, on the Kepler orbit about the
/// planet with semi-major axis `a` and eccentricity `e0`, prograde or retrograde, with the
/// planet's velocity added. With e0 = 0 it is `moon`.
pub fn birth(scene: &Restricted, a: f64, phase: f64, e0: f64, prograde: bool) -> [f64; 4] {
    let (s, c) = phase.sin_cos();
    let (r, v) = (a * (1.0 - e0), (scene.mu * (1.0 + e0) / (a * (1.0 - e0))).sqrt() * if prograde { 1.0 } else { -1.0 });
    scene.barycentric(0.0, &[r * c, r * s, -v * s, v * c])
}

/// The sample times: every P/64 for 50 periods.
pub fn times(scene: &Restricted) -> Vec<f64> {
    (1..=PERIODS * SAMPLES_PER_PERIOD).map(|j| j as f64 * scene.period() / SAMPLES_PER_PERIOD as f64).collect()
}

/// Did any of the states, at `times`, leave the 1.5 R_H sphere about the planet?
fn escaped(scene: &Restricted, times: &[f64], states: &[[f64; 4]]) -> bool {
    times.iter().zip(states).any(|(&t, s)| !(scene.planet_distance(t, s) <= ESCAPE_HILL * scene.hill()))
}

/// The planetocentric periapsis longitude at each state, unwrapped from the first: the direction
/// of the Laplace-Runge-Lenz vector of the state relative to the planet, on the inertial axes.
/// None: the apse is not defined (e is 0, a state is not finite) or jumps by more than π/2
/// between two samples.
pub fn apsides_series(scene: &Restricted, times: &[f64], states: &[[f64; 4]]) -> Option<Vec<f64>> {
    let mut out: Vec<f64> = Vec::with_capacity(states.len());
    for (&t, s) in times.iter().zip(states) {
        let w = scene.relative(t, s);
        let (r2, v2, rv) = (w[0] * w[0] + w[1] * w[1], w[2] * w[2] + w[3] * w[3], w[0] * w[2] + w[1] * w[3]);
        let k = v2 - scene.mu / r2.sqrt();
        let (ex, ey) = (k * w[0] - rv * w[2], k * w[1] - rv * w[3]);
        let varpi = ey.atan2(ex);
        // |LRL|/μ is the eccentricity: below 1e-9 the orbit is circular to rounding and has no apse.
        if !(ex.hypot(ey) > 1e-9 * scene.mu) || !varpi.is_finite() {
            return None;
        }
        let Some(&last) = out.last() else {
            out.push(varpi);
            continue;
        };
        let mut jump = (varpi - last) % std::f64::consts::TAU;
        if jump > std::f64::consts::PI {
            jump -= std::f64::consts::TAU;
        } else if jump < -std::f64::consts::PI {
            jump += std::f64::consts::TAU;
        }
        if jump.abs() > std::f64::consts::FRAC_PI_2 {
            return None;
        }
        out.push(last + jump);
    }
    (!out.is_empty()).then_some(out)
}

/// The apsidal precession rate, radians per planet period: the least-squares slope of the unwrapped
/// periapsis longitude against time. None: the apse is not defined (see `apsides_series`).
pub fn apsidal_rate(scene: &Restricted, times: &[f64], states: &[[f64; 4]]) -> Option<f64> {
    let varpi = apsides_series(scene, times, states)?;
    let u: Vec<f64> = times.iter().map(|&t| t / scene.period()).collect();
    let n = u.len() as f64;
    let (mu, mv) = (u.iter().sum::<f64>() / n, varpi.iter().sum::<f64>() / n);
    let (num, den) = (u.iter().zip(&varpi).map(|(a, b)| (a - mu) * (b - mv)).sum::<f64>(), u.iter().map(|a| (a - mu) * (a - mu)).sum::<f64>());
    (den > 0.0).then_some(num / den)
}

/// One run of the reference: the class and the states, up to the first escape.
struct Run {
    escaped: bool,
    states: Vec<[f64; 4]>,
}

/// The reference's run for `ship` to tolerance `rtol`, stopping at the first escape. None: gave up.
fn reference_run(scene: &Restricted, times: &[f64], ship: [f64; 4], rtol: f64) -> Option<Run> {
    let mut it = Integrator::new(scene, Model::Full, rtol, ship);
    let mut states = Vec::with_capacity(times.len());
    for &t in times {
        let state = it.advance(t)?;
        states.push(state);
        if escaped(scene, &[t], &[state]) {
            return Some(Run { escaped: true, states });
        }
    }
    Some(Run { escaped: false, states })
}

/// What the reference makes of one moon.
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Truth {
    /// Its class (true: escapes), converged and stable under the nudge.
    Class(bool),
    /// The class changes when a is multiplied by 1 + 1e-6.
    Chaotic,
    /// The class differs between the tolerances 1e-12 and 1e-13, or the integration gave up.
    Unconverged,
}

/// A moon, the reference's verdict on it, and (for a bound one whose apse is defined and whose
/// rate is stable) the reference's apsidal rate in radians per planet period.
pub struct Moon {
    pub ship: [f64; 4],
    pub truth: Truth,
    pub rate: Option<f64>,
}

/// The reference's verdict on moon `i` of the draws (circular births first, then the eccentric ones).
fn assess(scene: &Restricted, times: &[f64], i: usize, (a_hill, phase, e0): (f64, f64, f64)) -> Moon {
    let (a, prograde) = (a_hill * scene.hill(), i % 2 == 0);
    let ship = birth(scene, a, phase, e0, prograde);
    let run = reference_run(scene, times, ship, RTOL);
    let fine = || reference_run(scene, times, ship, RTOL_FINE);
    let nudged = || reference_run(scene, times, birth(scene, a * (1.0 + NUDGE), phase, e0, prograde), RTOL);
    let class = |r: &Option<Run>| r.as_ref().map(|r| r.escaped);
    let (truth, rate) = match &run {
        None => (Truth::Unconverged, None),
        Some(r) => {
            let fine = fine();
            if class(&run) != class(&fine) {
                (Truth::Unconverged, None)
            } else {
                let nudged = nudged();
                if class(&run) != class(&nudged) {
                    (Truth::Chaotic, None)
                } else if r.escaped {
                    (Truth::Class(true), None)
                } else {
                    let rate = |r: &Option<Run>| r.as_ref().and_then(|r| apsidal_rate(scene, times, &r.states));
                    let (a, f, n) = (rate(&run), rate(&fine), rate(&nudged));
                    let stable = a.is_some_and(|a| a != 0.0 && [f, n].iter().all(|o| o.is_some_and(|o| (o - a).abs() <= APSIDES_STABLE * a.abs())));
                    (Truth::Class(false), if stable { a } else { None })
                }
            }
        }
    };
    Moon { ship, truth, rate }
}

/// The moons, with the reference's verdict on each. None of this depends on the law, so it is
/// computed once per process, on up to four threads (each moon is independent of the others, so
/// the answer does not depend on the schedule).
pub fn moons() -> &'static Vec<Moon> {
    static MOONS: OnceLock<Vec<Moon>> = OnceLock::new();
    MOONS.get_or_init(|| {
        let scene = JUPITER;
        let draws: Vec<(f64, f64, f64)> = sample::moons(CIRCULAR).into_iter().map(|(a, p)| (a, p, 0.0)).chain(sample::eccentric_moons(ECCENTRIC)).collect();
        let (times, next) = (times(&scene), AtomicUsize::new(0));
        let threads = std::thread::available_parallelism().map_or(1, |n| n.get()).min(4);
        let mut done: Vec<(usize, Moon)> = std::thread::scope(|scope| {
            let workers: Vec<_> = (0..threads)
                .map(|_| {
                    scope.spawn(|| {
                        let mut mine = Vec::new();
                        loop {
                            let i = next.fetch_add(1, Ordering::Relaxed);
                            if i >= SEEDS {
                                return mine;
                            }
                            mine.push((i, assess(&scene, &times, i, draws[i])));
                        }
                    })
                })
                .collect();
            workers.into_iter().flat_map(|w| w.join().expect("a moon's reference panicked")).collect()
        });
        done.sort_by_key(|d| d.0);
        done.into_iter().map(|d| d.1).collect()
    })
}

pub fn b14(law: &dyn Law) -> Gate {
    let _quiet = super::scale::QUIET.read().unwrap_or_else(|e| e.into_inner());
    let scene = JUPITER;
    let times = times(&scene);
    let (mut judged, mut agree, mut escapes) = (0, 0, 0);
    let (mut rated, mut rate_ok, mut rate_worst) = (0, 0, 0.0f64);
    for m in moons() {
        let Truth::Class(class) = m.truth else { continue };
        judged += 1;
        escapes += class as usize;
        let states = law.restricted(&scene, m.ship, &times).filter(|s| s.len() == times.len());
        agree += states.as_ref().is_some_and(|s| escaped(&scene, &times, s) == class) as usize;
        if let Some(rate) = m.rate {
            rated += 1;
            let err = states.as_ref().and_then(|s| apsidal_rate(&scene, &times, s)).map_or(f64::INFINITY, |r| (r - rate).abs() / rate.abs());
            rate_ok += (err <= APSIDES_TOL) as usize;
            rate_worst = if rate_worst.is_nan() || err.is_nan() { f64::NAN } else { rate_worst.max(err) };
        }
    }
    let count = |t: Truth| moons().iter().filter(|m| m.truth == t).count();
    let (chaotic, unconverged) = (count(Truth::Chaotic), count(Truth::Unconverged));
    let bound = judged - escapes;
    let pass = judged >= JUDGED_MIN
        && agree * 100 >= 99 * judged
        && unconverged as f64 <= EXCLUDED_MAX * SEEDS as f64
        && rated >= APSIDES_MIN
        && rate_ok * 100 >= 99 * rated;
    let detail = format!(
        "Hill stability: {agree}/{judged} judged moons in the reference's class ({escapes} escape, {bound} stay); {chaotic} chaotic and {unconverged} not converged of {SEEDS} ({CIRCULAR} circular births, {ECCENTRIC} with e0 up to 0.3; needs {JUDGED_MIN} judged); apsides: {rate_ok}/{rated} bound moons with a rate within {:.0}% of the reference's, worst {rate_worst:.2e} ({} of {bound} without a stable rate; needs {APSIDES_MIN} rated)",
        APSIDES_TOL * 100.0,
        bound - rated
    );
    Gate { id: "B14", pass, detail, secs: 0.0 }
}

#[cfg(test)]
mod tests {
    use super::super::laws::{Echo, Events, Fault, Planted, Silent};
    use super::*;

    fn events(restricted: impl Fn(&Restricted, [f64; 4], &[f64]) -> Option<Vec<[f64; 4]>> + 'static) -> Events {
        Events { binary: Box::new(Some), restricted: Box::new(restricted) }
    }

    #[test]
    fn the_moon_is_on_a_circular_planetocentric_orbit_prograde_or_retrograde() {
        let s = JUPITER;
        for prograde in [true, false] {
            let a = 0.4 * s.hill();
            let w = s.relative(0.0, &moon(&s, a, 1.0, prograde));
            assert!((w[0].hypot(w[1]) / a - 1.0).abs() < 1e-12 && (w[2].hypot(w[3]) / (s.mu / a).sqrt() - 1.0).abs() < 1e-9);
            assert!((w[0] * w[2] + w[1] * w[3]).abs() < 1e-9 * a * w[2].hypot(w[3]));
            assert_eq!(w[0] * w[3] - w[1] * w[2] > 0.0, prograde);
        }
        assert_eq!(times(&s).len(), 3200);
        assert_eq!(*times(&s).last().unwrap(), 50.0 * s.period());
    }

    #[test]
    fn a_birth_is_a_kepler_orbit_about_the_planet_started_at_periapsis() {
        let s = JUPITER;
        let (a, e0, phase) = (0.5 * s.hill(), 0.3, 2.0);
        for prograde in [true, false] {
            let w = s.relative(0.0, &birth(&s, a, phase, e0, prograde));
            let (r, v2) = (w[0].hypot(w[1]), w[2] * w[2] + w[3] * w[3]);
            // Periapsis distance, and the vis-viva speed there: the energy is that of the semi-major axis a.
            assert!((r / (a * (1.0 - e0)) - 1.0).abs() < 1e-12 && (0.5 * v2 - s.mu / r + s.mu / (2.0 * a)).abs() < 1e-12 * s.mu / a, "{prograde}");
            // At periapsis the velocity is perpendicular to the radius, and the position points along `phase`.
            assert!((w[0] * w[2] + w[1] * w[3]).abs() < 1e-9 * r * v2.sqrt() && (w[1].atan2(w[0]) - phase).abs() < 1e-12);
            assert_eq!(w[0] * w[3] - w[1] * w[2] > 0.0, prograde);
        }
        assert_eq!(birth(&s, a, phase, 0.0, true), moon(&s, a, phase, true));
    }

    /// A planetocentric ellipse (semi-major axis 0.3 R_H, eccentricity e) whose periapsis advances at
    /// `rate` radians per planet period, sampled at the gate's first `n` times: barycentric states.
    fn precessing(s: &Restricted, e: f64, rate: f64, n: usize) -> (Vec<f64>, Vec<[f64; 4]>) {
        let a = 0.3 * s.hill();
        let (r, v) = (a * (1.0 - e), (s.mu * (1.0 + e) / (a * (1.0 - e))).sqrt());
        let ts: Vec<f64> = times(s)[..n].to_vec();
        let states = ts
            .iter()
            .map(|&t| {
                let (sn, c) = (rate * t / s.period()).sin_cos();
                s.barycentric(t, &[r * c, r * sn, -v * sn, v * c])
            })
            .collect();
        (ts, states)
    }

    #[test]
    fn the_apsidal_rate_of_a_precessing_ellipse_is_its_slope_and_a_jump_is_not_a_rate() {
        let s = JUPITER;
        for rate in [0.07, -0.3, 2.9e-3] {
            let (ts, states) = precessing(&s, 0.4, rate, 800);
            let got = apsidal_rate(&s, &ts, &states).unwrap();
            assert!((got - rate).abs() < 1e-9 * rate.abs().max(1e-3), "rate {rate}: {got}");
        }
        // A circular orbit has no apse; a series that flips by π has no rate.
        let (ts, states) = precessing(&s, 0.0, 0.07, 100);
        assert_eq!(apsidal_rate(&s, &ts, &states), None);
        let (ts, mut states) = precessing(&s, 0.4, 0.07, 100);
        for (k, st) in states.iter_mut().enumerate().skip(50) {
            *st = s.barycentric(ts[k], &s.relative(ts[k], st).map(|x| -x));
        }
        assert_eq!(apsidal_rate(&s, &ts, &states), None);
        assert_eq!(apsidal_rate(&s, &ts[..2], &[[f64::NAN; 4]; 2]), None);
    }

    #[test]
    fn the_reference_finds_the_known_stability_edges() {
        // Hamilton and Burns (1991): prograde moons are lost beyond about half a Hill radius, retrograde
        // ones last to about 0.9. Every judged circular birth must respect the edges with a margin; chaos is between.
        let mut judged = 0;
        for (i, ((a, _), m)) in sample::moons(CIRCULAR).into_iter().zip(moons()).enumerate() {
            let Truth::Class(escapes) = m.truth else { continue };
            judged += 1;
            let prograde = i % 2 == 0;
            if prograde && a < 0.35 {
                assert!(!escapes, "prograde a = {a} should stay");
            }
            if prograde && a > 0.55 {
                assert!(escapes, "prograde a = {a} should escape");
            }
            if !prograde && a < 0.75 {
                assert!(!escapes, "retrograde a = {a} should stay");
            }
        }
        assert!(judged >= JUDGED_MIN);
    }

    #[test]
    fn the_eccentric_births_carry_the_apsides_and_a_circular_birth_has_none() {
        let all = moons();
        assert_eq!(all.len(), SEEDS);
        let (circular, eccentric) = all.split_at(CIRCULAR);
        let rated = |ms: &[Moon]| ms.iter().filter(|m| m.rate.is_some()).count();
        let bound = |ms: &[Moon]| ms.iter().filter(|m| m.truth == Truth::Class(false)).count();
        // A moon born circular has e near 0 at the start, so its apse jumps: none of them is rated.
        assert_eq!((bound(circular) >= 70, rated(circular)), (true, 0));
        // The eccentric births have apses: two thirds of the bound ones are rated, and that is what the gate is asked on.
        assert!(bound(eccentric) >= 70 && rated(eccentric) * 3 >= bound(eccentric) * 2, "eccentric: {} rated of {} bound", rated(eccentric), bound(eccentric));
        assert!(rated(all) >= 3 * APSIDES_MIN / 2, "{} rated against a floor of {APSIDES_MIN}", rated(all));
    }

    #[test]
    fn a_law_that_never_escapes_or_always_escapes_or_cannot_answer_fails() {
        // Bound forever: the state it started with relative to the planet, carried along with the planet.
        let stays = events(|scene, ship, times| Some(times.iter().map(|&t| scene.barycentric(t, &scene.relative(0.0, &ship))).collect()));
        // Lost at once: 2 Hill radii from the planet at every time.
        let leaves = events(|scene, _, times| Some(times.iter().map(|&t| scene.barycentric(t, &[2.0 * scene.hill(), 0.0, 0.0, 0.0])).collect()));
        for law in [&stays, &leaves] {
            let g = b14(law);
            assert!(!g.pass && g.detail.contains("judged moons"), "{}", g.detail);
        }
        assert!(!b14(&Silent).pass);
        assert!(!b14(&events(|_, _, times| Some(times[1..].iter().map(|_| [0.0; 4]).collect()))).pass);
    }

    #[test]
    fn a_law_with_the_right_classes_and_apsides_twenty_percent_too_fast_fails_on_the_apsides_alone() {
        let g = b14(&Planted(Fault::Apsides));
        let classes: Vec<usize> = g.detail.split("Hill stability: ").nth(1).unwrap().split(['/', ' ']).take(2).map(|x| x.parse().unwrap()).collect();
        assert!(!g.pass && classes[0] == classes[1], "every class right: {}", g.detail);
        assert!(g.detail.contains("apsides: 0/"), "{}", g.detail);
        // And echo, which is the reference, has them all.
        let g = b14(&Echo);
        assert!(g.pass && g.detail.contains("worst "), "{}", g.detail);
    }

    #[test]
    fn escape_is_any_sample_beyond_one_and_a_half_hill_radii_and_junk_counts_as_escape() {
        let s = JUPITER;
        let at = |d: f64| [s.barycentric(0.0, &[d, 0.0, 0.0, 0.0])];
        assert!(!escaped(&s, &[0.0], &at(1.4999 * s.hill())));
        assert!(escaped(&s, &[0.0], &at(1.5001 * s.hill())));
        assert!(escaped(&s, &[0.0], &[[f64::NAN; 4]]));
    }
}
