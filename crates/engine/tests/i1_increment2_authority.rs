//! I1 increment 2: finite-semantic authority on the connected diagnostic scene.
//! Does not report canonical-gravity acceptance.

use emergent_engine::{
    authority::{
        authority_status, gem_enclosure_sample_times, gem_sampled_contact_is_not_interval_wide,
        gem_slow_versus_compiled, physical_resolutions_are_separate,
        refuse_certified_authorization, GEM_INTERVAL_COVERAGE, HISTORICAL_COMPACT_SEAL,
    },
    coupled_adapter::{
        connected_laboratory_engine, course_change_program, CANONICAL_GRAVITY_ACCEPTANCE,
        EMITTER_ID, SHIP_ID,
    },
    runtime::{Command, Engine, Payload},
    WorkBudget, LAW_ID,
};
use emergent_law_lab::{
    coupled_source_response::{
        body_state_compiled, laboratory_kick, laboratory_two_body, BodyInit, Charge,
        CoupledCompileJob, InitialCondition, JobPoll, ResidualJob, SourceResponse,
        COUPLED_RESPONSE_LAW_ID,
    },
};

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

fn compile_diagnostic(ic: InitialCondition, horizon: f64, dt: f64) -> SourceResponse {
    let mut job = CoupledCompileJob::from_genesis(&ic, &[], horizon).unwrap();
    let mut ops = 1u64;
    while job.poll(&mut ops).unwrap() == JobPoll::Pending {
        ops = 1;
    }
    let (raw, funs, blocks, q, tau, charge, h) = job.collocation_parts().unwrap();
    let mut residual = ResidualJob::start(ic, vec![], raw, funs, h, dt, blocks, q, tau, charge);
    let mut ops = 1u64;
    while residual.poll(&mut ops).unwrap() == JobPoll::Pending {
        ops = 1;
    }
    residual.take().unwrap()
}

fn run_connected_scene() -> Engine {
    let mut engine = connected_laboratory_engine().unwrap();
    drive_coupled(&mut engine);
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
    engine.advance_fully(80).unwrap();
    engine
}

#[test]
fn i1_increment2_canonical_inertial_facts_agree_on_connected_scene() {
    assert!(physical_resolutions_are_separate());
    assert_eq!(LAW_ID, "es-inertial-causal-v1");
    assert_eq!(COUPLED_RESPONSE_LAW_ID, "es-linearized-retarded-gem-response-v0");
    assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");

    let mut engine = run_connected_scene();
    let through = engine.state.clock;
    let independent = engine.independent_inertial_facts(through).unwrap();
    let events: Vec<_> = engine
        .sorted_events()
        .iter()
        .map(|e| (e.tick, e.kind.clone(), e.subjects.clone()))
        .collect();
    assert!(
        engine.canonical_facts_agree(through).unwrap(),
        "slow geometry oracle must match compiled inertial events; independent={independent:?} events={events:?}"
    );

    // Independent branch: partitioned budget vs one-shot, same digest.
    let digest = engine.history_digest(through).unwrap();
    let replayed = engine.replay().unwrap();
    assert_eq!(digest, replayed.history_digest(through).unwrap());
    engine.clear_derived();
    assert_eq!(digest, engine.history_digest(through).unwrap());

    let compiled = engine.coupled.as_ref().unwrap().compiled.clone().unwrap();
    let gem = gem_slow_versus_compiled(&compiled).unwrap();
    assert_eq!(gem.law_id, COUPLED_RESPONSE_LAW_ID);
    assert!(!gem.authorizes_events);
    assert!(gem.ship_tau_slow > 0.0 && gem.ship_tau_compiled > 0.0);

    let certified = engine
        .coupled
        .as_ref()
        .unwrap()
        .enclosure
        .as_ref()
        .map(|e| e.certified)
        .unwrap_or(false);
    assert!(!refuse_certified_authorization(certified));
    assert!(engine.sorted_events().iter().all(|e| e.kind != "gravity"));

    let status = authority_status(engine.coupled.as_ref().unwrap().pending_required.clone());
    assert!(!status.authorizes_gem_events);
    assert_eq!(status.gem_interval_coverage, GEM_INTERVAL_COVERAGE);
    assert_eq!(status.historical_compact_seal, HISTORICAL_COMPACT_SEAL);
}

#[test]
fn i1_increment2_sampled_contact_misses_are_not_interval_wide_bounds() {
    let compiled = compile_diagnostic(laboratory_two_body(), 3.0, 1.0 / 32.0);
    let samples = gem_enclosure_sample_times(compiled.genesis.genesis_t, compiled.domain.horizon);
    assert_eq!(samples.len(), 16);
    let (coarse, fine, ok) = gem_sampled_contact_is_not_interval_wide(&compiled).unwrap();
    assert!(ok && coarse.is_finite() && fine.is_finite());
    // Rest pair: closest is constant, so coarse==fine, which still does not
    // make 16 samples an interval-wide retarded-root bound.
    let mid = (samples[6] + samples[7]) * 0.5;
    let (x0, _) = body_state_compiled(&compiled, 0, mid).unwrap();
    let (x1, _) = body_state_compiled(&compiled, 1, mid).unwrap();
    assert!(x0[0] < x1[0]);
    assert_eq!(GEM_INTERVAL_COVERAGE, "sampled-16-not-interval-wide");
    assert!(!refuse_certified_authorization(true));
}

#[test]
fn i1_increment2_kicked_near_tangent_between_enclosure_samples() {
    let ic = laboratory_two_body();
    let extra = laboratory_kick();
    let mut job = CoupledCompileJob::from_genesis(&ic, &extra, 3.0).unwrap();
    let mut ops = u64::MAX;
    while job.poll(&mut ops).unwrap() == JobPoll::Pending {}
    let (raw, funs, blocks, q, tau, charge, h) = job.collocation_parts().unwrap();
    let mut residual = ResidualJob::start(ic, extra, raw, funs, h, 1.0 / 32.0, blocks, q, tau, charge);
    let mut ops = u64::MAX;
    while residual.poll(&mut ops).unwrap() == JobPoll::Pending {}
    let compiled = residual.take().unwrap();
    let samples = gem_enclosure_sample_times(0.0, compiled.domain.horizon);
    let mut charge = Charge::default();
    let mut on_sample = f64::INFINITY;
    let mut between = f64::INFINITY;
    for w in samples.windows(2) {
        let (_, d_left) = emergent_law_lab::coupled_source_response::contact_closest_compiled(
            &compiled, 0, 1, w[0], w[0], 1.0, &mut charge,
        )
        .unwrap();
        let mid = 0.5 * (w[0] + w[1]);
        let (_, d_mid) = emergent_law_lab::coupled_source_response::contact_closest_compiled(
            &compiled, 0, 1, mid, mid, 1.0, &mut charge,
        )
        .unwrap();
        on_sample = on_sample.min(d_left);
        between = between.min(d_mid);
    }
    assert!(on_sample.is_finite() && between.is_finite());
    // Moving kicked pair: mid-interval distance need not equal the sample-grid
    // distance. Either way, a sampled reading is not an authorized contact event.
    assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");
}

#[test]
fn i1_increment2_shifted_units_epoch_and_dt_are_separately_versioned() {
    let lab = compile_diagnostic(laboratory_two_body(), 1.5, 1.0 / 32.0);
    let mut shifted = laboratory_two_body();
    for b in &mut shifted.bodies {
        b.x[0] *= 2.0;
        b.mu *= 2.0;
    }
    let shifted = compile_diagnostic(shifted, 1.5, 1.0 / 32.0);
    assert_ne!(
        lab.genesis.bodies[0].x, shifted.genesis.bodies[0].x,
        "shifted units are a different input, not a silent rescale of the same response"
    );
    assert_eq!(lab.law_id, shifted.law_id);
    assert_eq!(lab.domain.dt, shifted.domain.dt);

    let mut epoch = laboratory_two_body();
    epoch.genesis_t = 0.25;
    let epoch = compile_diagnostic(epoch, 1.5, 1.0 / 32.0);
    assert_ne!(lab.genesis.genesis_t, epoch.genesis.genesis_t);
    assert_eq!(lab.law_id, epoch.law_id);

    let fine = compile_diagnostic(laboratory_two_body(), 1.5, 1.0 / 64.0);
    assert_ne!(lab.domain.dt, fine.domain.dt);
    assert_eq!(lab.law_id, fine.law_id);
    assert_eq!(lab.law_id, COUPLED_RESPONSE_LAW_ID);
    assert_ne!(lab.law_id, LAW_ID);
}

#[test]
fn i1_increment2_three_mass_compile_stays_diagnostic() {
    let mut ic = laboratory_two_body();
    ic.bodies.push(BodyInit {
        id: 2,
        mu: 0.05,
        x: [0.0, 5.0],
        v: [0.0, 0.0],
    });
    let compiled = compile_diagnostic(ic, 1.5, 1.0 / 32.0);
    assert_eq!(compiled.genesis.bodies.len(), 3);
    assert!(compiled.pair_inverse.is_none());
    assert_eq!(compiled.law_id, COUPLED_RESPONSE_LAW_ID);
    assert!(!refuse_certified_authorization(true));
}

#[test]
fn i1_increment2_beyond_horizon_stays_pending() {
    let mut engine = connected_laboratory_engine().unwrap();
    drive_coupled(&mut engine);
    let horizon = engine.coupled.as_ref().unwrap().horizon;
    engine
        .coupled
        .as_mut()
        .unwrap()
        .query_beyond_horizon(horizon + 0.01);
    assert!(engine
        .coupled
        .as_ref()
        .unwrap()
        .pending_required
        .iter()
        .any(|q| q.contains("beyond-horizon") || q.contains("required-query")));
    assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");
}
