//! I5 surviving-work measurements. CPU-only. Equal outcomes.
//!
//! Cuts this slice: full-history `received_knowledge` scan → per-observer
//! signal index + broadcast_receptions map; policy burn no longer walks
//! `events`; GEM n-body uses lazy pair inverse. Kernel KEEP stays in the
//! quiet/weak-kick domain. GPU not used (no measured crossover).
//! Not `production_law`. Does not mint `CANONICAL_GRAVITY_ACCEPTANCE`.

use emergent_engine::{
    coupled_adapter::{
        course_change_program, CANONICAL_GRAVITY_ACCEPTANCE, BEACON_ID, EMITTER_ID, SHIP_ID,
    },
    math::{r, Vec2},
    population::Family,
    propagator::Inertial,
    runtime::{Body, Command, Engine, Payload},
    WorkBudget, LAW_ID,
};
use emergent_law_lab::{
    coupled_source_response::{
        compile_source_response_opts, laboratory_two_body, CompileOpts, COUPLED_RESPONSE_LAW_ID,
    },
    i3_kernel::compile_memory_kernel_response,
    i3_secular::laboratory_circular_pair,
    i4_family_gem::{
        affine_family_members, measure_family_sourced_gem, merge_family_into_genesis,
    },
    i4_solar::I4_HORIZON,
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

fn rss_kb() -> Option<u64> {
    let pid = std::process::id().to_string();
    let out = std::process::Command::new("ps")
        .args(["-o", "rss=", "-p", &pid])
        .output()
        .ok()?;
    String::from_utf8(out.stdout)
        .ok()?
        .trim()
        .parse()
        .ok()
}

#[test]
fn i5_surviving_work_improves_knowledge_scan_at_equal_outcomes() {
    assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");
    assert_eq!(LAW_ID, "es-inertial-causal-v1");

    let family_report = measure_family_sourced_gem().expect("family gem");
    eprintln!(
        "I5_FAMILY admitted={} rem={} extract_ledger={} moment_ledger={}",
        family_report.admitted,
        family_report.remainder,
        family_report.extract_ledger,
        family_report.moment_ledger
    );

    let (members, _) = affine_family_members();
    let use_moment = family_report.matched;
    let (genesis, identities) = merge_family_into_genesis(
        laboratory_two_body(),
        members,
        use_moment,
    );
    assert_eq!(identities.count, 4);
    assert!((identities.mu_total - 0.04).abs() < 1e-12);

    let emitter = body(EMITTER_ID, "emitter", 0, 0, 0);
    let mut ship = body(SHIP_ID, "test-ship", 8, 0, 1);
    ship.stop_on_contact = true;
    let mut beacon = body(BEACON_ID, "beacon", 14, 0, 1);
    beacon.stop_on_contact = true;
    let family = Family::affine(
        "i5-fleet",
        10_000,
        4,
        0,
        Inertial::new(0, Vec2::new(20, 6), Vec2 { x: r(1) / r(8), y: r(0) }).unwrap(),
        Vec2::new(8, 0),
        r(1),
        r(10),
    );
    let mut engine = Engine::new(
        0x1500_51C5,
        vec![emitter, ship, beacon],
        vec![family],
    )
    .unwrap();
    engine
        .attach_coupled_laboratory(genesis, I4_HORIZON.min(2.0), 1.0 / 16.0)
        .unwrap();

    let cold = Instant::now();
    drive_coupled(&mut engine);
    let cold_ns = cold.elapsed().as_nanos();
    let compiled = engine.coupled.as_ref().unwrap().compiled.clone().unwrap();
    assert_eq!(compiled.law_id, COUPLED_RESPONSE_LAW_ID);
    let gem_bodies = compiled.genesis.bodies.len();
    assert!(
        gem_bodies >= 3,
        "family mass must source GEM; bodies={gem_bodies}"
    );

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
    engine.advance_fully(40).unwrap();

    let (full, indexed) = engine.knowledge_scan_width(SHIP_ID);
    let knowledge = engine.received_knowledge(SHIP_ID).unwrap();
    let digest = engine.history_digest(engine.state.clock).unwrap();
    let replayed = engine.replay().unwrap();
    assert_eq!(digest, replayed.history_digest(engine.state.clock).unwrap());
    assert_eq!(
        knowledge.received_signals,
        replayed.received_knowledge(SHIP_ID).unwrap().received_signals
    );

    let warm = Instant::now();
    let restored = Engine::from_state(engine.state.clone()).unwrap();
    let warm_knowledge = restored.received_knowledge(SHIP_ID).unwrap();
    let _ = restored.history_digest(restored.state.clock).unwrap();
    let warm_ns = warm.elapsed().as_nanos();
    assert_eq!(knowledge.received_signals, warm_knowledge.received_signals);
    let rss = rss_kb();
    let owned = serde_json::to_vec(&engine.state).map(|b| b.len()).unwrap_or(0);

    let quiet = compile_memory_kernel_response(laboratory_circular_pair(), vec![], 8.0).ok();
    let kernel_ledger = quiet.as_ref().map(|k| k.charge.ledger_total());
    let direct = compile_source_response_opts(
        laboratory_two_body(),
        vec![],
        2.0,
        1.0 / 16.0,
        CompileOpts {
            store_pair_inverse: false,
        },
    )
    .unwrap();

    eprintln!(
        "I5_CPU cold_ns={} warm_ns={} rss_kb={:?} owned_bytes={} gpu=none full_events={} indexed_arrivals={} improved={} gem_bodies={} pair_inverse={} kernel_ledger={:?} family_admitted={} digest_equal=true construction={} reconstruction={} fallback={} query_signals={}",
        cold_ns,
        warm_ns,
        rss,
        owned,
        full,
        indexed,
        indexed <= full,
        gem_bodies,
        direct.pair_inverse.is_none(),
        kernel_ledger,
        family_report.admitted,
        compiled.charge.init + compiled.charge.source_evolution,
        compiled.charge.reconstruction,
        compiled.charge.fallback,
        knowledge.received_signals.len()
    );
    assert!(
        indexed < full,
        "knowledge index must be strictly narrower than a full-history scan"
    );
    assert!(direct.pair_inverse.is_none(), "eager dense LU skipped");
    assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");
    assert!(!engine.sorted_events().iter().any(|e| e.kind == "gravity"));
}
