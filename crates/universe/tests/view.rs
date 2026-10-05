//! The view is a pure read of the state: the crossing it finds is a property of the state and not of where
//! the search started, and the keys held show within the frame, not at the next kick. Every test finishes
//! within a few seconds.
use emergent_universe::fleet::Order;
use emergent_universe::observe::root_state;
use emergent_universe::scenario::{plane, Plane};
use emergent_universe::view::{gather, gather_cached, View, ViewCache, TICK_SECONDS};
use emergent_universe::{Budget, Config};

fn angle(v: &View) -> f64 {
    v.heading[1].atan2(v.heading[0])
}
fn wrap(a: f64) -> f64 {
    (a + std::f64::consts::PI).rem_euclid(std::f64::consts::TAU) - std::f64::consts::PI
}

/// Each emitter's crossing is the last tick whose light has arrived: `g(t) = t + |x(t) − X| − T` is `≤ 0` at
/// the crossing and `> 0` one tick later (checked here by a second computation, plain readouts), and a cold
/// search, a warm one and one warmed by an unrelated moment of the universe all end on it: the same view.
#[test]
fn a_crossing_is_a_property_of_the_state_and_not_of_the_cache() {
    let mut p = plane(Config::default(), 3, Order::Sparse, 1, 12).unwrap();
    let frame = 340_000i64; // one 60 Hz frame at 100x
    let start = 2_000_000_000i64;
    p.u.settle(start);
    let mut stale = ViewCache::default();
    {
        // warmed far from where it will be used
        let mut q = plane(Config::default(), 3, Order::Sparse, 1, 12).unwrap();
        q.u.settle(500_000_000);
        gather_cached(&q.u, &q.names, &mut stale).unwrap();
    }
    let mut warm = ViewCache::default();
    let (mut cold_reads, mut warm_reads, mut bodies) = (0u64, 0u64, 0usize);
    for f in 0..40 {
        let t = start + f * frame;
        p.u.settle(t);
        p.u.now = t;
        let cold = gather(&p.u, &p.names).unwrap();
        let hot = gather_cached(&p.u, &p.names, &mut warm).unwrap();
        assert_eq!(cold, hot, "frame {f}: a warm cache changed the view");
        let mut c = ViewCache::default();
        let fresh = gather_cached(&p.u, &p.names, &mut c).unwrap();
        assert_eq!(cold, fresh, "frame {f}");
        if f == 0 {
            cold_reads = c.readouts;
            warm_reads = warm.readouts;
            let s = gather_cached(&p.u, &p.names, &mut stale).unwrap();
            assert_eq!(cold, s, "a cache warmed at another time changed the view");
        } else {
            warm_reads = warm_reads.min(warm.readouts);
        }
        bodies = cold.seen.iter().filter(|s| s.id < p.u.n_bodies()).count();
        // The bracket, from plain readouts.
        let ctx = p.u.ctx();
        let (xo, _) = root_state(&ctx, p.player, t).unwrap();
        for s in cold.seen.iter().filter(|s| s.id < p.u.n_bodies()) {
            let te = (t as f64 - s.age / TICK_SECONDS).round() as i64;
            let g = |tick: i64| {
                let (x, _) = root_state(&ctx, s.id, tick).unwrap();
                tick as f64 + ((x[0] - xo[0]).powi(2) + (x[1] - xo[1]).powi(2)).sqrt() - t as f64
            };
            assert!(g(te) <= 1e-5 && g(te + 1) > -1e-5, "frame {f}, {}: g({te}) = {}, g({}) = {}", s.name, g(te), te + 1, g(te + 1));
        }
    }
    println!("{bodies} bodies: {cold_reads} readouts to find every crossing cold, {warm_reads} warm");
    assert!(cold_reads >= 2 * bodies as u64, "a cold search takes several readouts per body");
    assert!(warm_reads as f64 <= 1.3 * bodies as f64, "a warm search takes about one: {warm_reads} for {bodies} bodies");
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
