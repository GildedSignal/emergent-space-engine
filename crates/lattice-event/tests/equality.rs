//! The event core against the chronon reference: identical world and log digests (and, for
//! small cases, identical sorted events) on every generator, size, horizon, budget slicing
//! and snapshot restore.
use emergent_lattice::{
    chronon::Chronon,
    law::{Container, Response, Tick, World},
    worlds::{self, Rng},
    Log, Stepper,
};
use emergent_lattice_event::{crowded_axes, genesis, EventCore, CLASS_MIN};

fn chronon(w: &World, horizon: Tick, keep: bool) -> Chronon {
    let mut c = Chronon::new(w.clone(), keep).unwrap();
    c.run_to(horizon);
    c
}

fn event(w: &World, horizon: Tick, keep: bool, budget: u64) -> EventCore {
    let mut e = EventCore::new(w.clone(), keep).unwrap();
    while e.tick() < horizon {
        e.advance(horizon, budget);
    }
    e
}

#[test]
fn small_worlds_equal_chronon_event_by_event() {
    let cases = [
        ("mixed48", worlds::mixed(48, 1024, 1)),
        ("mixed120", worlds::mixed(120, 256, 2)),
        ("gas64", worlds::gas(64, 0.1, 1024, 256, 3)),
        ("gas40-dense", worlds::gas(40, 0.3, 64, 32, 4)),
        ("packed64", worlds::packed(64, 8, 2, 1024, 1, 5)),
        ("random64-pass", worlds::random(64, 400, 1024, 1, 6, Response::Pass)),
    ];
    for (name, w0) in cases {
        let horizon = 600;
        let c = chronon(&w0, horizon, true);
        let e = event(&w0, horizon, true, u64::MAX);
        assert!(c.log().contacts > 0, "{name} must have contacts");
        assert_eq!(e.log().sorted(), c.log().sorted(), "{name} events");
        assert_eq!(e.world(), c.world(), "{name} state");
        assert_eq!(e.outcome(), c.outcome(), "{name} digests");
    }
}

#[test]
fn sizes_equal_chronon() {
    let cases = [
        ("gas16", worlds::gas(16, 0.1, 1024, 256, 11), 1500),
        ("gas256", worlds::gas(256, 0.1, 1024, 256, 12), 1500),
        ("gas1024", worlds::gas(1024, 0.1, 1024, 256, 13), 1500),
        ("gas512-dense", worlds::gas(512, 0.3, 256, 128, 14), 800),
        ("random256-pass", worlds::random(256, 400, 1024, 1, 15, Response::Pass), 2000),
        ("random2048-pass", worlds::random(2048, 2000, 1024, 1, 16, Response::Pass), 2000),
        ("packed256", worlds::packed(256, 8, 2, 1024, 1, 17), 1500),
        ("packed1024", worlds::packed(1024, 6, 2, 512, 1, 18), 1500),
        ("mixed200", worlds::mixed(200, 512, 19), 1500),
        ("mixed700", worlds::mixed(700, 1024, 20), 1000),
    ];
    for (name, w0, horizon) in cases {
        let c = chronon(&w0, horizon, false);
        let e = event(&w0, horizon, false, u64::MAX);
        assert!(c.log().contacts > 0, "{name} must have contacts");
        assert_eq!(e.outcome(), c.outcome(), "{name} digests");
        assert_eq!((e.log().contacts, e.log().walls), (c.log().contacts, c.log().walls), "{name} counts");
    }
}

#[test]
fn horizons_from_64_to_131072_ticks() {
    let cases = [
        ("gas16", worlds::gas(16, 0.1, 1024, 256, 7)),
        ("mixed12", worlds::mixed(12, 1024, 8)),
        ("packed16", worlds::packed(16, 4, 1, 1024, 1, 9)),
        ("random16-pass", worlds::random(16, 100, 1024, 1, 10, Response::Pass)),
    ];
    for (name, w0) in cases {
        let mut c = Chronon::new(w0.clone(), false).unwrap();
        let mut e = EventCore::new(w0.clone(), false).unwrap();
        for h in [64, 1000, 10_000, 100_000, 131_072] {
            c.run_to(h);
            e.run_to(h);
            assert_eq!(e.outcome(), c.outcome(), "{name} at {h}");
        }
        assert!(c.log().contacts > 0, "{name} must have contacts");
        // A fresh run straight to the far horizon agrees too.
        assert_eq!(event(&w0, 131_072, false, u64::MAX).outcome(), c.outcome(), "{name} fresh");
    }
}

#[test]
fn budgets_do_not_change_the_outcome() {
    let cases = [
        ("mixed200", worlds::mixed(200, 512, 21), 1500),
        ("gas256", worlds::gas(256, 0.1, 1024, 256, 3), 1000),
        ("packed400", worlds::packed(400, 8, 2, 1024, 1, 22), 600),
    ];
    for (name, w0, horizon) in cases {
        let expected = chronon(&w0, horizon, false).outcome();
        for budget in [1u64, 7, 64, u64::MAX] {
            let e = event(&w0, horizon, false, budget);
            assert_eq!(e.outcome(), expected, "{name} budget {budget}");
            if budget == 1 {
                // Overshoot below one step: one neighbourhood (small here) or 5 × batch.
                let m = e.metrics();
                assert!(m.max_unit_ops <= (5 * m.max_batch).max(64), "{name}: unit {} ops, batch {}", m.max_unit_ops, m.max_batch);
                assert!(m.units > m.fired, "{name}: budget 1 must split the work");
            }
        }
    }
}

#[test]
fn restore_from_mid_run_snapshots() {
    let w0 = worlds::mixed(200, 512, 21);
    let expected = chronon(&w0, 1500, false).outcome();
    // Event → event, snapshot at a whole call.
    let mut first = EventCore::new(w0.clone(), false).unwrap();
    first.run_to(700);
    let mut second = EventCore::new(first.world(), false).unwrap();
    second.run_to(1500);
    let mut log = first.log().clone();
    log.merge(second.log());
    assert_eq!((second.world().digest(), log.digest()), expected, "event → event");
    // Snapshots taken between budget-7 units, wherever the pending work stands.
    let mut sliced = EventCore::new(w0.clone(), false).unwrap();
    let mut logs = Log::new(false);
    let mut restarts = 0;
    while sliced.tick() < 1500 {
        sliced.advance(1500, 7);
        if sliced.metrics().units.is_multiple_of(997) {
            logs.merge(sliced.log());
            sliced = EventCore::new(sliced.world(), false).unwrap();
            restarts += 1;
        }
    }
    logs.merge(sliced.log());
    assert!(restarts > 3, "restarts {restarts}");
    assert_eq!((sliced.world().digest(), logs.digest()), expected, "sliced restarts");
    // Across modes: chronon snapshot → event core, and back.
    let mut c = Chronon::new(w0.clone(), false).unwrap();
    c.run_to(500);
    let mut e = EventCore::new(c.world(), false).unwrap();
    e.run_to(1000);
    let mut c2 = Chronon::new(e.world(), false).unwrap();
    c2.run_to(1500);
    let mut log = c.log().clone();
    log.merge(e.log());
    log.merge(c2.log());
    assert_eq!((c2.world().digest(), log.digest()), expected, "chronon → event → chronon");
}

#[test]
fn the_elastic_tail_rebuilds_the_grid() {
    // Cells exactly at the validity bound for the genesis speeds: the first component past
    // it must grow the grid, and nothing may change.
    for (name, w0, horizon) in [
        ("gas256", worlds::gas(256, 0.1, 1024, 256, 3), 2000),
        ("mixed300", worlds::mixed(300, 1024, 23), 1500),
    ] {
        let expected = chronon(&w0, horizon, false).outcome();
        for budget in [7u64, u64::MAX] {
            let mut e = EventCore::with_cell_side(w0.clone(), false, 0).unwrap();
            while e.tick() < horizon {
                e.advance(horizon, budget);
            }
            assert!(e.rebuilds() > 0, "{name} must rebuild");
            assert_eq!(e.outcome(), expected, "{name} budget {budget}");
        }
    }
}

#[test]
fn crowded_axes_never_touch() {
    let (w0, horizon) = crowded_axes(256, 1024, 1);
    let c = chronon(&w0, horizon, false);
    let e = event(&w0, horizon, false, u64::MAX);
    assert_eq!(c.log().contacts, 0);
    assert!(e.classes() >= 1, "the downward columns share one velocity");
    assert_eq!(e.outcome(), c.outcome());
}

/// Three fleets (one velocity each, so co-moving classes) crossing each other and a loose
/// crowd in a box: members bounce, stop or pass, leave their class, hit walls.
fn fleets(q: i64, seed: u64) -> World {
    let mut rng = Rng(seed);
    let mut bodies = Vec::new();
    let fleet = |bodies: &mut Vec<_>, rng: &mut Rng, origin: [i64; 2], k: [i64; 2], mass: i64, count: i64| {
        for i in 0..count {
            let x = [(origin[0] + 5 * (i % 10)) * q + rng.range(-q / 2, q / 2), (origin[1] + 5 * (i / 10)) * q + rng.range(-q / 2, q / 2)];
            let response = match rng.next() % 8 {
                0 => Response::Stop,
                1 => Response::Pass,
                _ => Response::Bounce,
            };
            bodies.push((x, k, mass, response));
        }
    };
    fleet(&mut bodies, &mut rng, [10, 10], [q / 4, 0], 2, 100);
    fleet(&mut bodies, &mut rng, [120, 20], [-q / 4, q / 16], 1, 100);
    fleet(&mut bodies, &mut rng, [60, 110], [0, -q / 8], 3, 80);
    for _ in 0..60 {
        let x = [rng.range(5 * q, 175 * q), rng.range(5 * q, 175 * q)];
        let k = [rng.range(-q / 3, q / 3), rng.range(-q / 3, q / 3)];
        bodies.push((x, k, rng.range(1, 4), Response::Bounce));
    }
    let bodies = bodies.into_iter().enumerate().map(|(i, (x, k, m, r))| genesis(i as u64 + 1, x, k, m, q, r)).collect();
    World::new(q, Some(Container { min: [0, 0], max: [180 * q, 180 * q] }), bodies).expect("fleet world")
}

#[test]
fn velocity_classes_equal_chronon() {
    for (seed, q) in [(1u64, 1024i64), (2, 256)] {
        let (w0, horizon) = (fleets(q, seed), 3000);
        let c = chronon(&w0, horizon, true);
        let mut probe = EventCore::new(w0.clone(), false).unwrap();
        probe.run_to(1);
        assert!(probe.classes() >= 3, "fleets of {} must form classes (min {CLASS_MIN})", probe.classes());
        assert!(c.log().contacts > 100, "the fleets must collide: {}", c.log().contacts);
        for budget in [7u64, u64::MAX] {
            let e = event(&w0, horizon, true, budget);
            assert_eq!(e.log().sorted(), c.log().sorted(), "seed {seed} budget {budget} events");
            assert_eq!(e.world(), c.world(), "seed {seed} budget {budget} state");
        }
        let mut first = EventCore::new(w0.clone(), false).unwrap();
        first.run_to(1200);
        let mut second = EventCore::new(first.world(), false).unwrap();
        second.run_to(horizon);
        let mut log = first.log().clone();
        log.merge(second.log());
        assert_eq!((second.world().digest(), log.digest()), c.outcome(), "seed {seed} restore");
    }
}

#[test]
fn dispersal_regrows_the_cells() {
    // A dense unbounded Pass world spreads out: the cells must follow the density (feedback
    // and drift rebuilds) and nothing may change.
    for (n, area, seed) in [(64u64, 100i64, 31u64), (200, 400, 32)] {
        let w0 = worlds::random(n, area, 1024, 1, seed, Response::Pass);
        let mut c = Chronon::new(w0.clone(), false).unwrap();
        for budget in [7u64, u64::MAX] {
            let mut e = EventCore::new(w0.clone(), false).unwrap();
            for h in [1000, 20_000, 100_000] {
                c.run_to(h);
                while e.tick() < h {
                    e.advance(h, budget);
                }
                assert_eq!(e.outcome(), c.outcome(), "n {n} budget {budget} at {h}");
            }
            assert!(e.rebuilds() >= 3, "n {n}: {} rebuilds", e.rebuilds());
            c = Chronon::new(w0.clone(), false).unwrap();
        }
    }
}
