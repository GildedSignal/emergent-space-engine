//! The flight recorder, flown through the session the way a player flies it (live frames, jittered, a wall budget that
//! bites), then replayed. Frozen before the first run:
//! 1. A recorded flight replays to the digest it was recorded with, whatever the thread count of the replay, and the
//!    comparison calls it the same.
//! 2. The digest can fail: a planted change (an input byte) gives another digest, named; a planted loss or refusal that was
//!    not recorded is a regression.
//! 3. A lost ship is recorded with its reason, its tick and a digest, and replays to the same loss, tick and digest; with
//!    its inputs removed the loss vanishes, and the comparison says so.
//! 4. `replay_all` prints a verdict a flight and exits non-zero on a regression only.
//! 5. A decision is logged at the tick it takes effect (the first flights the recorder replayed found that it was not: a frame
//!    that had resolved the player a tick past the presented tick took the decision there, and logged the presented tick).
use super::flight::Flight;
use super::replay::{compare, replay, replay_all, Stop};
use super::session::Session;
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::{Budget, Config};
use std::path::{Path, PathBuf};

fn tmp(name: &str) -> PathBuf {
    let d = std::env::temp_dir().join(format!("es-flights-{name}-{}", std::process::id()));
    let _ = std::fs::remove_dir_all(&d);
    std::fs::create_dir_all(&d).unwrap();
    d
}

fn read(path: &Path) -> Flight {
    serde_json::from_str(&std::fs::read_to_string(path).unwrap()).unwrap()
}

const SCRIPT: [(usize, u8); 6] = [(10, 0x81), (50, 0xF1), (90, 0xF5), (130, 0xF0), (170, 0x42), (200, 0x00)];

/// A live flight of the plane: a burn at level 8, up to 15, a turn, a coast, a reverse and a stop, with the wall's frames
/// jittered (`dts`, cycled) and a wall budget for the engine.
fn fly(dir: &Path, threads: usize, engine_ms: f64, dts: &[f64]) -> PathBuf {
    let mut s = Session::new(3, threads, 8, 100.0).unwrap();
    s.engine_ms = engine_ms;
    s.record_into(dir.to_path_buf());
    for f in 0..260 {
        let keys = SCRIPT.iter().rev().find(|(n, _)| *n <= f).map(|x| x.1);
        s.step(keys, dts[f % dts.len()]).unwrap();
    }
    s.finish("exit").expect("a flown session leaves a file")
}

#[test]
fn a_recorded_flight_replays_to_its_digest() {
    let dir = tmp("same");
    let t = std::time::Instant::now();
    let path = fly(&dir, 1, 5.0, &[1.0 / 60.0, 0.0171, 0.033, 0.0042]);
    let f = read(&path);
    println!("recorded in {:.1} s: {}", t.elapsed().as_secs_f64(), std::fs::read_to_string(&path).unwrap().trim());
    assert_eq!((f.format.as_str(), f.end.as_deref(), f.digest_source.as_deref()), ("es-flight-v1", Some("exit"), Some("live")));
    assert_eq!(f.inputs.len(), 6, "the six decisions, none per frame: {:?}", f.inputs);
    assert_eq!((f.commit.len(), f.law_hash.len(), f.members, f.threads, f.seed), (40, 16, 8, 1, 3));
    assert!(f.cut_tick.unwrap() >= f.presented_tick && f.digest.is_some() && f.loss.is_none() && f.refusals == 0 && f.other_refusals == 0, "{f:?}");
    for threads in [1, 4] {
        let mut g = f.clone();
        g.threads = threads;
        let r = replay(&g, None).unwrap();
        let v = compare(&g, &r);
        println!("replayed on {threads} thread(s) in {:.1} s: {}", r.seconds, &r.digest[..16]);
        assert_eq!(Some(&r.digest), f.digest.as_ref(), "{threads} threads: the live flight and its replay differ");
        assert!(v.same() && !v.regression, "{:?}", v.notes);
    }
    // Other wall frames, other budgets (a wall budget that bites resolves the player's items at other frames' ticks): every
    // flight, whatever its frames, replays to its own digest.
    for (threads, ms, dts) in [(2, 0.5, vec![1.0 / 144.0, 0.1, 0.0166]), (1, 3.0, vec![1.0 / 60.0]), (1, 5.0, vec![1.0 / 60.0]), (1, 8.0, vec![1.0 / 30.0]), (1, 5.0, vec![1.0 / 60.0]), (1, 3.0, vec![1.0 / 60.0])] {
        let g = read(&fly(&dir, threads, ms, &dts));
        let r = replay(&g, None).unwrap();
        assert_eq!(Some(&r.digest), g.digest.as_ref(), "a live flight (budget {ms} ms, frames {dts:?}, decisions {:?}) differs from its replay", g.inputs);
    }
    let _ = std::fs::remove_dir_all(&dir);
}

#[test]
fn a_planted_change_is_reported() {
    let dir = tmp("planted");
    let f = read(&fly(&dir, 1, 5.0, &[1.0 / 60.0]));
    // An input byte: the level of the second burn.
    let mut g = f.clone();
    g.inputs[1].1 = word(1, 14);
    let r = replay(&g, None).unwrap();
    assert_ne!(Some(&r.digest), f.digest.as_ref(), "a different input must give a different digest");
    let v = compare(&f, &r);
    println!("planted input byte: {:?}", v.notes);
    assert!(!v.same() && v.notes.iter().any(|n| n.contains("digest differs")), "{:?}", v.notes);
    // The control: the same file is the same.
    let control = compare(&f, &replay(&f, None).unwrap());
    assert!(control.same(), "{:?}", control.notes);
    // A refusal that was not recorded, and a loss that was not: regressions, named.
    let mut r2 = replay(&f, None).unwrap();
    r2.refusals = 2;
    let v = compare(&f, &r2);
    assert!(v.regression && v.notes.iter().any(|n| n.contains("refusals: 0 -> 2")), "{:?}", v.notes);
    let mut r3 = replay(&f, None).unwrap();
    r3.loss = Some(super::flight::Loss { reason: "hit Home at 1 km/s".into(), tick: 7 });
    let v = compare(&f, &r3);
    assert!(v.regression && v.notes.iter().any(|n| n.contains("a loss appeared")), "{:?}", v.notes);
    // A law that changed is a change to review, not a regression by itself.
    let mut h = f.clone();
    h.law_hash = "0123456789abcdef".into();
    let v = compare(&h, &replay(&g, None).unwrap());
    assert!(!v.regression && v.notes.iter().any(|n| n.contains("the law changed")), "{:?}", v.notes);
    let _ = std::fs::remove_dir_all(&dir);
}

/// A ship braked against its orbit falls into Home: reverse at level 4 from frame 3 (the loss of throttle.rs's wreck test).
fn crash(dir: &Path) -> PathBuf {
    let mut s = Session::new(1, 1, 16, 800.0).unwrap();
    s.record_into(dir.to_path_buf());
    let mut lost_at = None;
    for f in 0..3000 {
        let (v, _) = s.step(if f == 3 { Some(word(2, 4)) } else { None }, 0.1).unwrap();
        if v["alive"] == false && lost_at.is_none() {
            lost_at = Some(f);
            // a key pressed on the wreck: the flight is over, and the file keeps the log as it was at the loss
            let _ = s.step(Some(word(1, 9)), 0.1);
        }
        if lost_at.is_some_and(|l| f > l + 3) {
            break;
        }
    }
    assert!(lost_at.is_some(), "the ship should have crashed");
    s.finish("exit").unwrap()
}

#[test]
fn a_lost_ship_is_recorded_and_replays_to_the_same_loss() {
    let dir = tmp("loss");
    let t = std::time::Instant::now();
    let path = crash(&dir);
    let f = read(&path);
    println!("crash recorded in {:.1} s: {}", t.elapsed().as_secs_f64(), std::fs::read_to_string(&path).unwrap().trim());
    let loss = f.loss.clone().expect("a loss is recorded");
    assert!(loss.reason.starts_with("hit Home at "), "{}", loss.reason);
    assert_eq!((f.end.as_deref(), f.digest_source.as_deref()), (Some("loss"), Some("shadow")), "{f:?}");
    assert!(f.digest.is_some() && f.note.is_none(), "the shadow replay and the live loss agree: {:?}", f.note);
    assert_eq!(f.inputs.len(), 1, "the key pressed on the wreck is not part of the flight: {:?}", f.inputs);
    let r = replay(&f, None).unwrap();
    assert_eq!((&r.loss, Some(&r.digest)), (&f.loss, f.digest.as_ref()));
    assert!(compare(&f, &r).same());
    // Without its input the ship does not crash: the loss vanishes, and the comparison says so.
    let mut g = f.clone();
    g.inputs.clear();
    let r = replay(&g, None).unwrap();
    assert!(r.loss.is_none());
    let v = compare(&f, &r);
    println!("input removed: {:?}", v.notes);
    assert!(v.notes.iter().any(|n| n.contains("the loss vanished")) && v.notes.iter().any(|n| n.contains("digest differs")), "{:?}", v.notes);
    let _ = std::fs::remove_dir_all(&dir);
}

#[test]
fn replay_all_says_same_changed_and_regressed() {
    let dir = tmp("all");
    let good = fly(&dir, 1, 5.0, &[1.0 / 60.0]);
    let lost = crash(&dir);
    assert_eq!(replay_all(&dir, 55.0).unwrap(), 0, "the recorded flights replay as recorded");
    // A law change shows as changed, with exit 0; a loss that was not recorded is a regression, exit 1.
    let mut f = read(&good);
    f.law_hash = "0123456789abcdef".into();
    f.inputs[1].1 = word(1, 14);
    std::fs::write(&good, serde_json::to_string(&f).unwrap()).unwrap();
    assert_eq!(replay_all(&dir, 55.0).unwrap(), 0, "a changed digest under a changed law is reviewed, not failed");
    let mut l = read(&lost);
    l.loss = None;
    l.end = Some("exit".into());
    std::fs::write(&lost, serde_json::to_string(&l).unwrap()).unwrap();
    assert_eq!(replay_all(&dir, 55.0).unwrap(), 1, "a new loss fails the check");
    // No time: the flights are skipped and counted, not failed.
    assert_eq!(replay_all(&dir, 0.0).unwrap(), 0);
    // A deadline in the replay itself.
    assert!(matches!(replay(&l, Some(std::time::Instant::now())), Err(Stop::Deadline { .. })));
    let _ = std::fs::remove_dir_all(&dir);
}

/// The frames' event budgets of a live flight that the recorder's first replays caught (a 3 ms wall budget, frame 130 releasing a
/// level-15 burn): at frame 130 the player had been resolved to the presented tick plus one.
const BITING: [u64; 131] = [2, 2, 2, 2, 2, 2, 7, 2, 2, 2, 100, 61, 59, 49, 48, 48, 48, 48, 34, 34, 31, 31, 34, 31, 31, 34, 41, 31, 34, 31, 28, 16, 16, 16, 19, 16, 16, 16, 20, 16, 19, 16, 16, 16, 16, 16, 16, 19, 16, 16, 32, 30, 32, 32, 32, 32, 32, 32, 32, 32, 45, 48, 48, 48, 51, 48, 48, 48, 45, 45, 48, 48, 48, 48, 48, 48, 45, 45, 48, 48, 48, 48, 48, 48, 45, 45, 48, 48, 48, 48, 44, 48, 45, 32, 17, 11, 10, 13, 11, 10, 10, 14, 10, 10, 14, 10, 7, 14, 5, 5, 8, 5, 5, 9, 5, 5, 8, 5, 5, 11, 5, 6, 14, 14, 13, 13, 13, 13, 16, 12, 7];

/// Fly the first four decisions of [`SCRIPT`] with those frames, taking each decision at `tick(now, committed)`, then replay the log.
fn decision_flight_replays(tick: impl Fn(i64, i64) -> i64) -> bool {
    let mut p = plane(Config::default(), 3, Order::Sparse, 1, 8).unwrap();
    let mut keys = 0u8;
    for (f, &n) in BITING.iter().enumerate() {
        if let Some(k) = SCRIPT[..4].iter().rev().find(|(m, _)| *m <= f).map(|x| x.1) {
            if k != keys {
                let t = tick(p.u.now, p.u.bodies().event_time(p.player));
                p.u.input(t, k).unwrap();
                keys = k;
            }
        }
        p.u.frame_to(1.0 / 60.0, 100.0, Budget::events(n), i64::MAX);
    }
    let inputs = p.u.inputs.clone();
    let cut = super::flight::canonical_cut(&p.u);
    p.u.settle(cut);
    let mut q = plane(Config::default(), 3, Order::Sparse, 1, 8).unwrap();
    for &(t, w) in &inputs {
        q.u.schedule(t, w).unwrap();
    }
    q.u.settle(cut);
    q.u.digest() == p.u.digest()
}

#[test]
fn a_decision_is_logged_at_the_tick_it_takes_effect() {
    // The session's rule: at the later of the presented tick and the player's committed tick.
    assert!(decision_flight_replays(|now, committed| now.max(committed)), "a decision taken at its effective tick must replay exactly");
    // The control (the rule before the recorder): the presented tick alone. Documents the failure the test exists for.
    println!("decision at the presented tick alone replays exactly: {}", decision_flight_replays(|now, _| now));
}
