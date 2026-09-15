//! I1 increment 1: resumable diagnostic engine path on compiled GEM geometry.
//! Does not report canonical-gravity acceptance.

use emergent_engine::{
    coupled_adapter::{
        connected_laboratory_engine, course_change_program, BoundConsumers, CANONICAL_GRAVITY_ACCEPTANCE,
        BEACON_ID, EMITTER_ID, SHIP_ID,
    },
    runtime::{Command, Engine, Payload},
    WorkBudget,
};
use emergent_law_lab::coupled_source_response::{
    fly_ray_compiled, fly_ship_compiled, laboratory_kick, Charge, SourceResponse,
};
use std::time::Instant;

fn drive_coupled(engine: &mut Engine) {
    let mut pending = 0usize;
    loop {
        let result = engine.advance(0, WorkBudget::new(1)).unwrap();
        if engine.coupled.as_ref().is_some_and(|d| d.is_ready()) {
            break;
        }
        assert!(!result.complete || result.pending_jobs > 0);
        pending += 1;
        assert!(pending < 50_000, "coupled pipeline did not yield to completion");
    }
}

fn bind(engine: &mut Engine) -> BoundConsumers {
    engine
        .coupled
        .as_mut()
        .expect("diagnostic")
        .bind_consumers()
        .expect("compiled consumers")
        .clone()
}

#[test]
fn i1_increment1_connected_diagnostic_scene() {
    assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");

    let mut engine = connected_laboratory_engine().unwrap();
    assert_eq!(engine.coupled.as_ref().unwrap().stage_name(), "collocate");

    // Pause/resume at internal job boundaries (budget = 1).
    let first = engine.advance(0, WorkBudget::new(1)).unwrap();
    assert!(!first.complete);
    assert!(first.pending_jobs >= 1);
    assert!(!engine.coupled.as_ref().unwrap().is_ready());

    // In-process save/restore of an in-flight compile job.
    let snapshot = engine.coupled.as_ref().unwrap().clone();
    let mut restored_job = connected_laboratory_engine().unwrap();
    restored_job.coupled = Some(snapshot);
    drive_coupled(&mut restored_job);
    assert!(restored_job.coupled.as_ref().unwrap().is_ready());

    drive_coupled(&mut engine);
    let diag = engine.coupled.as_ref().unwrap();
    assert!(diag.is_ready());
    assert_eq!(diag.stage_name(), "ready");
    let compiled: SourceResponse = diag.compiled.clone().unwrap();
    assert!(
        !compiled.interval_functions.is_empty(),
        "selected geometry is interval functions, not adapter labels"
    );
    let max_uninterrupted = diag.max_uninterrupted_ns;
    assert!(max_uninterrupted > 0);

    let bound = bind(&mut engine);
    assert!(bound.ship.tau > 0.0);
    assert!(bound.ray.t > 0.1);
    assert!(bound.clock.is_finite() && bound.clock > 0.0 && bound.clock <= 1.0);
    assert!(bound.contact_d.is_finite() && bound.contact_d > 0.0);
    assert!(
        (bound.ship.tau - bound.chord_ship_tau).abs() > 1e-18
            || bound.ship.x != bound.source0.0,
        "compiled lookback must bind GEM interval functions, not a chord-only label"
    );

    // Different query orders: ray-then-ship vs ship-then-ray.
    let mut charge_a = Charge::default();
    let mut charge_b = Charge::default();
    let ship_a = fly_ship_compiled(
        &compiled, 0.1, [0.0, 3.0], [0.125, 0.0], 3.0, 1.0 / 32.0, &mut charge_a,
    )
    .unwrap();
    let ray_a = fly_ray_compiled(
        &compiled, 0.1, [0.0, 3.0], [1.0, 0.0], 8.0, 0.05, &mut charge_a,
    )
    .unwrap();
    let ray_b = fly_ray_compiled(
        &compiled, 0.1, [0.0, 3.0], [1.0, 0.0], 8.0, 0.05, &mut charge_b,
    )
    .unwrap();
    let ship_b = fly_ship_compiled(
        &compiled, 0.1, [0.0, 3.0], [0.125, 0.0], 3.0, 1.0 / 32.0, &mut charge_b,
    )
    .unwrap();
    assert_eq!(ship_a.tau, ship_b.tau);
    assert_eq!(ray_a.path, ray_b.path);

    // Cache clearing rebuilds the same compiled consumers.
    engine.clear_derived();
    let rebound = bind(&mut engine);
    assert_eq!(bound.ship.tau, rebound.ship.tau);
    assert_eq!(bound.contact_d, rebound.contact_d);

    // Pending required query stays visible past the admitted horizon.
    engine
        .coupled
        .as_mut()
        .unwrap()
        .query_beyond_horizon(99.0);
    assert!(engine
        .coupled
        .as_ref()
        .unwrap()
        .pending_required
        .iter()
        .any(|q| q.contains("beyond-horizon") || q.contains("required-query")));
    assert!(engine.coupled_pending_jobs() >= 1);

    // In-flight signal across CanonicalState save/restore.
    let signal_id = engine
        .intervene(
            EMITTER_ID,
            Command::SendSignal {
                target: SHIP_ID,
                payload: Payload::Ping,
            },
        )
        .unwrap();
    assert!(engine.state.signals.contains_key(&signal_id));
    engine.policy = Some(course_change_program(&signal_id));

    let dir = std::env::temp_dir().join(format!(
        "emergent-i1-signal-{}.json",
        std::process::id()
    ));
    engine.checkpoint(&dir).unwrap();
    let mut restored = Engine::restore(&dir).unwrap();
    let _ = std::fs::remove_file(&dir);
    restored.coupled = engine.coupled.clone();
    restored.policy = engine.policy.clone();
    assert!(
        restored.state.signals.contains_key(&signal_id),
        "in-flight signal must survive checkpoint restore"
    );

    let before_pos = restored.decode(SHIP_ID).unwrap().at(0);
    restored.advance_fully(80).unwrap();
    assert!(restored
        .sorted_events()
        .iter()
        .any(|e| e.kind == "signal_arrived"));
    assert!(restored
        .sorted_events()
        .iter()
        .any(|e| e.kind == "burn" && e.tick >= 8 && e.subjects.contains(&SHIP_ID)));
    let ship_now = restored.decode(SHIP_ID).unwrap();
    assert!(
        ship_now.at(16).x > before_pos.x,
        "received-message policy must change the ship's course; pos0={:?} pos16={:?} events={:?}",
        before_pos,
        ship_now.at(16),
        restored
            .sorted_events()
            .iter()
            .map(|e| (e.tick, e.kind.clone()))
            .collect::<Vec<_>>()
    );
    let kinds: Vec<_> = restored
        .sorted_events()
        .iter()
        .map(|e| (e.tick, e.kind.clone(), e.subjects.clone()))
        .collect();
    assert!(
        restored
            .sorted_events()
            .iter()
            .any(|e| e.kind == "contact"
                && e.subjects.contains(&SHIP_ID)
                && e.subjects.contains(&BEACON_ID))
            || restored
                .state
                .contacts
                .iter()
                .any(|c| c.0 == SHIP_ID || c.1 == SHIP_ID),
        "expected engine contact; events={kinds:?} ship={:?} vel={:?} clock={}",
        ship_now.at(restored.state.clock),
        ship_now.flow().velocity,
        restored.state.clock
    );

    // Delayed source feedback + repair on compiled geometry.
    let before_repair = bind(&mut restored);
    restored
        .start_coupled_repair(laboratory_kick())
        .unwrap();
    assert!(!restored.coupled.as_ref().unwrap().is_ready());
    let mut repair_pending = 0usize;
    loop {
        let _ = restored.advance(80, WorkBudget::new(1)).unwrap();
        if restored.coupled.as_ref().unwrap().is_ready() {
            break;
        }
        repair_pending += 1;
        assert!(repair_pending < 50_000);
    }
    assert!(repair_pending > 0, "repair must suspend at internal boundaries");
    let after_repair = bind(&mut restored);
    assert!(
        (after_repair.source0.0[0] - before_repair.source0.0[0]).abs() > 1e-12
            || (after_repair.source0.0[1] - before_repair.source0.0[1]).abs() > 1e-12
            || (after_repair.source1.0[1] - before_repair.source1.0[1]).abs() > 1e-12
            || (after_repair.ship.tau - before_repair.ship.tau).abs() > 1e-12,
        "repair after delayed kick must change compiled source/consumer geometry"
    );

    // Replay preserves inertial canonical facts (signals, burns, contacts).
    let replayed = restored.replay().unwrap();
    assert_eq!(
        restored.history_digest(restored.state.clock).unwrap(),
        replayed.history_digest(replayed.state.clock).unwrap()
    );

    // Allocation / destruction / finalization included in the measured duration.
    let drop_start = Instant::now();
    drop(compiled);
    drop(bound);
    let drop_ns = drop_start.elapsed().as_nanos();
    let measured = restored
        .coupled
        .as_ref()
        .unwrap()
        .max_uninterrupted_ns
        .saturating_add(drop_ns);
    assert!(measured >= max_uninterrupted);
    assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");
    assert!(
        restored.sorted_events().iter().all(|e| {
            e.kind != "gravity" && !e.kind.contains("gem") && e.kind != "certified_mass"
        }),
        "sampled enclosure must not authorize GEM events"
    );
}

#[test]
fn i1_increment2_sampled_certified_does_not_authorize_events() {
    let mut engine = connected_laboratory_engine().unwrap();
    drive_coupled(&mut engine);
    let horizon = engine.coupled.as_ref().unwrap().horizon;
    let _maybe_certified = engine
        .coupled
        .as_ref()
        .unwrap()
        .enclosure
        .as_ref()
        .map(|e| e.certified);
    engine
        .coupled
        .as_mut()
        .unwrap()
        .query_beyond_horizon(horizon + 1.0);
    assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");
    assert_eq!(emergent_engine::LAW_ID, "es-inertial-causal-v1");
    assert_eq!(
        emergent_law_lab::COUPLED_RESPONSE_LAW_ID,
        "es-linearized-retarded-gem-response-v0"
    );
    assert!(
        engine.sorted_events().is_empty()
            || engine
                .sorted_events()
                .iter()
                .all(|e| e.kind != "gravity" && !e.kind.contains("gem")),
        "diagnostic certified:true must not mint a canonical gravity event"
    );
    assert!(engine
        .coupled
        .as_ref()
        .unwrap()
        .pending_required
        .iter()
        .any(|q| q.contains("beyond-horizon") || q.contains("required-query")));
}
