//! The derived-cap + horizon composite (run 20261011-0224, second author on 20261011-0134-scout-7567),
//! evaluated on the REAL frozen B12 ships with the REAL shipped planted laws. Everything under
//! `behave/` is a verbatim copy of xtask/src/behave (sha256-checked); only this file and main.rs
//! are new.
//!
//! Composite contract (from the scout run's dossier, now on the real harness):
//!   PASS iff median_i( max_h(err_i) / max_1x(err_i) ) <= 2.0    (ratio clause)
//!      and max_i max_h(err_i) <= 1.05 * CAP_i                    (cap clause)
//! with CAP_i = TOL_B * Δa_i / (R_H/sep), Δa_i the accessible semimajor-axis band of ship i's
//! C_J level set (zero-velocity curve), clipped at the law's own AXIS_CAP on the outside.
//! TOL_B is a STATED requirement (max tolerated state-only handoff error per unit of (a−a₀)/(R_H/sep)),
//! not a fitted number; sensitivity to it is reported.
//!
//! The horizon series contains the 1× samples as an exact prefix (same P/8 grid from t = 0), so
//! max_1x is the maximum of the first 1601 samples of the SAME run — the prefix property the
//! checker demanded.
use crate::behave::laws::{Echo, Fault, Planted};
use crate::behave::restricted::{Restricted, JUPITER};
use crate::behave::sample::Rng;
use crate::behave::{fit, handoff, Law};
use serde_json::json;
use std::thread;

pub const RATIO_MAX: f64 = 2.0;
pub const CAP_MARGIN: f64 = 1.05;
/// Stated requirement: the largest tolerated state-only (bounded) handoff error per unit of
/// (a − a₀)/(R_H/sep). The planted `Bounded` law's own coefficient is 1e-7; verdict sensitivity
/// to TOL_B is reported so the coefficient is an explicit input, not a hidden fit.
pub const TOL_B: f64 = 1e-7;
/// The law's own outside clip (laws.rs AXIS_CAP): an unbound state reads this semimajor axis.
const AXIS_CAP: f64 = 10.0;
/// The planted bounded coefficient (laws.rs BOUNDED), read here only to build the unshipped
/// `leak` control (bounded + scale·walk).
const BOUNDED: f64 = 1e-7;

// ---- verbatim copies of laws.rs's private machinery (star_axis, lay) for the two controls that
// ---- are not shipped (const, leak); the shipped plants are called through their real Law impls.
fn star_axis(scene: &Restricted, t: f64, s: &[f64; 4]) -> f64 {
    let (energy, _) = scene.heliocentric(t, s);
    if energy < 0.0 { ((1.0 - scene.mu) / (-2.0 * energy) / scene.sep).min(AXIS_CAP) } else { AXIS_CAP }
}

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

fn bounded_shift(scene: &Restricted, ship: [f64; 4], times: &[f64], states: &[[f64; 4]]) -> Vec<f64> {
    let (a0, c0, unit) = (star_axis(scene, 0.0, &ship), scene.jacobi(0.0, &ship).abs(), scene.hill() / scene.sep);
    times.iter().zip(states).map(|(&t, s)| BOUNDED * (star_axis(scene, t, s) - a0) / unit * c0).collect()
}

/// `plant_compound`'s walk with an explicit amplitude and RNG-variant offset: shift = scale · sum
/// of unit-variance steps per entry into 3 R_H. variant 0 with scale = BOUNDED reproduces the
/// shipped `plant_compound`'s draws.
fn walk_shift(scene: &Restricted, ship: [f64; 4], times: &[f64], states: &[[f64; 4]], scale: f64, variant: u64) -> (Vec<f64>, usize) {
    let c0 = scene.jacobi(0.0, &ship).abs();
    let mut rng = Rng(ship.iter().fold(0x5EED ^ variant, |h, x| h.rotate_left(17) ^ x.to_bits()));
    let (mut sum, mut inside, mut entries) = (0.0, false, 0usize);
    let shift = times
        .iter()
        .zip(states)
        .map(|(&t, s)| {
            let now = scene.planet_distance(t, s) < 3.0 * scene.hill();
            if now && !inside {
                sum += (rng.unit() - 0.5) * 12f64.sqrt();
                entries += 1;
            }
            inside = now;
            scale * sum * c0
        })
        .collect();
    (shift, entries)
}

/// err(t) = |C_J(t) − C_J(0)|/C_J(0) against the ship's own initial state — handoff::err_series's
/// convention (c0 from the pristine ship, not the law's first answer). Infinite where the law
/// cannot answer.
fn err_series(scene: &Restricted, law: &dyn Law, ship: [f64; 4], times: &[f64]) -> Vec<f64> {
    let c0 = scene.jacobi(0.0, &ship);
    match law.restricted(scene, ship, times) {
        Some(states) if states.len() == times.len() => {
            states.iter().zip(times).map(|(s, &t)| ((scene.jacobi(t, s) - c0) / c0).abs()).collect()
        }
        _ => vec![f64::INFINITY; times.len()],
    }
}

/// The accessible semimajor-axis band of the C_J level set. Two channels:
/// 1. Near the planet (exact, on both axes): at planet distance r₂ the speed budget is
///    V = sqrt(U_eff − C) (U_eff maximised over the two axis directions, star- and anti-star-side,
///    which bracket the extremes of the r₁ term); if the minimum-direction heliocentric energy
///    E = (V − Ω·r₁)²/2 − (1−μ)/r₁ reaches ≥ 0 at ANY accessible r₂ down to the planet's radius,
///    the level set contains unbound states and the band's top is the law's own AXIS_CAP.
///    A grid cannot see this channel: it lives within a few planet radii of the planet.
/// 2. Far from the planet (grid over the rotating-frame plane, r₂ ≥ 0.15 sep): U_eff is smooth
///    at grid scale, and per position the energy spans [(V−Ωd)²/2 − (1−μ)/r₁, (V+Ωd)²/2 − (1−μ)/r₁]
///    (v_rot's direction free, d = |r − r_star|); a = (1−μ)/(−2E) for E < 0, else AXIS_CAP.
fn level_set_band(scene: &Restricted, c: f64, n: usize) -> (f64, f64) {
    let (mu, sep, omega) = (scene.mu, scene.sep, scene.omega());
    let a_of = |e: f64| if e < 0.0 { ((1.0 - mu) / (-2.0 * e) / sep).min(AXIS_CAP) } else { AXIS_CAP };
    // Channel 1: the near-planet axes, r₂ from the planet's radius to 0.3 sep, log-spaced.
    let (mut a_lo, mut a_hi) = (f64::INFINITY, 0.0f64);
    let (r_start, r_end, steps) = (scene.planet_radius, 0.3 * sep, 4000);
    for k in 0..=steps {
        let r2 = r_start * (r_end / r_start).powf(k as f64 / steps as f64);
        for side in [1.0f64, -1.0] {
            let r1 = sep - side * r2; // star side (side=1): r1 = sep − r2; anti-star: r1 = sep + r2
            let (x, y) = (side * r2, 0.0);
            let r_bary = ((x - sep * mu) * (x - sep * mu) + y * y).sqrt().max(1.0);
            let u_eff = omega * omega * r_bary * r_bary + 2.0 * (1.0 - mu) / r1 + 2.0 * mu / r2;
            if u_eff >= c {
                let v = (u_eff - c).sqrt();
                let e_min_dir = (v - omega * r1) * (v - omega * r1) / 2.0 - (1.0 - mu) / r1;
                if e_min_dir >= 0.0 {
                    return (0.0, AXIS_CAP); // the unbound channel is open: the full clip band
                }
            }
        }
    }
    // Channel 2: the far-field grid (r₂ ≥ 0.15 sep for the top side; near-planet states never
    // lower the bottom side because their energies run positive).
    let (sx, sy) = (-sep * mu, 0.0); // the star, in the rotating frame
    for i in 0..n {
        let x = (-1.25 + 2.5 * i as f64 / (n - 1) as f64) * sep;
        for j in 0..n {
            let y = (-1.25 + 2.5 * j as f64 / (n - 1) as f64) * sep;
            let (r1x, r1y) = (x - sx, y - sy);
            let (r2x, r2y) = (x - sep * (1.0 - mu), y);
            let (r1, r2) = ((r1x * r1x + r1y * r1y).sqrt(), (r2x * r2x + r2y * r2y).sqrt());
            let u_eff = omega * omega * (x * x + y * y) + 2.0 * (1.0 - mu) / r1 + 2.0 * mu / r2;
            if u_eff >= c {
                let v = (u_eff - c).sqrt();
                let (od, pot) = (omega * r1, (1.0 - mu) / r1);
                if r2 >= 0.15 * sep {
                    a_hi = a_hi.max(a_of((v - od) * (v - od) / 2.0 - pot));
                }
                a_lo = a_lo.min(a_of((v + od) * (v + od) / 2.0 - pot));
            }
        }
    }
    (a_lo, a_hi)
}

/// Brute-force check of the band: stratified random states exactly on the level set (rejection:
/// uniform position over the plane or near the planet/star, velocity uniform on the disc of
/// radius sqrt(U_eff − C) in the rotating frame), their osculating a via the real heliocentric
/// energy. Returns (n_states, min_a, max_a): the band must contain [min_a, max_a].
fn band_check(scene: &Restricted, c: f64, seed: u64, n: usize) -> (usize, f64, f64) {
    let (mu, sep, omega) = (scene.mu, scene.sep, scene.omega());
    let mut rng = Rng(seed);
    let (mut lo, mut hi, mut count) = (f64::INFINITY, 0.0f64, 0usize);
    let mut tries = 0;
    while count < n && tries < n * 4000 {
        tries += 1;
        let (x, y) = match count % 3 {
            0 => ((rng.unit() * 2.5 - 1.25) * sep, (rng.unit() * 2.5 - 1.25) * sep),
            1 => {
                let (r, th) = (scene.planet_radius * (1000.0f64).powf(rng.unit()), rng.unit() * std::f64::consts::TAU);
                (sep * (1.0 - mu) + r * th.cos(), r * th.sin())
            }
            _ => {
                let (r, th) = (0.02 * sep * (80.0f64).powf(rng.unit()), rng.unit() * std::f64::consts::TAU);
                (-sep * mu + r * th.cos(), r * th.sin())
            }
        };
        let (r1x, r1y, r2x, r2y) = (x + sep * mu, y, x - sep * (1.0 - mu), y);
        let (r1, r2) = ((r1x * r1x + r1y * r1y).sqrt(), (r2x * r2x + r2y * r2y).sqrt());
        let u_eff = omega * omega * (x * x + y * y) + 2.0 * (1.0 - mu) / r1 + 2.0 * mu / r2;
        if u_eff < c {
            continue;
        }
        let v = (u_eff - c).sqrt() * rng.unit().sqrt();
        let th = rng.unit() * std::f64::consts::TAU;
        let (vrx, vry) = (v * th.cos(), v * th.sin());
        // Barycentric inertial velocity: v_rot + Ω×r. The star's: Ω×r_star. Difference via heliocentric().
        let (vx, vy) = (vrx - omega * y, vry + omega * x);
        let (star_p, star_v) = scene.star(0.0);
        let (dx, dy, dvx, dvy) = (x - star_p[0], y - star_p[1], vx - star_v[0], vy - star_v[1]);
        let energy = 0.5 * (dvx * dvx + dvy * dvy) - (1.0 - mu) / (dx * dx + dy * dy).sqrt();
        let a = if energy < 0.0 { ((1.0 - mu) / (-2.0 * energy) / sep).min(AXIS_CAP) } else { AXIS_CAP };
        lo = lo.min(a);
        hi = hi.max(a);
        count += 1;
    }
    (count, lo, hi)
}

fn median(xs: &mut Vec<f64>) -> f64 {
    xs.iter_mut().for_each(|x| *x = if x.is_nan() { f64::INFINITY } else { *x });
    xs.sort_by(f64::total_cmp);
    let n = xs.len();
    if n % 2 == 1 { xs[n / 2] } else { 0.5 * (xs[n / 2 - 1] + xs[n / 2]) }
}

/// One leak control: (amplitude, rng variant).
pub type Leak = (f64, u64);
/// One ship's record: err series maxima at 1× (prefix) and the full horizon, per law.
/// `judged` mirrors handoff's private Kept::judged: converged and closest >= planet radius.
struct ShipOut {
    idx: usize,
    crossings: usize,
    closest_r: f64,
    judged: bool,
    c_j: f64,
    a0: f64,
    band: (f64, f64),
    band_check: (usize, f64, f64),
    cap: f64,
    entries_3rh: usize,
    laws: Vec<(String, f64, f64, Option<f64>)>, // (name, max_1x, max_h, exp_1x)
}

fn one_ship(k: &'static handoff::Kept, idx: usize, horizon_periods: usize, n_grid: usize, leaks: &[Leak]) -> ShipOut {
    let scene = &JUPITER;
    let ship = k.ship;
    let times: Vec<f64> = (0..=horizon_periods * handoff::COARSE)
        .map(|j| j as f64 * scene.period() / handoff::COARSE as f64)
        .collect();
    let n1 = handoff::PERIODS * handoff::COARSE + 1;
    let c0 = scene.jacobi(0.0, &ship);
    let a0 = star_axis(scene, 0.0, &ship);
    let band = level_set_band(scene, c0, n_grid);
    let bcheck = band_check(scene, c0, 0xB00_1EAF + idx as u64, 4000);
    let unit = scene.hill() / scene.sep;
    let cap = TOL_B * (band.1 - a0).max(a0 - band.0) / unit;
    let mut laws: Vec<(String, f64, f64, Option<f64>)> = Vec::new();
    let mut push = |name: &str, err: &Vec<f64>| {
        let max1 = err[..n1.min(err.len())].iter().fold(0.0f64, |m, e| m.max(*e));
        let maxh = err.iter().fold(0.0f64, |m, e| m.max(*e));
        let exp = if max1 > handoff::FLOOR { Some(fit::growth_exponent(&err[..n1.min(err.len())])) } else { None };
        laws.push((name.to_string(), max1, maxh, exp));
    };
    // The real shipped laws, through their real Law impls.
    for (name, law) in [
        ("echo", &Echo as &dyn Law),
        ("bounded", &Planted(Fault::Bounded) as &dyn Law),
        ("compound", &Planted(Fault::Compound) as &dyn Law),
        ("drift", &Planted(Fault::Drift) as &dyn Law),
        ("kick", &Planted(Fault::Kick) as &dyn Law),
    ] {
        push(name, &err_series(scene, law, ship, &times));
    }
    // The two unshipped controls, on the real echo states with the copied plant machinery.
    let echo_states = Echo.restricted(scene, ship, &times).unwrap_or_default();
    let c0abs = c0.abs();
    let const_states = lay(scene, echo_states.clone(), &vec![3e-8 * c0abs; times.len()]);
    let const_err: Vec<f64> = const_states.iter().zip(&times).map(|(s, &t)| ((scene.jacobi(t, s) - c0) / c0).abs()).collect();
    push("const", &const_err);
    let mut entries = 0usize;
    for &(e, variant) in leaks {
        let (mut shift, ent) = walk_shift(scene, ship, &times, &echo_states, e, variant);
        entries = entries.max(ent);
        for (s, b) in shift.iter_mut().zip(bounded_shift(scene, ship, &times, &echo_states)) {
            *s += b;
        }
        let states = lay(scene, echo_states.clone(), &shift);
        let err: Vec<f64> = states.iter().zip(&times).map(|(s, &t)| ((scene.jacobi(t, s) - c0) / c0).abs()).collect();
        push(&format!("leak_{e}_v{variant}"), &err);
    }
    ShipOut {
        idx,
        crossings: k.crossings,
        closest_r: k.closest / scene.planet_radius,
        judged: k.converged && k.closest >= scene.planet_radius,
        c_j: c0,
        a0,
        band,
        band_check: bcheck,
        cap,
        entries_3rh: entries,
        laws,
    }
}

/// The composite verdict on one law column, at a given TOL_B.
fn verdict(ships: &[ShipOut], name: &str, tol_b: f64) -> serde_json::Value {
    let rows: Vec<&ShipOut> = ships.iter().filter(|s| s.judged).collect();
    let mut ratios = Vec::new();
    let (mut worst, mut over_cap) = (0.0f64, 0usize);
    for s in &rows {
        if let Some(entry) = s.laws.iter().find(|(n, ..)| n == name) {
            let ratio = if entry.1 > 0.0 { entry.2 / entry.1 } else { f64::INFINITY };
            ratios.push(ratio);
            worst = worst.max(entry.2);
            let cap = tol_b / TOL_B * s.cap; // caps scale linearly with the stated tolerance
            if entry.2 > CAP_MARGIN * cap { over_cap += 1; }
        }
    }
    let med = median(&mut ratios.clone());
    let pass = med <= RATIO_MAX && over_cap == 0;
    json!({
        "verdict": if pass { "PASS" } else { "FAIL" },
        "median_ratio": med,
        "worst_max_err": worst,
        "ships_over_cap": over_cap,
        "n": ratios.len(),
    })
}

pub fn main_run(horizon_periods: usize, n_grid: usize, leaks: Vec<Leak>, threads: usize) -> serde_json::Value {
    let kept = handoff::kept();
    let mut chunks: Vec<Vec<(usize, &'static handoff::Kept)>> = vec![Vec::new(); threads];
    for (i, k) in kept.iter().enumerate() {
        chunks[i % threads].push((i, k));
    }
    let mut handles = Vec::new();
    for chunk in chunks {
        let leaks = leaks.clone();
        handles.push(thread::spawn(move || {
            chunk.into_iter().map(|(i, k)| one_ship(k, i, horizon_periods, n_grid, &leaks)).collect::<Vec<_>>()
        }));
    }
    let mut ships = handles.into_iter().flat_map(|h| h.join().expect("ship thread")).collect::<Vec<_>>();
    ships.sort_by_key(|s| s.idx);
    let mut names: Vec<String> = ships.first().map(|s| s.laws.iter().map(|(n, ..)| n.clone()).collect()).unwrap_or_default();
    names.sort();
    let core = ["echo", "const", "bounded", "compound", "drift", "kick"];
    let verdicts: serde_json::Value = core
        .iter()
        .map(|l| (l.to_string(), verdict(&ships, l, TOL_B)))
        .chain(names.iter().filter(|n| n.starts_with("leak")).map(|n| (n.clone(), verdict(&ships, n, TOL_B))))
        .collect::<serde_json::Map<String, serde_json::Value>>()
        .into();
    let tol3: serde_json::Value = core
        .iter().map(|l| (l.to_string(), verdict(&ships, l, 3e-7)))
        .collect::<serde_json::Map<String, serde_json::Value>>().into();
    let tol6: serde_json::Value = core
        .iter().map(|l| (l.to_string(), verdict(&ships, l, 1e-6)))
        .collect::<serde_json::Map<String, serde_json::Value>>().into();
    json!({
        "horizon_periods": horizon_periods,
        "tol_b": TOL_B,
        "grid": n_grid,
        "ships": ships.iter().map(|s| json!({
            "idx": s.idx, "crossings": s.crossings, "closest_planet_radii": s.closest_r,
            "judged": s.judged, "C_J": s.c_j, "a0_sep": s.a0, "band_lo_sep": s.band.0, "band_hi_sep": s.band.1,
            "cap": s.cap, "entries_3RH_full": s.entries_3rh,
            "band_check_n": s.band_check.0, "band_check_lo": s.band_check.1, "band_check_hi": s.band_check.2,
            "laws": s.laws.iter().map(|(n, m1, mh, e)| json!({
                "law": n, "max_1x": m1, "max_h": mh,
                "ratio": if *m1 > 0.0 { mh / m1 } else { f64::INFINITY },
                "exp_1x": e,
            })).collect::<Vec<_>>(),
        })).collect::<Vec<_>>(),
        "verdicts": verdicts,
        "verdicts_tol_3e-7": tol3,
        "verdicts_tol_1e-6": tol6,
    })
}
