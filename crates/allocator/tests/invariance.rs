//! Invariance is the licence for parallelism: the union of every region's world at the final
//! tick and the merged log must equal one Chronon over the whole scene, whatever the worker
//! count, unit budget or (sabotaged) forecasts.
use emergent_allocator::{scenes, Allocator, Config, Factory, Report};
use emergent_lattice::{chronon::Chronon, law::World, Stepper, Tick};
use std::sync::Arc;

fn factory() -> Factory<Chronon> {
    Arc::new(|w| Chronon::new(w, false).expect("a region's world is a valid world"))
}

fn reference(scene: &[World], t: Tick) -> (String, String) {
    let mut c = Chronon::new(scenes::union(scene), false).unwrap();
    c.run_to(t);
    c.outcome()
}

fn run(scene: &[World], t: Tick, cfg: Config) -> ((String, String), Report) {
    let mut a = Allocator::new(scene.to_vec(), factory(), cfg).unwrap();
    let rep = a.run_to(t);
    (a.outcome(), rep)
}

fn workers(n: usize) -> (usize, usize) {
    (n.min(4), n.saturating_sub(4))
}

/// 1, 2 and 8 workers × sabotage off/on × budgets of one chronon, 5000 ops and calibrated.
fn matrix(name: &str, scene: &[World], t: Tick) -> Vec<Report> {
    let expected = reference(scene, t);
    let mut reps = Vec::new();
    for n in [1, 2, 8] {
        for sabotage in [None, Some(0xBAD5EED)] {
            for budget in [Some(1), Some(5000), None] {
                let (p, e) = workers(n);
                let cfg = Config { p_workers: p, e_workers: e, fixed_budget: budget, sabotage, ..Config::default() };
                let (got, rep) = run(scene, t, cfg);
                let r = &rep.regions;
                eprintln!(
                    "{name} workers {n} sabotage {} budget {budget:?}: regions {}→{} (max {}), merges {}, splits {}, avoided {}, exceeded {}, rollbacks {}, units {}, {:.0} ms",
                    sabotage.is_some(), r.initial, r.last, r.max, r.merges, r.splits, r.merges_avoided, r.promises_exceeded, r.rollbacks, rep.units.count, rep.wall_seconds * 1e3
                );
                assert_eq!(got, expected, "{name}: workers {n}, sabotage {sabotage:?}, budget {budget:?}");
                reps.push(rep);
            }
        }
    }
    reps
}

#[test]
fn islands_equal_one_chronon() {
    // Four islands given as four worlds; the two Pass clusters close head-on and must merge.
    let scene = scenes::islands(256, 1);
    let reps = matrix("islands", &scene, 1200);
    assert!(reps.iter().all(|r| r.regions.max >= 4), "the scene must start as several regions");
    assert!(reps.iter().all(|r| r.regions.merges >= 1), "approaching groups must merge");
}

#[test]
fn diverging_groups_split_and_equal_one_chronon() {
    let scene = scenes::diverging(256, 5);
    let reps = matrix("diverging", &scene, 1200);
    assert!(reps.iter().any(|r| r.regions.splits >= 1 && r.regions.last >= 2), "separating groups must split");
}

#[test]
fn many_small_islands_equal_one_chronon() {
    // Nine clusters of three kinds on a grid, two of them drifting together.
    let scene = scenes::galaxy(256, 3, 3, 40, 450, 1, 11);
    let reps = matrix("galaxy", &scene, 800);
    assert!(reps.iter().all(|r| r.regions.initial >= 6));
}

#[test]
fn broken_speed_forecasts_are_caught_not_trusted() {
    // Zero margin: every promise is the region's current box, so any motion outgrows it. The
    // measured true boxes must widen promises or roll back, never corrupt the outcome.
    let scene = scenes::islands(256, 2);
    let expected = reference(&scene, 900);
    for n in [1, 8] {
        let (p, e) = workers(n);
        let (got, rep) = run(&scene, 900, Config { p_workers: p, e_workers: e, speed_margin: 0.0, ..Config::default() });
        eprintln!("zero margin workers {n}: exceeded {}, rollbacks {}, escalation {}", rep.regions.promises_exceeded, rep.regions.rollbacks, rep.regions.speed_escalation);
        assert_eq!(got, expected, "workers {n}");
        assert!(rep.regions.promises_exceeded + rep.regions.rollbacks > 0, "zero margin must exercise the certificate");
    }
    // Ten-times overconfident forecasts on a tight scene force real rollbacks.
    let tight = scenes::galaxy(256, 2, 2, 40, 150, 1, 3);
    let expected = reference(&tight, 900);
    let (got, rep) = run(&tight, 900, Config { speed_margin: 0.1, ..Config::default() });
    eprintln!("tight 0.1 margin: exceeded {}, rollbacks {}, wasted ops {}", rep.regions.promises_exceeded, rep.regions.rollbacks, rep.regions.wasted_ops);
    assert_eq!(got, expected);
}

#[test]
fn resuming_and_frames_keep_the_outcome() {
    // Batch in two legs, with a frame-harness session in between that leaves regions at
    // different ticks: the final union must still equal one Chronon.
    let scene = scenes::islands(256, 3);
    let expected = reference(&scene, 1000);
    let mut a = Allocator::new(scene.clone(), factory(), Config { p_workers: 2, e_workers: 2, ..Config::default() }).unwrap();
    a.run_to(300);
    let fr = a.run_frames(&emergent_allocator::FrameConfig { hz: 240.0, seconds: 0.3, rate: 600.0, ahead_seconds: 0.2, record: false });
    assert!(fr.frames.as_ref().unwrap().frames > 20);
    let rep = a.run_to(1000);
    assert_eq!(a.outcome(), expected);
    assert!(rep.regions.accepted_windows > 0);
}

#[test]
fn contained_world_is_one_region_and_exact() {
    let w = emergent_lattice::worlds::mixed(120, 256, 9);
    let expected = reference(std::slice::from_ref(&w), 700);
    for n in [1, 8] {
        let (p, e) = workers(n);
        let (got, rep) = run(std::slice::from_ref(&w), 700, Config { p_workers: p, e_workers: e, fixed_budget: Some(300), ..Config::default() });
        assert_eq!(got, expected);
        assert_eq!(rep.regions.max, 1);
    }
    assert!(Allocator::new(vec![w.clone(), scenes::islands(256, 1)[0].clone()], factory(), Config::default()).is_err());
}

/// Every round-3 switch, alone and all together, and other window grids: same digests.
#[test]
fn scheduler_switches_do_not_change_results() {
    let scene = scenes::islands(256, 6);
    let expected = reference(&scene, 900);
    let full = Config::default();
    let variants: Vec<(&str, Config)> = vec![
        ("round2", Config::round2()),
        ("no lanes", Config { lanes: false, ..full.clone() }),
        ("no queues", Config { queues: false, ..full.clone() }),
        ("no aimd", Config { aimd: false, ..full.clone() }),
        ("no eligibility", Config { eligibility: false, ..full.clone() }),
        ("no hysteresis", Config { hysteresis: false, ..full.clone() }),
        ("bisection finality", Config { fast_finality: false, ..full.clone() }),
        ("micro", Config { min_region: 8, ..full.clone() }),
        ("window 8, stride ≤ 32", Config { window: 8, stride: 1, stride_max: 32, ..full.clone() }),
        ("window 64 fixed", Config { window: 64, stride: 1, aimd: false, ..full.clone() }),
    ];
    for (name, cfg) in variants {
        for n in [1, 8] {
            for sabotage in [None, Some(99)] {
                let (p, e) = workers(n);
                let (got, rep) = run(&scene, 900, Config { p_workers: p, e_workers: e, sabotage, ..cfg.clone() });
                assert_eq!(got, expected, "{name}: workers {n}, sabotage {sabotage:?} (rollbacks {})", rep.regions.rollbacks);
            }
        }
    }
}

/// A dense relativistic gas region beside many small islands, under both schedulers.
#[test]
fn heavy_tail_equals_one_chronon() {
    let (scene, observer) = scenes::heavy_tail(256, 1024, 4, 6, 40, 400, 900, 3);
    let scene = scenes::with_law(scene, emergent_lattice::law::Law::Relativistic);
    let expected = reference(&scene, 320);
    for (name, cfg) in [("full", Config::default()), ("round2", Config::round2())] {
        for n in [1, 8] {
            for sabotage in [None, Some(7)] {
                let (p, e) = workers(n);
                let (got, rep) = run(&scene, 320, Config { p_workers: p, e_workers: e, sabotage, observer, ..cfg.clone() });
                eprintln!(
                    "heavy tail {name} workers {n} sabotage {}: regions {} (giants {}), rollbacks {}, lat small p99 {:.3} ms, {:.0} ms",
                    sabotage.is_some(), rep.regions.initial, rep.sched.giant_regions_last, rep.regions.rollbacks, rep.sched.latency_small_ms.p99, rep.wall_seconds * 1e3
                );
                assert_eq!(got, expected, "{name}: workers {n}, sabotage {sabotage:?}");
                if sabotage.is_none() {
                    assert!(rep.regions.initial >= 20, "the islands are separate regions");
                }
            }
        }
    }
}
