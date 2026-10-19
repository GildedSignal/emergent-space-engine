//! Playability (Julien, 12 October: "we want something functional ... i just don't want it buggy, fly like the sr 71").
//! The flight sweep found every loss in a 20 s flight to be a crash into Home: the nose started retrograde, and the HUD never
//! warned. Every test finishes within a few seconds.
//!
//! **Frozen before the first run.**
//! 1. `heading_of` inverts `direction` (integer CORDIC both ways): over 4096 headings and over vectors of any quadrant and
//!    magnitude, within 2e-7 turn.
//! 2. The player's nose starts along its velocity in its doll (cos of the angle ≥ 1 − 1e-9 for the plane, every seed tried, and
//!    for a player made from a state); the old start (heading 0 = +x) is retrograde there, so the control is real. A forward
//!    burn then raises the speed against Home and a reverse burn lowers it.
//! 3. The impact warning: braking from Home's low orbit lowers the periapsis under the surface. From the first frame the
//!    periapsis is under it the view holds an `Impact` (what: Home; when: the tick; where; how fast), never later than the plan
//!    holds its `Crash` item, and it is there exactly while the periapsis is under the surface (the certificate), then the
//!    prediction stays within 1% (and 1 s of game time) of the tick the ship is lost at, the countdown runs down with the
//!    game's clock, and the loss says it hit Home at that world time.
//! 4. The warning clears: burning forward from that course raises the periapsis above the surface, the view's impact is gone in
//!    that very frame, and the ship flies on for a further orbit alive with none.
use emergent_universe::body::What;
use emergent_universe::fleet::Order;
use emergent_universe::num::{to_f64, Tick};
use emergent_universe::scenario::{plane, stream, Plane, Stream};
use emergent_universe::thrust::{direction, heading_of, word};
use emergent_universe::view::{gather, View, TICK_SECONDS};
use emergent_universe::{Budget, Config};

fn unit(h: u32) -> [f64; 2] {
    direction(h).unwrap().map(to_f64)
}

#[test]
fn heading_of_inverts_direction() {
    let mut worst = 0f64;
    for k in 0..4096u64 {
        let h = (k * (1 << 20) + (k * 2_654_435_761) % (1 << 20)) as u32;
        let back = heading_of(direction(h).unwrap()).unwrap();
        let d = (back.wrapping_sub(h) as i32).unsigned_abs() as f64 / 4294967296.0;
        worst = worst.max(d);
    }
    assert!(worst < 2e-7, "round trip off by {worst:e} turn");
    // vectors of any quadrant, from tiny to huge magnitudes, and the axes themselves
    let mut seed = 0x9E37_79B9_7F4A_7C15u64;
    let mut next = || {
        seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        (seed >> 11) as f64 / (1u64 << 53) as f64
    };
    for k in 0..2000 {
        let (a, mag) = (next() * std::f64::consts::TAU, 2f64.powi((next() * 80.0 - 40.0) as i32));
        let v = [emergent_universe::num::from_f64(mag * a.cos()), emergent_universe::num::from_f64(mag * a.sin())];
        let h = heading_of(v).unwrap() as f64 / 4294967296.0 * std::f64::consts::TAU;
        let d = (h - a + std::f64::consts::PI).rem_euclid(std::f64::consts::TAU) - std::f64::consts::PI;
        assert!(d.abs() < 2e-6, "vector {k} at {a} rad (magnitude {mag:e}): heading off by {d:e} rad");
    }
    for (v, want) in [([1.0, 0.0], 0u32), ([0.0, 1.0], 1 << 30), ([-1.0, 0.0], 1 << 31), ([0.0, -1.0], 3 << 30)] {
        let h = heading_of(v.map(emergent_universe::num::from_f64)).unwrap();
        assert!((h.wrapping_sub(want) as i32).unsigned_abs() < 100, "axis {v:?}: heading {h}, want {want}");
    }
    assert_eq!(heading_of([emergent_space::orbit::Scalar::ZERO; 2]).unwrap(), 0, "no velocity, no heading");
}

fn start_velocity(p: &Plane) -> [f64; 2] {
    let (_, v) = p.u.rec(p.player).b.cartesian(0).unwrap();
    v.map(to_f64)
}

#[test]
fn the_nose_starts_along_the_velocity() {
    for seed in 1..=6u64 {
        let p = plane(Config::default(), seed, Order::Sparse, 1, 8).unwrap();
        let v = start_velocity(&p);
        let n = unit(p.u.rec(p.player).thrust.unwrap().heading);
        let cos = (v[0] * n[0] + v[1] * n[1]) / (v[0] * v[0] + v[1] * v[1]).sqrt();
        assert!(cos >= 1.0 - 1e-9, "seed {seed}: the nose is off the velocity (cos {cos})");
        // the control: the old heading (+x) is retrograde for this ship, which orbits along -x
        assert!(v[0] < 0.0, "seed {seed}: the control needs a ship moving along -x");
    }
    // a player made from a state (the stream's, along +y at 0.9c)
    let (u, _, player) = stream(0.9, 0.5, Stream::Across, 4, 1.0e6, 1_000_000).unwrap();
    let h = u.rec(player).thrust.unwrap().heading as f64 / 4294967296.0;
    assert!((h - 0.25).abs() < 1e-6, "a player moving along +y has its nose at a quarter turn: {h}");
}

fn doll_speed(v: &View) -> f64 {
    (v.doll_beta[0].powi(2) + v.doll_beta[1].powi(2)).sqrt()
}

#[test]
fn forward_burns_prograde_and_reverse_retrograde() {
    let at = |keys: u8| {
        let mut p = plane(Config::default(), 2, Order::Sparse, 1, 8).unwrap();
        p.u.input(0, word(keys, 4)).unwrap();
        p.u.settle(2_000_000); // ten seconds of game time: about 55 m/s of the 5.6 g burn per second
        p.u.now = 2_000_000;
        doll_speed(&gather(&p.u, &p.names).unwrap())
    };
    let (coast, fwd, rev) = (at(0), at(1), at(2));
    println!("speed against Home after 10 s: coast {coast:.6e} c, forward {fwd:.6e} c, reverse {rev:.6e} c");
    assert!(fwd > coast * 1.02, "forward must speed the ship up: {fwd:e} against coasting {coast:e}");
    assert!(rev < coast * 0.98, "reverse must slow it: {rev:e} against coasting {coast:e}");
}

/// One frame of the page's flight: 1/60 s of wall time at `rtf`, the engine unthrottled (a canonical schedule).
fn frame(p: &mut Plane, rtf: f64) -> View {
    p.u.frame(1.0 / 60.0, rtf, Budget::unlimited());
    gather(&p.u, &p.names).expect("the player has a view")
}

/// The certificate the engine plans its impact from: the reconciled coast's periapsis is under the surface.
/// A centred kick's raw tube includes prepaid thrust; cutting at the reading refunds it.
fn under_surface(p: &Plane) -> bool {
    let rec = p.u.rec(p.player);
    // Independently exercise the actual cut path; do not use the HUD's course helper as its oracle.
    let level = rec.thrust.unwrap().level;
    let cut = emergent_universe::step::decide(&p.u.ctx(), p.player, rec.clone(), p.u.now, word(0, level));
    assert_eq!(cut.rec.refusals, rec.refusals, "the warning's hypothetical cut must succeed");
    let b = cut.rec.b;
    // a turning tube whose periapsis is under it, or a plunge (an arc that ends at it)
    b.entry.trajectory.key().is_none_or(|k| b.to_doll(k.periapsis).unwrap() < p.u.dolls[b.doll as usize].surface)
}

fn planned_crash(p: &Plane) -> bool {
    p.u.rec(p.player).plan.iter().any(|i| i.what == What::Crash)
}

#[test]
fn the_hud_warns_of_an_impact_course_and_clears() {
    let rtf = 100.0;
    // 3 (and the quiet control): coast in Home's low orbit; there is no warning, ever.
    {
        let mut p = plane(Config::default(), 1, Order::Sparse, 1, 8).unwrap();
        for f in 0..400 {
            let v = frame(&mut p, rtf);
            assert!(v.impact.is_none() && !under_surface(&p), "frame {f}: a circular orbit above the surface holds no impact");
        }
    }
    // brake: reverse at level 4 until the course holds an impact
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 8).unwrap();
    p.u.input(p.u.now, word(2, 4)).unwrap();
    let (mut first, mut views) = (None, 0);
    for f in 0..2000 {
        let v = frame(&mut p, rtf);
        views += 1;
        // the warning is never later than the plan, and it is there exactly while the certificate holds
        assert_eq!(v.impact.is_some(), under_surface(&p), "frame {f}: the warning and the certificate differ");
        if planned_crash(&p) {
            assert!(v.impact.is_some(), "frame {f}: the plan holds a crash and the HUD does not warn");
        }
        if v.impact.is_some() {
            first = Some((f, v));
            break;
        }
    }
    let (f0, v0) = first.unwrap_or_else(|| panic!("braking for {views} frames never produced a warning"));
    let impact = v0.impact.clone().unwrap();
    println!("braked {f0} frames: {} (tick {}, at {:.3?}, {:.3e} c)", impact.sentence(), impact.tick, impact.at, impact.speed);
    assert_eq!(impact.body, "Home");
    assert_eq!(v0.doll, "Home");
    assert!(impact.seconds > 0.0 && (impact.at[0].powi(2) + impact.at[1].powi(2) - 1.0).abs() < 1e-9 && impact.speed > 0.0);
    assert!(impact.sentence().starts_with("Home's surface in "), "{}", impact.sentence());

    // The clearing: the same course, a second ship's life. Burn forward until the periapsis is above the surface.
    let mut q = plane(Config::default(), 1, Order::Sparse, 1, 8).unwrap();
    q.u.input(q.u.now, word(2, 4)).unwrap();
    for _ in 0..=f0 {
        frame(&mut q, rtf);
    }
    assert!(frame(&mut q, rtf).impact.is_some(), "the twin flight holds the same course");
    q.u.input(q.u.now, word(1, 4)).unwrap();
    let mut cleared = None;
    for f in 0..2000 {
        let v = frame(&mut q, rtf);
        assert_eq!(v.impact.is_some(), under_surface(&q), "burning out, frame {f}: the warning and the certificate differ");
        if v.impact.is_none() {
            cleared = Some(f);
            break;
        }
    }
    let cleared = cleared.expect("burning forward never cleared the warning");
    println!("burned forward {cleared} frames: the warning cleared");
    q.u.input(q.u.now, word(0, 4)).unwrap();
    // a further orbit (about 5,800 s of game time at 1.67 s a frame): alive, no warning
    for f in 0..4000 {
        let v = frame(&mut q, rtf);
        assert!(v.alive && v.impact.is_none(), "frame {f} after the clearing: alive {}, impact {:?}, loss {:?}", v.alive, v.impact, v.loss);
    }

    // Truth of the warning: coast from the first warning to the loss.
    p.u.input(p.u.now, word(0, 4)).unwrap();
    let mut last: Option<(Tick, View)> = None;
    let mut lost: Option<(usize, View)> = None;
    for f in 0..20_000 {
        let v = frame(&mut p, rtf);
        if !v.alive {
            lost = Some((f, v));
            break;
        }
        let impact = v.impact.clone().unwrap_or_else(|| panic!("coasting, frame {f}: the warning vanished with the ship alive"));
        if let Some((tick, prev)) = &last {
            // the countdown runs down with the game's clock (the tick the ship is read at)
            let ran = (v.tick - tick) as f64 * TICK_SECONDS;
            let down = prev.impact.as_ref().unwrap().seconds - impact.seconds;
            assert!((down - ran).abs() <= 1e-9 + 2e-3 * ran, "frame {f}: the countdown fell by {down} s while the game ran {ran} s");
        }
        last = Some((v.tick, v));
    }
    let (_, gone) = lost.expect("the ship coasted 20,000 frames on an impact course and was not lost");
    let (tick_before, before) = last.unwrap();
    let predicted = before.impact.unwrap();
    let loss = gone.loss.clone().unwrap();
    println!("lost: {loss}; the last warning said {} at tick {}", predicted.sentence(), predicted.tick);
    assert!(gone.impact.is_none(), "a wreck holds no warning");
    assert!(loss.starts_with("hit Home"), "{loss}");
    // The tick the ship is lost at, from replays of the same log: alive until the contact, lost at it (within 2 ms of game
    // time, the last warning's own age: kicks may have moved the course since).
    let log = p.u.inputs.clone();
    let alive_at = |t: Tick| {
        let mut q = plane(Config::default(), 1, Order::Sparse, 1, 8).unwrap();
        for &(at, keys) in &log {
            q.u.schedule(at, keys).unwrap();
        }
        q.u.settle(t);
        q.u.rec(q.player).alive
    };
    let tol = (predicted.tick - tick_before) / 1000 + 100;
    assert!(alive_at(predicted.tick - tol), "the ship is lost before the contact it was warned of (tick {})", predicted.tick - tol);
    assert!(!alive_at(predicted.tick + tol), "the ship is alive after the contact (tick {})", predicted.tick + tol);
}
