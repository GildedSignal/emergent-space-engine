use emergent_engine::{
    math::{r, Vec2},
    population::Family,
    propagator::Inertial,
    runtime::{Body, Payload},
    scenario, Command, Engine, WorkBudget,
};

fn body(id: u64, x: i128, y: i128, vx: i128, vy: i128, den: i128) -> Body {
    Body::new(
        id,
        format!("ship {id}"),
        Inertial::new(
            0,
            Vec2::new(x, y),
            Vec2 {
                x: r(vx) / r(den),
                y: r(vy) / r(den),
            },
        )
        .unwrap(),
        r(1) / r(8),
        r(1),
    )
}

#[test]
fn complete_causal_loop_and_independent_witness() {
    let mut e = scenario::causal_relay().unwrap();
    let witness = e.decode(4).unwrap();
    e.advance_fully(100).unwrap();
    let log = e.sorted_events();
    assert!(log
        .iter()
        .any(|e| e.kind == "signal_arrived" && e.tick == 14));
    assert!(log.iter().any(|e| e.kind == "contact" && e.tick == 43));
    assert!(log
        .iter()
        .any(|e| e.kind == "signal_arrived" && e.tick == 71));
    assert_eq!(e.decode(4).unwrap(), witness);
    assert_eq!(e.decode(2).unwrap().flow().velocity, Vec2::zero());
}

#[test]
fn budget_partition_subdivision_and_cold_restart_do_not_change_history() {
    let mut whole = scenario::causal_relay().unwrap();
    whole.advance_fully(100).unwrap();
    let mut chunked = scenario::causal_relay().unwrap();
    for t in [3, 14, 20, 43, 44, 71, 100] {
        let result = chunked.advance(t, WorkBudget::new(1)).unwrap();
        chunked = Engine::from_state(chunked.state.clone()).unwrap();
        // Restart from canonical state after partial evaluation, then finish the search.
        if !result.complete {
            chunked.advance_fully(t).unwrap();
        }
    }
    assert_eq!(
        whole.history_digest(100).unwrap(),
        chunked.history_digest(100).unwrap()
    );
    assert_eq!(
        whole.state.actuator_momentum,
        chunked.state.actuator_momentum
    );
}

#[test]
fn single_operation_continuations_terminate_and_preserve_result() {
    let mut reference = scenario::causal_relay().unwrap();
    reference.advance_fully(100).unwrap();
    let mut e = scenario::causal_relay().unwrap();
    let mut completed = false;
    for _ in 0..1000 {
        if e.advance(100, WorkBudget::new(1)).unwrap().complete {
            completed = true;
            break;
        }
    }
    assert!(completed);
    assert_eq!(
        e.history_digest(100).unwrap(),
        reference.history_digest(100).unwrap()
    );
}

#[test]
fn future_inspection_and_zero_budget_never_claim_completion() {
    let mut e = scenario::causal_relay().unwrap();
    assert!(e.inspect(2, 10).is_err());
    let before = e.history_digest(0).unwrap();
    let result = e.advance(100, WorkBudget::new(0)).unwrap();
    assert!(!result.complete);
    assert_eq!(e.history_digest(0).unwrap(), before);
}

#[test]
fn opposing_simultaneous_impulses_commute() {
    fn run(reverse: bool) -> Engine {
        let mut e = Engine::new(
            7,
            vec![
                body(1, -8, 0, 0, 0, 1),
                body(2, 8, 0, 0, 0, 1),
                body(3, 0, 0, 0, 0, 1),
            ],
            vec![],
        )
        .unwrap();
        for src in if reverse { [2, 1] } else { [1, 2] } {
            e.intervene(
                src,
                Command::SendSignal {
                    target: 3,
                    payload: Payload::Impulse {
                        delta: Vec2 {
                            x: r(if src == 1 { 1 } else { -1 }) / r(4),
                            y: r(0),
                        },
                    },
                },
            )
            .unwrap();
        }
        e.advance_fully(20).unwrap();
        e
    }
    let a = run(false);
    let b = run(true);
    assert_eq!(a.history_digest(20).unwrap(), b.history_digest(20).unwrap());
    assert_eq!(a.decode(3).unwrap().flow().velocity, Vec2::zero());
}

#[test]
fn invalid_simultaneous_burn_is_atomic() {
    let mut e = Engine::new(
        7,
        vec![
            body(1, -8, 0, 0, 0, 1),
            body(2, 8, 0, 0, 0, 1),
            body(3, 0, 0, 0, 0, 1),
        ],
        vec![],
    )
    .unwrap();
    for src in [1, 2] {
        e.intervene(
            src,
            Command::SendSignal {
                target: 3,
                payload: Payload::Impulse {
                    delta: Vec2 {
                        x: r(3) / r(4),
                        y: r(0),
                    },
                },
            },
        )
        .unwrap();
    }
    let before = serde_json::to_string(&e.state).unwrap();
    assert!(e.advance_fully(20).is_err());
    assert_eq!(before, serde_json::to_string(&e.state).unwrap());
}

#[test]
fn receiver_course_change_invalidates_old_signal_arrival() {
    let mut e = Engine::new(
        1,
        vec![body(1, 0, 0, 0, 0, 1), body(2, 10, 0, 1, 4, 8)],
        vec![],
    )
    .unwrap();
    e.intervene(
        1,
        Command::SendSignal {
            target: 2,
            payload: Payload::Ping,
        },
    )
    .unwrap();
    e.advance_fully(3).unwrap();
    e.intervene(
        2,
        Command::SetVelocity {
            velocity: Vec2::zero(),
        },
    )
    .unwrap();
    let position = e.decode(2).unwrap().at(3);
    e.advance_fully(100).unwrap();
    let t = e
        .sorted_events()
        .into_iter()
        .find(|x| x.kind == "signal_arrived")
        .unwrap()
        .tick;
    assert!(r(t) * r(t) >= position.norm_squared());
    assert!(r(t - 1) * r(t - 1) < position.norm_squared());
}

#[test]
fn family_splits_and_lookup_are_representation_only() {
    let base = scenario::population_fixture(1_000_000_000, 1).unwrap();
    let f = base.state.families[0].clone();
    let (a, b) = f.split(1_234_567).unwrap();
    let mut split = Engine::new(base.state.seed, vec![], vec![b, a]).unwrap();
    let mut whole = base;
    let hash = whole.history_digest(0).unwrap();
    for id in [10000, 10001, 512345678, 1000009999] {
        whole.inspect(id, 0).unwrap();
    }
    assert_eq!(whole.history_digest(0).unwrap(), hash);
    assert!(whole.state.bodies.is_empty());
    whole.advance_fully(scenario::TEN_BILLION_YEARS).unwrap();
    split.advance_fully(scenario::TEN_BILLION_YEARS).unwrap();
    assert_eq!(
        whole.history_digest(scenario::TEN_BILLION_YEARS).unwrap(),
        split.history_digest(scenario::TEN_BILLION_YEARS).unwrap()
    );
    assert_eq!(whole.metrics.search_operations, 0);
}

#[test]
fn one_ship_burn_extracts_only_that_identity() {
    let mut e = scenario::population_fixture(1_000_000_000, 1).unwrap();
    let id = 10000 + 700000000;
    let neighbor = e.decode(id + 1).unwrap();
    e.intervene(
        id,
        Command::SetVelocity {
            velocity: Vec2::zero(),
        },
    )
    .unwrap();
    assert_eq!(e.state.bodies.len(), 1);
    assert_eq!(e.decode(id + 1).unwrap(), neighbor);
    assert_eq!(e.logical_count(), 1_000_000_000);
}

#[test]
fn contacts_between_samples_are_not_missed() {
    let a = body(1, 0, 0, 3, 0, 4);
    let mut b = body(2, 1, 0, -3, 0, 4);
    b.radius = r(1) / r(100);
    let mut e = Engine::new(1, vec![a, b], vec![]).unwrap();
    e.advance_fully(2).unwrap();
    assert!(e
        .sorted_events()
        .iter()
        .any(|e| e.kind == "contact" && e.tick == 1));
}

#[test]
fn observational_queries_are_pure_and_occluders_block_light() {
    let mut obstacle = body(3, 5, 0, 0, 0, 1);
    obstacle.radius = r(1);
    let mut e = Engine::new(
        1,
        vec![body(1, 0, 0, 0, 0, 1), body(2, 10, 0, 0, 0, 1), obstacle],
        vec![],
    )
    .unwrap();
    e.advance_fully(100).unwrap();
    let before = serde_json::to_string(&e.state).unwrap();
    let observed = e.observe(1, 100, &[2, 3]).unwrap();
    assert!(!observed.iter().any(|x| x.entity == 2));
    assert!(observed.iter().any(|x| x.entity == 3));
    assert_eq!(before, serde_json::to_string(&e.state).unwrap());
}

#[test]
fn exhaustive_small_world_contact_oracle() {
    // Independent exact closest-approach check per continuous tick bin, no production root search.
    for x in -4..=4 {
        for y in -2..=2 {
            for numerator in [-3, -1, 1, 3] {
                let a = body(1, 0, 0, 0, 0, 1);
                let b = body(2, x, y, numerator, 1, 8);
                let radius = &a.radius + &b.radius;
                let mut expected = None;
                for tick in 1..=24 {
                    let d = b.at(tick - 1) - a.at(tick - 1);
                    let v = b.flow().velocity.clone();
                    let u = (-d.dot(&v) / v.norm_squared()).max(r(0)).min(r(1));
                    if (d + v * u).norm_squared() <= &radius * &radius {
                        expected = Some(tick);
                        break;
                    }
                }
                let mut e = Engine::new(42, vec![a, b], vec![]).unwrap();
                e.advance_fully(24).unwrap();
                let actual = e
                    .sorted_events()
                    .into_iter()
                    .find(|x| x.kind == "contact")
                    .map(|x| x.tick);
                assert_eq!(actual, expected, "x={x},y={y},v={numerator}");
            }
        }
    }
}

#[test]
fn stationary_family_source_moments_equal_materialized_sum() {
    let f = Family {
        name: "affine".into(),
        first_id: 100,
        count: 50,
        offset: 9,
        trajectory: Inertial::new(
            0,
            Vec2::new(3, -2),
            Vec2 {
                x: r(1) / r(3),
                y: r(0),
            },
        )
        .unwrap(),
        stride: Vec2::new(9, 7),
        radius: r(1),
        mass: r(3),
    };
    let sum = (100..150).fold(Vec2::zero(), |sum, id| {
        sum + f.member(id).unwrap().state_at(100) * r(3)
    });
    assert_eq!(sum, f.first_moment(100));
}

#[test]
fn extracted_family_collisions_match_a_materialized_population() {
    let f = Family {
        name: "route".into(),
        first_id: 100,
        count: 8,
        offset: 0,
        trajectory: Inertial::new(0, Vec2::new(10, 0), Vec2::zero()).unwrap(),
        stride: Vec2::new(8, 0),
        radius: r(1) / r(8),
        mass: r(1),
    };
    for changed in [100, 103, 107] {
        let explicit = (100..108)
            .map(|id| Body::new(id, "route", f.member(id).unwrap(), f.radius.clone(), r(1)))
            .collect();
        let mut a = Engine::new(7, vec![], vec![f.clone()]).unwrap();
        let mut b = Engine::new(7, explicit, vec![]).unwrap();
        let v = Vec2 {
            x: r(if changed == 100 { 1 } else { -1 }) / r(2),
            y: r(0),
        };
        for e in [&mut a, &mut b] {
            e.intervene(
                changed,
                Command::SetVelocity {
                    velocity: v.clone(),
                },
            )
            .unwrap();
            e.advance_fully(40).unwrap();
        }
        assert_eq!(a.sorted_events(), b.sorted_events());
        assert!(a.sorted_events().iter().any(|e| e.kind == "contact"));
    }
}

#[test]
fn extreme_identity_and_restored_range_order_are_validated() {
    let mut e = scenario::population_fixture(8, 2).unwrap();
    e.state.families.reverse();
    assert!(Engine::from_state(e.state).is_err());
    let mut f = scenario::population_fixture(8, 1)
        .unwrap()
        .state
        .families
        .remove(0);
    f.first_id = u64::MAX - 7;
    let mut e = Engine::new(7, vec![], vec![f]).unwrap();
    e.intervene(
        u64::MAX,
        Command::SetVelocity {
            velocity: Vec2::zero(),
        },
    )
    .unwrap();
    e.advance_fully(100).unwrap();
    assert_eq!(e.logical_count(), 8);
    assert!(e.position(u64::MAX, 100).is_ok());
}

#[test]
fn failed_notification_capacity_is_atomic_and_resumable() {
    let mut e = scenario::causal_relay().unwrap();
    e.advance_fully(42).unwrap();
    e.max_pending_jobs = 0;
    let before = serde_json::to_vec(&e.state).unwrap();
    assert!(e.advance_fully(100).is_err());
    assert_eq!(before, serde_json::to_vec(&e.state).unwrap());
    e.max_pending_jobs = 1000;
    e.state.emitter_sequence.insert(2, u64::MAX);
    let before = serde_json::to_vec(&e.state).unwrap();
    assert!(e.advance_fully(100).is_err());
    assert_eq!(before, serde_json::to_vec(&e.state).unwrap());
    e.state.emitter_sequence.insert(2, 0);
    e.advance_fully(100).unwrap();
    assert!(e
        .sorted_events()
        .iter()
        .any(|e| e.kind == "signal_arrived" && e.tick == 71));
}

#[test]
fn replay_rebuilds_causal_facts_from_genesis_and_commands() {
    let mut e = scenario::causal_relay().unwrap();
    e.advance_fully(20).unwrap();
    e.intervene(
        4,
        Command::SetVelocity {
            velocity: Vec2 {
                x: r(1) / r(8),
                y: r(0),
            },
        },
    )
    .unwrap();
    e.advance_fully(100).unwrap();
    let rebuilt = e.replay().unwrap();
    assert_eq!(
        serde_json::to_vec(&e.state).unwrap(),
        serde_json::to_vec(&rebuilt.state).unwrap()
    );
    e.state.events.clear();
    assert!(e.replay().is_err());
}

#[test]
fn indexed_occluders_match_individual_observations() {
    let f = Family {
        name: "occluders".into(),
        first_id: 100,
        count: 64,
        offset: 0,
        trajectory: Inertial::new(0, Vec2::new(5, 0), Vec2::zero()).unwrap(),
        stride: Vec2::new(0, 8),
        radius: r(1),
        mass: r(1),
    };
    let endpoints = vec![body(1, 0, 0, 0, 0, 1), body(2, 10, 0, 0, 0, 1)];
    let mut individual = endpoints.clone();
    individual
        .extend((100..164).map(|id| Body::new(id, "occluders", f.member(id).unwrap(), r(1), r(1))));
    let mut a = Engine::new(9, endpoints, vec![f]).unwrap();
    let mut b = Engine::new(9, individual, vec![]).unwrap();
    for e in [&mut a, &mut b] {
        e.advance_fully(100).unwrap();
    }
    assert_eq!(
        a.observe(1, 100, &[2]).unwrap(),
        b.observe(1, 100, &[2]).unwrap()
    );
    assert!(a.observe(1, 100, &[2]).unwrap().is_empty());
    for e in [&mut a, &mut b] {
        e.intervene(
            100,
            Command::SetVelocity {
                velocity: Vec2 {
                    x: r(0),
                    y: r(1) / r(2),
                },
            },
        )
        .unwrap();
        e.advance_fully(120).unwrap();
    }
    assert_eq!(
        a.observe(1, 120, &[2]).unwrap(),
        b.observe(1, 120, &[2]).unwrap()
    );
    assert_eq!(a.observe(1, 120, &[2]).unwrap().len(), 1);
}
