//! The fleet's life (docs/plane.md, foundations 1, 2 and 7): the frame's origin is a tube of its doll and takes
//! the doll's kicks; a member that leaves the frame is a tube of the doll, exactly as the frame handed it
//! over; a frame with nobody left to touch dissolves and costs nothing; and through all of it the universe's
//! digest depends on neither the order the battle is stepped in, the budget nor the threads. Each test
//! finishes within a few seconds.
use emergent_engine::{AnchorPolicy, Battle, Frame};
use emergent_lattice::law::{Body, Law, Response, World};
use emergent_lattice_event::EventCore;
use emergent_universe::fleet::{mean_motion, Order, Q};
use emergent_universe::observe::root_state;
use emergent_universe::scenario::{plane, plane_with};
use emergent_universe::view::gather;
use emergent_universe::{Budget, Config};
use std::collections::HashSet;

fn world(bodies: &[(f64, f64, [i64; 2], Response)]) -> World {
    let q = Q as f64;
    let bodies = bodies.iter().enumerate().map(|(i, &(x, y, k, r))| Body::new(i as u64 + 1, [(x * q) as i64, (y * q) as i64], k, 1, Q / 2, r)).collect();
    World::new(Q, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap()
}

/// Four members flying apart at 2^-11 c: they leave the frame (R/32 = 148 light-ticks) in about 3·10^5 ticks.
fn flyers() -> World {
    let v = Q >> 11;
    world(&[(10.0, 10.0, [v, v], Response::Pass), (-10.0, 10.0, [-v, v], Response::Pass), (-10.0, -10.0, [-v, -v], Response::Pass), (10.0, -10.0, [v, -v], Response::Pass)])
}

/// Three members at rest along the track (0, ±2 light-ticks): a drift-free epicycle, so they stay in the
/// frame, and nobody leaves, for as long as the test looks.
fn along_the_track() -> World {
    world(&[(-2.0, 0.0, [0, 0], Response::Pass), (0.0, 0.0, [0, 0], Response::Pass), (2.0, 0.0, [0, 0], Response::Pass)])
}

const FLEET_PHASE: u32 = 0x4000_0000;
const R_LAT: i64 = 4_740 * Q;

/// A member that left the frame is the tube the frame handed over: at its hand-off tick the body's position
/// and velocity in the root frame are the origin's plus the member's own (and what the engine still owes its
/// position), to 3·10^-8 root units (a lattice unit is 10^-6; f64's own resolution at 1 AU is 10^-8) and
/// 10^-12 c; it has the member's identity, and it is alive and planned.
#[test]
fn a_member_that_leaves_is_a_tube_of_the_doll_exactly_as_the_frame_handed_it_over() {
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
    let n0 = p.u.n_bodies();
    p.u.settle(6_000_000);
    let f = &p.u.fleets[0];
    assert!(f.live() && f.handoffs().len() >= 8, "members have left a frame that goes on: {}", f.handoffs().len());
    let leavers: Vec<usize> = (n0..p.u.n_bodies()).collect();
    assert_eq!(leavers.len(), f.handoffs().len());
    let ctx = p.u.ctx();
    let k = 2f64.powi(-20);
    for (&i, h) in leavers.iter().zip(f.handoffs()) {
        assert_eq!(p.u.info[i].from, Some((0, h.index as u16)), "identity");
        assert_eq!(p.u.info[i].born, h.tick);
        assert!(p.u.bodies().alive(i) && p.u.bodies().next_time(i).is_some(), "it is alive and planned");
        // the exact state the engine gives: the origin's tube plus the member's own, lattice units
        let (c, cv) = root_state(&ctx, p.planets[1], h.tick).unwrap();
        let tube_x = [h.tube.x[0] as f64 / 2f64.powi(32) + h.tube.radius as f64, h.tube.x[1] as f64 / 2f64.powi(32)];
        let tube_v = [h.tube.v[0] as f64 / 2f64.powi(48), h.tube.v[1] as f64 / 2f64.powi(48)];
        let (got, vel) = root_state(&ctx, i, h.tick).unwrap();
        for a in 0..2 {
            let want = c[a] + (tube_x[a] + h.x[a] as f64 + f.owed(h.index)[a] as f64 / 2f64.powi(48)) * k;
            assert!((got[a] - want).abs() < 3e-8, "body {i} axis {a}: position {} against {} (a lattice unit is {k:e})", got[a], want);
            let want_v = cv[a] + (tube_v[a] + h.v[a] as f64 / 2f64.powi(48)) / Q as f64;
            assert!((vel[a] - want_v).abs() < 1e-12, "body {i} axis {a}: velocity {} against {}", vel[a], want_v);
        }
    }
    println!("{} members left a live frame of 48; every one is the tube it left as", leavers.len());
}

/// A frame with nobody left to touch dissolves: every member is a body of the doll (none lost, none twice),
/// the battle is gone, nothing of the fleet is ever resolved again, and the universe goes on.
#[test]
fn a_dissolved_battle_costs_nothing() {
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
    let n0 = p.u.n_bodies();
    p.u.settle(1_500_000_000);
    let f = &p.u.fleets[0];
    assert!(!f.live() && f.members() == 0 && f.next_time().is_none(), "the battle is over");
    let s = p.u.stats;
    assert_eq!(s.dissolved, 1);
    assert_eq!(s.leavers, 48, "every member left the frame once");
    assert_eq!(p.u.n_bodies(), n0 + 48);
    let froms: HashSet<_> = (n0..p.u.n_bodies()).map(|i| p.u.info[i].from.unwrap()).collect();
    assert_eq!(froms.len(), 48, "no member twice");
    let (items, slices, kicks) = (s.items[4], s.slices, s.kicks);
    p.u.settle(6_000_000_000);
    let s2 = p.u.stats;
    assert_eq!((s2.items[4], s2.slices), (items, slices), "a dissolved battle is never resolved again");
    assert!(s2.kicks > kicks, "the universe goes on");
    println!("dissolved after {items} fleet items; {} of its 48 members have crashed since", (n0..p.u.n_bodies()).filter(|&i| !p.u.bodies().alive(i)).count());
}

/// The same universe in both orders of the battle, at every thread count and budget, through the whole of its
/// life (kicks of the origin, hand-outs, dissolution): one digest. A fleet that stays (the control) differs.
#[test]
fn the_digest_is_the_same_through_a_frames_whole_life() {
    let run = |order: Order, threads: usize, budget: Budget, step: i64, w: World| {
        let mut p = plane_with(Config::default(), 5, order, threads, w).unwrap();
        let horizon = 6_000_000i64;
        while p.u.now < horizon {
            let target = (p.u.now + step).min(horizon);
            let a = p.u.advance(target, budget);
            p.u.now = a.horizon.max(p.u.now);
            if a.events == 0 && a.overflow {
                p.u.settle(target);
            }
        }
        p.u.settle(horizon);
        (p.u.digest(), p.u.stats, p.u.fleets[0].live())
    };
    let (reference, st, live) = run(Order::Sparse, 1, Budget::unlimited(), 6_000_000, flyers());
    assert!(!live && st.dissolved == 1 && st.leavers == 4, "the life: {st:?}");
    for (order, threads, budget, step) in [(Order::Dense, 1usize, Budget::unlimited(), 6_000_000i64), (Order::Sparse, 4, Budget::events(3), 250_000), (Order::Dense, 2, Budget::events(11), 1_000_000), (Order::Sparse, 8, Budget::events(1), 90_000)] {
        let (d, s2, _) = run(order, threads, budget, step, flyers());
        assert_eq!(d, reference, "{order:?}, {threads} threads, {budget:?} per frame of {step} ticks");
        assert_eq!((s2.leavers, s2.dissolved), (4, 1));
    }
    let (other, _, live) = run(Order::Sparse, 1, Budget::unlimited(), 6_000_000, along_the_track());
    assert!(live, "three members at rest along the track stay");
    assert_ne!(other, reference);
}

/// The frame's origin is a tube of its doll like any other, and takes what the doll's kick sources do (the star's
/// tide, the moon's pull): the push the kicks give it over three quarters of an orbit equals, within 5%, the push
/// the same kicks give a ship on the same circle (the player, 22 km ahead), each measured against its own
/// unkicked orbit, one in the engine's lattice tube and the other in the doll's compiled one.
#[test]
fn the_origin_takes_the_dolls_kicks_like_a_ship() {
    let t = 800_000_000i64;
    let mut p = plane_with(Config::default(), 5, Order::Sparse, 1, along_the_track()).unwrap();
    p.u.settle(t);
    assert!(p.u.fleets[0].live() && p.u.stats.kicks > 0);
    // the fleet's origin against the same frame left alone (no parent kicks)
    let f = &p.u.fleets[0];
    let (kicked, _) = f.origin(t).unwrap();
    let n = mean_motion(-18, R_LAT).unwrap();
    let frame = Frame::on_orbit(Q, R_LAT, n, 0, FLEET_PHASE, 0).unwrap();
    let mut alone = Battle::new(EventCore::new(along_the_track(), false).unwrap(), frame, 1).with_anchoring(AnchorPolicy::default()).unwrap().with_min_members(2);
    alone.run_to(t).unwrap();
    let t0 = alone.tube_at(t).unwrap();
    let still = [t0.x[0] as f64 / 2f64.powi(32) + t0.radius as f64, t0.x[1] as f64 / 2f64.powi(32)];
    let d_fleet = [kicked[0] - still[0], kicked[1] - still[1]]; // lattice units
    // the ship's: against its first binding, never kicked
    let me = p.player;
    let ctx = p.u.ctx();
    let (x_now, _) = p.u.rec(me).b.cartesian(t).unwrap();
    let first = p.u.bodies().binding_at(me, 0).unwrap();
    let (x_still, _) = first.cartesian(t).unwrap();
    let f64_of = emergent_universe::num::to_f64;
    // Home units → lattice units: × 4
    let d_ship = [(f64_of(x_now[0]) - f64_of(x_still[0])) * 4.0, (f64_of(x_now[1]) - f64_of(x_still[1])) * 4.0];
    drop(ctx);
    let (mf, ms) = ((d_fleet[0].powi(2) + d_fleet[1].powi(2)).sqrt(), (d_ship[0].powi(2) + d_ship[1].powi(2)).sqrt());
    let cos = (d_fleet[0] * d_ship[0] + d_fleet[1] * d_ship[1]) / (mf * ms);
    println!("the kicks pushed the origin {mf:.4e} lattice units ({d_fleet:?}) and the ship {ms:.4e} ({d_ship:?}); cos {cos:.5}");
    assert!(mf > 1e5, "the kicks must move the origin by many lattice units, or the test measures nothing: {mf}");
    assert!(((mf - ms) / ms).abs() < 0.05 && cos > 0.9986, "the origin's push {mf:e} against the ship's {ms:e}, cos {cos}");
    // the control: without the kicks the frame is still (the unkicked battle is what it was compared to)
    assert!(still[0].hypot(still[1]) > 0.0);
}

/// A member keeps its identity through its hand-out: the view shows each ship of the fleet once, as a member of
/// the frame while it is in it and as a body of the doll after, with the same id.
#[test]
fn the_view_shows_each_member_once_and_keeps_its_identity() {
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
    let mut seen_counts = Vec::new();
    for h in [1_000_000i64, 4_000_000, 5_000_000, 6_000_000, 9_000_000, 30_000_000] {
        p.u.settle(h);
        p.u.now = h;
        let v = gather(&p.u, &p.names).unwrap();
        let ids: Vec<usize> = v.seen.iter().filter(|s| s.kind == 4).map(|s| s.id).collect();
        let unique: HashSet<_> = ids.iter().collect();
        assert_eq!(unique.len(), ids.len(), "t={h}: a ship is shown twice");
        assert!(ids.iter().all(|&id| (1_000_000..1_000_048).contains(&id)));
        seen_counts.push((h, ids.len(), p.u.fleets[0].members(), p.u.stats.leavers));
    }
    println!("{seen_counts:?}");
    let (_, shown, members, leavers) = seen_counts[3];
    assert!(leavers > 0 && members > 0 && shown + 2 >= members + leavers as usize - 2, "members and leavers are all shown: {seen_counts:?}");
}
