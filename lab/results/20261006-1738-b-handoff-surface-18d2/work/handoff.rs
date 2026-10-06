//! The single-surface handoff's probes (the Opus motion memo §4, P4 and the moon of step 3), through the
//! plane's public API only, on the frozen B12–B14 scene (a star and a Jupiter-like planet of a thousandth
//! of the total, `sep = 5.27e8 M`, so the Jacobi constant is the exact invariant of the plane's model).
//! Frozen before the first run; floats appear only in the oracle (the Jacobi constant), never in the law.
//!
//! - **P4**: regular satellites at 0.3, 0.5 and 0.9 R_H, prograde and retrograde, 2,000 planet periods.
//!   The Jacobi error, sampled at P/64, split into ten decades of 200 periods: the median of each decade,
//!   and the ratio of the last decade's to the first's. Bounded is about 1, a random walk about 3.2; the
//!   memo kills at 1.3. Where each satellite lives is the surface's own choice (predicted in
//!   `predictions.md`: 0.3 R_H in the planet's doll, 0.5 and 0.9 in the root doll), and is reported.
//! - **A moon born in the planet's doll never leaves** (step 3's test): a circular birth at 0.3 R_H,
//!   both senses, 100 planet periods: the body's doll never changes, no handoff is counted, it stays
//!   bound. Births at 0.9 R_H are released at their first s-boundary — the surface working — and are
//!   reported as the control.
use emergent_space::orbit::Scalar;
use emergent_universe::num::{from_f64, s, to_f64};
use emergent_universe::observe;
use emergent_universe::scenario::STAR_RADIUS;
use emergent_universe::universe::Universe;
use emergent_universe::{Config, Kind, OrbitSpec};

/// The scene of B12–B14 (frozen): mass ratio, separation, radius, all in units of the total mass.
const MU: f64 = 1e-3;
const SEP: f64 = 5.27e8;
const PLANET_RADIUS: f64 = 6.9e2;

/// The plane's own build of the judge's scene (see `xtask/src/behave/plane.rs`): the root unit is the
/// star's mass, so every length and time crosses as `/(1 − μ)` and velocities unchanged.
fn scene(step_log2: i32) -> Universe {
    let to_root = 1.0 / (1.0 - MU);
    let mut u = Universe::new(s(STAR_RADIUS), Config { step_log2, ..Config::default() });
    u.threads = 1;
    let planet = u
        .add_body(
            Kind::Planet,
            OrbitSpec { doll: 0, periapsis: from_f64(SEP * to_root), e_q48: 0, clockwise: false, angle: 0, phase: 0 },
            Scalar::ZERO,
        )
        .unwrap();
    let mass = emergent_universe::world::Mass::of(from_f64(MU / (1.0 - MU))).unwrap();
    let surface = from_f64(PLANET_RADIUS * to_root).scale(-mass.octave).unwrap();
    u.add_doll("planet", planet, mass, surface).unwrap();
    u
}

/// The Jacobi constant of the plane's heliocentric model (the indirect term included), in floats, from
/// root-frame states: the same oracle `tests/motion.rs` judges its handoffs with.
fn jacobi(u: &Universe, planet: usize, ship: usize, t: i64) -> f64 {
    let ctx = u.ctx();
    let (xs, vs) = observe::root_state(&ctx, ship, t).unwrap();
    let (xp, _) = observe::root_state(&ctx, planet, t).unwrap();
    let mu = MU / (1.0 - MU);
    let r = (xs[0] * xs[0] + xs[1] * xs[1]).sqrt();
    let d = ((xs[0] - xp[0]).powi(2) + (xs[1] - xp[1]).powi(2)).sqrt();
    let rp3 = (xp[0] * xp[0] + xp[1] * xp[1]).powf(1.5);
    let e = 0.5 * (vs[0] * vs[0] + vs[1] * vs[1]) - 1.0 / r - mu / d + mu * (xs[0] * xp[0] + xs[1] * xp[1]) / rp3;
    let l = xs[0] * vs[1] - xs[1] * vs[0];
    let omega = (1.0 + mu).sqrt() * rp3.sqrt() / rp3;
    e - omega * l
}

/// A satellite's heliocentric start (the plane's root doll, the star's own barycentric state removed):
/// a circular planetocentric orbit of radius `a_hill` Hill radii, phase zero (behind the planet), at the
/// Kepler speed about the planet.
fn satellite(u: &mut Universe, planet: usize, a_hill: f64, prograde: bool) -> usize {
    let (xp, wp) = {
        let ctx = u.ctx();
    let t = 0i64;
        let t = 0i64;
        let state = (observe::root_state(&ctx, planet, t).unwrap(), observe::root_state(&ctx, planet, t).unwrap());
        let ((xp, _), (_, wp)) = state;
        (xp, wp)
    };
    let mu = MU / (1.0 - MU);
    let to_root = 1.0 / (1.0 - MU);
    let hill = SEP * (MU / 3.0).cbrt();
    let a = a_hill * hill * to_root;
    let v = (mu / a).sqrt();
    // The planet sits at angle 0; the satellite behind it, on the same circle of the star.
    let (dx, dy) = (-a, 0.0);
    let (dvx, dvy) = if prograde { (0.0, -v) } else { (0.0, v) };
    u.add_body_state(
        Kind::Ship,
        0,
        [from_f64(xp[0] + dx), from_f64(xp[1] + dy)],
        [from_f64(wp[0] + dvx), from_f64(wp[1] + dvy)],
        Scalar::ZERO,
    )
    .unwrap()
}

/// The planet's period in root ticks.
fn period(u: &mut Universe, planet: usize) -> i64 {
    use emergent_space::binding::Trajectory;
    match &u.rec(planet).b.entry.trajectory {
        Trajectory::Cycle(o) => o.period().unwrap().fixed(0).unwrap() as i64,
        _ => unreachable!(),
    }
}

#[test]
fn p4_regular_satellites_stay_bounded_over_two_thousand_periods() {
    const PERIODS: i64 = 2000;
    const DECADES: usize = 10;
    let planet = 0; // the first body added
    // (The satellite for each case is made in its own universe: the Jacobi constant is per ship.)
    let p = period(&mut scene(7), planet);
    let mut worst = 1.0f64;
    for (a_hill, prograde) in [(0.3f64, true), (0.3, false), (0.5, true), (0.5, false), (0.9, true), (0.9, false)] {
        let mut u = scene(7);
        let ship = satellite(&mut u, planet, a_hill, prograde);
        u.start().unwrap();
        let c0 = jacobi(&u, planet, ship, 0);
        let per_samples = 64;
        let mut decades = vec![vec![], vec![], vec![], vec![], vec![], vec![], vec![], vec![], vec![], vec![]];
        for n in 0..(PERIODS * per_samples) {
            let t = (n as i128 * p as i128 / per_samples as i128) as i64;
            u.settle(t);
            if !u.bodies().alive(ship) {
                panic!("the satellite at {a_hill} R_H {} was lost", if prograde { "prograde" } else { "retrograde" });
            }
            let c = jacobi(&u, planet, ship, t);
            let d = n as i64 / (PERIODS * per_samples as i64 / DECADES as i64);
            decades[d as usize].push((c - c0).abs() / c0.abs());
        }
        let medians: Vec<f64> = decades.iter().map(|d| d[d.len() / 2]).collect();
        let ratio = medians[DECADES - 1] / medians[0];
        let doll = u.rec(ship).b.doll;
        println!(
            "P4 {a_hill} R_H {}: median Jacobi error {:.2e} → {:.2e} → {:.2e}, decade ratio {ratio:.3}, ends in doll {doll}, {} events",
            if prograde { "prograde" } else { "retrograde" },
            medians[0], medians[DECADES / 2], medians[DECADES - 1],
            u.rec(ship).events
        );
        worst = worst.max(ratio);
        if ratio > 1.3 {
            println!("P4 FAIL: the decade ratio at {a_hill} R_H {} is {ratio}", if prograde { "prograde" } else { "retrograde" });
        }
    }
    println!("P4: worst decade ratio {worst:.3}");
}

#[test]
fn a_moon_born_in_the_planets_doll_never_leaves() {
    const PERIODS: i64 = 100;
    let mut u = scene(7);
    let planet = 0;
    let p = period(&mut u, planet);
    let hill_root = SEP * (MU / 3.0).cbrt() / (1.0 - MU);
    for (a_hill, prograde, stays) in [(0.3f64, true, true), (0.3, false, true), (0.9, true, false)] {
        let mut u = scene(7);
        let doll = *u.info[planet].doll.as_ref().unwrap();
        let shift = u.dolls[doll as usize].shift as i32;
        let mu = to_f64(u.dolls[doll as usize].unit.mu);
        let a = a_hill * hill_root * 2f64.powi(shift); // child units
        let v = (mu / a).sqrt();
        let moon = u
            .add_body_state(Kind::Ship, doll, [from_f64(a), from_f64(0.0)], [from_f64(0.0), from_f64(if prograde { v } else { -v })], Scalar::ZERO)
            .unwrap();
        u.start().unwrap();
        let mut left = None;
        for n in 1..=64 * PERIODS {
            let t = (n as i128 * p as i128 / 64) as i64;
            u.settle(t);
            if !u.bodies().alive(moon) {
                panic!("the moon at {a_hill} R_H died at sample {n}");
            }
            if u.rec(moon).b.doll != doll && left.is_none() {
                left = Some(n);
            }
        }
        println!(
            "moon at {a_hill} R_H {}: handoffs {} (of which leaving the doll at sample {:?}), {} events, still {} bound",
            if prograde { "prograde" } else { "retrograde" },
            u.stats.handoffs,
            left,
            u.rec(moon).events,
            if left.is_some() { "out" } else { "in" }
        );
        assert_eq!(left.is_none(), stays, "the moon at {a_hill} R_H {} should have stayed: {stays}", if prograde { "prograde" } else { "retrograde" });
        if stays {
            assert_eq!(u.stats.handoffs, 0, "a moon born in the doll is never handed off");
        }
    }
}
