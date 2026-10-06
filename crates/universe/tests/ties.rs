//! Ties (docs/law.md, 5 October; lab run 20261005-0543-redteam-6254): events at the same root-clock time that share a
//! body are one batch, resolved by the contact law's canonical batch rule; events that share no body commute; the
//! queue's key is (time, smallest body id, kind), so every schedule, budget and thread count pops the same sequence.
//!
//! **Frozen before the first run.** In this crate that is three claims, each on a scene built to tie:
//! 1. *Independent events commute.* Twelve ships, six places on one orbit shape each taken twice (two ships in the same
//!    state have the same physical step under the motion law v2, which is a function of the state, so every kick and
//!    boundary of the two is on the same tick: the tie is by construction; before v2 an orbit shape was a step, and twelve
//!    places on it tied), made in six different orders (so with twelve different assignments of ids): each ship's whole
//!    history is the same record whichever order it was made in, whichever other ships exist, on 1 and 4 threads, under
//!    any budget and frame size.
//! 2. *Events that read a body at its own tick read it in the order of their keys.* A third planet (a body stepped by its
//!    own orbit's period, as the planets are; a ship's step is a function of its state under the motion law v2, so none
//!    ties with a planet by construction) on the first planet's own orbit shape ties with it at every event. Made after the planet it reads the planet after the planet's event
//!    (the smaller id goes first); made before, it reads it before: each assignment of ids is one history on every
//!    schedule, and the two assignments are two histories (the control: the key is observable, so it can fail).
//! 3. *A same-epoch three-body contact is one batch.* Three members of the fleet's frame, the outer two closing on the
//!    middle one so that both pairs touch in the same chronon (masses 1, 3 and 2: the order of the impulses is
//!    observable), give one digest in both orders of the battle, on 1 and 4 threads, under any budget, and the
//!    contacts happened.
use emergent_lattice::law::{Body, Law, Response, World};
use emergent_space::orbit::Scalar;
use emergent_universe::fleet::{Order, Q};
use emergent_universe::num::s;
use emergent_universe::scenario::{plane_with, STAR_RADIUS};
use emergent_universe::universe::Universe;
use emergent_universe::{Budget, Config, Kind, OrbitSpec};

const SEP: i64 = 527_000_000;

fn spec(angle: u32, phase: u32) -> OrbitSpec {
    OrbitSpec { doll: 0, periapsis: s(SEP * 3 / 2), e_q48: (1u64 << 48) / 10, clockwise: false, angle, phase }
}

/// A star, a planet in a doll (so the ships have something to read), and ships made in `order` from `places`
/// (angle, phase): the ship made k-th has id `1 + k`. Returns the universe and the ids in `places` order.
fn scene(places: &[(u32, u32)], order: &[usize]) -> (Universe, Vec<usize>) {
    let mut u = Universe::new(s(STAR_RADIUS), Config::default());
    let planet = u.add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: s(SEP), e_q48: 0, clockwise: false, angle: 0, phase: 0 }, Scalar::ZERO).unwrap();
    u.add_doll("planet", planet, -10, Scalar::raw(49_000, 10).unwrap()).unwrap();
    let mut ids = vec![0; places.len()];
    for &k in order {
        ids[k] = u.add_body(Kind::Ship, spec(places[k].0, places[k].1), Scalar::ZERO).unwrap();
    }
    u.start().unwrap();
    (u, ids)
}

/// One run: frames of `dt` seconds at `rtf` under `budget`, with a frame allowance, then settle to the cut.
fn go(u: &mut Universe, cut: i64, dt: f64, budget: Budget, frames: usize) {
    for _ in 0..frames {
        if u.now >= cut {
            break;
        }
        u.frame_to(dt, 1.0e6, budget, cut);
    }
    u.settle(cut);
}

#[test]
fn independent_events_commute() {
    // six places, each twice: the two ships of a place are in one state, so they tie at every event
    let places: Vec<(u32, u32)> = (0..12).map(|k| ((k / 2 * 715_827_882) as u32, (k / 2 * 1_431_655_765u32).wrapping_add(0x1000_0000))).collect();
    let cut = 500_000_000_000_000i64; // three periods of the ships' orbit
    let mut reference: Option<Vec<String>> = None;
    let orders: [&[usize]; 6] = [
        &[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        &[11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
        &[5, 0, 9, 3, 11, 1, 7, 2, 10, 4, 8, 6],
        &[3, 3 + 1, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2],
        &[6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5],
        &[1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10],
    ];
    let schedules: [(usize, f64, Budget); 3] = [(1, 0.05, Budget::unlimited()), (4, 0.01, Budget::events(7)), (2, 0.2, Budget::events(1))];
    let mut ties = 0usize;
    for (n, order) in orders.iter().enumerate() {
        let (threads, dt, budget) = schedules[n % 3];
        let (mut u, ids) = scene(&places, order);
        u.threads = threads;
        // every ship's next item, at the start: it ties with its twin's (one state, one step)
        let firsts: Vec<i64> = ids.iter().map(|&i| u.rec(i).plan[0].t).collect();
        ties += firsts.iter().filter(|&&t| firsts.iter().filter(|&&u| u == t).count() >= 2).count();
        go(&mut u, cut, dt, budget, 400);
        // the catalogue slot a tube's key indexes is an allocation, not a history: it is left out, as the digest leaves it out
        let records: Vec<String> = ids
            .iter()
            .map(|&i| {
                let rec = u.rec(i);
                format!("{:?}", rec).replace(&format!("Tube {{ key: {},", rec.b.tube.key), "Tube { key: _,")
            })
            .collect();
        assert!(u.rec(ids[0]).events > 300, "the ships were kicked: {}", u.rec(ids[0]).events);
        for k in (0..12).step_by(2) {
            let twin = |i: usize| format!("{:?}", u.rec(ids[i]).b.event_time) + &format!("{:?}", u.rec(ids[i]).ext) + &format!("{:?}", u.rec(ids[i]).carry);
            assert_eq!(twin(k), twin(k + 1), "order {n}: two ships in one state have one history");
        }
        match &reference {
            None => reference = Some(records),
            Some(r) => {
                for (k, rec) in records.iter().enumerate() {
                    assert_eq!(rec, &r[k], "order {n}, ship {k}: its history depends on the order the ships were made in, or on the schedule");
                }
            }
        }
    }
    println!("{ties} ties of the first items across the six scenes");
    assert!(ties >= 6 * 12, "the ships must tie at their first item, or the test measures nothing: {ties}");
}

#[test]
fn a_ship_that_ties_with_a_planet_reads_it_in_the_order_of_their_keys() {
    let cut = 2_000_000_000_000_000i64;
    // Two planets that pull each other (so they have events), and a third planet (nothing pulls it, and it pulls nothing) on the
    // first planet's orbit shape (the same period, so the same step and every tick) at another place on it; made after the
    // planets, or before.
    let run = |ship_first: bool, threads: usize, dt: f64, budget: Budget, frames: usize| -> String {
        let mut u = Universe::new(s(STAR_RADIUS), Config::default());
        let a_spec = OrbitSpec { doll: 0, periapsis: s(SEP), e_q48: (1u64 << 48) / 20, clockwise: false, angle: 0, phase: 0 };
        let b_spec = OrbitSpec { doll: 0, periapsis: s(3 * SEP), e_q48: 0, clockwise: false, angle: 1 << 30, phase: 1 << 31 };
        let ship_spec = OrbitSpec { phase: 1 << 30, ..a_spec };
        let ship = if ship_first { Some(u.add_body(Kind::Planet, ship_spec, Scalar::ZERO).unwrap()) } else { None };
        let a = u.add_body(Kind::Planet, a_spec, Scalar::ZERO).unwrap();
        let b = u.add_body(Kind::Planet, b_spec, Scalar::ZERO).unwrap();
        let ship = ship.unwrap_or_else(|| u.add_body(Kind::Planet, ship_spec, Scalar::ZERO).unwrap());
        // each planet pulls a thousandth of the star's pull, and has a doll
        u.add_doll("a", a, -9, Scalar::raw(49_000, 9).unwrap()).unwrap();
        u.add_doll("b", b, -9, Scalar::raw(49_000, 9).unwrap()).unwrap();
        u.start().unwrap();
        u.threads = threads;
        // they tie: the same shape, the same step, the same ticks
        assert_eq!(u.rec(a).plan[0].t, u.rec(ship).plan[0].t, "the first items must tie");
        go(&mut u, cut, dt, budget, frames);
        assert!(u.rec(ship).events > 100 && u.rec(a).events > 100, "the ship and the planet were kicked: {} {}", u.rec(ship).events, u.rec(a).events);
        let rec = |i: usize| {
            let r = u.rec(i);
            format!("{:?}", r).replace(&format!("Tube {{ key: {},", r.b.tube.key), "Tube { key: _,")
        };
        format!("{:?} {:?} {}", rec(ship), rec(a), u.digest())
    };
    let schedules: [(usize, f64, Budget, usize); 4] = [(1, 0.05, Budget::unlimited(), 100), (4, 0.01, Budget::events(3), 100), (2, 0.3, Budget::events(1), 100), (1, 0.0007, Budget::events(0), 10)];
    let (mut after, mut before) = (Vec::new(), Vec::new());
    for (threads, dt, budget, frames) in schedules {
        after.push(run(false, threads, dt, budget, frames));
        before.push(run(true, threads, dt, budget, frames));
    }
    assert!(after.iter().all(|r| r == &after[0]), "ship after the planet: the history depends on the schedule");
    assert!(before.iter().all(|r| r == &before[0]), "ship before the planet: the history depends on the schedule");
    // the control: the key is observable (two assignments of ids are two histories), so the test can fail
    assert_ne!(after[0], before[0], "the order of the keys of a tie does not show in the history: the test measures nothing");
}

/// Three members of the frame: 1 and 3 close on 2 (masses 1, 3, 2) so that both pairs touch in one chronon.
fn trio() -> World {
    let v = Q >> 6; // c/64: the gap of 2Q closes to the contact distance Q in 32 chronons, for both pairs at once
    let mk = |id: u64, x: i64, k: i64, m: i64| Body::new(id, [x, 0], [k, 0], m, Q / 2, Response::Bounce);
    World::new(Q, None, vec![mk(1, -2 * Q, v, 1), mk(2, 0, 0, 3), mk(3, 2 * Q, -v, 2)]).unwrap().with_law(Law::RelativisticV1).unwrap()
}

#[test]
fn a_same_epoch_three_body_contact_is_one_batch() {
    let horizon = 400_000i64;
    let run = |order: Order, threads: usize, budget: Budget, step: i64| {
        let mut p = plane_with(Config::default(), 5, order, threads, trio()).unwrap();
        while p.u.now < horizon {
            let target = (p.u.now + step).min(horizon);
            let a = p.u.advance(target, budget);
            p.u.now = a.horizon.max(p.u.now);
            if a.events == 0 && a.overflow {
                p.u.settle(target);
            }
        }
        p.u.settle(horizon);
        (p.u.digest(), p.u.fleets[0].contacts(), p.u.fleets[0].outcome_digest())
    };
    let (reference, contacts, outcome) = run(Order::Sparse, 1, Budget::unlimited(), horizon);
    println!("trio: {contacts} contacts, digest {}", &reference[..16]);
    assert!(contacts >= 2, "both pairs touched: {contacts}");
    for (order, threads, budget, step) in [(Order::Dense, 1usize, Budget::unlimited(), horizon), (Order::Sparse, 4, Budget::events(2), 5_000), (Order::Dense, 2, Budget::events(1), 1_000), (Order::Sparse, 8, Budget::events(13), 77_777)] {
        let (d, c, o) = run(order, threads, budget, step);
        assert_eq!((c, &o), (contacts, &outcome), "{order:?}, {threads} threads: the battle's outcome");
        assert_eq!(d, reference, "{order:?}, {threads} threads, {budget:?} per frame of {step} ticks");
    }
}
