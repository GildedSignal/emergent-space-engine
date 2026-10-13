//! **P2, burning back out.** A ship that has braked to rest above a planet falls (P1); the player must be able to climb back:
//! a radial or near-radial state going *up* has no periapsis either, so it needs a tube too (the leg up to where it turns, and
//! the fall back, one arc: `emergent_space::plunge::Plunge::outbound`).
//!
//! **Frozen before the first run.** A planet of the plane's Home kind (a mass of 2^-18 of the star's, 4,313 root units of
//! radius, in the star's doll), a player at rest above it on its +x axis (so the nose, at heading 0, is radially outward;
//! the nose of a body made at rest has no velocity to follow). Every case: zero refusals and no fault, and the ship alive
//! until the surface where it falls.
//! 1. *A toss* (forward at level 6, 8 and 9 for 3 s of game time, then coast): the energy is below escape, the ship rises to an apoapsis
//!    and falls back. The tube it flies is a plunge arc (the control that the new path is the one tested); the apoapsis is
//!    within 2% of the Newtonian one from the energy the burn gave it (the star's tide at that height is under 1e-3); the HUD
//!    warns of the impact as soon as the burn stops (the arc ends at the surface), and the ship is alive just before the
//!    predicted tick and lost just after it (within 1e-3 of the time left, and three times the star's tide at the apoapsis,
//!    `2^18 (r/a)³`, which moves the course: it is 1e-6 at level 6 and 2e-3 at level 9).
//! 2. *A burn out* (forward at level 10 for 10 s, then coast): the energy is above escape, the ship rises for good, is
//!    released from the planet's doll at its edge into the star's, and is alive there a day of game time later, with no
//!    warning at any frame and nothing refused.
use emergent_space::orbit::Scalar;
use emergent_universe::num::{to_f64, Tick};
use emergent_universe::scenario::STAR_RADIUS;
use emergent_universe::thrust::word;
use emergent_universe::view::{gather, TICK_SECONDS};
use emergent_universe::{Config, Kind, OrbitSpec, Universe};

const SURFACE_ROOT: i64 = 4_313;
const MASS_LOG2: i32 = -18;
/// The player's id: the planet is body 0.
const ME: usize = 1;

/// The star, a planet on a circle at 1 AU, a player at rest at `radii` planet radii on the planet's +x axis (in its doll).
fn world(radii: f64) -> Universe {
    let mut u = Universe::new(Scalar::integer(STAR_RADIUS), Config::default());
    let planet = u.add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: Scalar::integer(99_300_000), e_q48: 0, clockwise: false, angle: 0, phase: 0 }, Scalar::ZERO).unwrap();
    let surface = Scalar::raw(SURFACE_ROOT as i128, -MASS_LOG2).unwrap(); // root units → planet units: × 2^-octave
    let doll = u.add_doll("planet", planet, MASS_LOG2, surface).unwrap();
    // at rest, in the planet's units (its surface in them is 4313 · 2^18)
    let r0 = emergent_universe::num::from_f64(radii * to_f64(surface));
    u.add_body_state(Kind::Player, doll, [r0, Scalar::ZERO], [Scalar::ZERO; 2], Scalar::ZERO).expect("a player at rest above a planet has a tube");
    u.start().unwrap();
    u
}

/// The player's position and speed against the planet (the doll's units, `M = c = 1`) at `t`, from the tube.
fn state_at(u: &Universe, t: Tick) -> ([f64; 2], [f64; 2]) {
    let (x, v) = u.rec(ME).b.cartesian(t).unwrap();
    (x.map(to_f64), v.map(to_f64))
}

fn r_of(x: [f64; 2]) -> f64 {
    (x[0] * x[0] + x[1] * x[1]).sqrt()
}

/// Forward at `level` from tick 0 for `burn` ticks, then coast.
fn burn(u: &mut Universe, level: u8, burn: Tick) {
    u.input(0, word(1, level)).unwrap();
    u.settle(burn);
    u.input(burn, word(0, level)).unwrap();
}

#[test]
fn a_toss_rises_to_its_apoapsis_and_falls_back_to_the_surface() {
    for level in [6u8, 8, 9] {
        a_toss(level);
    }
}

fn a_toss(level: u8) {
    let mut u = world(5.0);
    assert!(matches!(u.rec(ME).b.entry.trajectory, emergent_space::binding::Trajectory::Plunge(_)), "at rest above the planet is a fall");
    let burn_ticks = (3.0 / TICK_SECONDS) as Tick;
    burn(&mut u, level, burn_ticks);
    u.now = burn_ticks;
    let rec = u.rec(ME);
    assert!(rec.alive && rec.refusals == 0 && rec.fault.is_none(), "after the burn: alive {}, refusals {}, fault {:?}", rec.alive, rec.refusals, rec.fault);
    // the burn's gift, from the state the tube holds now (planet units, M = 1): Newtonian energy and apoapsis
    let t1 = burn_ticks + 1;
    u.settle(t1);
    let (x, v) = state_at(&u, u.rec(ME).b.event_time.max(burn_ticks));
    let (r1, v2) = (r_of(x), v[0] * v[0] + v[1] * v[1]);
    let energy = 0.5 * v2 - 1.0 / r1;
    assert!(energy < 0.0, "the toss must be bound: E {energy}");
    let apo = -1.0 / energy;
    // the tube now is a plunge arc, anchored at the apoapsis
    let rec = u.rec(ME);
    let anchor = match &rec.b.entry.trajectory {
        emergent_space::binding::Trajectory::Plunge(p) => to_f64(p.initial_radius()),
        t => panic!("a near-radial rise is a plunge arc, not {t:?}"),
    };
    println!("toss at level {level}: burn gave E {energy:.4e}; Newtonian apoapsis {apo:.6e}, the arc's {anchor:.6e}; radius now {r1:.4e}");
    assert!(((anchor - apo) / apo).abs() < 0.02, "apoapsis {anchor:e} against the Newtonian {apo:e}");
    // the HUD warns of the impact
    let view = gather(&u, &[]).unwrap();
    let impact = view.impact.clone().expect("the way back down is an impact course");
    assert_eq!(impact.body, "planet");
    println!("{}", impact.sentence());
    // alive until the predicted contact, lost at it
    let tick = impact.tick;
    // The star's tide at the apoapsis moves the course: its size against the planet's pull, `2^18 (r/a)³`, is the share of the
    // remaining time that can be off (a toss to a few radii is within 1e-3 of it).
    let tide = 2f64.powi(18) * (apo * 2f64.powi(MASS_LOG2) / 99_300_000.0).powi(3);
    let tol = ((tick - u.now) as f64 * (1e-3 + 3.0 * tide)) as Tick + 100;
    let mut before = world(5.0);
    burn(&mut before, level, burn_ticks);
    before.settle(tick - tol);
    assert!(before.rec(ME).alive && before.rec(ME).refusals == 0, "the ship is lost before the contact it was warned of");
    before.settle(tick + tol);
    let r = before.rec(ME);
    assert!(!r.alive && r.refusals == 0 && r.fault.is_none(), "alive {}, refusals {}, fault {:?}", r.alive, r.refusals, r.fault);
}

#[test]
fn a_burn_out_leaves_the_planet_and_is_alive_in_the_stars_doll() {
    let mut u = world(5.0);
    let burn_ticks = (10.0 / TICK_SECONDS) as Tick;
    burn(&mut u, 10, burn_ticks);
    // a day of game time, in frames of ten minutes: no warning at any of them, nothing refused
    let day = (86_400.0 / TICK_SECONDS) as Tick;
    let frame = (600.0 / TICK_SECONDS) as Tick;
    let mut released = None;
    let mut t = burn_ticks;
    while t < day {
        t = (t + frame).min(day);
        u.settle(t);
        u.now = t;
        let rec = u.rec(ME);
        assert!(rec.alive && rec.refusals == 0 && rec.fault.is_none(), "tick {t}: alive {}, refusals {}, fault {:?}", rec.alive, rec.refusals, rec.fault);
        let view = gather(&u, &[]).unwrap();
        assert!(view.impact.is_none(), "tick {t}: a warning on an escape: {:?}", view.impact);
        if released.is_none() && rec.b.doll == 0 {
            released = Some(t);
        }
    }
    let released = released.expect("the ship never left the planet's doll");
    println!("released from the planet's doll into the star's at tick {released} ({:.0} s of game time)", released as f64 * TICK_SECONDS);
}

/// Schwarzschild radial fall from rest at `r0` to `rs` (`M = 1`): coordinate time. (P1's oracle.)
fn fall_time(r0: f64, rs: f64) -> f64 {
    let eta = (2.0 * rs / r0 - 1.0).acos();
    let a = (r0 / 2.0 - 1.0).sqrt();
    2.0 * ((a + (eta / 2.0).tan()) / (a - (eta / 2.0).tan())).abs().ln() + 2.0 * a * (eta + r0 / 4.0 * (eta + eta.sin()))
}

/// A ship going up from `r1 = k R` at a fraction of the local escape speed, with a tangential speed of 1e-13 c (a near-radial
/// state: L² far below 12 M²): it rises to the apoapsis of its energy, turns, and falls to the surface. Against the exact
/// geodesic: `E² = f/(1 − w²)` for a local speed `w`, the apoapsis `2/(1 − E²)`, and the time to the surface the rise (the
/// fall from the apoapsis to `r1`) plus the fall from it to `R`. Worst error ≤ 1e-2 in the apoapsis and in the time; zero
/// refusals; alive before the surface and lost at it; and the way up is a reflected arc of the same compile (the control).
#[test]
fn a_toss_from_a_given_state_matches_the_exact_geodesic() {
    let surface = 471_000i64;
    let mut worst = (0f64, 0f64);
    for ratio in [2i64, 5, 20] {
        for frac in [0.2, 0.5, 0.9] {
            let r1 = (surface * ratio) as f64;
            let f = 1.0 - 2.0 / r1;
            let w = frac * (2.0 / r1).sqrt(); // local speed, a fraction of the Newtonian escape speed
            let e2 = f / (1.0 - w * w);
            let r_apo = 2.0 / (1.0 - e2);
            assert!(r_apo > r1);
            let t_exact = fall_time(r_apo, r1) + fall_time(r_apo, surface as f64);
            // the state: coordinate radial velocity f·w outward, tangential 1e-13
            let make = || {
                let mut u = Universe::new(Scalar::integer(surface), Config::default());
                u.add_body_state(Kind::Player, 0, [Scalar::integer(surface * ratio), Scalar::ZERO], [emergent_universe::num::from_f64(f * w), emergent_universe::num::from_f64(1e-13)], Scalar::ZERO)
                    .expect("a near-radial rise has a tube");
                u.start().unwrap();
                u
            };
            let u = make();
            let rec = u.rec(0);
            let apo = match &rec.b.entry.trajectory {
                emergent_space::binding::Trajectory::Plunge(p) => to_f64(p.initial_radius()),
                t => panic!("ratio {ratio}, frac {frac}: expected a plunge arc, got {t:?}"),
            };
            let err_apo = (apo - r_apo) / r_apo;
            let alive_at = |t: Tick| {
                let mut u = make();
                u.settle(t);
                u.rec(0).alive
            };
            let (mut lo, mut hi) = (0i64, (t_exact * 1.5) as i64 + 10);
            assert!(!alive_at(hi) && alive_at(lo));
            while hi - lo > 1 {
                let mid = lo + (hi - lo) / 2;
                if alive_at(mid) {
                    lo = mid;
                } else {
                    hi = mid;
                }
            }
            let err_t = (hi as f64 - t_exact) / t_exact;
            let r = {
                let mut u = make();
                u.settle(hi);
                u.rec(0)
            };
            println!("r1 = {ratio} R, {frac} of escape: apoapsis {apo:.5e} (exact {r_apo:.5e}, {err_apo:+.1e}), time to the surface {hi:.5e} (exact {t_exact:.5e}, {err_t:+.1e})");
            assert!(!r.alive && r.refusals == 0 && r.fault.is_none());
            assert!(err_apo.abs() <= 1e-2 && err_t.abs() <= 1e-2, "ratio {ratio}, frac {frac}: apoapsis {err_apo:+.2e}, time {err_t:+.2e}");
            worst = (worst.0.max(err_apo.abs()), worst.1.max(err_t.abs()));
        }
    }
    println!("P2 toss: worst relative error {:.2e} (apoapsis), {:.2e} (time to the surface)", worst.0, worst.1);
}
