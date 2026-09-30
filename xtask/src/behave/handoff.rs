//! B12 handoffs (docs/law.md; principle 13: errors never compound). A ship crosses the edge of a
//! planet's doll (its sphere of influence) again and again, and each crossing is a handoff between
//! two frames. The circular restricted three-body problem has an exact invariant, the Jacobi
//! constant, so the judge reads the law's handoff error from it: a law that hands off without
//! conserving it drifts, and the drift's growth exponent is the error type (0: bounded).
//!
//! - Seeds: a ship on a circular barycentric orbit of radius sep·(1 ± x), x = (R_H/sep)·U[1.5, 3],
//!   started at an angle from the planet in [30°, 330°], run for 200 planet periods.
//! - Kept: only ships that the judge's reference sees cross the R_SOI sphere (going in or out)
//!   at least 20 times, counted from P/256 samples, and whose reference is converged: its Jacobi
//!   constant at the law's samples agrees between the tolerances 1e-12 and 1e-13 to 1e-9 relative.
//!   Candidates are drawn in order until 16 are kept or 256 are tried; fewer than 16 fail the gate.
//!   Ships that cross enough but are not converged are excluded and counted.
//! - Frozen: the search is deterministic but chaotic, so its answer moves with the last bit of
//!   the arithmetic (one ship in 40 of a rerun changes). The 16 kept candidates are therefore
//!   frozen in `sample::HANDOFF_KEPT`, found by [`search`] (the ignored test re-derives them), and
//!   the gate does not count crossings again: it checks that the reference is still converged on
//!   them (more than 10% of the ships not converged fails the gate) and reports this run's counts.
//! - The law is asked for the ship's states every P/8. Per ship, err(t) = |C_J(t) − C_J(0)|/|C_J(0)|
//!   at those samples and its growth exponent is `fit::growth_exponent(err)`.
//! - PASS iff the median ship's exponent is at most 0.2 and every ship's largest err is at most 1e-4.
use super::restricted::{self, Integrator, Model, Restricted, JUPITER, RTOL, RTOL_FINE};
use super::{fit, sample, Gate, Law, GROWTH_MAX};
use std::sync::OnceLock;

pub const PERIODS: usize = 200;
/// Law samples per period, and the finer samples the crossings are counted on.
pub const COARSE: usize = 8;
pub const FINE: usize = 256;
pub const CANDIDATES: usize = 256;
pub const KEEP: usize = 16;
pub const CROSSINGS_MIN: usize = 20;
pub const ERR_MAX: f64 = 1e-4;
/// The reference's Jacobi constant must agree between its two tolerances to this, relative.
pub const CONVERGED: f64 = 1e-9;
/// The share of kept ships that may be excluded.
pub const EXCLUDED_MAX: f64 = 0.1;

/// A ship on the circular barycentric orbit of radius sep·(1 + side·x), x = (R_H/sep)·k, at angle
/// `alpha` from the planet, moving counter-clockwise at the circular speed r^(−1/2).
pub fn ship(scene: &Restricted, side: f64, k: f64, alpha: f64) -> [f64; 4] {
    let r = scene.sep * (1.0 + side * scene.hill() / scene.sep * k);
    let v = r.powf(-0.5);
    [r * alpha.cos(), r * alpha.sin(), -v * alpha.sin(), v * alpha.cos()]
}

/// The times of the law's samples: t = 0 and then every P/`COARSE` up to `PERIODS` periods.
pub fn coarse_times(scene: &Restricted) -> Vec<f64> {
    (0..=PERIODS * COARSE).map(|j| j as f64 * scene.period() / COARSE as f64).collect()
}

/// A frozen ship as this run's reference sees it: its state, how often the reference crossed
/// R_SOI, and whether the reference is converged on it.
pub struct Kept {
    pub ship: [f64; 4],
    pub crossings: usize,
    pub converged: bool,
}

/// The judge's reference on `ship` to tolerance `rtol`: the crossings of R_SOI counted at the fine
/// samples, and the Jacobi constant at the coarse ones. None: the integration gave up.
fn watch(scene: &Restricted, ship: [f64; 4], rtol: f64) -> Option<(usize, Vec<f64>)> {
    let mut it = Integrator::new(scene, Model::Full, rtol, ship);
    let (mut inside, mut crossings, mut jacobi) = (None, 0, Vec::new());
    for j in 0..=PERIODS * FINE {
        let t = j as f64 * scene.period() / FINE as f64;
        let state = it.advance(t)?;
        let now = scene.planet_distance(t, &state) < scene.soi();
        crossings += inside.is_some_and(|before| before != now) as usize;
        inside = Some(now);
        if j % (FINE / COARSE) == 0 {
            jacobi.push(scene.jacobi(t, &state));
        }
    }
    Some((crossings, jacobi))
}

/// The reference's crossings of R_SOI on `ship`, and whether it is converged (None: it gave up).
fn assess(scene: &Restricted, ship: [f64; 4]) -> Option<(usize, bool)> {
    let times = coarse_times(scene);
    let (crossings, reference) = watch(scene, ship, RTOL)?;
    let c0 = scene.jacobi(0.0, &ship);
    let finer = restricted::reference(scene, ship, &times, RTOL_FINE);
    Some((crossings, finer.is_some_and(|f| f.iter().zip(&times).zip(&reference).all(|((s, &t), &c)| ((scene.jacobi(t, s) - c) / c0).abs() <= CONVERGED))))
}

/// The search of the contract, run once to freeze `sample::HANDOFF_KEPT`: the indices of the
/// first 16 candidates that cross R_SOI at least 20 times with a converged reference, how many
/// candidates it drew, and how many crossed enough but were not converged (excluded).
pub fn search() -> (Vec<usize>, usize, usize) {
    let scene = JUPITER;
    let (mut kept, mut tried, mut excluded) = (Vec::new(), 0, 0);
    for (i, (side, k, alpha)) in sample::handoffs(CANDIDATES).into_iter().enumerate() {
        if kept.len() == KEEP {
            break;
        }
        tried += 1;
        match assess(&scene, ship(&scene, side, k, alpha)) {
            Some((c, true)) if c >= CROSSINGS_MIN => kept.push(i),
            Some((c, false)) if c >= CROSSINGS_MIN => excluded += 1,
            _ => {}
        }
    }
    (kept, tried, excluded)
}

/// The frozen ships, each assessed by this run's reference. None of this depends on the law, so
/// it is computed once per process.
pub fn kept() -> &'static Vec<Kept> {
    static KEPT: OnceLock<Vec<Kept>> = OnceLock::new();
    KEPT.get_or_init(|| {
        let scene = JUPITER;
        let draws = sample::handoffs(sample::HANDOFF_KEPT.iter().max().map_or(0, |m| m + 1));
        sample::HANDOFF_KEPT
            .iter()
            .map(|&i| {
                let ship = ship(&scene, draws[i].0, draws[i].1, draws[i].2);
                let (crossings, converged) = assess(&scene, ship).unwrap_or((0, false));
                Kept { ship, crossings, converged }
            })
            .collect()
    })
}

/// The median of `xs`, NaN counted as infinity so that it fails; the mean of the middle two.
fn median(mut xs: Vec<f64>) -> f64 {
    xs.iter_mut().for_each(|x| *x = if x.is_nan() { f64::INFINITY } else { *x });
    xs.sort_by(f64::total_cmp);
    match xs.len() {
        0 => f64::INFINITY,
        n if n % 2 == 1 => xs[n / 2],
        n => 0.5 * (xs[n / 2 - 1] + xs[n / 2]),
    }
}

/// The law's err series on one ship (infinite where it cannot answer), from its states at `times`.
fn err_series(scene: &Restricted, law: &dyn Law, ship: [f64; 4], times: &[f64]) -> Vec<f64> {
    let c0 = scene.jacobi(0.0, &ship);
    match law.restricted(scene, ship, times) {
        Some(states) if states.len() == times.len() => states.iter().zip(times).map(|(s, &t)| ((scene.jacobi(t, s) - c0) / c0).abs()).collect(),
        _ => vec![f64::INFINITY; times.len()],
    }
}

pub fn b12(law: &dyn Law) -> Gate {
    let scene = JUPITER;
    let kept = kept();
    let times = coarse_times(&scene);
    let (mut exponents, mut worst_err) = (Vec::new(), 0.0f64);
    for k in kept.iter().filter(|k| k.converged) {
        let err = err_series(&scene, law, k.ship, &times);
        exponents.push(fit::growth_exponent(&err));
        worst_err = err.iter().fold(worst_err, |m, e| if m.is_nan() || e.is_nan() { f64::NAN } else { m.max(*e) });
    }
    let excluded = kept.len() - exponents.len();
    let (median_exp, worst_exp) = (median(exponents.clone()), exponents.iter().fold(f64::NEG_INFINITY, |m, &e| if e.is_nan() { f64::INFINITY } else { m.max(e) }));
    let pass = kept.len() >= KEEP && excluded as f64 <= EXCLUDED_MAX * kept.len() as f64 && median_exp <= GROWTH_MAX && worst_err <= ERR_MAX;
    let crossings = |f: fn(usize, usize) -> usize| kept.iter().map(|k| k.crossings).reduce(f).unwrap_or(0);
    let detail = format!(
        "handoffs: {} frozen ships (this run's reference crosses R_SOI {}..{} times, at least {CROSSINGS_MIN} when frozen), {excluded} not converged; median growth exponent {median_exp:.3} (limit {GROWTH_MAX}), worst {worst_exp:.3}; worst err {worst_err:.2e} (limit {ERR_MAX:.0e})",
        kept.len(),
        crossings(usize::min),
        crossings(usize::max)
    );
    Gate { id: "B12", pass, detail, secs: 0.0 }
}

#[cfg(test)]
mod tests {
    use super::super::laws::{Echo, Events, Fault, Planted, Silent};
    use super::*;

    fn events(restricted: impl Fn(&Restricted, [f64; 4], &[f64]) -> Option<Vec<[f64; 4]>> + 'static) -> Events {
        Events { binary: Box::new(Some), restricted: Box::new(restricted) }
    }

    #[test]
    fn the_ship_is_on_a_circular_barycentric_orbit_at_the_drawn_distance() {
        let s = JUPITER;
        for (side, k, alpha) in sample::handoffs(8) {
            let st = ship(&s, side, k, alpha);
            let r = st[0].hypot(st[1]);
            let x = (r / s.sep - 1.0).abs();
            assert!((x / (s.hill() / s.sep * k) - 1.0).abs() < 1e-12 && (r > s.sep) == (side > 0.0));
            assert!((st[2].hypot(st[3]) * r.sqrt() - 1.0).abs() < 1e-12 && (st[0] * st[2] + st[1] * st[3]).abs() < 1e-12 * r * st[2].hypot(st[3]));
            assert!(((st[1].atan2(st[0]) - alpha).rem_euclid(std::f64::consts::TAU)).min(std::f64::consts::TAU - (st[1].atan2(st[0]) - alpha).rem_euclid(std::f64::consts::TAU)) < 1e-12);
        }
    }

    #[test]
    fn the_frozen_list_is_sixteen_distinct_ascending_candidates_and_the_ships_cross_and_converge() {
        let list = sample::HANDOFF_KEPT;
        assert!(list.len() == KEEP && list.windows(2).all(|w| w[0] < w[1]) && list[KEEP - 1] < CANDIDATES);
        let kept = kept();
        // The counts move with the last bit of the arithmetic (chaos): all that is asked here is that
        // the ships are still busy, and that the reference is still converged on almost all of them.
        assert!(kept.iter().all(|k| k.crossings >= CROSSINGS_MIN / 2), "{:?}", kept.iter().map(|k| k.crossings).collect::<Vec<_>>());
        assert!(kept.iter().filter(|k| k.converged).count() * 10 >= 9 * KEEP);
    }

    #[test]
    #[ignore = "re-derives the frozen ships (about 3 s); run it, and update sample::HANDOFF_KEPT, when the reference changes"]
    fn the_frozen_ships_are_what_the_search_finds() {
        let (found, tried, excluded) = search();
        println!("HANDOFF_KEPT = {found:?}; {tried} candidates drawn, {excluded} not converged");
        assert_eq!(found, sample::HANDOFF_KEPT);
    }

    #[test]
    fn the_reference_without_the_conservation_drifts_but_stays_far_inside_the_bound() {
        // Float64's own drift is about 1e-10 here: the gate fails such a law on the exponent alone
        // (planted-drift, in the events tests), so the ships must show it, and echo must not.
        let (scene, times) = (JUPITER, coarse_times(&JUPITER));
        for k in kept().iter().filter(|k| k.converged) {
            let raw = err_series(&scene, &Planted(Fault::Drift), k.ship, &times);
            let held = err_series(&scene, &Echo, k.ship, &times);
            assert!(raw.iter().all(|&e| e < 1e-8) && held.iter().all(|&e| e < 1e-13), "raw {:e} held {:e}", raw.iter().cloned().fold(0.0, f64::max), held.iter().cloned().fold(0.0, f64::max));
            assert!(raw.iter().cloned().fold(0.0, f64::max) > 100.0 * held.iter().cloned().fold(0.0, f64::max));
        }
    }

    #[test]
    fn a_law_that_cannot_answer_or_answers_short_or_junk_fails() {
        assert!(!b12(&Silent).pass);
        assert!(!b12(&events(|scene, ship, times| {
            let mut s = Echo.restricted(scene, ship, times)?;
            s.pop();
            Some(s)
        }))
        .pass);
        assert!(!b12(&events(|_, _, times| Some(times.iter().map(|_| [f64::NAN; 4]).collect()))).pass);
    }

    #[test]
    fn a_slow_leak_far_inside_the_bound_fails_on_the_exponent() {
        // Speeds grow by 1e-12 per planet period: the Jacobi error stays under 1e-9 but rises steadily.
        let leak = events(|scene, ship, times| {
            let s = Echo.restricted(scene, ship, times)?;
            Some(s.iter().zip(times).map(|(st, &t)| [st[0], st[1], st[2] * (1.0 + 1e-12 * t / scene.period()), st[3] * (1.0 + 1e-12 * t / scene.period())]).collect())
        });
        let g = b12(&leak);
        assert!(!g.pass && !g.detail.contains("worst err 1.") && g.detail.contains("(limit 1e-4)"), "{}", g.detail);
        let (scene, times) = (JUPITER, coarse_times(&JUPITER));
        let err = err_series(&scene, &leak, kept()[0].ship, &times);
        assert!(err.iter().all(|&e| e < 1e-6) && fit::growth_exponent(&err) > 0.8, "{}", fit::growth_exponent(&err));
    }

    #[test]
    fn the_median_counts_nan_as_infinity_and_takes_the_middle_pair() {
        assert_eq!(median(vec![3.0, 1.0, 2.0]), 2.0);
        assert_eq!(median(vec![4.0, 1.0, 2.0, 3.0]), 2.5);
        assert_eq!(median(vec![f64::NAN, f64::NAN, 1.0]), f64::INFINITY);
        assert_eq!(median(vec![]), f64::INFINITY);
    }
}
