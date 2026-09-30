//! B10 cost against N (docs/law.md; principles 1, 3 and 6: the cheapest compute is compute not
//! done, and cost follows change). A frozen scene is n bodies in one doll, orbits drawn from the
//! seeds, no events beyond the orbits. The judge asks the law for the CPU seconds it spends on the
//! scene (building it and advancing it `GAME_SECONDS`) at n = 10^3 .. 10^6, fits the exponent of
//! cost against n (least squares on the log-log points), and passes iff it is at most 1.1.
//!
//! - The judge does not take the law's word for its cost: each answer is the larger of the law's
//!   claim and the judge's own wall time around the call. A law cannot hide work by under-reporting.
//! - Sizes are chosen to fit `BUDGET_S` of wall time. Before each size the judge predicts its cost
//!   from the sizes already run (at the local exponent, never below 1) and skips it if it would not
//!   fit, since a call cannot be interrupted. Fewer than 3 measured sizes fail the gate.
//! - Small costs are repeated and the median kept. Nothing else is smoothed: heat and load are part
//!   of the measurement (AGENTS.md). One untimed call at the smallest size precedes the runs.
//! - The 10^9 extrapolation is reported, not gated: core-seconds per game-second, and the real-time
//!   factor on 8 cores. Game time is in units of M/c³ (G = c = M = 1), the judge's only time unit.
use super::{sample, Gate, Law};
use std::hint::black_box;
use std::sync::{Mutex, RwLock};
use std::time::Instant;

pub const SIZES: [usize; 4] = [1_000, 10_000, 100_000, 1_000_000];
/// Game time each scene is advanced, in units of M: about 13 radial periods of the median orbit.
pub const GAME_SECONDS: f64 = 1e5;
pub const EXPONENT_MAX: f64 = 1.1;
/// Wall time the whole gate may spend (the phase is killed at 60 s).
pub const BUDGET_S: f64 = 40.0;
pub const CORES: f64 = 8.0;
pub const TARGET_N: f64 = 1e9;
const MIN_SIZES: usize = 3;

/// Timing gates in one process take turns, so parallel tests do not time each other.
static TIMING: Mutex<()> = Mutex::new(());
/// The events gates (B12-B14) hold this for reading while they compute; B10 holds it for writing
/// while it times. In one process (the tests) B10 then never times against their heavy work, which
/// would tilt its exponent. The CLI runs one gate at a time, so there it costs nothing.
pub(super) static QUIET: RwLock<()> = RwLock::new(());

/// `echo`'s frozen scene: the seed-sampled orbits, then zero work per orbit until an event. The
/// only cost is to exist: O(n).
pub fn echo_scene_cost(n: usize, _game_seconds: f64) -> Option<f64> {
    let t = Instant::now();
    let scene = sample::bound_orbits(n);
    black_box(&scene);
    Some(t.elapsed().as_secs_f64())
}

/// The planted flaw of B10: every orbit meets every other orbit (all pairs, no cells and no
/// aggregates). O(n²).
pub fn quadratic_scene_cost(n: usize, _game_seconds: f64) -> Option<f64> {
    let t = Instant::now();
    let keys: Vec<u64> = sample::bound_orbits(n).iter().map(|&(p, e)| p.to_bits() ^ e.to_bits().rotate_left(17)).collect();
    let mut acc = 0u64;
    for &a in &keys {
        for &b in &keys {
            acc = acc.wrapping_add((a ^ b).rotate_left(7));
        }
    }
    black_box(acc);
    Some(t.elapsed().as_secs_f64())
}

/// One run at size n: (cost, whether the law claimed under half the judge's wall time). The cost is
/// the larger of the claim and the wall. None if the law cannot answer or answers junk.
fn run_once(law: &dyn Law, n: usize) -> Option<(f64, bool)> {
    let t = Instant::now();
    let claim = law.scene_cost(n, GAME_SECONDS)?;
    let wall = t.elapsed().as_secs_f64();
    (claim.is_finite() && claim >= 0.0).then_some((claim.max(wall), claim < 0.5 * wall))
}

/// The exponent b and intercept a of log10 cost = a + b log10 n, by least squares.
fn fit(pts: &[(usize, f64)]) -> (f64, f64) {
    let xy: Vec<(f64, f64)> = pts.iter().map(|&(n, c)| ((n as f64).log10(), c.log10())).collect();
    let m = xy.len() as f64;
    let (mx, my) = (xy.iter().map(|p| p.0).sum::<f64>() / m, xy.iter().map(|p| p.1).sum::<f64>() / m);
    let b = xy.iter().map(|p| (p.0 - mx) * (p.1 - my)).sum::<f64>() / xy.iter().map(|p| (p.0 - mx).powi(2)).sum::<f64>();
    (b, my - b * mx)
}

fn secs(s: f64) -> String {
    match s {
        s if s < 1e-6 => format!("{:.0} ns", s * 1e9),
        s if s < 1e-3 => format!("{:.1} us", s * 1e6),
        s if s < 1.0 => format!("{:.1} ms", s * 1e3),
        s => format!("{s:.2} s"),
    }
}
fn size(n: usize) -> String {
    format!("1e{}", (n as f64).log10().round())
}

pub fn b10(law: &dyn Law) -> Gate {
    let _turn = TIMING.lock().unwrap_or_else(|e| e.into_inner());
    let _quiet = QUIET.write().unwrap_or_else(|e| e.into_inner());
    let start = Instant::now();
    let left = || BUDGET_S - start.elapsed().as_secs_f64();
    let fail = |detail: String| Gate { id: "B10", pass: false, detail, secs: 0.0 };
    let Some((warm, _)) = run_once(law, SIZES[0]) else {
        return fail(format!("cost against n: not implemented, or a NaN or negative cost at n={}", size(SIZES[0])));
    };
    let (mut pts, mut not_run, mut under, mut runs): (Vec<(usize, f64)>, Vec<(usize, f64)>, usize, usize) = (Vec::new(), Vec::new(), 0, 0);
    for (i, &n) in SIZES.iter().enumerate() {
        let predicted = match pts.as_slice() {
            [] => warm,
            [(n0, c0)] => c0 * n as f64 / *n0 as f64,
            [.., (na, ca), (nb, cb)] => {
                let local = ((cb / ca).ln() / (*nb as f64 / *na as f64).ln()).clamp(1.0, 3.0);
                cb * (n as f64 / *nb as f64).powf(local)
            }
        };
        if predicted > left() {
            not_run = SIZES[i..].iter().map(|&m| (m, predicted * (m as f64 / n as f64))).collect();
            break;
        }
        let mut reps = match predicted {
            p if p <= 0.005 => 7,
            p if p <= 0.06 => 5,
            p if p <= 1.0 => 3,
            _ => 1,
        };
        while reps > 1 && predicted * reps as f64 > left() {
            reps -= 1;
        }
        let mut costs = Vec::with_capacity(reps);
        for _ in 0..reps {
            let Some((cost, low)) = run_once(law, n) else {
                return fail(format!("cost against n: a NaN or negative cost at n={}", size(n)));
            };
            costs.push(cost);
            under += low as usize;
            runs += 1;
        }
        costs.sort_by(f64::total_cmp);
        pts.push((n, costs[costs.len() / 2]));
    }
    let listed = pts.iter().map(|&(n, c)| format!("n={} {}", size(n), secs(c))).collect::<Vec<_>>().join(", ");
    let skipped = if not_run.is_empty() {
        String::new()
    } else {
        format!("; not run for want of time: {}", not_run.iter().map(|&(n, p)| format!("n={} (predicted {})", size(n), secs(p))).collect::<Vec<_>>().join(", "))
    };
    let honest = if under > 0 { format!("; the law claimed under half the judge's wall time in {under} of {runs} runs (the wall time was used)") } else { String::new() };
    if pts.len() < MIN_SIZES {
        return fail(format!("cost against n: only {} of {} sizes fit {BUDGET_S:.0} s: {listed}{skipped}{honest}", pts.len(), SIZES.len()));
    }
    let (b, a) = fit(&pts);
    let per_game_second = 10f64.powf(a + b * TARGET_N.log10()) / GAME_SECONDS;
    let detail = format!(
        "cost against n: {listed}; exponent {b:.3} (limit {EXPONENT_MAX}); n=1e9 extrapolates to {per_game_second:.1e} core-s per game-s, real-time factor {:.1e} on {CORES:.0} cores (reported){skipped}{honest}",
        CORES / per_game_second
    );
    Gate { id: "B10", pass: b <= EXPONENT_MAX, detail, secs: 0.0 }
}

#[cfg(test)]
mod tests {
    use super::super::laws::{Echo, Fault, Planted};
    use super::*;

    /// A law that answers only the scene's cost, from a closure.
    struct Scene(Box<dyn Fn(usize) -> Option<f64>>);
    impl Law for Scene {
        fn advance_per_cycle(&self, _: f64, _: f64) -> Option<(f64, f64, f64)> {
            None
        }
        fn deflection(&self, _: f64) -> Option<f64> {
            None
        }
        fn captured(&self, _: f64, _: f64) -> bool {
            false
        }
        fn photon_captured(&self, _: f64) -> bool {
            false
        }
        fn long_run(&self, _: f64, _: f64, _: usize) -> Vec<(f64, f64, f64, f64)> {
            Vec::new()
        }
        fn scene_cost(&self, n: usize, _: f64) -> Option<f64> {
            (self.0)(n)
        }
    }
    fn scene(f: impl Fn(usize) -> Option<f64> + 'static) -> Scene {
        Scene(Box::new(f))
    }
    /// The exponent printed in a detail line.
    fn exponent(g: &Gate) -> f64 {
        g.detail.split("exponent ").nth(1).unwrap().split(' ').next().unwrap().parse().unwrap()
    }

    #[test]
    fn the_fit_recovers_exponents_and_the_extrapolation_is_arithmetic() {
        let pts: Vec<(usize, f64)> = SIZES.iter().map(|&n| (n, 2e-9 * (n as f64).powf(1.25))).collect();
        let (b, a) = fit(&pts);
        assert!((b - 1.25).abs() < 1e-9 && (10f64.powf(a) - 2e-9).abs() < 1e-15, "{b} {a}");
        // Exactly linear at 1e-7 s per body: 1e9 bodies cost 100 core-s, that is 1e-3 per game-s of 1e5,
        // and 8 cores run it at a real-time factor of 8000.
        let g = b10(&scene(|n| Some(1e-7 * n as f64)));
        assert!(g.pass && (exponent(&g) - 1.0).abs() < 1e-6, "{}", g.detail);
        assert!(g.detail.contains("1.0e-3 core-s per game-s") && g.detail.contains("real-time factor 8.0e3 on 8 cores"), "{}", g.detail);
    }

    #[test]
    fn the_limit_is_an_exponent_of_1_1() {
        for (alpha, pass) in [(0.0, true), (0.5, true), (1.0, true), (1.09, true), (1.11, false), (1.5, false), (2.0, false)] {
            let g = b10(&scene(move |n| Some(1e-9 * (n as f64).powf(alpha) + if alpha == 0.0 { 1e-5 } else { 0.0 })));
            assert_eq!(g.pass, pass, "alpha {alpha}: {}", g.detail);
        }
    }

    #[test]
    fn echo_is_linear_and_the_planted_quadratic_is_not() {
        let g = b10(&Echo);
        assert!(g.pass && !g.detail.contains("not run") && g.detail.contains("n=1e6"), "{}", g.detail);
        let q = b10(&Planted(Fault::Quadratic));
        assert!(!q.pass && exponent(&q) > 1.8, "{}", q.detail);
        // All pairs at 10^6 bodies is 10^12 pair steps: the judge predicts it and does not run it.
        assert!(q.detail.contains("not run for want of time: n=1e6"), "{}", q.detail);
    }

    #[test]
    fn a_law_too_slow_to_measure_fails_and_the_judge_never_starts_a_run_it_cannot_finish() {
        // 1 ms per body: 1 s at n = 1e3, 10 s at 1e4, and 100 s predicted at 1e5, over the 40 s budget.
        let g = b10(&scene(|n| Some(1e-3 * n as f64)));
        assert!(!g.pass && g.detail.contains("only 2 of 4 sizes") && g.detail.contains("n=1e5 (predicted 100.00 s)"), "{}", g.detail);
    }

    #[test]
    fn a_law_cannot_hide_work_by_reporting_less() {
        // It claims zero and does n^1.5 real steps: the judge's wall time exposes the exponent.
        let g = b10(&scene(|n| {
            let mut a = 0u64;
            for i in 0..((n as f64).powf(1.5) / 8.0) as u64 {
                a = a.wrapping_add(black_box(i));
            }
            black_box(a);
            Some(0.0)
        }));
        assert!(!g.pass && exponent(&g) > 1.3 && g.detail.contains("the law claimed under half the judge's wall time"), "{}", g.detail);
    }

    #[test]
    fn unimplemented_nan_and_negative_costs_fail() {
        for law in [scene(|_| None), scene(|_| Some(f64::NAN)), scene(|_| Some(-1.0)), scene(|n| if n > 1000 { None } else { Some(1e-6) })] {
            let g = b10(&law);
            assert!(!g.pass && !g.detail.contains("exponent"), "{}", g.detail);
        }
    }
}
