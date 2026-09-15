//! I3: two-region advancement and population representation costs.
//! Broadcast range walk and GEM family perturbation remain named holes.

use emergent_engine::{
    math::{r, Vec2},
    population::Family,
    propagator::Inertial,
    runtime::{Body, Command, Engine, Payload},
    IncomingInfluence, WorkBudget,
};
use std::time::Instant;

fn body(id: u64, x: i128, y: i128) -> Body {
    Body::new(
        id,
        format!("b{id}"),
        Inertial::new(0, Vec2::new(x, y), Vec2::zero()).unwrap(),
        r(1),
        r(1),
    )
}

#[test]
fn i3_two_region_advance_is_not_one_clock_overlay() {
    let mut engine = Engine::new(
        0x13C0_0001,
        vec![body(1, 0, 0), body(2, 8, 0), body(10, 0, 1000), body(11, 8, 1000)],
        vec![],
    )
    .unwrap();
    engine.register_region("south", 1, 2).unwrap();
    engine.register_region("north", 10, 11).unwrap();

    engine
        .intervene(
            1,
            Command::SendSignal {
                target: 2,
                payload: Payload::Ping,
            },
        )
        .unwrap();

    engine
        .advance_region("south", 12, WorkBudget::new(100_000))
        .unwrap();
    assert_eq!(engine.scheduler.region("south").unwrap().certified_through, 12);
    assert_eq!(
        engine.scheduler.region("north").unwrap().certified_through,
        0,
        "north must not inherit south's physics clock"
    );
    assert!(
        engine
            .sorted_events()
            .iter()
            .any(|e| e.kind == "signal_arrived" && e.subjects.contains(&2)),
        "south region must actually commit its arrivals"
    );
    assert!(
        engine
            .sorted_events()
            .iter()
            .filter(|e| e.subjects.contains(&10) || e.subjects.contains(&11))
            .all(|e| e.kind != "signal_arrived"),
        "north must not receive south's signal as a silent global advance"
    );

    engine
        .advance_region("north", 6, WorkBudget::new(100_000))
        .unwrap();
    assert_eq!(engine.scheduler.region("south").unwrap().certified_through, 12);
    assert_eq!(engine.scheduler.region("north").unwrap().certified_through, 6);
    assert!(engine.scheduler.global_cut().is_none());

    let bid = engine
        .intervene(
            1,
            Command::Broadcast {
                lo: 10,
                hi: 11,
                payload: Payload::Ping,
            },
        )
        .unwrap();
    engine
        .note_arriving_influence(
            "north",
            IncomingInfluence {
                id: bid.clone(),
                source_region: "south".into(),
                emission_tick: engine.scheduler.region("south").unwrap().certified_through,
                earliest_arrival: engine.scheduler.region("south").unwrap().certified_through,
            },
        )
        .unwrap();
    engine
        .advance_region("north", 20, WorkBudget::new(100_000))
        .unwrap();
    engine
        .reconcile_region("north", &bid, 20)
        .unwrap();
    engine.certify_region("south", 12).unwrap();
}

#[test]
fn i3_overlapping_regions_require_joint_solve() {
    let mut engine = Engine::new(
        0x13C0_0002,
        vec![body(1, 0, 0), body(2, 2, 0)],
        vec![],
    )
    .unwrap();
    engine.register_region("a", 1, 1).unwrap();
    engine.register_region("b", 2, 2).unwrap();
    let err_a = engine
        .advance_region("a", 4, WorkBudget::new(100_000))
        .unwrap_err();
    let err_b = engine
        .advance_region("b", 4, WorkBudget::new(100_000))
        .unwrap_err();
    assert!(
        err_a.to_string().contains("joint solve") || err_a.to_string().contains("overlap"),
        "close bodies over the same window must not independently certify; {err_a}"
    );
    assert!(
        err_b.to_string().contains("joint solve") || err_b.to_string().contains("overlap"),
        "close bodies over the same window must not independently certify; {err_b}"
    );
    engine
        .advance_joint("a", "b", 4, WorkBudget::new(100_000))
        .unwrap();
    assert_eq!(engine.scheduler.region("a").unwrap().certified_through, 4);
    assert_eq!(engine.scheduler.region("b").unwrap().certified_through, 4);
}

#[test]
fn i3_population_bytes_per_distinction_not_a_solved_population() {
    fn lane(count: u64) -> Family {
        Family::affine(
            "i3-lane",
            10_000,
            count,
            0,
            Inertial::new(0, Vec2::new(0, 50), Vec2 { x: r(1) / r(8), y: r(0) }).unwrap(),
            Vec2::new(8, 0),
            r(1),
            r(1),
        )
    }
    let small = Engine::new(1, vec![body(1, 0, 0)], vec![lane(8)]).unwrap();
    let large = Engine::new(1, vec![body(1, 0, 0)], vec![lane(64)]).unwrap();
    let bytes8 = serde_json::to_vec(&small.state.families).unwrap().len();
    let bytes64 = serde_json::to_vec(&large.state.families).unwrap().len();
    let per8 = bytes8 as f64 / 8.0;
    let per64 = bytes64 as f64 / 64.0;
    eprintln!("I3_POP family_bytes 8={bytes8} 64={bytes64} per_id {per8} vs {per64}");
    assert!(
        per64 < per8,
        "affine generator must not grow linearly with logical membership"
    );
    assert_eq!(large.logical_count(), 65);
    let war = Family::affine(
        "war",
        10_000,
        8,
        0,
        Inertial::new(0, Vec2::new(0, 50), Vec2 { x: r(1) / r(8), y: r(0) }).unwrap(),
        Vec2::new(8, 0),
        r(1),
        r(1),
    );
    let peace = Family::affine(
        "peace",
        10_000,
        8,
        0,
        Inertial::new(0, Vec2::new(0, 50), Vec2 { x: r(1) / r(8), y: r(0) }).unwrap(),
        Vec2::new(8, 0),
        r(1),
        r(1),
    );
    assert_eq!(war.mass, peace.mass);
    assert_eq!(war.count, peace.count);
    assert_eq!(war.stride, peace.stride);
    assert_eq!(war.radius, peace.radius);

    let t0 = Instant::now();
    let mut e = Engine::new(2, vec![body(1, 0, 0)], vec![lane(16)]).unwrap();
    e.intervene(
        10_000,
        Command::SetVelocity {
            velocity: Vec2 { x: r(0), y: r(1) / r(8) },
        },
    )
    .unwrap();
    let _ = e.try_remerge_extracted(10_000).unwrap();
    e.intervene(
        1,
        Command::SetCourseRange {
            lo: 10_008,
            hi: 10_015,
            at: 0,
            velocity: Vec2 { x: r(1) / r(8), y: r(0) },
        },
    )
    .unwrap();
    let _ = e.try_remerge_adjacent_families().unwrap();
    let frag_ns = t0.elapsed().as_nanos();
    eprintln!("I3_POP fragment_remerge_ns={frag_ns} logical={}", e.logical_count());
    eprintln!("I3_REJECT population-as-solved: broadcast still walks materialized ranges; this is generator bytes only");
}

#[test]
fn i3_history_reconstruction_total_cost_is_not_source_only() {
    let mut engine = Engine::new(
        0x13C0_0003,
        vec![body(1, 0, 0), body(2, 8, 0)],
        vec![],
    )
    .unwrap();
    engine
        .intervene(
            1,
            Command::SendSignal {
                target: 2,
                payload: Payload::Ping,
            },
        )
        .unwrap();
    engine.advance_fully(24).unwrap();
    let resident = engine.resident_history_bytes();
    let dir = std::env::temp_dir().join(format!(
        "emergent-i3-archive-{}-{}",
        std::process::id(),
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos()
    ));
    let t_seal = Instant::now();
    engine.seal_archive(&dir, 4).unwrap();
    let seal_ns = t_seal.elapsed().as_nanos();
    let evicted = engine.evict_resident_history().unwrap();
    let after = engine.resident_history_bytes();
    let t_cold = Instant::now();
    let cold = Engine::observe_archived(&dir, 1, 8, &[2]).unwrap();
    let cold_ns = t_cold.elapsed().as_nanos();
    let t_restore = Instant::now();
    let restored = Engine::restore_archive(&dir).unwrap();
    let restore_ns = t_restore.elapsed().as_nanos();
    eprintln!(
        "I3_HIST resident_bytes={resident} after_evict={after} evicted={evicted} seal_ns={seal_ns} cold_ns={cold_ns} restore_ns={restore_ns} cold_hits={}",
        cold.len()
    );
    assert!(evicted > 0);
    assert!(after < resident);
    assert_eq!(restored.state.clock, 24);
    eprintln!(
        "I3_KEEP selective cold observe vs full restore only when the query is admitted; restore_ns={restore_ns} is the reconstruction ledger, not a source-only saving"
    );
    let _ = std::fs::remove_dir_all(&dir);
}
