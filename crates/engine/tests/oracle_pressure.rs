use emergent_engine::scenario::{packed_overlap_island, PACKED_ISLAND_HORIZON};

#[test]
fn packed_pressure_oracle_matches() {
    let mut e = packed_overlap_island().unwrap();
    e.advance_fully(PACKED_ISLAND_HORIZON).unwrap();
    let oracle = e.independent_inertial_facts(e.state.clock).unwrap();
    let mut actual: Vec<_> = e
        .sorted_events()
        .into_iter()
        .filter(|e| e.kind == "contact")
        .map(|e| {
            (
                e.tick,
                e.subjects[0].min(e.subjects[1]),
                e.subjects[0].max(e.subjects[1]),
            )
        })
        .collect();
    actual.sort_unstable();
    actual.dedup();
    let missing: Vec<_> = actual
        .iter()
        .filter(|v| !oracle.contacts.contains(v))
        .collect();
    let extra: Vec<_> = oracle
        .contacts
        .iter()
        .filter(|v| !actual.contains(v))
        .collect();
    eprintln!(
        "oracle={} actual={} missing={missing:?} extra={extra:?}",
        oracle.contacts.len(),
        actual.len()
    );
    assert_eq!(oracle.contacts, actual);
}

use emergent_engine::{
    math::{r, Vec2},
    population::Family,
    propagator::Inertial,
    runtime::{Body, Command},
    Engine,
};

fn ball(id: u64, x: i128, vx: i128) -> Body {
    Body::new(
        id,
        "oracle",
        Inertial::new(
            0,
            Vec2::new(x, 0),
            Vec2 {
                x: r(vx) / r(4),
                y: r(0),
            },
        )
        .unwrap(),
        r(1),
        r(1),
    )
}

#[test]
fn genesis_overlap_and_reburn_follow_revision_semantics() {
    let mut e = Engine::new(1, vec![ball(1, 0, 0), ball(2, 1, 0)], vec![]).unwrap();
    assert!(e.independent_inertial_facts(0).unwrap().contacts.is_empty());
    e.intervene(
        1,
        Command::SetCourse {
            at: 3,
            velocity: Vec2::zero(),
        },
    )
    .unwrap();
    e.advance_fully(6).unwrap();
    assert_eq!(
        e.independent_inertial_facts(6).unwrap().contacts,
        vec![(1, 1, 2), (4, 1, 2)]
    );
    assert!(e.canonical_facts_agree(6).unwrap());
}

#[test]
fn contact_stop_does_not_emit_again_on_new_stop_segment() {
    let mut a = ball(1, 0, 1);
    a.stop_on_contact = true;
    let mut e = Engine::new(2, vec![a, ball(2, 3, 0)], vec![]).unwrap();
    e.advance_fully(10).unwrap();
    assert_eq!(
        e.independent_inertial_facts(10).unwrap().contacts,
        vec![(4, 1, 2)]
    );
    assert!(e.canonical_facts_agree(10).unwrap());
}

#[test]
fn family_history_and_materialized_bank_agree_across_varied_initial_states() {
    // Predeclared bank: change spacing, source position and velocity, not just seed metadata.
    for seed in 0..12u64 {
        let family = Family::affine(
            "bank",
            100,
            3,
            0,
            Inertial::new(0, Vec2::new(4 + (seed % 3) as i128, 0), Vec2::zero()).unwrap(),
            Vec2::new(4 + (seed % 2) as i128, 0),
            r(1),
            r(1),
        );
        let bodies = vec![ball(1, -((seed % 4) as i128), 1 + (seed % 2) as i128)];
        let mut materialized = bodies.clone();
        materialized.extend(emergent_engine::scenario::materialize_family(&family));
        let mut compressed = Engine::new(seed, bodies, vec![family]).unwrap();
        let mut explicit = Engine::new(seed, materialized, vec![]).unwrap();
        for engine in [&mut compressed, &mut explicit] {
            engine
                .intervene(
                    100,
                    Command::SetCourseRange {
                        lo: 100,
                        hi: 102,
                        at: 6,
                        velocity: Vec2 {
                            x: r(-1) / r(8),
                            y: r(0),
                        },
                    },
                )
                .unwrap();
            engine.advance_fully(24).unwrap();
            assert!(engine.canonical_facts_agree(24).unwrap(), "seed={seed}");
        }
        assert_eq!(
            compressed.independent_inertial_facts(24).unwrap(),
            explicit.independent_inertial_facts(24).unwrap(),
            "seed={seed}"
        );
    }
}

#[test]
fn oracle_refuses_unbounded_materialization() {
    let e = emergent_engine::scenario::population_fixture(1_000_000_000, 1).unwrap();
    let mut e = e;
    e.advance_fully(1).unwrap();
    assert!(matches!(
        e.independent_inertial_facts(1),
        Err(emergent_engine::EngineError::ResourceLimit(_))
    ));
}

#[test]
fn oracle_detects_deleted_contact_record_and_coincident_signal_arrival() {
    use emergent_engine::runtime::Payload;
    let mut e = Engine::new(5, vec![ball(1, 0, 0), ball(2, 0, 0)], vec![]).unwrap();
    let signal = e
        .intervene(
            1,
            Command::SendSignal {
                target: 2,
                payload: Payload::Ping,
            },
        )
        .unwrap();
    e.advance_fully(2).unwrap();
    assert_eq!(
        e.independent_inertial_facts(2).unwrap().arrivals,
        vec![(1, 1, 2, signal)]
    );
    assert!(e.canonical_facts_agree(2).unwrap());
    e.state.events.retain(|_, event| event.kind != "contact");
    assert!(!e.canonical_facts_agree(2).unwrap());
}

#[test]
fn independent_predicate_catches_between_tick_contact_and_left_tangent() {
    let mut moving = ball(1, 0, 0);
    moving.segments[0].origin.x = -r(1) / r(4);
    moving.segments[0].velocity.x = r(1) / r(2);
    moving.radius = r(1) / r(32);
    let mut target = ball(2, 0, 0);
    target.radius = r(1) / r(32);
    let mut e = Engine::new(6, vec![moving, target], vec![]).unwrap();
    e.advance_fully(2).unwrap();
    assert_eq!(
        e.independent_inertial_facts(2).unwrap().contacts,
        vec![(1, 1, 2)]
    );
    assert!(e.canonical_facts_agree(2).unwrap());
    // Initially tangent and separating: the sole zero at the open left edge is excluded.
    let mut e = Engine::new(7, vec![ball(1, 0, -1), ball(2, 2, 0)], vec![]).unwrap();
    e.advance_fully(2).unwrap();
    assert!(e.independent_inertial_facts(2).unwrap().contacts.is_empty());
    assert!(e.canonical_facts_agree(2).unwrap());
}

#[test]
fn simultaneous_contact_and_individual_burn_consumes_resulting_revision() {
    let mut e = Engine::new(9, vec![ball(1, 0, 1), ball(2, 3, 0)], vec![]).unwrap();
    e.intervene(
        1,
        Command::SetCourse {
            at: 4,
            velocity: Vec2::zero(),
        },
    )
    .unwrap();
    e.advance_fully(7).unwrap();
    assert_eq!(
        e.independent_inertial_facts(7).unwrap().contacts,
        vec![(4, 1, 2)]
    );
    assert!(e.canonical_facts_agree(7).unwrap());
}

#[test]
fn oracle_detects_one_missing_of_two_coincident_signals() {
    use emergent_engine::runtime::Payload;
    let mut e = Engine::new(10, vec![ball(1, 0, 0), ball(2, 0, 0)], vec![]).unwrap();
    for _ in 0..2 {
        e.intervene(
            1,
            Command::SendSignal {
                target: 2,
                payload: Payload::Ping,
            },
        )
        .unwrap();
    }
    e.advance_fully(2).unwrap();
    assert_eq!(e.independent_inertial_facts(2).unwrap().arrivals.len(), 2);
    assert!(e.canonical_facts_agree(2).unwrap());
    let key = e
        .state
        .events
        .iter()
        .find(|(_, e)| e.kind == "signal_arrived")
        .unwrap()
        .0
        .clone();
    e.state.events.remove(&key);
    assert!(!e.canonical_facts_agree(2).unwrap());
}

#[test]
fn oracle_refuses_ambiguous_range_order_and_excessive_work() {
    let family = Family::affine(
        "ambiguous",
        100,
        2,
        0,
        Inertial::new(0, Vec2::zero(), Vec2::zero()).unwrap(),
        Vec2::new(4, 0),
        r(1),
        r(1),
    );
    let mut e = Engine::new(11, vec![], vec![family]).unwrap();
    for velocity in [
        Vec2::zero(),
        Vec2 {
            x: r(1) / r(8),
            y: r(0),
        },
    ] {
        e.intervene(
            100,
            Command::SetCourseRange {
                lo: 100,
                hi: 101,
                at: 2,
                velocity,
            },
        )
        .unwrap();
    }
    e.advance_fully(3).unwrap();
    assert!(matches!(
        e.independent_inertial_facts(3),
        Err(emergent_engine::EngineError::Unsupported(_))
    ));
    let mut e = Engine::new(12, vec![ball(1, 0, 0), ball(2, 10, 0)], vec![]).unwrap();
    e.advance_fully(10_000_000).unwrap();
    assert!(matches!(
        e.independent_inertial_facts(10_000_000),
        Err(emergent_engine::EngineError::ResourceLimit(_))
    ));
}
