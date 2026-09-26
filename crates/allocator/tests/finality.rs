//! Frames must never show a past that later changes. Forced conflicts (zero speed margin,
//! sabotaged forecasts) make lineages roll back while frames run; every snapshot any frame
//! drew must equal the canonical history (one Chronon over the whole scene) at its tick.
use emergent_allocator::{scenes, Allocator, Config, Factory, FrameConfig, Snap};
use emergent_lattice::{
    chronon::Chronon,
    law::{Response, World},
    worlds, Stepper,
};
use std::sync::Arc;

fn factory() -> Factory<Chronon> {
    Arc::new(|w| Chronon::new(w, false).expect("a region's world is a valid world"))
}

/// Each drawn snapshot equals the reference world restricted to its bodies at its tick.
fn audit(scene: &[World], mut drawn: Vec<Arc<Snap>>) -> usize {
    drawn.sort_by_key(|s| s.tick);
    let mut c = Chronon::new(scenes::union(scene), false).unwrap();
    for s in &drawn {
        c.run_to(s.tick);
        let w = c.world();
        let ids: std::collections::HashSet<u64> = s.world.bodies.iter().map(|b| b.id).collect();
        let reference = World {
            bodies: w.bodies.iter().filter(|b| ids.contains(&b.id)).cloned().collect(),
            consumed: w.consumed.iter().filter(|p| ids.contains(&p.a) && ids.contains(&p.b)).copied().collect(),
            ..s.world.clone()
        };
        assert_eq!(s.world.digest(), reference.digest(), "drawn part of {} bodies at tick {} differs from the canonical history", ids.len(), s.tick);
    }
    drawn.len()
}

#[test]
fn frames_never_show_a_revised_past() {
    // Elastic law: no hard speed, so parts are published at the global all-verified tick.
    let scene = scenes::islands(256, 4);
    let cfg = Config { p_workers: 2, e_workers: 2, speed_margin: 0.0, sabotage: Some(3), observer: [0, 0], view_radius: 200 * 256, ..Config::default() };
    let mut a = Allocator::new(scene.clone(), factory(), cfg).unwrap();
    let rep = a.run_frames(&FrameConfig { hz: 240.0, seconds: 1.5, rate: 700.0, ahead_seconds: 0.3, record: true });
    let n = audit(&scene, a.drawn());
    let f = rep.frames.as_ref().unwrap();
    eprintln!(
        "elastic: {n} drawn parts audited, rollbacks {} (regions {}), depth max {}, present {:.0}, frame work max {:.3} ms",
        rep.regions.rollbacks, rep.regions.rolled_back_regions, rep.regions.rollback_depth_chronons.max, rep.sim.present_end, f.work_ms.max
    );
    assert!(rep.regions.rollbacks > 0, "the run must roll back while frames draw");
    assert!(rep.sim.present_end > 300.0, "frames must advance past the conflicts");
    assert_eq!(f.final_lead_chronons.max, 0.0, "without a hard speed nothing is shown beyond the global frontier");
}

#[test]
fn light_cone_finality_publishes_ahead_and_never_revises() {
    // Pass discs never change velocity and Stop bodies only halt: the genesis maximum is a
    // hard speed the law guarantees here, so near parts may be shown ahead of far laggards.
    let q = 256;
    let mut parts = Vec::new();
    for (i, off) in [[0, 0], [300, 0], [0, 300], [2500, 0], [0, 2500], [2500, 2500]].into_iter().enumerate() {
        let w = worlds::random(40, 300, q, 1, 20 + i as u64, Response::Pass);
        let drift = if i == 1 { [-q / 8, 0] } else { [0, 0] };
        parts.push(scenes::world(&w, scenes::place(&w, 1 + 1000 * i as u64, off, 1, 2, drift)));
    }
    let p = worlds::packed(36, 4, 1, q, 1, 9);
    parts.push(scenes::world(&p, scenes::place(&p, 9001, [1200, 1200], 1, 2, [0, 0])));
    // A heavy, distant cluster: its large light delay lets it lag (causal slack), holding the
    // global frontier back while the near regions become final ahead of it.
    let heavy = worlds::random(1500, 30, q, 1, 77, Response::Pass);
    parts.push(scenes::world(&heavy, scenes::place(&heavy, 20_001, [6000, 6000], 1, 2, [0, 0])));
    let hard = scenes::union(&parts).bodies.iter().map(|b| b.k[0].abs().max(b.k[1].abs())).max().unwrap();
    let cfg = Config { p_workers: 2, e_workers: 2, speed_margin: 0.0, sabotage: Some(5), hard_speed: Some(hard), view_radius: 100 * q, ..Config::default() };
    let mut a = Allocator::new(parts.clone(), factory(), cfg).unwrap();
    let rep = a.run_frames(&FrameConfig { hz: 240.0, seconds: 1.5, rate: 700.0, ahead_seconds: 0.4, record: true });
    let n = audit(&parts, a.drawn());
    let f = rep.frames.as_ref().unwrap();
    eprintln!(
        "light cone: {n} drawn parts audited, rollbacks {}, final lead p50/max {:.0}/{:.0}, violations {}, present {:.0}",
        rep.regions.rollbacks, f.final_lead_chronons.p50, f.final_lead_chronons.max, rep.finality.hard_speed_violations, rep.sim.present_end
    );
    assert_eq!(rep.finality.hard_speed_violations, 0);
    assert!(rep.regions.rollbacks > 0, "the run must roll back while frames draw");
    assert!(f.final_lead_chronons.max > 0.0, "some part must be final ahead of the global frontier");
}

#[test]
fn rollback_is_scoped_to_the_conflict() {
    // Two clusters collide near the origin; five others are far away. Rollbacks must restore
    // only the colliding lineages, and the far islands must never be touched.
    let q = 256;
    let mut parts = Vec::new();
    let offs = [[0, 0], [260, 0], [3000, 0], [0, 3000], [3000, 3000], [6000, 0], [0, 6000]];
    for (i, off) in offs.into_iter().enumerate() {
        let w = worlds::random(40, 300, q, 1, 40 + i as u64, Response::Bounce);
        let drift = match i {
            0 => [q / 8, 0],
            1 => [-q / 8, 0],
            _ => [0, 0],
        };
        parts.push(scenes::world(&w, scenes::place(&w, 1 + 1000 * i as u64, off, 1, 2, drift)));
    }
    let mut c = Chronon::new(scenes::union(&parts), false).unwrap();
    c.run_to(900);
    let expected = c.outcome();
    for n in [1, 8] {
        let cfg = Config { p_workers: n.min(4), e_workers: n.saturating_sub(4), speed_margin: 0.0, ..Config::default() };
        let mut a = Allocator::new(parts.clone(), factory(), cfg).unwrap();
        let rep = a.run_to(900);
        let r = &rep.regions;
        eprintln!("scoped workers {n}: rollbacks {}, regions restored {}, depth max {}, regions {}→{}", r.rollbacks, r.rolled_back_regions, r.rollback_depth_chronons.max, r.initial, r.last);
        assert_eq!(a.outcome(), expected, "workers {n}");
        assert!(r.rollbacks > 0, "the collision must be detected");
        assert!(r.rolled_back_regions <= 3 * r.rollbacks, "a rollback restores the colliding lineages, not the scene");
        assert!(r.last >= 6, "far islands stay separate regions");
    }
}

#[test]
fn relativistic_scene_is_final_ahead_of_the_frontier() {
    // Under the relativistic law |k| < c at every tick: that bound (c − 1 quantum per axis)
    // gives per-region light-cone finality with bouncing bodies, no hard speed configured.
    // A dense gas far away needs ~75 ms of one core per 32-chronon stride, so it cannot finish
    // its first stride before the light islands finish theirs: the global frontier is held at
    // its clock while the islands, thousands of light-chronons away, are final ahead of it.
    let q = 256;
    let mut parts = Vec::new();
    for (i, off) in [[0, 0], [400, 0], [0, 400], [400, 400]].into_iter().enumerate() {
        let w = if i % 2 == 0 { scenes::loose_mixed(36, q, 30 + i as u64) } else { worlds::random(40, 300, q, 1, 30 + i as u64, Response::Bounce) };
        parts.push(scenes::world(&w, scenes::place(&w, 1 + 1000 * i as u64, off, 1, 1, [0, 0])));
    }
    parts.push(scenes::loose_gas(4096, q, q / 4, 8, 100_000, [6000, 6000]));
    let parts = scenes::with_law(parts, emergent_lattice::law::Law::Relativistic);
    let cfg = Config { p_workers: 2, e_workers: 2, view_radius: 100 * q, sabotage: Some(11), ..Config::default() };
    let mut a = Allocator::new(parts.clone(), factory(), cfg).unwrap();
    let rep = a.run_frames(&FrameConfig { hz: 240.0, seconds: 1.0, rate: 500.0, ahead_seconds: 0.5, record: true });
    let n = audit(&parts, a.drawn());
    let f = rep.frames.as_ref().unwrap();
    eprintln!(
        "relativistic: {n} drawn parts audited, light cone {}, final lead p50/max {:.0}/{:.0}, rollbacks {}, violations {}, present {:.0}, frontier {}",
        rep.finality.light_cone, f.final_lead_chronons.p50, f.final_lead_chronons.max, rep.regions.rollbacks, rep.finality.hard_speed_violations, rep.sim.present_end, rep.finality.frontier
    );
    assert!(rep.finality.light_cone && rep.finality.hard_speed_violations == 0);
    assert!(f.final_lead_chronons.max > 0.0, "some part must be final ahead of the global frontier");
}
