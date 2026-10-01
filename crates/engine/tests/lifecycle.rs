//! A frame's life, as the events layer lives it (docs/plane.md, "the fleet's lifecycle"): the parent's kick
//! on the frame's origin, a frame that ends when too few members are left to touch, and the whole frame
//! handed out at once. Each is an event of the law, so lockstep and sparse give the same bits, and a control
//! that does not do it must differ.
use emergent_engine::{AnchorPolicy, Battle, Frame, Outcome};
use emergent_lattice::law::{Body, Law, Response, World};
use emergent_lattice::{chronon::Chronon, Kickable, Stepper};
use emergent_lattice_event::EventCore;

const Q: i64 = 1 << 20;
const DR: i64 = 1 << 22;
const R: i64 = 1000 * DR;
const N: u64 = 1 << 46;
/// Under half a period (2π/n is about 103,000 chronons): the cluster has not yet sheared out of the size rule.
const HORIZON: i64 = 40_000;

fn frame() -> Frame {
    Frame::new(Q, R, N).unwrap()
}

fn anchored<S: Kickable>(s: S, threads: usize) -> Battle<S> {
    Battle::new(s, frame(), threads).with_anchoring(AnchorPolicy::default()).unwrap()
}

fn world(at: &[(f64, f64, i64)]) -> World {
    let bodies = at.iter().enumerate().map(|(i, &(x, y, m))| Body::new(i as u64 + 1, [(x * DR as f64) as i64, (y * DR as f64) as i64], [0, 0], m, 1000, Response::Pass)).collect();
    World::new(Q, None, bodies).unwrap().with_law(Law::RelativisticV1).unwrap()
}

/// Five members within a few dr of each other (R/32 is 31 dr).
fn cluster() -> World {
    world(&[(1.0, 0.0, 4), (2.0, 1.0, 4), (0.5, -1.0, 4), (1.5, 0.5, 4), (0.0, 0.0, 4)])
}

/// The cluster and three members 50 to 80 dr out: they leave at genesis.
fn outliers() -> World {
    world(&[(1.0, 0.0, 4), (2.0, 1.0, 4), (0.5, -1.0, 4), (1.5, 0.5, 4), (0.0, 0.0, 4), (60.0, 0.0, 1), (-50.0, 20.0, 1), (10.0, 80.0, 1)])
}

/// A velocity kick of the origin (`2^-48` lattice units per chronon): the origin's velocity gains exactly
/// it, its position does not move, and no member is touched; both orders and every thread count agree; and
/// the unkicked control differs. At a short time the origin is displaced from the control by `dv·Δt`.
#[test]
fn the_parents_kick_changes_the_origins_velocity_and_nobody_elses() {
    let dv = [3i128 << 38, -(5i128 << 38)];
    let t0 = 10_003;
    fn go<S: Kickable>(s: S, threads: usize, dv: Option<[i128; 2]>, t0: i64) -> (Outcome, emergent_engine::Tube, emergent_engine::Tube, Vec<[i64; 2]>, Vec<[i64; 2]>) {
        let mut b = anchored(s, threads);
        b.run_to(t0).unwrap();
        let before = b.tube_at(t0).unwrap();
        let mut m0 = Vec::new();
        b.stepper().motions(&mut m0);
        if let Some(dv) = dv {
            b.kick_origin(dv).unwrap();
        }
        let after = b.tube_at(t0).unwrap();
        let mut m1 = Vec::new();
        b.stepper().motions(&mut m1);
        assert_eq!(m0, m1, "the members are not kicked by their origin's kick");
        b.run_to(t0 + 30_000).unwrap();
        let later = b.tube_at(t0 + 100).unwrap();
        (b.outcome(), before, after, m0.iter().map(|m| m.x).collect(), vec![later.x, later.v].into_iter().map(|a| [a[0] as i64, a[1] as i64]).collect())
    }
    let (oa, before, after, _, _) = go(Chronon::new(cluster(), false).unwrap(), 1, Some(dv), t0);
    assert_eq!(after.x, before.x, "the position does not move");
    assert_eq!(after.v, [before.v[0] + dv[0], before.v[1] + dv[1]], "the velocity gains exactly the kick");
    for (name, o) in [
        ("sparse", go(EventCore::new(cluster(), false).unwrap(), 1, Some(dv), t0).0),
        ("sparse, 4 threads", go(EventCore::new(cluster(), false).unwrap(), 4, Some(dv), t0).0),
        ("lockstep, 8 threads", go(Chronon::new(cluster(), false).unwrap(), 8, Some(dv), t0).0),
    ] {
        assert_eq!(o, oa, "{name}");
    }
    let control = go(Chronon::new(cluster(), false).unwrap(), 1, None, t0).0;
    assert_ne!(control, oa, "the unkicked frame is another universe");
    // A short time after the kick the origin is where the control's is plus dv·Δt (Δt = 100, the orbit turns 0.6%).
    let (c, k) = {
        let run = |dv: Option<[i128; 2]>| {
            let mut b = anchored(Chronon::new(cluster(), false).unwrap(), 1);
            b.run_to(t0).unwrap();
            if let Some(dv) = dv {
                b.kick_origin(dv).unwrap();
            }
            b.run_to(t0 + 100).unwrap();
            b.tube_at(t0 + 100).unwrap()
        };
        (run(None), run(Some(dv)))
    };
    for i in 0..2 {
        let (got, want) = ((k.x[i] - c.x[i]) as f64, (dv[i] * 100) as f64 / (1u128 << 16) as f64);
        assert!((got - want).abs() < 0.01 * want.abs(), "axis {i}: displaced {got:e}, dv·Δt is {want:e}");
    }
}

/// A frame with fewer than `n` members left hands the rest out at the anchor that leaves fewer: the three
/// far members leave at genesis, the five of the cluster are fewer than six, and everyone has gone at tick
/// 0 and the frame has ended there. With `n = 2` the cluster stays (a control), and a lone member goes.
#[test]
fn a_frame_with_too_few_members_ends_at_its_anchor() {
    fn go<S: Kickable>(s: S, n: usize) -> (Outcome, Battle<S>) {
        let mut b = anchored(s, 1).with_min_members(n);
        b.run_to(HORIZON).unwrap();
        (b.outcome(), b)
    }
    let (oa, a) = go(Chronon::new(outliers(), false).unwrap(), 6);
    let (ob, b) = go(EventCore::new(outliers(), false).unwrap(), 6);
    assert_eq!(oa, ob, "both orders");
    assert!(a.is_dissolved() && b.is_dissolved());
    assert_eq!(a.stepper().tick(), 0, "the frame ended at the genesis anchor, whatever the horizon");
    assert_eq!(a.handoffs().iter().map(|h| h.index).collect::<Vec<_>>(), vec![5, 6, 7, 0, 1, 2, 3, 4], "the leavers of the size rule first, then the rest");
    assert_eq!(a.stats().handed_out, 8);
    assert!(a.active().iter().all(|&x| !x));
    // Control: with two as the least, five members stay in the frame, and it keeps running.
    let (_, c) = go(Chronon::new(outliers(), false).unwrap(), 2);
    assert!(!c.is_dissolved() && c.stepper().tick() == HORIZON && c.active().iter().filter(|&&x| x).count() == 5);
    // Without a minimum the frame never ends, whoever is in it.
    let mut d = anchored(Chronon::new(outliers(), false).unwrap(), 1);
    d.run_to(HORIZON).unwrap();
    assert!(!d.is_dissolved() && d.stepper().tick() == HORIZON);
    // A lone member: one in the cluster and two far out. The far ones leave, and one member is fewer than two.
    let lone = || world(&[(0.0, 0.0, 4), (60.0, 0.0, 1), (-50.0, 20.0, 1)]);
    let (_, l) = go(Chronon::new(lone(), false).unwrap(), 2);
    assert!(l.is_dissolved() && l.stats().handed_out == 3, "a lone member is a tube of the parent");
}

/// `dissolve` hands every member out at the committed tick as it stands: the records hold exactly the
/// lattice state (`x`, `k + c/2^48`) and the sub-unit position remainder (`owed`), the origin's tube
/// is the one at that tick, and both orders agree.
#[test]
fn the_whole_frame_can_be_handed_out_at_once() {
    fn go<S: Kickable>(s: S) -> (Outcome, Vec<(usize, [i64; 2], [i128; 2])>, Vec<[i128; 2]>) {
        let mut b = anchored(s, 1);
        b.run_to(HORIZON).unwrap();
        let t = b.stepper().tick();
        let mut m = Vec::new();
        b.stepper().motions(&mut m);
        let carries = b.carries().to_vec();
        let tube = b.tube_at(t).unwrap();
        let rep = b.dissolve().unwrap();
        assert_eq!(rep.handed_out, vec![0, 1, 2, 3, 4]);
        assert!(b.is_dissolved() && !rep.moved && !rep.refused);
        assert_eq!(b.stepper().tick(), t, "nothing ran");
        let mut owed = Vec::new();
        let mut out = Vec::new();
        for h in b.handoffs() {
            assert_eq!(h.tick, t);
            assert_eq!(h.tube, tube, "the origin's tube at that tick");
            assert_eq!(h.x, m[h.index].x, "the position as it stands");
            assert_eq!(h.v, [((m[h.index].k[0] as i128) << 48) + carries[h.index][0] as i128, ((m[h.index].k[1] as i128) << 48) + carries[h.index][1] as i128]);
            owed.push(b.owed(h.index));
            out.push((h.index, h.x, h.v));
        }
        (b.outcome(), out, owed)
    }
    let a = go(Chronon::new(cluster(), false).unwrap());
    let b = go(EventCore::new(cluster(), false).unwrap());
    assert_eq!(a, b, "both orders");
    assert!(a.2.iter().any(|o| *o != [0, 0]), "the cluster has been falling for 40,000 chronons: it owes sub-unit drift");
}
