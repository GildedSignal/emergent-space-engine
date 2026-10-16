//! The plane as a whole: one digest independent of budget, threads and observation; the fleet's
//! battle bit-identical across steppers; the player's thrust against the work it does; bounded work
//! per frame. Every test finishes within 60 s.
use emergent_universe::fleet::Order;
use emergent_universe::scenario::{plane, Plane};
use emergent_universe::view::gather;
use emergent_universe::{Budget, Config};

const MEMBERS: u64 = 24;
const HORIZON: i64 = 2_000_000_000; // 2.7 hours of game time
/// Short burns (10 s each at 0.35 g): forward, forward and right, reverse, left. A long burn from a low
/// orbit puts the periapsis under the surface, and a lost player has no clock to read.
const INPUTS: [(i64, u8); 8] = [(10_000_000, 1), (12_000_000, 0), (300_000_000, 9), (302_000_000, 0), (900_000_000, 2), (902_000_000, 0), (1_200_000_000, 4), (1_201_000_000, 0)];

/// Run a plane to `HORIZON` the way a player's frames would: `step`-tick frames, `budget` events
/// each, with the scripted inputs at their ticks, and settle at the end (the canonical cut).
fn run(order: Order, threads: usize, budget: Budget, step: i64, observe: bool, inputs: &[(i64, u8)]) -> (Plane, String) {
    let mut p = plane(Config::default(), 7, order, threads, MEMBERS).unwrap();
    let mut next_input = 0;
    while p.u.now < HORIZON {
        let mut target = (p.u.now + step).min(HORIZON);
        if let Some(&(t, _)) = inputs.get(next_input) {
            target = target.min(t.max(p.u.now + 1));
        }
        let a = p.u.advance(target, budget);
        p.u.now = a.horizon.max(p.u.now);
        if observe {
            let _ = gather(&p.u, &p.names);
        }
        if let Some(&(t, keys)) = inputs.get(next_input) {
            if p.u.now >= t {
                p.u.input(t, keys).unwrap();
                next_input += 1;
            }
        }
        // A frame budget that cannot ever finish its mandatory work would never end this loop.
        if a.events == 0 && a.horizon <= p.u.now - 0 && a.overflow {
            p.u.settle(target);
        }
    }
    p.u.settle(HORIZON);
    let d = p.u.digest();
    (p, d)
}

#[test]
fn the_same_digest_at_every_budget_and_thread_count() {
    let reference = run(Order::Sparse, 1, Budget::unlimited(), HORIZON, false, &INPUTS);
    let s = reference.0.u.stats;
    println!("reference: {} events (kicks {}, handoffs {}, slices {}, decisions {}), digest {}", s.events(), s.kicks, s.handoffs, s.slices, s.decisions, &reference.1[..16]);
    assert!(s.kicks > 1000 && s.decisions == INPUTS.len() as u64 && s.slices > 100);
    for (threads, events, step) in [(1usize, 13u64, 3_000_000i64), (2, 200, 40_000_000), (4, 7, 1_000_000), (8, 64, 100_000_000), (3, u64::MAX, 7_000_000)] {
        let (p, d) = run(Order::Sparse, threads, Budget::events(events), step, false, &INPUTS);
        println!("threads {threads}, {events} events per frame of {step} ticks: {} events, digest {}", p.u.stats.events(), &d[..16]);
        assert_eq!(d, reference.1, "threads {threads}, budget {events}");
    }
    // Controls: the digest must be able to fail. Another input log, and another seed, give another digest.
    let other = run(Order::Sparse, 1, Budget::unlimited(), HORIZON, false, &INPUTS[..3]);
    assert_ne!(other.1, reference.1, "a different player gives a different universe");
    let mut q = plane(Config::default(), 8, Order::Sparse, 1, MEMBERS).unwrap();
    q.u.settle(HORIZON);
    assert_ne!(q.u.digest(), reference.1);
}

#[test]
fn observation_never_changes_the_digest() {
    let quiet = run(Order::Sparse, 1, Budget::events(50), 20_000_000, false, &INPUTS);
    let watched = run(Order::Sparse, 1, Budget::events(50), 20_000_000, true, &INPUTS);
    assert_eq!(quiet.1, watched.1, "gathering the view every frame changed the universe");
    // And reading anything at any tick, after the fact, changes nothing either.
    let before = watched.0.u.digest();
    let v = gather(&watched.0.u, &watched.0.names).unwrap();
    for i in 0..watched.0.u.n_bodies() {
        for t in [0i64, 5_000_000, 700_000_000, HORIZON] {
            let _ = emergent_universe::observe::root_state(&watched.0.u.ctx(), i, t);
        }
    }
    assert_eq!(watched.0.u.digest(), before);
    println!("view at tick {}: {} things arrive; observer clock rate {:.12}, proper {:.3} s of {:.3} s", v.tick, v.seen.len(), v.rate, v.proper_seconds, v.coordinate_seconds);
    assert!(v.seen.len() > 30, "the star, the planets, the moon, the ships and the fleet all arrive: {}", v.seen.len());
    assert!(v.rate < 1.0 && v.rate > 0.999999, "{}", v.rate);
}

#[test]
fn the_fleets_battle_is_bit_identical_across_steppers() {
    let h = 3_000_000;
    let a = {
        let mut p = plane(Config::default(), 3, Order::Dense, 1, MEMBERS).unwrap();
        p.u.settle(h);
        p
    };
    let b = {
        let mut p = plane(Config::default(), 3, Order::Sparse, 2, MEMBERS).unwrap();
        p.u.settle(h);
        p
    };
    let (fa, fb) = (&a.u.fleets[0], &b.u.fleets[0]);
    println!("fleet: {} contacts, {} epochs, {} anchors", fa.contacts(), fa.epochs(), fa.anchors());
    assert!(fa.contacts() > 0, "the battle must happen");
    assert_eq!(fa.outcome(), fb.outcome(), "lockstep and sparse give the same world, log and tide digests");
    assert_eq!(a.u.digest(), b.u.digest());
}

#[test]
fn a_burn_changes_the_energy_by_the_work_done() {
    let mut p = plane(Config::default(), 5, Order::Sparse, 1, 8).unwrap();
    let me = p.player;
    let alpha = 2f64.powi(Config::default().thrust_log2); // rapidity per tick
    p.u.settle(1000);
    let energy = |p: &Plane, t: i64| {
        let (x, v) = p.u.rec(me).b.cartesian(t).unwrap();
        let f = |s: emergent_space::orbit::Scalar| emergent_universe::num::to_f64(s);
        let (x, v) = ([f(x[0]), f(x[1])], [f(v[0]), f(v[1])]);
        (0.5 * (v[0] * v[0] + v[1] * v[1]) - 1.0 / (x[0] * x[0] + x[1] * x[1]).sqrt(), v)
    };
    let t0 = 2_000_000;
    p.u.settle(t0);
    p.u.input(t0, 1).unwrap();
    let (e0, _) = energy(&p, t0);
    // Burn along the heading (the x axis) for 20 s of game time, sampling the work F·v.
    let (mut work, mut t) = (0.0, t0);
    let t1 = t0 + 4_000_000;
    let dt = 20_000;
    let (mut last_v, mut last_t) = (energy(&p, t0).1, t0);
    while t < t1 {
        t += dt;
        p.u.settle(t);
        let (_, v) = energy(&p, t);
        // the heading is fixed (no turn key): thrust is along +x; trapezoid of alpha * vx
        work += alpha * 0.5 * (last_v[0] + v[0]) * (t - last_t) as f64;
        last_v = v;
        last_t = t;
    }
    p.u.input(t1, 0).unwrap();
    let (e1, _) = energy(&p, t1);
    let d = e1 - e0;
    println!("burn: energy changed by {d:.4e}, the work done {work:.4e}");
    assert!(((d - work) / work).abs() < 0.03, "ΔE {d:e} against work {work:e}");
    assert!(work.abs() > 1e-12, "the burn must do work");
}

#[test]
fn work_per_frame_is_bounded_and_overflow_is_a_dip_not_a_hitch() {
    let mut p = plane(Config::default(), 11, Order::Sparse, 1, MEMBERS).unwrap();
    // A tiny budget and a huge appetite: the frame resolves at most a handful of events, the
    // presented time stays behind its target (the real-time factor dips), and nothing blocks.
    let mut dips = 0;
    let mut last = 0;
    for _ in 0..200 {
        let f = p.u.frame(1.0 / 60.0, 5_000_000.0, Budget::events(3));
        assert!(f.presented >= last && f.presented <= f.target, "the presented time never runs ahead of the work");
        assert!(f.events <= 3 + 64, "a frame's work is bounded by its budget (plus the items it pulls): {}", f.events);
        dips += f.overflow as u32;
        last = f.presented;
    }
    println!("overflow frames: {dips} of 200");
    assert!(dips > 0, "the scene must overflow a 3-event budget at 5e6x");
    // The same universe, unthrottled, reaches the same state at the same cut.
    let h = p.u.now;
    let mut q = plane(Config::default(), 11, Order::Sparse, 1, MEMBERS).unwrap();
    q.u.settle(h);
    p.u.settle(h);
    assert_eq!(p.u.digest(), q.u.digest(), "the budget changed when work was done, never what");
}

#[test]
fn encounters_are_exact_and_sit_behind_one_seam() {
    use emergent_universe::encounter::{Encounter, Encounters};
    use emergent_universe::num::s;
    use emergent_universe::scenario::restricted;
    use emergent_universe::{Kind, OrbitSpec};
    use emergent_space::orbit::Scalar;
    let mut w = restricted(-10, 527_000_000, 49_000, &[], 1).unwrap();
    let edge = emergent_universe::num::to_f64(w.u.dolls[1].edge);
    let p = s((edge * 0.1) as i64);
    // Three bodies on one circle about the planet: the player; one 30 km ahead (near, not touching);
    // one 100 m ahead of that... and one that touches (50 planet-units ≈ 70 m ahead of the player).
    let r = Scalar::raw(34, 0).unwrap(); // 34 planet units = 49 m
    let spec = |dq: u32| OrbitSpec { doll: 1, periapsis: p, e_q48: 0, clockwise: false, angle: (1 << 30) + dq, phase: 0 };
    let me = w.u.add_body(Kind::Player, spec(0), r).unwrap();
    let near = w.u.add_body(Kind::Ship, spec(4100), r).unwrap();
    let touching = w.u.add_body(Kind::Ship, spec(1), r).unwrap();
    w.u.start().unwrap();
    w.u.settle(40_000_000_000);
    let (n, contacts) = (w.u.stats.encounters, w.u.contacts);
    println!("encounters {n}, contacts {contacts}, logged {}", w.u.enc_log.len());
    assert!(n > 0 && contacts > 0 && contacts < n, "the neighbour is found, and only the touching body is in contact");
    assert!(w.u.enc_log.iter().any(|e: &Encounter| e.b == near && !e.contact) && w.u.enc_log.iter().any(|e| e.b == touching && e.contact));
    assert!(w.u.enc_log.iter().all(|e| e.a == me));
    // The seam: another finder replaces the check without touching the rest.
    struct Nothing;
    impl Encounters for Nothing {
        fn find(&self, _: &emergent_universe::ctx::Ctx, _: usize, _: i64, _: i64) -> Vec<Encounter> {
            Vec::new()
        }
    }
    let before = w.u.stats.encounters;
    w.u.set_encounters(Box::new(Nothing));
    w.u.settle(60_000_000_000);
    assert_eq!(w.u.stats.encounters, before, "a replaced finder finds what it finds");
}
