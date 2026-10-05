//! Replays are exact (docs/law.md, "Ties": a decision takes effect at its logged canonical tick, never at a wall-derived
//! one; lab run 20261005-0543-taleb-c271: the paced bench was irreproducible because decisions were logged at
//! wall-derived ticks and the digest was taken wherever `now` stopped).
//!
//! **Frozen before the first run.** One input log at canonical ticks and one canonical cut give one digest, whatever
//! carried the universe there: frames of any size and jitter (a paced run's wall dt), any budget, a budget that bites
//! (every frame resolves a handful of events, or none), any thread count, and a key held for a thousand frames. The
//! decisions come out of the run exactly as they went in: none moved, none dropped. Controls (the digest must be able
//! to fail): another log, another cut, and a decision taken at a wall-derived tick (`input(now)` on a lagging
//! `now`) each give another digest.
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::{Budget, Config};

const CUT: i64 = 400_000_000; // 33 minutes of game time
const RTF: f64 = 100.0;
/// The player's keys at canonical ticks: a burn forward held for 40 s of game time, a burn forward and right, a reverse.
const LOG: [(i64, u8); 6] = [(10_000_000, 1), (18_000_000, 0), (150_000_000, 9), (153_000_000, 0), (300_000_000, 2), (301_000_000, 0)];

/// Run to `cut` the way a player's frames would: `dts` (wall seconds per frame, cycled), `budget` per frame, a
/// `frames` allowance (a budget that bites will not finish in it), then settle to the cut. Returns the digest and the
/// decisions as taken.
fn run(log: &[(i64, u8)], cut: i64, dts: &[f64], budget: Budget, frames: usize, threads: usize) -> (String, Vec<(i64, u8)>) {
    let mut p = plane(Config::default(), 3, Order::Sparse, threads, 16).unwrap();
    for &(t, k) in log {
        p.u.schedule(t, k).unwrap();
    }
    for f in 0..frames {
        if p.u.now >= cut {
            break;
        }
        p.u.frame_to(dts[f % dts.len()], RTF, budget, cut);
    }
    p.u.settle(cut);
    (p.u.digest(), p.u.inputs.clone())
}

#[test]
fn one_log_and_one_cut_give_one_digest_on_any_schedule() {
    let (reference, taken) = run(&LOG, CUT, &[1.0 / 60.0], Budget::unlimited(), 100_000, 1);
    assert_eq!(taken, LOG.to_vec(), "the decisions as taken are the decisions as logged");
    println!("reference {}: {} decisions", &reference[..16], taken.len());
    let paced = [1.0 / 60.0, 0.0171, 0.0158, 0.033, 0.0166, 0.1, 0.0042, 0.0167]; // a wall's frames: jitter, a hitch, a long one
    let schedules: [(&[f64], Budget, usize, usize); 6] = [
        (&paced, Budget::unlimited(), 100_000, 1),
        (&paced, Budget::unlimited(), 100_000, 4),
        (&[1.0 / 37.0, 1.0 / 144.0], Budget::events(40), 100_000, 2),
        // a budget that bites: a handful of events a frame cannot reach the cut in the allowance, the rest is the cut's settle
        (&paced, Budget::events(5), 300, 1),
        (&paced, Budget::events(1), 50, 3),
        // no budget at all: the frames resolve nothing, and the cut's settle does everything
        (&[1.0 / 60.0], Budget::events(0), 40, 1),
    ];
    for (dts, budget, frames, threads) in schedules {
        let (d, taken) = run(&LOG, CUT, dts, budget, frames, threads);
        println!("{budget:?}, {threads} threads, {frames} frames: {}", &d[..16]);
        assert_eq!(taken, LOG.to_vec(), "{budget:?}: a decision moved or was dropped");
        assert_eq!(d, reference, "{budget:?}, {threads} threads, dts {dts:?}");
    }
    // a wall budget that bites by the clock (the engine's own, 5 ms, and one far below any frame's work)
    for ms in [5.0, 0.001] {
        let mut p = plane(Config::default(), 3, Order::Sparse, 1, 16).unwrap();
        for &(t, k) in &LOG {
            p.u.schedule(t, k).unwrap();
        }
        for f in 0..200 {
            p.u.frame_to(paced[f % paced.len()], RTF, Budget::wall(ms), CUT);
        }
        p.u.settle(CUT);
        assert_eq!(p.u.inputs, LOG.to_vec(), "wall budget {ms} ms: a decision moved or was dropped");
        assert_eq!(p.u.digest(), reference, "wall budget {ms} ms");
    }
}

#[test]
fn the_controls_can_fail() {
    let (reference, _) = run(&LOG, CUT, &[1.0 / 60.0], Budget::unlimited(), 100_000, 1);
    // another log
    let (other, _) = run(&LOG[..4], CUT, &[1.0 / 60.0], Budget::unlimited(), 100_000, 1);
    assert_ne!(other, reference, "a different player gives a different universe");
    // the same log at a decision moved by one tick
    let mut moved = LOG;
    moved[2].0 += 1;
    let (shifted, _) = run(&moved, CUT, &[1.0 / 60.0], Budget::unlimited(), 100_000, 1);
    assert_ne!(shifted, reference, "a decision one tick later is another history");
    // another cut
    let (later, _) = run(&LOG, CUT + 40_000_000, &[1.0 / 60.0], Budget::unlimited(), 100_000, 1);
    assert_ne!(later, reference, "another cut is another state");
    // the old way: a decision taken at the presented tick of a frame under a budget that bites lands wherever `now`
    // is, so two runs with different pacing disagree (here one tick of a frame apart is enough)
    let wall_derived = |dt: f64| {
        let mut p = plane(Config::default(), 3, Order::Sparse, 1, 16).unwrap();
        let mut sent = 0;
        while p.u.now < CUT {
            if sent < LOG.len() && p.u.now >= LOG[sent].0 {
                p.u.input(p.u.now, LOG[sent].1).unwrap(); // the logged tick is whatever `now` was
                sent += 1;
            }
            p.u.frame_to(dt, RTF, Budget::unlimited(), CUT);
        }
        p.u.settle(CUT);
        (p.u.digest(), p.u.inputs.clone())
    };
    let (a, la) = wall_derived(1.0 / 60.0);
    let (b, lb) = wall_derived(1.0 / 50.0);
    assert_ne!(la, lb, "the wall-derived ticks differ with the pacing");
    assert_ne!(a, b, "and so do the histories");
}

/// A key held for a thousand frames is one decision, and the held state is the same on any frame schedule.
#[test]
fn a_key_held_for_a_thousand_frames_is_one_decision() {
    let log = [(1_000_000i64, 1u8), (390_000_000, 0)];
    let (a, taken) = run(&log, CUT, &[1.0 / 60.0], Budget::unlimited(), 100_000, 1);
    assert_eq!(taken, log.to_vec());
    let (b, _) = run(&log, CUT, &[0.021, 0.0113, 0.05], Budget::events(9), 100_000, 2);
    assert_eq!(a, b);
}
