//! The doll's origin falls, and masses carry a mantissa (docs/law.md, 5 October). Floats appear only in the
//! oracles here (the law has none).
//!
//! **Frozen before the first run.**
//! - Mantissa: a ship on a circle about a planet of mass 1/999 of the star's (`Mass::ratio(1, 999)`, not a power of
//!   two) has the period `2π·√(a³/m)` of Kepler's law in root units, to 1e-7 (the Newtonian error at the radius
//!   chosen is about 1e-9), and the same planet given as the nearest power of two (`2^-10`) has a different one:
//!   the mantissa is in the law, not rounded away.
//! - Fall: at the doll's origin a body is not accelerated in the doll's own frame (exactly zero); anywhere else the
//!   level-0 acceleration of a secondary is the heliocentric one, `gm·[(x_p − x)/|x_p − x|³ − x_p/|x_p|³]`, to 1e-12
//!   relative; and one kick of a ship in the restricted problem changes its velocity by that, to 1e-6 (the kick's
//!   weight is the step, and the velocity word's quantum is far below), where the same kick without the fall
//!   differs by more than 10%.
//! - Far from the planet a ship keeps its orbit: a ship on the barycentric circle at three separations, outside the
//!   planet's, keeps its barycentric radius within 5e-4 over five of its orbits. First run: 2.0e-4 (the tide);
//!   control, the same run with the fall removed from the kick (a uniform push of the planet's whole pull, balanced
//!   by nothing): 6.5e-3, 32 times farther.
use emergent_space::orbit::Scalar;
use emergent_universe::body::What;
use emergent_universe::force::{acceleration, Secondary};
use emergent_universe::num::{s, to_f64, V2};
use emergent_universe::scenario::STAR_RADIUS;
use emergent_universe::universe::Universe;
use emergent_universe::{step, Config, Kind, Mass, OrbitSpec};

use emergent_universe::num::from_f64 as sc;
fn v2(x: f64, y: f64) -> V2 {
    [sc(x), sc(y)]
}

/// A star, a planet of mass `mu` on a circle of radius `sep` (turns `0`), and ships: `(radius, angle)`.
fn system(mu: Mass, sep: i64, ships: &[(i64, u32)]) -> (Universe, usize, Vec<usize>) {
    let mut u = Universe::new(s(STAR_RADIUS), Config::default());
    let planet = u
        .add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: s(sep), e_q48: 0, clockwise: false, angle: 0, phase: 0 }, Scalar::ZERO)
        .unwrap();
    u.add_doll("planet", planet, mu, Scalar::raw(49_000, -mu.octave).unwrap()).unwrap();
    let ids = ships
        .iter()
        .map(|&(r, a)| u.add_body(Kind::Ship, OrbitSpec { doll: 0, periapsis: s(r), e_q48: 0, clockwise: false, angle: a, phase: 0 }, Scalar::ZERO).unwrap())
        .collect();
    u.start().unwrap();
    (u, planet, ids)
}

#[test]
fn a_mass_with_a_mantissa_is_in_the_law() {
    let a_f = 1i64 << 40; // the ship's circle, in the planet doll's units: GM/a ≈ 1e-9 at the planet's mass
    let period_ticks = |mu: Mass| -> f64 {
        let mut u = Universe::new(s(STAR_RADIUS), Config::default());
        let planet = u.add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: s(1 << 33), e_q48: 0, clockwise: false, angle: 0, phase: 0 }, Scalar::ZERO).unwrap();
        let d = u.add_doll("planet", planet, mu, Scalar::raw(49_000, -mu.octave).unwrap()).unwrap();
        let ship = u.add_body(Kind::Ship, OrbitSpec { doll: d, periapsis: s(a_f), e_q48: 0, clockwise: false, angle: 0, phase: 0 }, Scalar::ZERO).unwrap();
        u.start().unwrap();
        let b = u.rec(ship).b;
        let emergent_space::binding::Trajectory::Cycle(c) = &b.entry.trajectory else { unreachable!() };
        // the compiled period is in the units of the planet's mass; to the doll's by the mantissa, to root ticks by the exponent
        to_f64(b.to_doll(c.period().unwrap()).unwrap()) * 2f64.powi(-(u.dolls[d as usize].shift as i32))
    };
    let kepler = |mu: Mass| -> f64 {
        let a_root = a_f as f64 * 2f64.powi(mu.octave);
        let m_root = to_f64(mu.value().unwrap());
        2.0 * std::f64::consts::PI * (a_root.powi(3) / m_root).sqrt()
    };
    let one_in_999 = Mass::ratio(1, 999).unwrap();
    assert!(one_in_999.mantissa != Scalar::ONE && one_in_999.octave == -10, "1/999 is not a power of two: {one_in_999:?}");
    let (got, want) = (period_ticks(one_in_999), kepler(one_in_999));
    println!("planet of 1/999: period {got:.6e} ticks, Kepler {want:.6e}, relative {:.2e}", got / want - 1.0);
    assert!((got / want - 1.0).abs() < 1e-7);
    // the old call, a power of two, goes through the same law
    let two_pow = Mass::from(-10);
    let (got2, want2) = (period_ticks(two_pow), kepler(two_pow));
    assert!((got2 / want2 - 1.0).abs() < 1e-7);
    // and the mantissa is not rounded away: 2^-10 is a different planet (2.5% lighter)
    assert!((got / got2 - 1.0).abs() > 0.01, "the two masses give the same period: {got} {got2}");
}

#[test]
fn the_origin_is_not_accelerated_in_its_own_frame_and_the_fall_has_the_right_sign() {
    let gm = Scalar::raw((1.001e-3 * 2f64.powi(60)) as i128, -60).unwrap();
    let xp = [3.0e3, 1.0e3];
    let sec = [Secondary { gm, pos: v2(xp[0], xp[1]), vel: [Scalar::ZERO; 2], edge: s(1) }];
    // at the origin: the secondary's pull and the origin's fall cancel exactly
    let a0 = acceleration(0, [Scalar::ZERO; 2], &sec, None).unwrap();
    assert!(a0[0].is_zero() && a0[1].is_zero(), "the star feels itself fall: {a0:?}");
    // elsewhere: the heliocentric acceleration, against floats
    let g = to_f64(gm);
    for x in [[-2.0e3, 4.0e3], [1.5e3, -2.5e3], [-3.0e3, -1.0e3], [2.9e3, 1.0e3]] {
        let a = acceleration(0, v2(x[0], x[1]), &sec, None).unwrap();
        let (dx, dy) = (xp[0] - x[0], xp[1] - x[1]);
        let d3 = (dx * dx + dy * dy).powf(1.5);
        let p3 = (xp[0] * xp[0] + xp[1] * xp[1]).powf(1.5);
        let want = [g * (dx / d3 - xp[0] / p3), g * (dy / d3 - xp[1] / p3)];
        let got = [to_f64(a[0]), to_f64(a[1])];
        let err = ((got[0] - want[0]).hypot(got[1] - want[1])) / want[0].hypot(want[1]);
        assert!(err < 1e-12, "x {x:?}: {got:?} against {want:?} ({err:e})");
        // the direct pull alone differs: the fall is a term of the same size (except next to the secondary,
        // the last point, where the pull is all there is: there the check is the float comparison above)
        let direct = [g * dx / d3, g * dy / d3];
        let differs = (direct[0] - want[0]).hypot(direct[1] - want[1]) > 0.05 * want[0].hypot(want[1]);
        assert!(differs || x == [2.9e3, 1.0e3], "x {x:?}: the fall is a negligible term here");
    }
}

/// The first kick of ship `i`, replayed against the plane's own resolver: the velocity it gives, in the
/// doll's units, with its weight (the physical time of its tick of the clock) and the root-frame floats of the ship and the planet then.
fn first_kick(u: &Universe, planet: usize, i: usize) -> ([f64; 2], f64, [f64; 2], [f64; 2]) {
    let mut rec = u.rec(i);
    while !matches!(rec.plan.first().map(|p| p.what), Some(What::Kick(0))) {
        rec.plan.remove(0);
    }
    let t = rec.plan[0].t;
    let before = rec.b.readout(t).unwrap();
    let ctx = u.ctx();
    // The weight of the kick: Δs·f'(U_P + c) at its place and time (the motion law v2: the physical time of one tick of the
    // fictitious clock), in the star's doll, where a tick is a unit of its time.
    let h = {
        let ext = rec.ext.expect("a ship of the root doll is stepped by the clock");
        let (x, _) = emergent_universe::bind::scalars(&before).unwrap();
        let f = emergent_universe::force::field(&ctx.secondaries(0, t, i).unwrap(), x).unwrap();
        to_f64(ext.time(ext.y(f.potential).unwrap(), ext.ds).unwrap())
    };
    let (x, _) = emergent_universe::observe::root_state(&ctx, i, t).unwrap();
    let (xp, _) = emergent_universe::observe::root_state(&ctx, planet, t).unwrap();
    let upd = step::process(&ctx, i, rec);
    assert_eq!(upd.kind, step::Resolved::Kick);
    let after = upd.rec.b.readout(t).unwrap();
    let v = |st: &emergent_space::binding::IntegerState, c: usize| st.velocity[c] as f64 * 2f64.powi(st.velocity_exponent as i32);
    ([v(&after, 0) - v(&before, 0), v(&after, 1) - v(&before, 1)], h, x, xp)
}

#[test]
fn one_kick_carries_the_fall_against_a_float_restricted_problem() {
    let mu = Mass::ratio(1, 999).unwrap();
    let g = to_f64(mu.value().unwrap());
    let sep = 527_000_000i64;
    // ships at half and at one and a half separations, at angles away from the planet's (it is at angle 0 at tick 0)
    let (u, planet, ids) = system(mu, sep, &[(sep / 2, 0x4000_0000), (sep * 3 / 2, 0xA000_0000), (sep * 3, 0x2000_0000)]);
    for &i in &ids {
        let (dv, h, x, xp) = first_kick(&u, planet, i);
        let (dx, dy) = (xp[0] - x[0], xp[1] - x[1]);
        let d3 = (dx * dx + dy * dy).powf(1.5);
        let p3 = (xp[0] * xp[0] + xp[1] * xp[1]).powf(1.5);
        let with = [h * g * (dx / d3 - xp[0] / p3), h * g * (dy / d3 - xp[1] / p3)];
        let without = [h * g * dx / d3, h * g * dy / d3];
        let norm = |a: [f64; 2]| a[0].hypot(a[1]);
        let (e_with, e_without) = (norm([dv[0] - with[0], dv[1] - with[1]]) / norm(with), norm([dv[0] - without[0], dv[1] - without[1]]) / norm(with));
        println!("ship {i}: |dv| {:.4e}; against the heliocentric kick {e_with:.2e}, against the direct pull alone {e_without:.2e}", norm(dv));
        assert!(e_with < 1e-6, "ship {i}: the kick {dv:?} against {with:?}");
        assert!(e_without > 0.1, "ship {i}: the direct pull alone matches the kick ({e_without:.2e}): the fall is missing");
    }
}

#[test]
fn far_from_the_planet_a_ship_keeps_its_orbit() {
    let mu = Mass::ratio(1, 999).unwrap();
    let q = to_f64(mu.value().unwrap()); // the planet over the star
    let w = q / (1.0 + q); // the star sits at −w of the planet's heliocentric position, barycentrically
    let sep = 527_000_000f64;
    let r_b = 3.0 * sep;
    // the planet's circle, and the ship's circular barycentric orbit (total mass 1 + q), in the star's frame
    let omega = ((1.0 + q) / sep.powi(3)).sqrt();
    let (xp, vp) = ([sep, 0.0], [0.0, omega * sep]);
    let alpha = 0.7f64;
    let vc = ((1.0 + q) / r_b).sqrt();
    let x_h = [r_b * alpha.cos() + w * xp[0], r_b * alpha.sin() + w * xp[1]];
    let v_h = [-vc * alpha.sin() + w * vp[0], vc * alpha.cos() + w * vp[1]];
    let mut u = Universe::new(s(STAR_RADIUS), Config::default());
    let planet = u.add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: sc(sep), e_q48: 0, clockwise: false, angle: 0, phase: 0 }, Scalar::ZERO).unwrap();
    u.add_doll("planet", planet, mu, Scalar::raw(49_000, -mu.octave).unwrap()).unwrap();
    let ship = u.add_body_state(Kind::Ship, 0, v2(x_h[0], x_h[1]), v2(v_h[0], v_h[1]), Scalar::ZERO).unwrap();
    u.start().unwrap();
    let bary = |u: &Universe, t: i64| {
        let ctx = u.ctx();
        let (x, _) = emergent_universe::observe::root_state(&ctx, ship, t).unwrap();
        let (xp, _) = emergent_universe::observe::root_state(&ctx, planet, t).unwrap();
        (x[0] - w * xp[0]).hypot(x[1] - w * xp[1])
    };
    let period = 2.0 * std::f64::consts::PI * r_b.powf(1.5) / (1.0 + q).sqrt();
    let r_start = bary(&u, 0);
    assert!((r_start / r_b - 1.0).abs() < 1e-9, "the start is the barycentric circle: {}", r_start / r_b - 1.0);
    let mut worst = 0.0f64;
    for k in 1..=40 {
        let t = (k as f64 * period / 8.0) as i64;
        u.settle(t);
        worst = worst.max((bary(&u, t) / r_start - 1.0).abs());
    }
    println!("a ship at three separations keeps its barycentric radius to {worst:.2e} over five orbits");
    assert!(u.rec(ship).alive);
    assert!(worst < 5e-4, "the ship's barycentric radius moved by {worst:e}");
}
