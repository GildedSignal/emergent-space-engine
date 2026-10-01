//! The view is a pure read of the state, and the keys held show within the frame, not at the next kick.
//! Every test finishes within a few seconds.
use emergent_universe::fleet::Order;
use emergent_universe::scenario::{plane, Plane};
use emergent_universe::view::{gather, View};
use emergent_universe::{Budget, Config};

fn angle(v: &View) -> f64 {
    v.heading[1].atan2(v.heading[0])
}
fn wrap(a: f64) -> f64 {
    (a + std::f64::consts::PI).rem_euclid(std::f64::consts::TAU) - std::f64::consts::PI
}

/// Holding a turn key changes the heading the view shows on the very next frame, by the turn the law owes
/// (`2^turn_log2` turns per unit of proper time), at 1x and at 100x; holding forward changes the velocity by
/// the burn owed; and the stored state is never more than one frame behind the keys.
fn hold(rtf: f64, keys: u8) -> (Plane, Vec<View>, Vec<i64>) {
    let mut p = plane(Config::default(), 2, Order::Sparse, 1, 8).unwrap();
    p.u.input(0, keys).unwrap();
    let (mut views, mut ticks) = (Vec::new(), Vec::new());
    for _ in 0..30 {
        let f = p.u.frame(1.0 / 60.0, rtf, Budget::unlimited());
        ticks.push(f.ticks);
        // every key held is re-asserted at the frame's start: the stored state is within a frame
        let th = p.u.rec(p.player).thrust.unwrap();
        if keys != 0 {
            assert!(p.u.now - th.since <= f.ticks + 1, "the stored thrust is {} ticks behind the presented tick (a frame is {})", p.u.now - th.since, f.ticks);
        }
        views.push(gather(&p.u, &p.names).unwrap());
    }
    (p, views, ticks)
}

#[test]
fn holding_turn_changes_the_heading_on_the_next_frame() {
    for rtf in [1.0, 100.0] {
        let (p, views, ticks) = hold(rtf, 4);
        let per_tick = std::f64::consts::TAU * 2f64.powi(Config::default().turn_log2);
        let mut last = 0.0; // heading 0 at the start
        for (f, (v, &dt)) in views.iter().zip(&ticks).enumerate() {
            let a = angle(v);
            let d = wrap(a - last);
            let want = -per_tick * dt as f64 * v.rate;
            assert!(want != 0.0 && ((d - want) / want).abs() < 0.02, "rtf {rtf}, frame {f}: heading turned by {d:e}, the law owes {want:e}");
            last = a;
        }
        println!("rtf {rtf}: after 30 frames the heading is {:.4} deg (stored: {:.4})", angle(views.last().unwrap()).to_degrees(), p.u.rec(p.player).thrust.unwrap().heading as f64 / 4294967296.0 * 360.0 - 360.0);
    }
}

#[test]
fn holding_forward_changes_the_velocity_on_the_next_frame() {
    for rtf in [1.0, 100.0] {
        let (_, thrusting, ticks) = hold(rtf, 1);
        let (_, coasting, _) = hold(rtf, 0);
        let alpha = 2f64.powi(Config::default().thrust_log2);
        let mut elapsed = 0.0;
        for (f, ((a, b), &dt)) in thrusting.iter().zip(&coasting).zip(&ticks).enumerate().take(3) {
            elapsed += dt as f64 * a.rate;
            // the heading is +x in the doll's frame, so the burn is along x (the velocities are in the root frame)
            let dv = a.beta[0] - b.beta[0];
            assert!(((dv - alpha * elapsed) / (alpha * elapsed)).abs() < 0.02, "rtf {rtf}, frame {f}: velocity changed by {dv:e}, the burn owed is {:e}", alpha * elapsed);
        }
    }
}

/// A pure read: looking at the view writes nothing, and the keys held are in the input log (one decision per
/// frame), so replaying the log gives the same universe.
#[test]
fn the_keys_held_are_in_the_input_log_and_replay_to_the_same_universe() {
    let mut p = plane(Config::default(), 4, Order::Sparse, 1, 8).unwrap();
    for f in 0..40 {
        match f {
            5 => p.u.input(p.u.now, 9).unwrap(),
            20 => p.u.input(p.u.now, 2).unwrap(),
            30 => p.u.input(p.u.now, 0).unwrap(),
            _ => {}
        }
        p.u.frame(1.0 / 60.0, 100.0, Budget::events(50));
        let _ = gather(&p.u, &p.names);
    }
    let log = p.u.inputs.clone();
    assert!(log.len() >= 26, "a decision at every frame while a key is held (frames 5 to 29), and the three presses: {}", log.len());
    let h = p.u.now;
    p.u.settle(h);
    let want = p.u.digest();
    let mut q = plane(Config::default(), 4, Order::Sparse, 1, 8).unwrap();
    for &(t, keys) in &log {
        q.u.settle(t);
        q.u.input(t, keys).unwrap();
    }
    q.u.settle(h);
    assert_eq!(q.u.digest(), want, "the input log did not reproduce the universe");
}
