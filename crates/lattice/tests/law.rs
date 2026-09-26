//! The contract's own checks: predicates against brute scans, the grid against all pairs,
//! component locality, the ledgers, slicing and snapshot-restore invariance.
use emergent_lattice::{
    chronon::Chronon,
    law::{self, Body, Response, World},
    worlds::{self, Rng},
    Event, Kind, Log, Stepper,
};
use std::collections::HashMap;

#[test]
fn first_hit_equals_brute_scan() {
    let mut rng = Rng(7);
    let mut hits = 0;
    for _ in 0..200_000 {
        let d = [rng.range(-300, 300) as i128, rng.range(-300, 300) as i128];
        let w = [rng.range(-20, 20) as i128, rng.range(-20, 20) as i128];
        let reach = rng.range(1, 40) as i128;
        let brute = (0..2000i64).find(|&u| law::hit([d[0] + w[0] * u as i128, d[1] + w[1] * u as i128], w, reach));
        assert_eq!(law::first_hit(d, w, reach), brute, "d {d:?} w {w:?} reach {reach}");
        hits += brute.is_some() as u32;
    }
    assert!(hits > 1000, "the scan must exercise hits, got {hits}");
}

#[test]
fn first_wall_equals_brute_scan() {
    let mut rng = Rng(11);
    for _ in 0..100_000 {
        let lo = [0, 0];
        let hi = [rng.range(1, 400), rng.range(1, 400)];
        let x = [rng.range(-20, 420), rng.range(-20, 420)];
        let k = [rng.range(-9, 9), rng.range(-9, 9)];
        let brute = (1..2000i64).find(|&s| law::at_wall([x[0] + k[0] * s, x[1] + k[1] * s], k, lo, hi));
        assert_eq!(law::first_wall(x, k, lo, hi), brute, "x {x:?} k {k:?} hi {hi:?}");
    }
}

/// All pairs every chronon, no grid: the plainest reading of the law.
fn brute(mut w: World, horizon: i64) -> (World, Log) {
    let mut consumed: HashMap<(usize, usize), (u32, u32)> = HashMap::new();
    let mut log = Log::new(true);
    for t in w.tick + 1..=horizon {
        let n = w.bodies.len();
        let mut pairs = vec![];
        for i in 0..n {
            for j in i + 1..n {
                let (a, b) = (&w.bodies[i], &w.bodies[j]);
                if consumed.get(&(i, j)) == Some(&(a.rev, b.rev)) {
                    continue;
                }
                if law::hit(law::sub(b.x, a.x), law::sub(b.k, a.k), (a.radius + b.radius) as i128) {
                    pairs.push((i, j));
                }
            }
        }
        for b in w.bodies.iter_mut() {
            b.x = [b.x[0] + b.k[0], b.x[1] + b.k[1]];
        }
        let walls: Vec<bool> = w
            .bodies
            .iter()
            .map(|b| {
                b.response == Response::Bounce
                    && w.container.is_some_and(|c| {
                        let (lo, hi) = c.inset(b.radius);
                        law::at_wall(b.x, b.k, lo, hi)
                    })
            })
            .collect();
        let (container, lw, q) = (w.container, w.law, w.q);
        law::respond(lw, q, &mut w.bodies, &pairs, &walls, container.as_ref(), &mut w.wall_momentum);
        for &(i, j) in &pairs {
            consumed.insert((i, j), (w.bodies[i].rev, w.bodies[j].rev));
            log.record(Event { tick: t, kind: Kind::Contact, a: w.bodies[i].id, b: w.bodies[j].id });
        }
        for (i, &on) in walls.iter().enumerate() {
            if on {
                log.record(Event { tick: t, kind: Kind::Wall, a: w.bodies[i].id, b: 0 });
            }
        }
        w.tick = t;
    }
    w.consumed = consumed
        .iter()
        .map(|(&(i, j), &(ra, rb))| law::Consumed { a: w.bodies[i].id, b: w.bodies[j].id, rev_a: ra, rev_b: rb })
        .collect();
    (w.canonical(), log)
}

#[test]
fn grid_equals_all_pairs() {
    let cases = [
        worlds::mixed(48, 1024, 1),
        worlds::mixed(120, 256, 2),
        worlds::gas(64, 0.1, 1024, 256, 3),
        worlds::gas(40, 0.3, 64, 32, 4),
        worlds::packed(64, 8, 2, 1024, 1, 5),
        worlds::random(64, 400, 1024, 1, 6, Response::Pass),
        worlds::gas(64, 0.1, 1024, 256, 7).with_law(law::Law::Relativistic).unwrap(),
        worlds::mixed(48, 1024, 8).with_law(law::Law::Relativistic).unwrap(),
    ];
    for (n, w0) in cases.into_iter().enumerate() {
        let horizon = 600;
        let (bw, blog) = brute(w0.clone(), horizon);
        let mut c = Chronon::new(w0, true).unwrap();
        c.run_to(horizon);
        assert!(blog.contacts > 0, "case {n} must have contacts");
        assert_eq!(c.log().sorted(), blog.sorted(), "case {n} events");
        assert_eq!(c.world(), bw, "case {n} state");
        assert_eq!(c.outcome(), (bw.digest(), blog.digest()), "case {n} digests");
    }
}

#[test]
fn components_resolve_independently() {
    // Two separate three-body pile-ups in one chronon, plus a wall body.
    let q = 64;
    let mk = |id: u64, x: [i64; 2], k: [i64; 2], m: i64| Body { id, x, k, mass: m, radius: q, response: Response::Bounce, residual: id as i64 - 3, rev: 0, carry: [0, 0] };
    let bodies = vec![
        mk(1, [0, 0], [30, 3], 1),
        mk(2, [120, 5], [0, 0], 3),
        mk(3, [240, -7], [-29, 1], 2),
        mk(4, [5000, 0], [17, -5], 2),
        mk(5, [5125, 9], [-11, 2], 1),
        mk(6, [5250, 0], [-23, 0], 4),
    ];
    let pairs = vec![(0, 1), (1, 2), (3, 4), (4, 5)];
    let walls = vec![false; 6];
    let mut whole = bodies.clone();
    let mut wm = [0, 0];
    law::resolve(&mut whole, &pairs, &walls, None, &mut wm);
    let mut split = bodies.clone();
    let (left, right) = split.split_at_mut(3);
    law::resolve(left, &[(0, 1), (1, 2)], &[false; 3], None, &mut wm);
    law::resolve(right, &[(0, 1), (1, 2)], &[false; 3], None, &mut wm);
    assert_eq!(whole, split);
    assert_ne!(whole, bodies, "the impulses must change something");
}

#[test]
fn ledgers_are_exact_and_the_carry_is_bounded() {
    let w0 = worlds::gas(256, 0.1, 1024, 256, 9);
    let mut c = Chronon::new(w0.clone(), false).unwrap();
    c.run_to(4096);
    let w = c.world();
    assert!(c.log().contacts > 1000);
    assert_eq!(w.energy() - w0.energy(), w.residual(), "energy ledger");
    let (p0, p1) = (w0.momentum(), w.momentum());
    assert_eq!([p1[0] - p0[0] + w.wall_momentum[0] as i128, p1[1] - p0[1] + w.wall_momentum[1] as i128], [0, 0], "momentum ledger");
    // Frozen before running: one body owes at most four one-quantum energy errors, 4·2·|k|max.
    let kmax = w0.bodies.iter().map(|b| b.k[0].abs().max(b.k[1].abs())).max().unwrap() as i128 * 2;
    let bound = 4 * 2 * kmax;
    assert!(w.bodies.iter().all(|b| (b.residual as i128).abs() <= bound), "carry bounded by {bound}");
    let (lo, hi) = (0, 0);
    let _ = (lo, hi);
    let side = w0.container.unwrap().max[0];
    assert!(w.bodies.iter().all(|b| b.x[0] >= -1024 && b.x[1] >= -1024 && b.x[0] <= side + 1024 && b.x[1] <= side + 1024), "contained within one chronon of travel");
}

/// The relativistic law in the chronon reference: nothing massive reaches c, the
/// 4-momentum ledgers are exact, and slicing does not change the outcome.
#[test]
fn relativistic_gas_keeps_c_and_exact_ledgers() {
    use emergent_lattice::relativity::{carried, total};
    // A hot gas with heavy and light ships, so Newtonian bounces would break c.
    let mut w0 = worlds::mixed(256, 256, 31);
    for b in &mut w0.bodies {
        b.response = Response::Bounce;
        b.k = [b.k[0] * 5 / 4, b.k[1] * 5 / 4]; // up to 0.88c at genesis
    }
    let w0 = w0.with_law(law::Law::Relativistic).unwrap();
    let mut c = Chronon::new(w0.clone(), false).unwrap();
    c.run_to(4000);
    let w = c.world();
    assert!(c.log().contacts > 1000);
    assert!(w.bodies.iter().all(|b| (b.k[0] as i128).pow(2) + (b.k[1] as i128).pow(2) < (w.q as i128).pow(2)));
    let (t0, t1, cr) = (total(&w0), total(&w), carried(&w));
    assert_eq!(t1[0] - t0[0], cr[0], "energy ledger");
    for a in 0..2 {
        assert_eq!(t1[1 + a] - t0[1 + a] + w.wall_momentum[a] as i128, cr[1 + a], "momentum ledger {a}");
    }
    let mut s = Chronon::new(w0, false).unwrap();
    while s.tick() < 4000 {
        s.advance(4000, 777);
    }
    assert_eq!(s.outcome(), c.outcome());
}

#[test]
fn slicing_and_restore_do_not_change_the_outcome() {
    let w0 = worlds::mixed(200, 512, 21);
    let mut whole = Chronon::new(w0.clone(), false).unwrap();
    whole.run_to(1500);
    let expected = whole.outcome();
    for budget in [1u64, 97, 5000] {
        let mut s = Chronon::new(w0.clone(), false).unwrap();
        while s.tick() < 1500 {
            s.advance(1500, budget);
        }
        assert_eq!(s.outcome(), expected, "budget {budget}");
    }
    // Restore from a mid-run snapshot and merge the two logs.
    let mut first = Chronon::new(w0, false).unwrap();
    first.run_to(700);
    let mut second = Chronon::new(first.world(), false).unwrap();
    second.run_to(1500);
    let mut log = first.log().clone();
    log.merge(second.log());
    assert_eq!((second.world().digest(), log.digest()), expected);
}
