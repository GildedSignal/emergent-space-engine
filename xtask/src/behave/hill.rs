//! B14 Hill stability (docs/law.md; principle 20: behaviours over many seeds). A moon at 0.2 to 0.9
//! Hill radii from the planet is either bound for 50 planet orbits or it escapes, and which one
//! depends on the tide: prograde moons past about half a Hill radius are lost, retrograde ones
//! last to nearly one. A law that mishandles the star's tide inside the doll gets the classes wrong.
//!
//! - Seeds: 128 moons on circular planetocentric orbits, a uniform in [0.2, 0.9]·R_H, prograde for
//!   even seeds and retrograde for odd, phase uniform. The moon's speed is √(μ/a) added to the planet's.
//! - Run 50 planet periods, sampled every P/64 for the law and the reference alike. Escaped iff
//!   the distance from the planet exceeds 1.5·R_H at any sample.
//! - Judged: the reference is converged (the class is the same at tolerance 1e-13) and its class
//!   is unchanged when a is multiplied by (1 + 1e-6). The rest are chaotic, and are not asked.
//!   More than 10% of the seeds not converged fails the gate.
//! - PASS iff at least 64 seeds are judged and at least 99% of them have the reference's class.
use super::restricted::{Integrator, Model, Restricted, JUPITER, RTOL, RTOL_FINE};
use super::{sample, Gate, Law};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::OnceLock;

pub const SEEDS: usize = 128;
pub const PERIODS: usize = 50;
pub const SAMPLES_PER_PERIOD: usize = 64;
/// Escaped: farther than this many Hill radii from the planet at a sample.
pub const ESCAPE_HILL: f64 = 1.5;
/// The perturbation of a that the class must survive, relative.
pub const NUDGE: f64 = 1e-6;
pub const JUDGED_MIN: usize = 64;
pub const EXCLUDED_MAX: f64 = 0.1;

/// The moon on a circular orbit of radius `a` (units of M) about the
/// planet, at `phase`, prograde or retrograde, with the planet's velocity added.
pub fn moon(scene: &Restricted, a: f64, phase: f64, prograde: bool) -> [f64; 4] {
    let (s, c) = phase.sin_cos();
    let v = (scene.mu / a).sqrt() * if prograde { 1.0 } else { -1.0 };
    scene.barycentric(0.0, &[a * c, a * s, -v * s, v * c])
}

/// The sample times: every P/64 for 50 periods.
pub fn times(scene: &Restricted) -> Vec<f64> {
    (1..=PERIODS * SAMPLES_PER_PERIOD).map(|j| j as f64 * scene.period() / SAMPLES_PER_PERIOD as f64).collect()
}

/// Did any of the states, at `times`, leave the 1.5 R_H sphere about the planet?
fn escaped(scene: &Restricted, times: &[f64], states: &[[f64; 4]]) -> bool {
    times.iter().zip(states).any(|(&t, s)| !(scene.planet_distance(t, s) <= ESCAPE_HILL * scene.hill()))
}

/// The reference's class for `ship` to tolerance `rtol`, stopping at the first escape. None: gave up.
fn reference_escapes(scene: &Restricted, times: &[f64], ship: [f64; 4], rtol: f64) -> Option<bool> {
    let mut it = Integrator::new(scene, Model::Full, rtol, ship);
    for &t in times {
        let state = it.advance(t)?;
        if escaped(scene, &[t], &[state]) {
            return Some(true);
        }
    }
    Some(false)
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

/// The reference's verdict on moon `i` of the draws: the ship and what the reference makes of it.
fn assess(scene: &Restricted, times: &[f64], i: usize, (a_hill, phase): (f64, f64)) -> ([f64; 4], Truth) {
    let (a, prograde) = (a_hill * scene.hill(), i % 2 == 0);
    let ship = moon(scene, a, phase, prograde);
    let class = reference_escapes(scene, times, ship, RTOL);
    let truth = match class {
        None => Truth::Unconverged,
        Some(_) if class != reference_escapes(scene, times, ship, RTOL_FINE) => Truth::Unconverged,
        Some(_) if class != reference_escapes(scene, times, moon(scene, a * (1.0 + NUDGE), phase, prograde), RTOL) => Truth::Chaotic,
        Some(c) => Truth::Class(c),
    };
    (ship, truth)
}

/// The moons, with the reference's verdict on each. None of this depends on the law, so it is
/// computed once per process, on up to four threads (each moon is independent of the others, so
/// the answer does not depend on the schedule).
pub fn moons() -> &'static Vec<([f64; 4], Truth)> {
    static MOONS: OnceLock<Vec<([f64; 4], Truth)>> = OnceLock::new();
    MOONS.get_or_init(|| {
        let scene = JUPITER;
        let (times, draws, next) = (times(&scene), sample::moons(SEEDS), AtomicUsize::new(0));
        let threads = std::thread::available_parallelism().map_or(1, |n| n.get()).min(4);
        let mut done: Vec<(usize, ([f64; 4], Truth))> = std::thread::scope(|scope| {
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
    for (ship, truth) in moons() {
        let Truth::Class(class) = *truth else { continue };
        judged += 1;
        escapes += class as usize;
        agree += law.restricted(&scene, *ship, &times).is_some_and(|s| s.len() == times.len() && escaped(&scene, &times, &s) == class) as usize;
    }
    let count = |t: Truth| moons().iter().filter(|m| m.1 == t).count();
    let (chaotic, unconverged) = (count(Truth::Chaotic), count(Truth::Unconverged));
    let pass = judged >= JUDGED_MIN && agree * 100 >= 99 * judged && unconverged as f64 <= EXCLUDED_MAX * SEEDS as f64;
    let detail = format!(
        "Hill stability: {agree}/{judged} judged moons in the reference's class ({escapes} escape, {} stay); {chaotic} chaotic and {unconverged} not converged of {SEEDS} (needs {JUDGED_MIN} judged)",
        judged - escapes
    );
    Gate { id: "B14", pass, detail, secs: 0.0 }
}

#[cfg(test)]
mod tests {
    use super::super::laws::{Events, Silent};
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
    fn the_reference_finds_the_known_stability_edges() {
        // Hamilton and Burns (1991): prograde moons are lost beyond about half a Hill radius, retrograde
        // ones last to about 0.9. Every judged seed must respect the edges with a margin; chaos is between.
        let mut judged = 0;
        for (i, ((a, _), (_, truth))) in sample::moons(SEEDS).into_iter().zip(moons()).enumerate() {
            let Truth::Class(escapes) = *truth else { continue };
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
    fn escape_is_any_sample_beyond_one_and_a_half_hill_radii_and_junk_counts_as_escape() {
        let s = JUPITER;
        let at = |d: f64| [s.barycentric(0.0, &[d, 0.0, 0.0, 0.0])];
        assert!(!escaped(&s, &[0.0], &at(1.4999 * s.hill())));
        assert!(escaped(&s, &[0.0], &at(1.5001 * s.hill())));
        assert!(escaped(&s, &[0.0], &[[f64::NAN; 4]]));
    }
}
