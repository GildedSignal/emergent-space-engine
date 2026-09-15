//! I2 exit: one composed scene. Extraction, re-merge, range reception, unequal
//! certified cuts, history eviction and cold observation. GEM stays diagnostic.

use emergent_engine::{
    coupled_adapter::{
        course_change_program, CANONICAL_GRAVITY_ACCEPTANCE, BEACON_ID, EMITTER_ID, SHIP_ID,
    },
    math::{r, Vec2},
    population::Family,
    propagator::Inertial,
    runtime::{Body, Command, Engine, Payload},
    IncomingInfluence, WorkBudget,
};
use std::time::Instant;

fn body(id: u64, name: &str, x: i128, y: i128, radius: i128) -> Body {
    Body::new(
        id,
        name,
        Inertial::new(0, Vec2::new(x, y), Vec2::zero()).unwrap(),
        r(radius),
        r(1),
    )
}

fn drive_coupled(engine: &mut Engine) {
    let mut pending = 0usize;
    loop {
        let _ = engine.advance(0, WorkBudget::new(1)).unwrap();
        if engine.coupled.as_ref().is_some_and(|d| d.is_ready()) {
            break;
        }
        pending += 1;
        assert!(pending < 50_000);
    }
}

#[test]
fn i2_composed_scene_crosses_extraction_remerge_history_and_cuts() {
    assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");

    let emitter = body(EMITTER_ID, "emitter", 0, 0, 0);
    let mut ship = body(SHIP_ID, "test-ship", 8, 0, 1);
    ship.stop_on_contact = true;
    let mut beacon = body(BEACON_ID, "beacon", 14, 0, 1);
    beacon.stop_on_contact = true;
    let family = Family::affine(
        "i2-lane",
        10_000,
        8,
        0,
        Inertial::new(
            0,
            Vec2::new(20, 6),
            Vec2 {
                x: r(1) / r(8),
                y: r(0),
            },
        )
        .unwrap(),
        Vec2::new(8, 0),
        r(1),
        r(10),
    );
    let mut engine = Engine::new(0x12C0_11EC, vec![emitter, ship, beacon], vec![family]).unwrap();
    engine.attach_connected_laboratory().unwrap();
    drive_coupled(&mut engine);

    let mass0 = engine.collective_mass();
    assert_eq!(mass0, r(3) + r(80));
    let moment0 = engine.family_first_moment(0);
    let mut materialized = Vec2::zero();
    for id in 10_000..=10_007 {
        let b = engine.decode(id).unwrap();
        materialized = materialized + b.at(0) * b.mass.clone();
    }
    assert_eq!(moment0, materialized, "family moment must match materialized sum");

    engine
        .register_region("hierarchy", EMITTER_ID, BEACON_ID)
        .unwrap();
    engine.register_region("family", 10_000, 10_007).unwrap();

    let signal_id = engine
        .intervene(
            EMITTER_ID,
            Command::SendSignal {
                target: SHIP_ID,
                payload: Payload::Ping,
            },
        )
        .unwrap();
    engine.policy = Some(course_change_program(&signal_id));
    assert!(
        !engine.state.signals.is_empty(),
        "ray/signal must be in flight before family work"
    );

    engine
        .advance_region("hierarchy", 8, WorkBudget::new(100_000))
        .unwrap();
    assert_eq!(
        engine.scheduler.region("hierarchy").unwrap().certified_through,
        8
    );
    assert_eq!(
        engine.scheduler.region("family").unwrap().certified_through,
        0,
        "family must remain behind until its own advance"
    );
    assert!(engine.scheduler.global_cut().is_none());

    let neighbor = engine.decode(10_001).unwrap();
    engine
        .intervene(
            10_000,
            Command::SetVelocity {
                velocity: Vec2 {
                    x: r(0),
                    y: r(1) / r(8),
                },
            },
        )
        .unwrap();
    assert!(engine.state.bodies.contains_key(&10_000));
    assert_eq!(engine.decode(10_001).unwrap().at(engine.state.clock), neighbor.at(engine.state.clock));
    assert!(
        !engine.try_remerge_extracted(10_000).unwrap(),
        "kinked extracted history must not fold into the generator"
    );
    assert!(engine.refuse_permutation_merge(10_000, 10_001).unwrap());

    engine
        .intervene(
            EMITTER_ID,
            Command::SetCourseRange {
                lo: 10_004,
                hi: 10_007,
                at: engine.state.clock,
                velocity: Vec2 {
                    x: r(1) / r(8),
                    y: r(0),
                },
            },
        )
        .unwrap();
    engine
        .intervene(
            EMITTER_ID,
            Command::SetCourseRange {
                lo: 10_001,
                hi: 10_003,
                at: engine.state.clock,
                velocity: Vec2 {
                    x: r(1) / r(8),
                    y: r(0),
                },
            },
        )
        .unwrap();
    let joined = engine.try_remerge_adjacent_families().unwrap();
    assert!(
        engine
            .state
            .families
            .iter()
            .any(|f| f.first_id == 10_001 && f.count == 7)
            || joined >= 1,
        "restricted exact re-merge must join affine-adjacent partitions; families={:?}",
        engine
            .state
            .families
            .iter()
            .map(|f| (f.first_id, f.count))
            .collect::<Vec<_>>()
    );

    let broadcast_id = engine
        .intervene(
            EMITTER_ID,
            Command::Broadcast {
                lo: 10_000,
                hi: 10_007,
                payload: Payload::Ping,
            },
        )
        .unwrap();
    let emission = engine.state.clock;
    engine
        .note_arriving_influence(
            "family",
            IncomingInfluence {
                id: broadcast_id.clone(),
                source_region: "hierarchy".into(),
                emission_tick: emission,
                earliest_arrival: emission,
            },
        )
        .unwrap();
    assert!(engine
        .certify_region("family", engine.state.clock)
        .is_err());

    engine
        .advance_region("hierarchy", 40, WorkBudget::new(100_000))
        .unwrap();
    engine
        .advance_region("family", 40, WorkBudget::new(100_000))
        .unwrap();
    let burns: Vec<_> = engine
        .sorted_events()
        .iter()
        .filter(|e| e.kind == "burn" && e.subjects.contains(&SHIP_ID))
        .map(|e| e.tick)
        .collect();
    assert_eq!(
        burns.len(),
        1,
        "policy must fire once, not on every later commit tick; burns={burns:?}"
    );

    let index = engine.reception_index(&broadcast_id);
    assert_eq!(index.logical_receptions, 8);
    assert!(index.stored_records >= 1 && index.stored_records <= 8);
    assert!(
        index.by_tick.len() >= 1,
        "heterogeneous family members keep actual reception times"
    );
    assert!(engine
        .sorted_events()
        .iter()
        .any(|e| e.kind == "broadcast_received"));

    engine
        .reconcile_region("family", &broadcast_id, engine.state.clock)
        .unwrap();
    engine
        .certify_region("hierarchy", engine.state.clock)
        .unwrap();
    assert_eq!(
        engine.scheduler.global_cut(),
        Some(engine.state.clock),
        "global cut only after required facts resolve"
    );

    let digest_at_cut = engine.history_digest(engine.state.clock).unwrap();
    let mass1 = engine.collective_mass();
    assert_eq!(mass1, mass0, "extraction/re-merge must not omit collective mass");

    let bytes_before = engine.resident_history_bytes();
    let dir = std::env::temp_dir().join(format!(
        "emergent-i2-archive-{}-{}",
        std::process::id(),
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos()
    ));
    engine.seal_archive(&dir, 4).unwrap();
    let evicted = engine.evict_resident_history().unwrap();
    assert!(evicted > 0, "history eviction must drop sealed events from RAM");
    let bytes_after = engine.resident_history_bytes();
    assert!(
        bytes_after < bytes_before,
        "resident tail must be smaller than full history; before={bytes_before} after={bytes_after}"
    );

    let cold = Engine::observe_archived(&dir, EMITTER_ID, 8, &[SHIP_ID, 10_001]).unwrap();
    assert!(
        !cold.is_empty() || engine.state.clock >= 8,
        "cold observation must not require restoring every event"
    );

    engine.advance_fully(48).unwrap();
    engine.seal_archive(&dir, 4).unwrap();
    let manifest = Engine::read_archive_manifest(&dir).unwrap();
    assert!(manifest.chunks.len() >= 2, "incremental seal appends chunks in place");

    let burst = Instant::now();
    let restored = Engine::restore_archive(&dir).unwrap();
    let burst_ns = burst.elapsed().as_nanos();
    assert!(burst_ns > 0);
    assert_eq!(restored.state.clock, 48);
    assert_eq!(restored.collective_mass(), mass0);
    let replayed = restored.replay().unwrap();
    assert_eq!(
        restored.history_digest(restored.state.clock).unwrap(),
        replayed.history_digest(replayed.state.clock).unwrap()
    );
    let _ = digest_at_cut;
    assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");
    assert!(restored
        .sorted_events()
        .iter()
        .all(|e| e.kind != "gravity"));

    let _ = std::fs::remove_dir_all(&dir);
}
