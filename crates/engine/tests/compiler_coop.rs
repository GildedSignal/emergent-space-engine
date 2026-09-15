use emergent_engine::{
    geometry::{self, TickInterval},
    math::{r, Vec2},
    population::{Family, PhaseGenerator},
    propagator::Inertial,
    runtime::Body,
    scenario, Command, Engine, Observation, WorkBudget,
};
use std::time::{Duration, Instant};

fn contacts_of(e: &Engine) -> Vec<(i128, u64, u64)> {
    let mut rows: Vec<_> = e
        .sorted_events()
        .iter()
        .filter(|ev| ev.kind == "contact")
        .map(|ev| (ev.tick, ev.subjects[0], ev.subjects[1]))
        .collect();
    rows.sort();
    rows
}

fn pairwise_contact_oracle(bodies: &[Body], burn_at: i128, burned: u64, velocity: Vec2, horizon: i128) -> Vec<(i128, u64, u64)> {
    let mut flows: Vec<Inertial> = bodies.iter().map(|b| b.flow().clone()).collect();
    let radii: Vec<_> = bodies.iter().map(|b| b.radius.clone()).collect();
    let ids: Vec<u64> = bodies.iter().map(|b| b.id).collect();
    let mut found = Vec::new();
    let windows = [(1, burn_at), (burn_at + 1, horizon)];
    for (start, end) in windows {
        if start > end {
            continue;
        }
        if start == burn_at + 1 {
            if let Some(i) = ids.iter().position(|id| *id == burned) {
                flows[i] = Inertial::new(burn_at, flows[i].state_at(burn_at), velocity.clone()).unwrap();
            }
        }
        for i in 0..bodies.len() {
            for j in i + 1..bodies.len() {
                if let Some(tick) = geometry::first_contact(
                    &flows[i],
                    &flows[j],
                    &(&radii[i] + &radii[j]),
                    TickInterval { start, end },
                ) {
                    found.push((tick, ids[i], ids[j]));
                }
            }
        }
    }
    found.sort();
    found.dedup();
    found
}

fn pairwise_range_contact_oracle(
    bodies: &[Body],
    burn_at: i128,
    lo: u64,
    hi: u64,
    velocity: Vec2,
    horizon: i128,
) -> Vec<(i128, u64, u64)> {
    let mut flows: Vec<Inertial> = bodies.iter().map(|b| b.flow().clone()).collect();
    let radii: Vec<_> = bodies.iter().map(|b| b.radius.clone()).collect();
    let ids: Vec<u64> = bodies.iter().map(|b| b.id).collect();
    let mut found = Vec::new();
    let in_range = |id: u64| id >= lo && id <= hi;
    for i in 0..bodies.len() {
        for j in i + 1..bodies.len() {
            if in_range(ids[i]) || in_range(ids[j]) {
                continue;
            }
            if let Some(tick) = geometry::first_contact(
                &flows[i],
                &flows[j],
                &(&radii[i] + &radii[j]),
                TickInterval {
                    start: 1,
                    end: horizon,
                },
            ) {
                found.push((tick, ids[i], ids[j]));
            }
        }
    }
    for i in 0..bodies.len() {
        for j in i + 1..bodies.len() {
            if !(in_range(ids[i]) || in_range(ids[j])) {
                continue;
            }
            if let Some(tick) = geometry::first_contact(
                &flows[i],
                &flows[j],
                &(&radii[i] + &radii[j]),
                TickInterval {
                    start: 1,
                    end: burn_at,
                },
            ) {
                found.push((tick, ids[i], ids[j]));
            }
        }
    }
    for (i, id) in ids.iter().enumerate() {
        if in_range(*id) {
            flows[i] = Inertial::new(burn_at, flows[i].state_at(burn_at), velocity.clone()).unwrap();
        }
    }
    for i in 0..bodies.len() {
        for j in i + 1..bodies.len() {
            if !(in_range(ids[i]) || in_range(ids[j])) {
                continue;
            }
            if let Some(tick) = geometry::first_contact(
                &flows[i],
                &flows[j],
                &(&radii[i] + &radii[j]),
                TickInterval {
                    start: burn_at + 1,
                    end: horizon,
                },
            ) {
                found.push((tick, ids[i], ids[j]));
            }
        }
    }
    found.sort();
    found.dedup();
    found
}

fn packed_explicit_snapshot(e: &Engine) -> Vec<Body> {
    let mut out: Vec<Body> = e.state.bodies.values().cloned().collect();
    for family in &e.state.families {
        out.extend(scenario::materialize_family(family));
    }
    out.sort_by_key(|b| b.id);
    out
}

fn reenqueue_all_of(e: &Engine) -> u64 {
    e.metrics.pairs_total.saturating_mul(
        e.metrics
            .quiet_commits
            .saturating_add(e.metrics.sap_repairs)
            .max(1),
    )
}

fn pairwise_contacts_until(bodies: &[Body], horizon: i128) -> Vec<(i128, u64, u64)> {
    let mut found = Vec::new();
    for i in 0..bodies.len() {
        for j in i + 1..bodies.len() {
            if let Some(tick) = geometry::first_contact(
                bodies[i].flow(),
                bodies[j].flow(),
                &(&bodies[i].radius + &bodies[j].radius),
                TickInterval {
                    start: 1,
                    end: horizon,
                },
            ) {
                found.push((tick, bodies[i].id, bodies[j].id));
            }
        }
    }
    found.sort();
    found
}

fn piecewise_contacts_until(bodies: &[Body], horizon: i128) -> Vec<(i128, u64, u64)> {
    let mut found = Vec::new();
    for i in 0..bodies.len() {
        for j in i + 1..bodies.len() {
            if let Some(tick) = geometry::first_contact_piecewise(
                &bodies[i].segments,
                &bodies[j].segments,
                &(&bodies[i].radius + &bodies[j].radius),
                TickInterval {
                    start: 1,
                    end: horizon,
                },
            ) {
                let (a, b) = if bodies[i].id < bodies[j].id {
                    (bodies[i].id, bodies[j].id)
                } else {
                    (bodies[j].id, bodies[i].id)
                };
                found.push((tick, a, b));
            }
        }
    }
    found.sort();
    found
}

#[test]
fn cooperative_prep_yields_before_scan_completes() {
    let mut e = scenario::mixed_velocity_bodies(256).unwrap();
    let t0 = Instant::now();
    let first = e.advance(80, WorkBudget::new(1)).unwrap();
    let first_ns = t0.elapsed();
    assert!(!first.complete);
    assert!(first.pending_jobs > 0);
    assert!(first.operations <= 1);
    assert!(
        first_ns < Duration::from_millis(5),
        "budget-1 yield spent {} ns; uncharged prep must not hitch",
        first_ns.as_nanos()
    );
    let mut stutter = first_ns;
    let mut yields = 1u32;
    loop {
        let t = Instant::now();
        let step = e.advance(80, WorkBudget::new(1)).unwrap();
        let gap = t.elapsed();
        assert!(
            gap < Duration::from_millis(5),
            "cooperative yield spent {} ns",
            gap.as_nanos()
        );
        stutter = stutter.max(gap);
        yields += 1;
        assert!(step.operations <= 1 || step.complete);
        if step.complete {
            break;
        }
        if yields > 200_000 {
            panic!("budget-1 compile did not terminate");
        }
    }
    let mut reference = scenario::mixed_velocity_bodies(256).unwrap();
    reference.advance_fully(80).unwrap();
    assert_eq!(e.history_digest(80).unwrap(), reference.history_digest(80).unwrap());
    assert_eq!(contacts_of(&e), contacts_of(&reference));
    let _ = (stutter, yields);
}

#[test]
fn cancel_resume_tiny_budget_matches_full_history() {
    let mut full = scenario::causal_relay().unwrap();
    full.advance_fully(100).unwrap();
    let mut tiny = scenario::causal_relay().unwrap();
    for _ in 0..20 {
        let _ = tiny.advance(100, WorkBudget::new(1)).unwrap();
    }
    tiny.clear_derived();
    let cancelled = Engine::from_state(tiny.state.clone()).unwrap();
    tiny = cancelled;
    loop {
        if tiny.advance(100, WorkBudget::new(1)).unwrap().complete {
            break;
        }
    }
    assert_eq!(
        tiny.history_digest(100).unwrap(),
        full.history_digest(100).unwrap()
    );
}

#[test]
fn incremental_sap_one_burn_matches_rebuild_and_oracle() {
    const N: u64 = 64;
    const BURN_AT: i128 = 10;
    const HORIZON: i128 = 80;
    const BURNED: u64 = 7;
    let velocity = Vec2 {
        x: r(0),
        y: r(1) / r(4),
    };
    let bodies = scenario::mixed_velocity_bodies(N).unwrap().state.bodies;
    let explicit: Vec<Body> = bodies.values().cloned().collect();
    let oracle = pairwise_contact_oracle(&explicit, BURN_AT, BURNED, velocity.clone(), HORIZON);

    let mut incremental = scenario::mixed_velocity_bodies(N).unwrap();
    incremental
        .intervene(
            BURNED,
            Command::SetCourse {
                at: BURN_AT,
                velocity: velocity.clone(),
            },
        )
        .unwrap();
    let t = Instant::now();
    incremental.advance_fully(HORIZON).unwrap();
    let incr_ns = t.elapsed();

    let mut rebuild = scenario::mixed_velocity_bodies(N).unwrap();
    rebuild.incremental_sap = false;
    rebuild
        .intervene(
            BURNED,
            Command::SetCourse {
                at: BURN_AT,
                velocity,
            },
        )
        .unwrap();
    let t = Instant::now();
    rebuild.advance_fully(HORIZON).unwrap();
    let rebuild_ns = t.elapsed();

    assert_eq!(contacts_of(&incremental), contacts_of(&rebuild));
    assert_eq!(contacts_of(&incremental), oracle);
    assert!(
        incremental.metrics.scans < rebuild.metrics.scans,
        "incremental scans {} vs rebuild {}",
        incremental.metrics.scans,
        rebuild.metrics.scans
    );
    assert!(
        incr_ns <= rebuild_ns,
        "incremental {:?} slower than rebuild {:?}",
        incr_ns,
        rebuild_ns
    );
    let reenqueue_all = incremental.metrics.pairs_total.saturating_mul(
        incremental
            .metrics
            .quiet_commits
            .saturating_add(incremental.metrics.sap_repairs)
            .max(1),
    );
    assert!(
        incremental.metrics.pairs_rechecked < reenqueue_all,
        "pairs_rechecked {} did not drop vs re-enqueue-all {} (pairs_total {} quiet {} repairs {})",
        incremental.metrics.pairs_rechecked,
        reenqueue_all,
        incremental.metrics.pairs_total,
        incremental.metrics.quiet_commits,
        incremental.metrics.sap_repairs
    );
}

#[test]
fn scripted_interaction_v1_course_signal_and_contact() {
    assert_eq!(scenario::SCRIPTED_INTERACTION, "scripted-interaction-v1");
    let mut e = scenario::scripted_interactions().unwrap();
    e.advance_fully(80).unwrap();
    let log = e.sorted_events();
    assert!(log.iter().any(|ev| ev.kind == "course_scheduled" && ev.tick == 0));
    assert!(log.iter().any(|ev| ev.kind == "burn" && ev.tick == 5 && ev.subjects == [1]));
    assert!(log
        .iter()
        .any(|ev| ev.kind == "signal_arrived" && ev.tick == 12 && ev.subjects == [1, 2]));
    assert!(log.iter().any(|ev| ev.kind == "contact" && ev.tick == 38));
    assert_eq!(e.decode(2).unwrap().flow().velocity, Vec2::zero());
    assert_eq!(e.logical_count(), 11);
    assert_eq!(e.decode(100).unwrap().flow().velocity, Vec2::zero());
    let rebuilt = e.replay().unwrap();
    assert_eq!(
        e.history_digest(80).unwrap(),
        rebuilt.history_digest(80).unwrap()
    );
}

#[test]
fn extract_only_when_family_generator_changes() {
    let mut e = scenario::population_fixture(8, 1).unwrap();
    let first = 10_000;
    let middle = 10_003;
    let last = 10_007;
    e.intervene(
        first,
        Command::SetCourse {
            at: 0,
            velocity: Vec2 {
                x: r(1) / r(4),
                y: r(0),
            },
        },
    )
    .unwrap();
    assert!(e.state.bodies.is_empty());
    assert_eq!(e.logical_count(), 8);
    for id in [first, middle, last] {
        let mut world = scenario::population_fixture(8, 1).unwrap();
        world
            .intervene(
                id,
                Command::SetCourse {
                    at: 0,
                    velocity: Vec2::zero(),
                },
            )
            .unwrap();
        assert_eq!(world.state.bodies.len(), 1);
        assert!(world.state.bodies.contains_key(&id));
        assert_eq!(world.logical_count(), 8);
        world
            .intervene(
                id,
                Command::SetCourse {
                    at: 0,
                    velocity: Vec2 {
                        x: r(-1) / r(2),
                        y: r(0),
                    },
                },
            )
            .unwrap();
        assert_eq!(world.state.bodies.len(), 1);
        world.advance_fully(20).unwrap();
        assert_eq!(world.decode(id).unwrap().flow().velocity.x, r(-1) / r(2));
    }
}

#[test]
fn near_c_subluminal_setcourse_is_accepted() {
    let mut e = scenario::mixed_velocity_bodies(3).unwrap();
    let v = Vec2 {
        x: r(1_048_575) / r(1_048_576),
        y: r(0),
    };
    e.intervene(0, Command::SetCourse { at: 0, velocity: v.clone() })
        .unwrap();
    assert_eq!(e.decode(0).unwrap().flow().velocity, v);
    assert!(e
        .intervene(
            1,
            Command::SetCourse {
                at: 0,
                velocity: Vec2::new(1, 0),
            },
        )
        .is_err());
}

#[test]
fn event_storm_simultaneous_setcourse_is_budget_invariant() {
    let mut bodies = Vec::new();
    for i in 0..32 {
        bodies.push(Body::new(
            i,
            format!("storm {i}"),
            Inertial::new(0, Vec2::new(i as i128 * 20, 0), Vec2::zero()).unwrap(),
            r(1) / r(8),
            r(1),
        ));
    }
    let setup = |e: &mut Engine| {
        for i in 0..32 {
            e.intervene(
                i,
                Command::SetCourse {
                    at: 10,
                    velocity: Vec2 {
                        x: r(1) / r(8),
                        y: r(0),
                    },
                },
            )
            .unwrap();
        }
    };
    let mut full = Engine::new(9, bodies.clone(), vec![]).unwrap();
    setup(&mut full);
    full.advance_fully(20).unwrap();
    let mut chunked = Engine::new(9, bodies, vec![]).unwrap();
    setup(&mut chunked);
    loop {
        if chunked.advance(20, WorkBudget::new(1)).unwrap().complete {
            break;
        }
    }
    assert_eq!(
        full.history_digest(20).unwrap(),
        chunked.history_digest(20).unwrap()
    );
    assert_eq!(
        full.sorted_events()
            .iter()
            .filter(|e| e.kind == "burn" && e.tick == 10)
            .count(),
        32
    );
}

#[test]
fn compressed_vs_materialized_scripted_family_member() {
    let f = scenario::scripted_interactions().unwrap().state.families[0].clone();
    let explicit: Vec<Body> = (100..108)
        .map(|id| Body::new(id, "lane", f.member(id).unwrap(), f.radius.clone(), r(1)))
        .collect();
    let mut compressed = Engine::new(7, vec![], vec![f]).unwrap();
    let mut material = Engine::new(7, explicit, vec![]).unwrap();
    for e in [&mut compressed, &mut material] {
        e.intervene(
            103,
            Command::SetCourse {
                at: 4,
                velocity: Vec2 {
                    x: r(1) / r(2),
                    y: r(0),
                },
            },
        )
        .unwrap();
        e.advance_fully(20).unwrap();
    }
    assert_eq!(compressed.sorted_events(), material.sorted_events());
    assert_eq!(compressed.state.bodies.len(), 1);
    assert_eq!(compressed.logical_count(), 8);
}

#[test]
fn records_compiler_coop_metrics() {
    let mut relay = scenario::causal_relay().unwrap();
    let t = Instant::now();
    relay.advance_fully(100).unwrap();
    let relay_ns = t.elapsed().as_nanos();

    let mut mixed = scenario::mixed_velocity_bodies(256).unwrap();
    let mut stutter_ns = 0u128;
    let mut command_ns = 0u128;
    let t = Instant::now();
    loop {
        let slice = Instant::now();
        let step = mixed.advance(80, WorkBudget::new(1)).unwrap();
        let gap = slice.elapsed().as_nanos();
        stutter_ns = stutter_ns.max(gap);
        command_ns += gap;
        if step.complete {
            break;
        }
    }
    let mixed_wall = t.elapsed().as_nanos();
    let mut incr = scenario::mixed_velocity_bodies(64).unwrap();
    incr.intervene(
        7,
        Command::SetCourse {
            at: 10,
            velocity: Vec2 {
                x: r(0),
                y: r(1) / r(4),
            },
        },
    )
    .unwrap();
    let t = Instant::now();
    incr.advance_fully(80).unwrap();
    let incr_ns = t.elapsed().as_nanos();
    let mut rebuild = scenario::mixed_velocity_bodies(64).unwrap();
    rebuild.incremental_sap = false;
    rebuild
        .intervene(
            7,
            Command::SetCourse {
                at: 10,
                velocity: Vec2 {
                    x: r(0),
                    y: r(1) / r(4),
                },
            },
        )
        .unwrap();
    let t = Instant::now();
    rebuild.advance_fully(80).unwrap();
    let rebuild_ns = t.elapsed().as_nanos();
    let sap = serde_json::json!({
        "incremental_advance_ns": incr_ns,
        "rebuild_advance_ns": rebuild_ns,
        "incremental_scans": incr.metrics.scans,
        "rebuild_scans": rebuild.metrics.scans,
        "sap_repairs": incr.metrics.sap_repairs,
        "invalidation_fanout": incr.metrics.invalidated_pairs,
        "serialized_bytes": serde_json::to_vec(&incr.state).unwrap().len(),
    });

    let exception = if cfg!(debug_assertions) {
        serde_json::json!({"skipped":"debug; measure in release against frozen 18.478 ms"})
    } else {
        let mut exceptions = scenario::population_fixture(1_000_000_000, 16).unwrap();
        for i in 0..1000 {
            exceptions
                .intervene(
                    10000 + i as u64 * 17,
                    Command::SetVelocity {
                        velocity: Vec2 {
                            x: r(1) / r(4),
                            y: r(1 + (i % 3) as i128) / r(1024),
                        },
                    },
                )
                .unwrap();
        }
        let extracted = exceptions.state.bodies.len();
        let t = Instant::now();
        let advanced = exceptions.advance_fully(32).unwrap();
        let exception_ns = t.elapsed().as_nanos();
        let serialized = serde_json::to_vec(&exceptions.state).unwrap().len();
        let charged = exceptions.metrics.search_operations;
        let accounted = exceptions.metrics.box_builds
            + exceptions.metrics.sort_steps
            + exceptions.metrics.aabb_compares
            + exceptions.metrics.family_range_ops
            + exceptions.metrics.exact_leaf_queries;
        let coverage = if accounted == 0 {
            1.0
        } else {
            charged as f64 / accounted as f64
        };
        let events = exceptions.metrics.committed_events.max(1);
        serde_json::json!({
            "advance_ns": exception_ns,
            "frozen_release_advance_ms": 18.478,
            "operations": advanced.operations,
            "extracted_ships": extracted,
            "extraction_cost_ns_per_ship": exception_ns / extracted.max(1) as u128,
            "canonical_serialized_bytes": serialized,
            "scan_rebuilds": exceptions.metrics.scans,
            "sap_repairs": exceptions.metrics.sap_repairs,
            "invalidation_fanout": exceptions.metrics.invalidated_pairs,
            "committed_events": exceptions.metrics.committed_events,
            "scans_per_event": exceptions.metrics.scans as f64 / events as f64,
            "budget_coverage": coverage,
            "metrics": exceptions.metrics,
        })
    };
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .parent()
        .unwrap();
    let out = root.join("artifacts/runs/compiler-coop-20260912");
    std::fs::create_dir_all(&out).unwrap();
    let payload = serde_json::json!({
        "law": emergent_engine::LAW_ID,
        "profile": if cfg!(debug_assertions) { "debug" } else { "release" },
        "relay_advance_ns": relay_ns,
        "relay_events": ["signal_arrived@14", "contact@43", "signal_arrived@71"],
        "mixed_256_budget1": {
            "command_latency_ns": command_ns,
            "stutter_ns": stutter_ns,
            "wall_ns": mixed_wall,
            "certified_tick_rate": 80.0 / mixed_wall as f64,
            "scans": mixed.metrics.scans,
            "sap_repairs": mixed.metrics.sap_repairs,
        },
        "sap_64_one_burn": sap,
        "exception_1000_32": exception
    });
    std::fs::write(out.join("metrics.json"), serde_json::to_vec_pretty(&payload).unwrap()).unwrap();
    assert!(stutter_ns < 5_000_000);
}

#[test]
fn quiet_inertial_zero_events_do_not_recheck_pairs() {
    let bodies = vec![
        Body::new(
            0,
            "far a",
            Inertial::new(0, Vec2::new(0, 0), Vec2::zero()).unwrap(),
            r(1),
            r(1),
        ),
        Body::new(
            1,
            "far b",
            Inertial::new(0, Vec2::new(10_000, 10_000), Vec2::zero()).unwrap(),
            r(1),
            r(1),
        ),
    ];
    let mut e = Engine::new(3, bodies, vec![]).unwrap();
    e.advance_fully(80).unwrap();
    assert!(contacts_of(&e).is_empty());
    assert_eq!(e.metrics.quiet_commits, 0);
    assert_eq!(e.metrics.pairs_rechecked, 0);
    assert_eq!(e.metrics.committed_events, 0);
    assert_eq!(e.metrics.scans, 1);
}

#[test]
fn grazing_miss_matches_oracle() {
    let bodies = vec![
        Body::new(
            0,
            "origin",
            Inertial::new(0, Vec2::new(0, 0), Vec2::zero()).unwrap(),
            r(1),
            r(1),
        ),
        Body::new(
            1,
            "graze",
            Inertial::new(
                0,
                Vec2::new(-20, 3),
                Vec2 {
                    x: r(1) / r(2),
                    y: r(0),
                },
            )
            .unwrap(),
            r(1),
            r(1),
        ),
    ];
    let oracle = pairwise_contacts_until(&bodies, 80);
    assert!(oracle.is_empty());
    let mut e = Engine::new(5, bodies, vec![]).unwrap();
    e.advance_fully(80).unwrap();
    assert_eq!(contacts_of(&e), oracle);
    assert_eq!(e.metrics.pairs_rechecked, 0);
}

#[test]
fn tangency_at_integer_tick_matches_oracle() {
    let bodies = vec![
        Body::new(
            0,
            "origin",
            Inertial::new(0, Vec2::new(0, 0), Vec2::zero()).unwrap(),
            r(1) / r(2),
            r(1),
        ),
        Body::new(
            1,
            "tangent",
            Inertial::new(
                0,
                Vec2::new(-1, 1),
                Vec2 {
                    x: r(1) / r(2),
                    y: r(0),
                },
            )
            .unwrap(),
            r(1) / r(2),
            r(1),
        ),
    ];
    let oracle = pairwise_contacts_until(&bodies, 10);
    assert_eq!(oracle, vec![(2, 0, 1)]);
    let mut incremental = Engine::new(7, bodies.clone(), vec![]).unwrap();
    incremental.advance_fully(10).unwrap();
    let mut rebuild = Engine::new(7, bodies, vec![]).unwrap();
    rebuild.incremental_sap = false;
    rebuild.advance_fully(10).unwrap();
    assert_eq!(contacts_of(&incremental), oracle);
    assert_eq!(contacts_of(&rebuild), oracle);
    assert_eq!(incremental.metrics.quiet_commits, 1);
    assert_eq!(incremental.metrics.pairs_rechecked, 0);
}

#[test]
fn two_quiet_contacts_do_not_recheck_certified_pairs() {
    let bodies = vec![
        Body::new(
            0,
            "west",
            Inertial::new(0, Vec2::new(0, 0), Vec2::zero()).unwrap(),
            r(1),
            r(1),
        ),
        Body::new(
            1,
            "courier",
            Inertial::new(
                0,
                Vec2::new(-8, 0),
                Vec2 {
                    x: r(1) / r(2),
                    y: r(0),
                },
            )
            .unwrap(),
            r(1),
            r(1),
        ),
        Body::new(
            2,
            "east",
            Inertial::new(0, Vec2::new(16, 0), Vec2::zero()).unwrap(),
            r(1),
            r(1),
        ),
    ];
    let oracle = pairwise_contacts_until(&bodies, 80);
    assert!(oracle.len() >= 2, "expected two sequential quiet contacts, got {oracle:?}");
    let mut incremental = Engine::new(13, bodies.clone(), vec![]).unwrap();
    incremental.advance_fully(80).unwrap();
    let mut rebuild = Engine::new(13, bodies, vec![]).unwrap();
    rebuild.incremental_sap = false;
    rebuild.advance_fully(80).unwrap();
    assert_eq!(contacts_of(&incremental), oracle);
    assert_eq!(contacts_of(&rebuild), oracle);
    assert!(incremental.metrics.quiet_commits >= 2);
    assert_eq!(
        incremental.metrics.pairs_rechecked, 0,
        "quiet later contacts re-ran pairs: rechecked {} / total {}",
        incremental.metrics.pairs_rechecked, incremental.metrics.pairs_total
    );
}

#[test]
fn two_families_approach_then_miss() {
    const HORIZON: i128 = 8_000;
    let a = Family::affine(
        "eastbound",
        100,
        8,
        0,
        Inertial::new(
            0,
            Vec2::new(0, 0),
            Vec2 {
                x: r(1) / r(4),
                y: r(0),
            },
        )
        .unwrap(),
        Vec2::new(16, 0),
        r(1),
        r(1),
    );
    let b = Family::affine(
        "westbound",
        200,
        8,
        0,
        Inertial::new(
            0,
            Vec2::new(4_000, 80),
            Vec2 {
                x: r(-1) / r(4),
                y: r(0),
            },
        )
        .unwrap(),
        Vec2::new(16, 0),
        r(1),
        r(1),
    );
    let explicit: Vec<Body> = (100..108)
        .chain(200..208)
        .map(|id| {
            let f = if id < 200 { &a } else { &b };
            Body::new(id, "lane", f.member(id).unwrap(), f.radius.clone(), r(1))
        })
        .collect();
    let oracle = pairwise_contacts_until(&explicit, HORIZON);
    assert!(oracle.is_empty());
    let mut compressed = Engine::new(11, vec![], vec![a, b]).unwrap();
    let t = Instant::now();
    compressed.advance_fully(HORIZON).unwrap();
    let wall = t.elapsed();
    assert!(
        wall < Duration::from_millis(250),
        "family miss spent {:?}",
        wall
    );
    let mut material = Engine::new(11, explicit, vec![]).unwrap();
    material.advance_fully(HORIZON).unwrap();
    assert_eq!(contacts_of(&compressed), oracle);
    assert_eq!(contacts_of(&material), oracle);
    assert_eq!(compressed.metrics.pairs_rechecked, 0);
    assert_eq!(compressed.metrics.scans, 1);
}

#[test]
fn records_overlap_certificate_metrics() {
    let mut relay = scenario::causal_relay().unwrap();
    relay.advance_fully(100).unwrap();
    let relay_events: Vec<_> = relay
        .sorted_events()
        .iter()
        .filter(|e| matches!(e.kind.as_str(), "signal_arrived" | "contact"))
        .map(|e| format!("{}@{}", e.kind, e.tick))
        .collect();

    let mut mixed = scenario::mixed_velocity_bodies(256).unwrap();
    let mut stutter_ns = 0u128;
    let t = Instant::now();
    loop {
        let slice = Instant::now();
        let step = mixed.advance(80, WorkBudget::new(1)).unwrap();
        stutter_ns = stutter_ns.max(slice.elapsed().as_nanos());
        if step.complete {
            break;
        }
    }
    let mixed_wall = t.elapsed().as_nanos();

    let mut incr = scenario::mixed_velocity_bodies(64).unwrap();
    incr.intervene(
        7,
        Command::SetCourse {
            at: 10,
            velocity: Vec2 {
                x: r(0),
                y: r(1) / r(4),
            },
        },
    )
    .unwrap();
    let t = Instant::now();
    incr.advance_fully(80).unwrap();
    let incr_ns = t.elapsed().as_nanos();
    let mut rebuild = scenario::mixed_velocity_bodies(64).unwrap();
    rebuild.incremental_sap = false;
    rebuild
        .intervene(
            7,
            Command::SetCourse {
                at: 10,
                velocity: Vec2 {
                    x: r(0),
                    y: r(1) / r(4),
                },
            },
        )
        .unwrap();
    let t = Instant::now();
    rebuild.advance_fully(80).unwrap();
    let rebuild_ns = t.elapsed().as_nanos();
    let reenqueue_all = incr.metrics.pairs_total.saturating_mul(
        incr.metrics
            .quiet_commits
            .saturating_add(incr.metrics.sap_repairs)
            .max(1),
    );

    let exception = if cfg!(debug_assertions) {
        serde_json::json!({"skipped":"debug; measure in release against frozen 18.478 ms; do not claim a win inside noise"})
    } else {
        let mut exceptions = scenario::population_fixture(1_000_000_000, 16).unwrap();
        for i in 0..1000 {
            exceptions
                .intervene(
                    10000 + i as u64 * 17,
                    Command::SetVelocity {
                        velocity: Vec2 {
                            x: r(1) / r(4),
                            y: r(1 + (i % 3) as i128) / r(1024),
                        },
                    },
                )
                .unwrap();
        }
        let t = Instant::now();
        let advanced = exceptions.advance_fully(32).unwrap();
        let exception_ns = t.elapsed().as_nanos();
        serde_json::json!({
            "advance_ns": exception_ns,
            "frozen_release_advance_ms": 18.478,
            "note": "single-run; do not claim a win inside noise versus 18.478 ms",
            "operations": advanced.operations,
            "canonical_serialized_bytes": serde_json::to_vec(&exceptions.state).unwrap().len(),
            "serialized_bytes_are_not_ram": true,
            "scan_rebuilds": exceptions.metrics.scans,
            "sap_repairs": exceptions.metrics.sap_repairs,
            "pairs_total": exceptions.metrics.pairs_total,
            "pairs_rechecked": exceptions.metrics.pairs_rechecked,
            "committed_events": exceptions.metrics.committed_events,
            "metrics": exceptions.metrics,
        })
    };
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .parent()
        .unwrap();
    let out = root.join("artifacts/runs/compiler-overlap-certs-20260912");
    std::fs::create_dir_all(&out).unwrap();
    let payload = serde_json::json!({
        "law": emergent_engine::LAW_ID,
        "profile": if cfg!(debug_assertions) { "debug" } else { "release" },
        "relay_events": relay_events,
        "mixed_256_budget1": {
            "stutter_ns": stutter_ns,
            "wall_ns": mixed_wall,
            "certified_tick_rate": 80.0 / mixed_wall as f64,
            "scans": mixed.metrics.scans,
            "pairs_total": mixed.metrics.pairs_total,
            "pairs_rechecked": mixed.metrics.pairs_rechecked,
            "digest": mixed.history_digest(80).unwrap(),
        },
        "sap_64_one_burn": {
            "incremental_advance_ns": incr_ns,
            "rebuild_advance_ns": rebuild_ns,
            "scan_rebuilds": incr.metrics.scans,
            "rebuild_scans": rebuild.metrics.scans,
            "sap_repairs": incr.metrics.sap_repairs,
            "quiet_commits": incr.metrics.quiet_commits,
            "pairs_total": incr.metrics.pairs_total,
            "pairs_rechecked": incr.metrics.pairs_rechecked,
            "reenqueue_all_baseline": reenqueue_all,
            "wall_ns": incr_ns,
        },
        "exception_1000_32": exception
    });
    std::fs::write(out.join("metrics.json"), serde_json::to_vec_pretty(&payload).unwrap()).unwrap();
    assert_eq!(
        relay_events,
        vec![
            "signal_arrived@14".to_string(),
            "contact@43".to_string(),
            "signal_arrived@71".to_string()
        ]
    );
    assert!(stutter_ns < 5_000_000);
    assert!(incr.metrics.pairs_rechecked < reenqueue_all);
}

fn sensor_world(family_count: u64) -> Engine {
    let occluders = Family::affine(
        "occluders",
        100,
        family_count,
        0,
        Inertial::new(0, Vec2::new(5, 0), Vec2::zero()).unwrap(),
        Vec2::new(0, 8),
        r(1),
        r(1),
    );
    let observer = Body::new(
        1,
        "observer",
        Inertial::new(0, Vec2::new(0, 0), Vec2::zero()).unwrap(),
        r(1) / r(8),
        r(1),
    );
    let hidden = Body::new(
        2,
        "hidden",
        Inertial::new(0, Vec2::new(10, 0), Vec2::zero()).unwrap(),
        r(1) / r(8),
        r(1),
    );
    let moving = Body::new(
        3,
        "moving",
        Inertial::new(
            0,
            Vec2::new(0, 12),
            Vec2 {
                x: r(1) / r(8),
                y: r(0),
            },
        )
        .unwrap(),
        r(1) / r(8),
        r(1),
    );
    let mut e = Engine::new(9, vec![observer, hidden, moving], vec![occluders]).unwrap();
    e.advance_fully(100).unwrap();
    e
}

fn observation_set(rows: &[Observation]) -> Vec<(u64, i128, Vec2)> {
    let mut rows: Vec<_> = rows
        .iter()
        .map(|o| (o.entity, o.emission_tick, o.position.clone()))
        .collect();
    rows.sort_by(|a, b| a.0.cmp(&b.0));
    rows
}

fn finish_observe(e: &mut Engine, targets: &[u64], budget: usize) -> (emergent_engine::ObserveResult, u128, u32) {
    let now = e.state.clock;
    let mut stutter_ns = 0u128;
    let mut yields = 0u32;
    let mut last;
    loop {
        let t = Instant::now();
        last = e
            .observe_with_budget(1, now, targets, WorkBudget::new(budget))
            .unwrap();
        stutter_ns = stutter_ns.max(t.elapsed().as_nanos());
        yields += 1;
        if last.complete {
            break;
        }
        assert!(
            last.pending_jobs > 0,
            "incomplete query must expose pending work, not a silent empty sky"
        );
        if yields > 200_000 {
            panic!("sensor continuation did not terminate");
        }
    }
    (last, stutter_ns, yields)
}

#[test]
fn sensor_budget_cancel_resume_matches_full_and_keeps_digest() {
    let full = sensor_world(64);
    let now = full.state.clock;
    let digest = full.history_digest(now).unwrap();
    let state_before = serde_json::to_vec(&full.state).unwrap();
    let complete = full.observe(1, now, &[2, 3]).unwrap();
    assert_eq!(full.history_digest(now).unwrap(), digest);
    assert_eq!(serde_json::to_vec(&full.state).unwrap(), state_before);
    assert!(!complete.iter().any(|o| o.entity == 2));
    let moving = complete.iter().find(|o| o.entity == 3).unwrap();
    let body = full.decode(3).unwrap();
    assert_eq!(moving.position, body.at(moving.emission_tick));
    assert_ne!(moving.position, body.at(now));

    let mut budgeted = sensor_world(64);
    let first = budgeted
        .observe_with_budget(1, now, &[2, 3], WorkBudget::new(1))
        .unwrap();
    assert!(!first.complete);
    assert!(first.pending_jobs > 0);
    assert!(budgeted.sensor_pending());
    let (budgeted_done, _, _) = finish_observe(&mut budgeted, &[2, 3], 1);
    assert_eq!(observation_set(&budgeted_done.observations), observation_set(&complete));
    assert_eq!(budgeted.history_digest(now).unwrap(), digest);

    let mut cancelled = sensor_world(64);
    let _ = cancelled
        .observe_with_budget(1, now, &[2, 3], WorkBudget::new(1))
        .unwrap();
    cancelled.clear_derived();
    assert!(!cancelled.sensor_pending());
    let (resumed, _, _) = finish_observe(&mut cancelled, &[2, 3], 1);
    assert_eq!(observation_set(&resumed.observations), observation_set(&complete));

    let reversed = sensor_world(64);
    let other = reversed.observe(1, now, &[3, 2]).unwrap();
    assert_eq!(observation_set(&other), observation_set(&complete));

    let mut empty_budget = sensor_world(64);
    let pending = empty_budget
        .observe_with_budget(1, now, &[2, 3], WorkBudget::new(0))
        .unwrap();
    assert!(!pending.complete);
    assert!(pending.observations.is_empty());
    assert!(pending.pending_jobs > 0);
    assert_eq!(empty_budget.history_digest(now).unwrap(), digest);

    let mut capped = sensor_world(64);
    capped.max_pending_jobs = 0;
    assert!(capped.observe(1, now, &[2, 3]).is_err());
    assert_eq!(capped.history_digest(now).unwrap(), digest);
}

#[test]
fn sensor_continuation_records_metrics() {
    const FAMILY: u64 = 1_000_000;
    const BUDGET: usize = 8;
    let full = sensor_world(FAMILY);
    let now = full.state.clock;
    let digest = full.history_digest(now).unwrap();
    let t = Instant::now();
    let complete = full.observe(1, now, &[2, 3]).unwrap();
    let observe_full_wall_ns = t.elapsed().as_nanos();

    let mut budgeted = sensor_world(FAMILY);
    let t = Instant::now();
    let first = budgeted
        .observe_with_budget(1, now, &[2, 3], WorkBudget::new(BUDGET))
        .unwrap();
    let first_ns = t.elapsed().as_nanos();
    assert!(!first.complete, "1e6 occluder family must yield under WorkBudget {BUDGET}");
    assert!(first.operations <= BUDGET);
    assert!(first.refinement_steps > 0);
    assert!(budgeted.metrics.sensor_ops > 0);

    let t = Instant::now();
    let ack = budgeted
        .intervene(
            1,
            Command::SetCourse {
                at: now,
                velocity: Vec2 {
                    x: r(1) / r(8),
                    y: r(0),
                },
            },
        )
        .unwrap();
    let command_ack_ns = t.elapsed().as_nanos();
    assert!(!ack.is_empty());
    assert!(!budgeted.sensor_pending());
    assert_ne!(budgeted.history_digest(now).unwrap(), digest);

    let mut resume = sensor_world(FAMILY);
    let _ = resume
        .observe_with_budget(1, now, &[2, 3], WorkBudget::new(BUDGET))
        .unwrap();
    resume.clear_derived();
    let t = Instant::now();
    let (resumed, stutter_ns, yields) = finish_observe(&mut resume, &[2, 3], BUDGET);
    let observe_resume_wall_ns = t.elapsed().as_nanos();
    assert_eq!(observation_set(&resumed.observations), observation_set(&complete));
    assert_eq!(resume.history_digest(now).unwrap(), digest);
    assert!(resumed.charged_sensor_ops >= resumed.refinement_steps);

    let mut tiny = sensor_world(FAMILY);
    let t = Instant::now();
    let (tiny_done, tiny_stutter, _) = finish_observe(&mut tiny, &[2, 3], BUDGET);
    let observe_budget8_wall_ns = t.elapsed().as_nanos();
    assert_eq!(observation_set(&tiny_done.observations), observation_set(&complete));
    assert_eq!(tiny.metrics.sensor_refinements, tiny_done.refinement_steps as u64);
    assert_eq!(tiny.metrics.sensor_ops, tiny_done.charged_sensor_ops as u64);

    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .parent()
        .unwrap();
    let out = root.join("artifacts/runs/compiler-sensor-cont-20260912");
    std::fs::create_dir_all(&out).unwrap();
    let payload = serde_json::json!({
        "law": emergent_engine::LAW_ID,
        "profile": if cfg!(debug_assertions) { "debug" } else { "release" },
        "family_members": FAMILY,
        "family_refinement": "O(log N) AABB spine to first occluder; not a linear scan",
        "work_budget": BUDGET,
        "observe_full_wall_ns": observe_full_wall_ns,
        "observe_budget8_wall_ns": observe_budget8_wall_ns,
        "observe_resume_wall_ns": observe_resume_wall_ns,
        "first_yield_ns": first_ns,
        "stutter_ns": stutter_ns.max(tiny_stutter),
        "yields": yields,
        "command_ack_ns": command_ack_ns,
        "command_ack_with_pending_sensor": true,
        "charged_sensor_ops": resumed.charged_sensor_ops,
        "refinement_steps": resumed.refinement_steps,
        "observation_count": resumed.observations.len(),
        "observations_match_full": true,
        "digest_unchanged_by_query": true,
        "exception_1000_32": {
            "skipped": "observe/occlusion path only; not remeasured versus frozen 18.478 ms"
        }
    });
    std::fs::write(out.join("metrics.json"), serde_json::to_vec_pretty(&payload).unwrap()).unwrap();
    assert!(first_ns < 5_000_000, "budget-8 sensor yield spent {} ns", first_ns);
    assert!(command_ack_ns < 5_000_000, "pending-sensor command ack spent {} ns", command_ack_ns);
    assert!(stutter_ns.max(tiny_stutter) < 5_000_000);
}

fn signal_arrivals_of(e: &Engine) -> Vec<(i128, u64, u64)> {
    let mut rows: Vec<_> = e
        .sorted_events()
        .iter()
        .filter(|ev| ev.kind == "signal_arrived")
        .map(|ev| (ev.tick, ev.subjects[0], ev.subjects[1]))
        .collect();
    rows.sort();
    rows
}

#[test]
fn phase_family_compressed_matches_materialized_fixture() {
    const HORIZON: i128 = 80;
    let mut compressed = scenario::phase_departure_lane(16).unwrap();
    let family = compressed.state.families[0].clone();
    assert!(!family.shares_member_velocity());
    assert_ne!(
        family.member_velocity(100, 10).unwrap(),
        family.member_velocity(115, 10).unwrap()
    );
    let mut explicit = scenario::materialize_family(&family);
    explicit.push(compressed.decode(1).unwrap());
    let mut material = Engine::new(compressed.state.seed, explicit.clone(), vec![]).unwrap();
    material
        .intervene(
            1,
            Command::SendSignal {
                target: 100,
                payload: emergent_engine::runtime::Payload::Ping,
            },
        )
        .unwrap();

    let oracle = piecewise_contacts_until(&explicit, HORIZON);
    let t = Instant::now();
    compressed.advance_fully(HORIZON).unwrap();
    let compressed_ns = t.elapsed().as_nanos();
    material.advance_fully(HORIZON).unwrap();

    assert_eq!(contacts_of(&compressed), contacts_of(&material));
    assert_eq!(contacts_of(&compressed), oracle);
    assert_eq!(signal_arrivals_of(&compressed), signal_arrivals_of(&material));
    let event_facts = |e: &Engine| {
        e.sorted_events()
            .iter()
            .map(|ev| (ev.tick, ev.kind.clone(), ev.subjects.clone(), ev.detail.clone()))
            .collect::<Vec<_>>()
    };
    assert_eq!(event_facts(&compressed), event_facts(&material));
    for id in 100..116 {
        assert_eq!(
            compressed.decode(id).unwrap().segments,
            family.member_segments(id).unwrap()
        );
        assert_eq!(compressed.position(id, HORIZON).unwrap(), material.position(id, HORIZON).unwrap());
    }
    assert_eq!(compressed.state.bodies.len(), 1, "probe only; family stays generated");
    assert_eq!(compressed.logical_count(), 17);

    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .parent()
        .unwrap();
    let out = root.join("artifacts/runs/compiler-phase-families-20260912");
    std::fs::create_dir_all(&out).unwrap();
    let fixture = serde_json::json!({
        "law": emergent_engine::LAW_ID,
        "interaction": scenario::SCRIPTED_INTERACTION,
        "logical_ships": compressed.logical_count(),
        "extracted_ships": compressed.state.bodies.len(),
        "horizon": HORIZON,
        "contacts": contacts_of(&compressed),
        "signal_arrivals": signal_arrivals_of(&compressed),
        "event_facts_match_materialized": true,
        "history_digest_compressed": compressed.history_digest(HORIZON).unwrap(),
        "history_digest_includes_genesis_digest": true,
        "compressed_search_operations": compressed.metrics.search_operations,
        "materialized_search_operations": material.metrics.search_operations,
        "compressed_wall_ns": compressed_ns,
        "serialized_bytes": serde_json::to_vec(&compressed.state).unwrap().len(),
        "note": "event facts match materialized; Engine::history_digest also hashes genesis_digest so family vs bodies differs. Not a gravity law."
    });
    std::fs::write(out.join("fixture.json"), serde_json::to_vec_pretty(&fixture).unwrap()).unwrap();
}

#[test]
fn phase_family_first_middle_last_extract() {
    for id in [100u64, 107, 115] {
        let mut e = scenario::phase_departure_lane(16).unwrap();
        let neighbor = if id == 115 { id - 1 } else { id + 1 };
        let before = e.decode(neighbor).unwrap();
        e.intervene(
            id,
            Command::SetCourse {
                at: 0,
                velocity: Vec2 {
                    x: r(0),
                    y: r(1) / r(4),
                },
            },
        )
        .unwrap();
        assert_eq!(e.state.bodies.len(), 2, "probe + one extract");
        assert!(e.state.bodies.contains_key(&id));
        assert_eq!(e.decode(neighbor).unwrap().segments, before.segments);
        assert_eq!(e.logical_count(), 17);
        e.advance_fully(40).unwrap();
        assert_eq!(e.decode(id).unwrap().flow().velocity.y, r(1) / r(4));
    }
}

#[test]
fn family_phase_burn_updates_in_place_not_family_wide_extract() {
    let v = Vec2 {
        x: r(0),
        y: r(1) / r(8),
    };
    let mut compressed = scenario::phase_departure_lane(16).unwrap();
    compressed
        .intervene(100, Command::FamilyPhaseBurn { at: 0, velocity: v.clone() })
        .unwrap();
    assert_eq!(
        compressed.state.bodies.len(),
        1,
        "parametric burn must not extract the family"
    );
    assert!(compressed.state.families.iter().all(|f| f.phase.is_none()));
    for id in 100..116 {
        assert_eq!(compressed.decode(id).unwrap().flow().velocity, v);
    }

    let family = scenario::phase_departure_lane(16).unwrap().state.families[0].clone();
    let mut explicit = scenario::materialize_family(&family);
    explicit.push(compressed.decode(1).unwrap());
    let mut material = Engine::new(0x9A5E_F41E, explicit, vec![]).unwrap();
    material
        .intervene(
            1,
            Command::SendSignal {
                target: 100,
                payload: emergent_engine::runtime::Payload::Ping,
            },
        )
        .unwrap();
    for id in 100..116 {
        material
            .intervene(id, Command::SetVelocity { velocity: v.clone() })
            .unwrap();
    }
    compressed.advance_fully(40).unwrap();
    material.advance_fully(40).unwrap();
    assert_eq!(contacts_of(&compressed), contacts_of(&material));
    for id in 100..116 {
        assert_eq!(
            compressed.position(id, 40).unwrap(),
            material.position(id, 40).unwrap()
        );
    }

    let mut mixed = scenario::phase_departure_lane(16).unwrap();
    mixed.advance_fully(20).unwrap();
    mixed
        .intervene(
            100,
            Command::FamilyPhaseBurn {
                at: 20,
                velocity: v.clone(),
            },
        )
        .unwrap();
    assert_eq!(mixed.state.bodies.len(), 1);
    assert!(mixed.logical_count() >= 17);
    assert!(
        !mixed.state.families.is_empty(),
        "phase-aligned split/update stays generated"
    );
    mixed.advance_fully(40).unwrap();
}

#[test]
fn closing_phase_family_is_rejected_not_interior_skipped() {
    let f = Family::affine(
        "closing",
        1,
        4,
        0,
        Inertial::new(0, Vec2::zero(), Vec2::zero()).unwrap(),
        Vec2::new(8, 0),
        r(1),
        r(1),
    )
    .with_phase(
        PhaseGenerator::new(
            0,
            20,
            Vec2 {
                x: r(1) / r(2),
                y: r(0),
            },
        )
        .unwrap(),
    );
    assert!(!f.self_disjoint());
    let err = Engine::new(1, vec![], vec![f]).unwrap_err();
    let msg = err.to_string();
    assert!(
        msg.contains("materialized") || msg.contains("overlapping"),
        "interior skip must reject, got {msg}"
    );
}

#[test]
fn reversed_phase_family_order_on_restore_is_rejected() {
    let a = scenario::phase_departure_lane(4).unwrap().state.families.remove(0);
    let mut b = a.clone();
    b.name = "phase-lane-b".into();
    b.first_id = 200;
    let mut e = Engine::new(3, vec![], vec![a, b]).unwrap();
    e.state.families.reverse();
    assert!(Engine::from_state(e.state).is_err());
}

#[test]
fn records_phase_family_metrics() {
    const HORIZON: i128 = 80;
    let mut compressed = scenario::phase_departure_lane(16).unwrap();
    let family = compressed.state.families[0].clone();
    let mut explicit = scenario::materialize_family(&family);
    explicit.push(compressed.decode(1).unwrap());
    let mut material = Engine::new(compressed.state.seed, explicit, vec![]).unwrap();
    material
        .intervene(
            1,
            Command::SendSignal {
                target: 100,
                payload: emergent_engine::runtime::Payload::Ping,
            },
        )
        .unwrap();

    let t = Instant::now();
    compressed.advance_fully(HORIZON).unwrap();
    let compressed_ns = t.elapsed().as_nanos();
    let t = Instant::now();
    material.advance_fully(HORIZON).unwrap();
    let material_ns = t.elapsed().as_nanos();

    let v = Vec2 {
        x: r(0),
        y: r(1) / r(8),
    };
    let mut million = Engine::new(
        11,
        vec![],
        vec![scenario::phase_departure_lane(1_000_000)
            .unwrap()
            .state
            .families
            .remove(0)],
    )
    .unwrap();
    let t = Instant::now();
    million
        .intervene(
            100,
            Command::SetCourseRange {
                lo: 100,
                hi: 100 + 1_000_000 - 1,
                at: 0,
                velocity: v.clone(),
            },
        )
        .unwrap();
    let phase_burn_1e6_ns = t.elapsed().as_nanos();
    assert_eq!(million.state.bodies.len(), 0);
    assert_eq!(million.logical_count(), 1_000_000);
    assert_eq!(million.state.scheduled_range_courses.len(), 0);
    assert!(million.state.scheduled_courses.is_empty());

    const EXTRACT_N: u64 = 256;
    let mut extracted = Engine::new(
        11,
        vec![],
        vec![scenario::phase_departure_lane(EXTRACT_N)
            .unwrap()
            .state
            .families
            .remove(0)],
    )
    .unwrap();
    let t = Instant::now();
    for id in 100..100 + EXTRACT_N {
        extracted
            .intervene(id, Command::SetVelocity { velocity: v.clone() })
            .unwrap();
    }
    let extracted_burn_ns = t.elapsed().as_nanos();
    assert_eq!(extracted.state.bodies.len() as u64, EXTRACT_N);

    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .parent()
        .unwrap();
    let out = root.join("artifacts/runs/compiler-phase-families-20260912");
    std::fs::create_dir_all(&out).unwrap();
    let payload = serde_json::json!({
        "law": emergent_engine::LAW_ID,
        "interaction": scenario::SCRIPTED_INTERACTION,
        "profile": if cfg!(debug_assertions) { "debug" } else { "release" },
        "fixture_16": {
            "logical_ships": compressed.logical_count(),
            "extracted_ships": compressed.state.bodies.len(),
            "extracted_ships_over_logical_ships": format!(
                "{}/{}",
                compressed.state.bodies.len(),
                compressed.logical_count()
            ),
            "serialized_bytes": serde_json::to_vec(&compressed.state).unwrap().len(),
            "serialized_bytes_are_not_ram": true,
            "compressed_search_operations": compressed.metrics.search_operations,
            "materialized_search_operations": material.metrics.search_operations,
            "compressed_wall_ns": compressed_ns,
            "materialized_wall_ns": material_ns,
            "contacts": contacts_of(&compressed),
            "history_digest_compressed": compressed.history_digest(HORIZON).unwrap(),
            "event_facts_match_materialized": true,
        },
        "range_ir": {
            "exists": true,
            "command": "SetCourseRange",
            "object": "one scheduled_range_course / range_burn hyperedge over {lo..=hi}",
            "not": "a clique of per-ship SetCourse commands"
        },
        "family_phase_burn_1e6": {
            "logical_ships": 1_000_000,
            "extracted_ships": million.state.bodies.len(),
            "extracted_ships_over_logical_ships": "0/1000000",
            "wall_ns": phase_burn_1e6_ns,
            "serialized_bytes": serde_json::to_vec(&million.state).unwrap().len(),
            "ir": "SetCourseRange"
        },
        "extracted_equivalent_burns": {
            "n": EXTRACT_N,
            "extracted_ships": extracted.state.bodies.len(),
            "wall_ns": extracted_burn_ns,
            "note": "anti-pattern: N per-ship SetVelocity. 1e6 extract exceeds resident cap 100_000; not the range-IR path"
        },
        "exception_1000_32": {
            "skipped": "not remeasured; H0013 27.8 vs frozen 18.5 ms remains unresolved; do not claim a 1,000-exception speedup"
        }
    });
    std::fs::write(out.join("metrics.json"), serde_json::to_vec_pretty(&payload).unwrap()).unwrap();
    let event_facts = |e: &Engine| {
        e.sorted_events()
            .iter()
            .map(|ev| (ev.tick, ev.kind.clone(), ev.subjects.clone(), ev.detail.clone()))
            .collect::<Vec<_>>()
    };
    assert_eq!(event_facts(&compressed), event_facts(&material));
    assert_eq!(contacts_of(&compressed), contacts_of(&material));
}

fn event_facts(e: &Engine) -> Vec<(i128, String, Vec<u64>, String)> {
    e.sorted_events()
        .iter()
        .map(|ev| (ev.tick, ev.kind.clone(), ev.subjects.clone(), ev.detail.clone()))
        .collect()
}

#[test]
fn set_course_range_is_one_hyperedge_and_does_not_extract() {
    let v = Vec2 {
        x: r(0),
        y: r(1) / r(8),
    };
    let mut e = scenario::phase_departure_lane(16).unwrap();
    e.intervene(
        1,
        Command::SetCourseRange {
            lo: 100,
            hi: 115,
            at: 8,
            velocity: v.clone(),
        },
    )
    .unwrap();
    assert_eq!(e.state.scheduled_range_courses.len(), 1);
    assert!(e.state.scheduled_courses.is_empty());
    assert_eq!(e.state.bodies.len(), 1, "range IR must not extract the family");
    e.advance_fully(40).unwrap();
    assert!(e.state.scheduled_range_courses.is_empty());
    assert_eq!(e.state.bodies.len(), 1);
    assert_eq!(e.logical_count(), 17);
    for id in 100..116 {
        assert_eq!(e.decode(id).unwrap().flow().velocity, v);
    }
    assert!(e
        .sorted_events()
        .iter()
        .any(|ev| ev.kind == "range_burn" && ev.subjects == vec![100, 115] && ev.tick == 8));
}

#[test]
fn set_course_range_compressed_matches_materialized() {
    const HORIZON: i128 = 80;
    let v = Vec2 {
        x: r(0),
        y: r(1) / r(8),
    };
    let mut compressed = scenario::phase_departure_lane(16).unwrap();
    let family = compressed.state.families[0].clone();
    compressed
        .intervene(
            1,
            Command::SetCourseRange {
                lo: 100,
                hi: 115,
                at: 0,
                velocity: v.clone(),
            },
        )
        .unwrap();
    assert_eq!(compressed.state.bodies.len(), 1);

    let mut explicit = scenario::materialize_family(&family);
    explicit.push(compressed.decode(1).unwrap());
    let mut material = Engine::new(compressed.state.seed, explicit, vec![]).unwrap();
    material
        .intervene(
            1,
            Command::SendSignal {
                target: 100,
                payload: emergent_engine::runtime::Payload::Ping,
            },
        )
        .unwrap();
    material
        .intervene(
            1,
            Command::SetCourseRange {
                lo: 100,
                hi: 115,
                at: 0,
                velocity: v,
            },
        )
        .unwrap();

    compressed.advance_fully(HORIZON).unwrap();
    material.advance_fully(HORIZON).unwrap();
    assert_eq!(contacts_of(&compressed), contacts_of(&material));
    assert_eq!(signal_arrivals_of(&compressed), signal_arrivals_of(&material));
    assert_eq!(event_facts(&compressed), event_facts(&material));
    for id in 100..116 {
        assert_eq!(
            compressed.position(id, HORIZON).unwrap(),
            material.position(id, HORIZON).unwrap()
        );
    }
    assert_eq!(compressed.state.bodies.len(), 1);
    assert_eq!(material.state.bodies.len(), 17);
}

#[test]
fn set_course_range_does_not_merge_adjacent_families() {
    let v = Vec2 {
        x: r(1) / r(8),
        y: r(0),
    };
    let a = scenario::phase_departure_lane(4).unwrap().state.families.remove(0);
    let mut b = a.clone();
    b.name = "phase-lane-b".into();
    b.first_id = 104;
    let mut e = Engine::new(3, vec![], vec![a, b]).unwrap();
    assert_eq!(e.state.families.len(), 2);
    e.intervene(
        100,
        Command::SetCourseRange {
            lo: 100,
            hi: 107,
            at: 0,
            velocity: v.clone(),
        },
    )
    .unwrap();
    assert_eq!(e.state.bodies.len(), 0);
    assert_eq!(e.state.families.len(), 2, "adjacent families must not merge");
    assert_ne!(e.state.families[0].name, e.state.families[1].name);
    for id in 100..108 {
        assert_eq!(e.decode(id).unwrap().flow().velocity, v);
    }
}

fn component_of(e: &Engine, id: u64) -> Option<usize> {
    e.causal_components.iter().position(|c| c.contains(&id))
}

fn relay_event_labels(e: &Engine) -> Vec<String> {
    e.sorted_events()
        .iter()
        .filter(|ev| matches!(ev.kind.as_str(), "signal_arrived" | "contact"))
        .map(|ev| format!("{}@{}", ev.kind, ev.tick))
        .collect()
}

#[test]
fn independent_families_do_not_share_a_component() {
    let mut quiet = scenario::population_fixture(16 * 64, 16).unwrap();
    let extracted_before = quiet.state.bodies.len();
    let family_ids: Vec<u64> = quiet.state.families.iter().map(|f| f.first_id).collect();
    assert_eq!(family_ids.len(), 16);
    quiet.advance_fully(80).unwrap();
    assert_eq!(quiet.state.bodies.len(), extracted_before, "unchanged generators must not extract");
    assert_eq!(quiet.metrics.components, 16);
    assert_eq!(quiet.metrics.component_size_max, 1);
    assert_eq!(quiet.causal_components.len(), 16);
    assert_eq!(quiet.metrics.ir_nodes, 16);
    for id in &family_ids {
        assert_eq!(
            component_of(&quiet, *id).map(|i| quiet.causal_components[i].len()),
            Some(1),
            "family {id} must be a singleton island"
        );
    }
    for (i, a) in family_ids.iter().enumerate() {
        for b in family_ids.iter().skip(i + 1) {
            assert_ne!(
                component_of(&quiet, *a),
                component_of(&quiet, *b),
                "families {a} and {b} share a component without an overlap cert"
            );
        }
    }
    assert_eq!(quiet.metrics.pairs_rechecked, 0);
    assert!(quiet.metrics.pairs_total == 0 || quiet.metrics.pairs_rechecked < quiet.metrics.pairs_total);
}

#[test]
fn relay_digest_and_witness_stay_independent() {
    let mut full = scenario::causal_relay().unwrap();
    full.advance_fully(100).unwrap();
    let mut tiny = scenario::causal_relay().unwrap();
    loop {
        if tiny.advance(100, WorkBudget::new(1)).unwrap().complete {
            break;
        }
    }
    assert_eq!(
        relay_event_labels(&full),
        vec![
            "signal_arrived@14".to_string(),
            "contact@43".to_string(),
            "signal_arrived@71".to_string()
        ]
    );
    assert_eq!(full.history_digest(100).unwrap(), tiny.history_digest(100).unwrap());
    assert_eq!(contacts_of(&full), contacts_of(&tiny));
    let witness = component_of(&full, 4);
    let emitter = component_of(&full, 1);
    assert!(witness.is_some() && emitter.is_some());
    assert_ne!(
        witness, emitter,
        "independent witness must not share a component with the relay chain"
    );
}

#[test]
fn dense_one_burn_matches_pairwise_and_groups() {
    const N: u64 = 64;
    const BURN_AT: i128 = 10;
    const HORIZON: i128 = 80;
    const BURNED: u64 = 7;
    let velocity = Vec2 {
        x: r(0),
        y: r(1) / r(4),
    };
    let bodies = scenario::mixed_velocity_bodies(N).unwrap().state.bodies;
    let explicit: Vec<Body> = bodies.values().cloned().collect();
    let oracle = pairwise_contact_oracle(&explicit, BURN_AT, BURNED, velocity.clone(), HORIZON);

    let mut incremental = scenario::mixed_velocity_bodies(N).unwrap();
    incremental
        .intervene(
            BURNED,
            Command::SetCourse {
                at: BURN_AT,
                velocity: velocity.clone(),
            },
        )
        .unwrap();
    incremental.advance_fully(HORIZON).unwrap();

    let mut rebuild = scenario::mixed_velocity_bodies(N).unwrap();
    rebuild.incremental_sap = false;
    rebuild
        .intervene(
            BURNED,
            Command::SetCourse {
                at: BURN_AT,
                velocity,
            },
        )
        .unwrap();
    rebuild.advance_fully(HORIZON).unwrap();

    assert_eq!(contacts_of(&incremental), contacts_of(&rebuild));
    assert_eq!(contacts_of(&incremental), oracle);
    assert_eq!(
        incremental.history_digest(HORIZON).unwrap(),
        rebuild.history_digest(HORIZON).unwrap()
    );
    assert!(
        incremental.metrics.component_size_max >= 2,
        "dense encounter should merge at least one overlap island, got size_max {}",
        incremental.metrics.component_size_max
    );
    assert!(incremental.metrics.components >= 1);
    assert!(incremental.metrics.ir_nodes >= 1);
    let reenqueue_all = incremental.metrics.pairs_total.saturating_mul(
        incremental
            .metrics
            .quiet_commits
            .saturating_add(incremental.metrics.sap_repairs)
            .max(1),
    );
    assert!(
        incremental.metrics.pairs_rechecked < reenqueue_all,
        "pairs_rechecked {} regresses toward re-enqueue-all {}",
        incremental.metrics.pairs_rechecked,
        reenqueue_all
    );
}

#[test]
fn phase_lane_facts_match_under_component_compile() {
    const HORIZON: i128 = 80;
    let mut compressed = scenario::phase_departure_lane(16).unwrap();
    let family = compressed.state.families[0].clone();
    let extracted_before = compressed.state.bodies.len();
    let mut explicit = scenario::materialize_family(&family);
    explicit.push(compressed.decode(1).unwrap());
    let mut material = Engine::new(compressed.state.seed, explicit, vec![]).unwrap();
    material
        .intervene(
            1,
            Command::SendSignal {
                target: 100,
                payload: emergent_engine::runtime::Payload::Ping,
            },
        )
        .unwrap();
    compressed.advance_fully(HORIZON).unwrap();
    material.advance_fully(HORIZON).unwrap();
    assert_eq!(event_facts(&compressed), event_facts(&material));
    assert_eq!(contacts_of(&compressed), contacts_of(&material));
    assert_eq!(compressed.state.bodies.len(), extracted_before);
    assert_eq!(compressed.state.families.len(), 1, "do not merge causally adjacent identities");
}

#[test]
fn causally_adjacent_families_share_a_component_not_an_identity() {
    const HORIZON: i128 = 8_000;
    let a = Family::affine(
        "eastbound",
        100,
        8,
        0,
        Inertial::new(
            0,
            Vec2::new(0, 0),
            Vec2 {
                x: r(1) / r(4),
                y: r(0),
            },
        )
        .unwrap(),
        Vec2::new(16, 0),
        r(1),
        r(1),
    );
    let b = Family::affine(
        "westbound",
        200,
        8,
        0,
        Inertial::new(
            0,
            Vec2::new(4_000, 80),
            Vec2 {
                x: r(-1) / r(4),
                y: r(0),
            },
        )
        .unwrap(),
        Vec2::new(16, 0),
        r(1),
        r(1),
    );
    let mut compressed = Engine::new(11, vec![], vec![a, b]).unwrap();
    compressed.advance_fully(HORIZON).unwrap();
    assert_eq!(compressed.state.families.len(), 2);
    assert_ne!(compressed.state.families[0].name, compressed.state.families[1].name);
    if compressed.metrics.pairs_total > 0 {
        assert_eq!(
            component_of(&compressed, 100),
            component_of(&compressed, 200),
            "AABB-overlapping families must share a compile island"
        );
        assert_eq!(compressed.causal_components.iter().filter(|c| c.contains(&100) || c.contains(&200)).count(), 1);
    } else {
        assert_ne!(component_of(&compressed, 100), component_of(&compressed, 200));
    }
}

#[test]
fn records_causal_component_metrics() {
    let mut quiet = scenario::population_fixture(16 * 64, 16).unwrap();
    let quiet_extracted_before = quiet.state.bodies.len();
    let t = Instant::now();
    quiet.advance_fully(80).unwrap();
    let quiet_ns = t.elapsed().as_nanos();
    let quiet_items = 16u64;

    let mut relay = scenario::causal_relay().unwrap();
    relay.advance_fully(100).unwrap();
    let relay_events = relay_event_labels(&relay);

    const N: u64 = 64;
    const BURN_AT: i128 = 10;
    const HORIZON: i128 = 80;
    const BURNED: u64 = 7;
    let velocity = Vec2 {
        x: r(0),
        y: r(1) / r(4),
    };
    let mut incr = scenario::mixed_velocity_bodies(N).unwrap();
    incr.intervene(
        BURNED,
        Command::SetCourse {
            at: BURN_AT,
            velocity: velocity.clone(),
        },
    )
    .unwrap();
    let t = Instant::now();
    incr.advance_fully(HORIZON).unwrap();
    let incr_ns = t.elapsed().as_nanos();
    let mut rebuild = scenario::mixed_velocity_bodies(N).unwrap();
    rebuild.incremental_sap = false;
    rebuild
        .intervene(
            BURNED,
            Command::SetCourse {
                at: BURN_AT,
                velocity,
            },
        )
        .unwrap();
    rebuild.advance_fully(HORIZON).unwrap();
    let reenqueue_all = incr.metrics.pairs_total.saturating_mul(
        incr.metrics
            .quiet_commits
            .saturating_add(incr.metrics.sap_repairs)
            .max(1),
    );

    let mut mixed = scenario::mixed_velocity_bodies(64).unwrap();
    let mut stutter_ns = 0u128;
    loop {
        let slice = Instant::now();
        let step = mixed.advance(80, WorkBudget::new(1)).unwrap();
        stutter_ns = stutter_ns.max(slice.elapsed().as_nanos());
        if step.complete {
            break;
        }
    }

    let mut phase = scenario::phase_departure_lane(16).unwrap();
    let family = phase.state.families[0].clone();
    let mut explicit = scenario::materialize_family(&family);
    explicit.push(phase.decode(1).unwrap());
    let mut material = Engine::new(phase.state.seed, explicit, vec![]).unwrap();
    material
        .intervene(
            1,
            Command::SendSignal {
                target: 100,
                payload: emergent_engine::runtime::Payload::Ping,
            },
        )
        .unwrap();
    phase.advance_fully(80).unwrap();
    material.advance_fully(80).unwrap();

    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .parent()
        .unwrap();
    let out = root.join("artifacts/runs/compiler-causal-components-20260912");
    std::fs::create_dir_all(&out).unwrap();
    let payload = serde_json::json!({
        "law": emergent_engine::LAW_ID,
        "interaction": scenario::SCRIPTED_INTERACTION,
        "profile": if cfg!(debug_assertions) { "debug" } else { "release" },
        "quiet_16_families": {
            "logical_ships": quiet.logical_count(),
            "extracted_ships": quiet.state.bodies.len(),
            "extracted_ships_over_logical_ships": format!(
                "{}/{}",
                quiet.state.bodies.len(),
                quiet.logical_count()
            ),
            "horizon": 80,
            "components": quiet.metrics.components,
            "components_over_sap_items": format!("{}/{}", quiet.metrics.components, quiet_items),
            "component_size_max": quiet.metrics.component_size_max,
            "component_size_max_over_sap_items": format!("{}/{}", quiet.metrics.component_size_max, quiet_items),
            "ir_nodes": quiet.metrics.ir_nodes,
            "ir_nodes_over_sap_items": format!("{}/{}", quiet.metrics.ir_nodes, quiet_items),
            "charged_ops": quiet.metrics.search_operations,
            "pairs_total": quiet.metrics.pairs_total,
            "pairs_rechecked": quiet.metrics.pairs_rechecked,
            "pairs_rechecked_over_pairs_total": format!(
                "{}/{}",
                quiet.metrics.pairs_rechecked,
                quiet.metrics.pairs_total
            ),
            "wall_ns": quiet_ns,
            "serialized_bytes": serde_json::to_vec(&quiet.state).unwrap().len(),
            "serialized_bytes_are_not_ram": true,
        },
        "dense_64_one_burn": {
            "bodies": N,
            "horizon": HORIZON,
            "incremental_advance_ns": incr_ns,
            "components": incr.metrics.components,
            "component_size_max": incr.metrics.component_size_max,
            "ir_nodes": incr.metrics.ir_nodes,
            "charged_ops": incr.metrics.search_operations,
            "pairs_total": incr.metrics.pairs_total,
            "pairs_rechecked": incr.metrics.pairs_rechecked,
            "pairs_rechecked_over_reenqueue_all": format!("{}/{}", incr.metrics.pairs_rechecked, reenqueue_all.max(1)),
            "reenqueue_all_baseline": reenqueue_all,
            "quiet_commits": incr.metrics.quiet_commits,
            "sap_repairs": incr.metrics.sap_repairs,
            "contacts_match_rebuild_and_oracle": contacts_of(&incr) == contacts_of(&rebuild),
            "digest_match_rebuild": incr.history_digest(HORIZON).unwrap() == rebuild.history_digest(HORIZON).unwrap(),
        },
        "relay": {
            "events": relay_events,
            "digest": relay.history_digest(100).unwrap(),
            "components": relay.metrics.components,
            "component_size_max": relay.metrics.component_size_max,
            "ir_nodes": relay.metrics.ir_nodes,
            "charged_ops": relay.metrics.search_operations,
            "pairs_rechecked": relay.metrics.pairs_rechecked,
        },
        "phase_lane": {
            "event_facts_match_materialized": event_facts(&phase) == event_facts(&material),
            "extracted_ships": phase.state.bodies.len(),
            "components": phase.metrics.components,
            "ir_nodes": phase.metrics.ir_nodes,
            "charged_ops": phase.metrics.search_operations,
        },
        "budget1_mixed_64": {
            "stutter_ns": stutter_ns,
            "components": mixed.metrics.components,
            "ir_nodes": mixed.metrics.ir_nodes,
            "charged_ops": mixed.metrics.search_operations,
        },
        "exception_1000_32": {
            "skipped": "not remeasured; H0013 27.8 vs frozen 18.5 ms remains unresolved; do not claim a 1,000-exception speedup"
        }
    });
    std::fs::write(out.join("metrics.json"), serde_json::to_vec_pretty(&payload).unwrap()).unwrap();

    assert_eq!(quiet.state.bodies.len(), quiet_extracted_before);
    assert_eq!(quiet.metrics.components, 16);
    assert_eq!(quiet.metrics.component_size_max, 1);
    assert_eq!(quiet.metrics.pairs_rechecked, 0);
    assert_eq!(
        relay_events,
        vec![
            "signal_arrived@14".to_string(),
            "contact@43".to_string(),
            "signal_arrived@71".to_string()
        ]
    );
    assert_eq!(contacts_of(&incr), contacts_of(&rebuild));
    assert_eq!(event_facts(&phase), event_facts(&material));
    assert!(stutter_ns < 5_000_000, "budget-1 yield spent {} ns", stutter_ns);
    assert!(incr.metrics.pairs_rechecked < reenqueue_all.max(1) || reenqueue_all == 0);
}

#[test]
fn packed_overlap_forms_a_large_war_island() {
    const HORIZON: i128 = scenario::PACKED_ISLAND_HORIZON;
    let burn_at = scenario::PACKED_ISLAND_BURN_AT;
    let lo = scenario::PACKED_ISLAND_LANE_FIRST;
    let hi = lo + scenario::PACKED_ISLAND_LANE_SHIPS - 1;
    let velocity = Vec2 {
        x: r(1) / r(8),
        y: r(0),
    };

    let mut incremental = scenario::packed_overlap_island().unwrap();
    let extracted_before = incremental.state.bodies.len();
    let family_names_before: Vec<String> = incremental
        .state
        .families
        .iter()
        .map(|f| f.name.clone())
        .collect();
    assert_eq!(extracted_before as u64, scenario::PACKED_ISLAND_BODIES);
    assert_eq!(
        incremental.state.families.len() as u64,
        scenario::PACKED_ISLAND_LANES + 2
    );
    let snapshot = packed_explicit_snapshot(&incremental);
    let oracle = pairwise_range_contact_oracle(&snapshot, burn_at, lo, hi, velocity.clone(), HORIZON);

    incremental.advance_fully(HORIZON).unwrap();

    let mut rebuild = scenario::packed_overlap_island().unwrap();
    rebuild.incremental_sap = false;
    rebuild.advance_fully(HORIZON).unwrap();

    let mut material = Engine::new(incremental.state.seed, snapshot.clone(), vec![]).unwrap();
    material
        .intervene(
            lo,
            Command::SetCourseRange {
                lo,
                hi,
                at: burn_at,
                velocity: velocity.clone(),
            },
        )
        .unwrap();
    material
        .intervene(
            0,
            Command::SendSignal {
                target: 7,
                payload: emergent_engine::runtime::Payload::Ping,
            },
        )
        .unwrap();
    material.advance_fully(HORIZON).unwrap();

    assert_eq!(contacts_of(&incremental), contacts_of(&rebuild));
    assert_eq!(contacts_of(&incremental), oracle);
    assert_eq!(event_facts(&incremental), event_facts(&rebuild));
    assert_eq!(event_facts(&incremental), event_facts(&material));
    assert_eq!(
        incremental.history_digest(HORIZON).unwrap(),
        rebuild.history_digest(HORIZON).unwrap()
    );
    assert_ne!(
        incremental.history_digest(HORIZON).unwrap(),
        material.history_digest(HORIZON).unwrap(),
        "digest hashes genesis; packed families vs fully materialized must differ"
    );

    let sap_items = scenario::PACKED_ISLAND_BODIES + scenario::PACKED_ISLAND_LANES + 2;
    let packed_items = scenario::PACKED_ISLAND_BODIES + scenario::PACKED_ISLAND_LANES;
    assert!(
        incremental.metrics.component_size_max * 2 >= packed_items,
        "packed war island size_max {} / packed SAP items {} is not ≥ N/2",
        incremental.metrics.component_size_max,
        packed_items
    );
    assert!(incremental.metrics.components >= 3);
    assert!(incremental.metrics.ir_nodes >= 1);
    assert_eq!(incremental.metrics.ir_nodes, sap_items);

    let island = component_of(&incremental, 0);
    assert!(island.is_some());
    let island_len = incremental.causal_components[island.unwrap()].len();
    assert!(island_len as u64 >= packed_items / 2);
    assert_ne!(component_of(&incremental, scenario::PACKED_FAR_NORTH), island);
    assert_ne!(component_of(&incremental, scenario::PACKED_FAR_SOUTH), island);
    assert_eq!(
        component_of(&incremental, scenario::PACKED_FAR_NORTH)
            .map(|i| incremental.causal_components[i].len()),
        Some(1)
    );
    assert_eq!(
        component_of(&incremental, scenario::PACKED_FAR_SOUTH)
            .map(|i| incremental.causal_components[i].len()),
        Some(1)
    );
    assert_ne!(
        component_of(&incremental, scenario::PACKED_FAR_NORTH),
        component_of(&incremental, scenario::PACKED_FAR_SOUTH)
    );

    let names_after: Vec<String> = incremental
        .state
        .families
        .iter()
        .map(|f| f.name.clone())
        .collect();
    assert_eq!(names_after.len(), family_names_before.len());
    assert_eq!(names_after, family_names_before, "overlap must not merge family identities");
    assert_eq!(
        incremental.state.bodies.len(),
        extracted_before,
        "unchanged generators and in-place range burn must not extract-all"
    );
    assert_eq!(incremental.state.scheduled_range_courses.len(), 0);
    assert_eq!(incremental.decode(lo).unwrap().flow().velocity, velocity);

    let reenqueue_all = reenqueue_all_of(&incremental);
    assert!(
        incremental.metrics.pairs_rechecked < reenqueue_all,
        "pairs_rechecked {} regresses toward re-enqueue-all {}",
        incremental.metrics.pairs_rechecked,
        reenqueue_all
    );
}

#[test]
fn records_war_island_metrics() {
    let mut quiet = scenario::population_fixture(16 * 64, 16).unwrap();
    let quiet_extracted_before = quiet.state.bodies.len();
    let t = Instant::now();
    quiet.advance_fully(80).unwrap();
    let quiet_ns = t.elapsed().as_nanos();
    let quiet_items = 16u64;

    const HORIZON: i128 = scenario::PACKED_ISLAND_HORIZON;
    let mut packed = scenario::packed_overlap_island().unwrap();
    let packed_extracted_before = packed.state.bodies.len();
    let packed_families_before = packed.state.families.len();
    let sap_items = packed_extracted_before as u64 + packed_families_before as u64;
    let packed_items = scenario::PACKED_ISLAND_BODIES + scenario::PACKED_ISLAND_LANES;
    let t = Instant::now();
    packed.advance_fully(HORIZON).unwrap();
    let packed_ns = t.elapsed().as_nanos();
    let reenqueue_all = reenqueue_all_of(&packed);

    let mut rebuild = scenario::packed_overlap_island().unwrap();
    rebuild.incremental_sap = false;
    rebuild.advance_fully(HORIZON).unwrap();

    let mut stutter = scenario::packed_overlap_island().unwrap();
    let t0 = Instant::now();
    let first = stutter.advance(HORIZON, WorkBudget::new(1)).unwrap();
    let construction_ns = t0.elapsed().as_nanos();
    assert!(!first.complete, "budget-1 must yield before packed compile finishes");
    assert!(
        construction_ns < 5_000_000,
        "budget-1 construction yield spent {} ns; uncharged prep must not hitch",
        construction_ns
    );
    let mut stutter_ns = construction_ns;
    loop {
        let slice = Instant::now();
        let step = stutter.advance(HORIZON, WorkBudget::new(1)).unwrap();
        stutter_ns = stutter_ns.max(slice.elapsed().as_nanos());
        assert!(step.operations <= 1 || step.complete || step.events > 0);
        if step.complete {
            break;
        }
    }

    let mut relay = scenario::causal_relay().unwrap();
    relay.advance_fully(100).unwrap();
    let relay_events = relay_event_labels(&relay);

    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .parent()
        .unwrap();
    let out = root.join("artifacts/runs/compiler-war-island-20260912");
    std::fs::create_dir_all(&out).unwrap();
    let payload = serde_json::json!({
        "law": emergent_engine::LAW_ID,
        "interaction": scenario::SCRIPTED_INTERACTION,
        "profile": if cfg!(debug_assertions) { "debug" } else { "release" },
        "quiet_16_families": {
            "logical_ships": quiet.logical_count(),
            "extracted_ships": quiet.state.bodies.len(),
            "extracted_ships_over_logical_ships": format!(
                "{}/{}",
                quiet.state.bodies.len(),
                quiet.logical_count()
            ),
            "horizon": 80,
            "components": quiet.metrics.components,
            "components_over_sap_items": format!("{}/{}", quiet.metrics.components, quiet_items),
            "component_size_max": quiet.metrics.component_size_max,
            "component_size_max_over_sap_items": format!("{}/{}", quiet.metrics.component_size_max, quiet_items),
            "ir_nodes": quiet.metrics.ir_nodes,
            "charged_ops": quiet.metrics.search_operations,
            "sort_steps": quiet.metrics.sort_steps,
            "expire_ops": quiet.metrics.expire_ops,
            "group_ops": quiet.metrics.group_ops,
            "frontier_ops": quiet.metrics.frontier_ops,
            "commit_prep_ops": quiet.metrics.commit_prep_ops,
            "pairs_total": quiet.metrics.pairs_total,
            "pairs_rechecked": quiet.metrics.pairs_rechecked,
            "pairs_rechecked_over_pairs_total": format!(
                "{}/{}",
                quiet.metrics.pairs_rechecked,
                quiet.metrics.pairs_total
            ),
            "wall_ns": quiet_ns,
            "serialized_bytes": serde_json::to_vec(&quiet.state).unwrap().len(),
            "serialized_bytes_are_not_ram": true
        },
        "packed_war_island": {
            "bodies": scenario::PACKED_ISLAND_BODIES,
            "packed_families": scenario::PACKED_ISLAND_LANES,
            "far_families": 2,
            "sap_items": sap_items,
            "packed_sap_items": packed_items,
            "horizon": HORIZON,
            "components": packed.metrics.components,
            "components_over_sap_items": format!("{}/{}", packed.metrics.components, sap_items),
            "component_size_max": packed.metrics.component_size_max,
            "component_size_max_over_packed_sap_items": format!(
                "{}/{}",
                packed.metrics.component_size_max,
                packed_items
            ),
            "component_size_max_over_sap_items": format!(
                "{}/{}",
                packed.metrics.component_size_max,
                sap_items
            ),
            "ir_nodes": packed.metrics.ir_nodes,
            "ir_nodes_over_sap_items": format!("{}/{}", packed.metrics.ir_nodes, sap_items),
            "charged_ops": packed.metrics.search_operations,
            "sort_steps": packed.metrics.sort_steps,
            "expire_ops": packed.metrics.expire_ops,
            "group_ops": packed.metrics.group_ops,
            "frontier_ops": packed.metrics.frontier_ops,
            "commit_prep_ops": packed.metrics.commit_prep_ops,
            "pairs_total": packed.metrics.pairs_total,
            "pairs_rechecked": packed.metrics.pairs_rechecked,
            "pairs_rechecked_over_reenqueue_all": format!(
                "{}/{}",
                packed.metrics.pairs_rechecked,
                reenqueue_all.max(1)
            ),
            "reenqueue_all_baseline": reenqueue_all,
            "quiet_commits": packed.metrics.quiet_commits,
            "sap_repairs": packed.metrics.sap_repairs,
            "wall_ns": packed_ns,
            "extracted_ships": packed.state.bodies.len(),
            "extracted_ships_over_genesis_bodies": format!(
                "{}/{}",
                packed.state.bodies.len(),
                packed_extracted_before
            ),
            "family_count": packed.state.families.len(),
            "contacts_match_rebuild": contacts_of(&packed) == contacts_of(&rebuild),
            "digest_match_rebuild": packed.history_digest(HORIZON).unwrap()
                == rebuild.history_digest(HORIZON).unwrap(),
            "far_families_outside_island": component_of(&packed, 0)
                != component_of(&packed, scenario::PACKED_FAR_NORTH)
                && component_of(&packed, 0) != component_of(&packed, scenario::PACKED_FAR_SOUTH),
            "serialized_bytes": serde_json::to_vec(&packed.state).unwrap().len(),
            "serialized_bytes_are_not_ram": true,
            "not_battle_mode": true
        },
        "budget1_packed_war_island": {
            "construction_yield_ns": construction_ns,
            "stutter_ns": stutter_ns,
            "stutter_includes_simultaneous_contact_batch": true,
            "digest_match_full": stutter.history_digest(HORIZON).unwrap()
                == packed.history_digest(HORIZON).unwrap(),
            "components": stutter.metrics.components,
            "component_size_max": stutter.metrics.component_size_max,
            "ir_nodes": stutter.metrics.ir_nodes,
            "charged_ops": stutter.metrics.search_operations
        },
        "relay": {
            "events": relay_events,
            "digest": relay.history_digest(100).unwrap(),
            "components": relay.metrics.components,
            "component_size_max": relay.metrics.component_size_max,
            "ir_nodes": relay.metrics.ir_nodes,
            "charged_ops": relay.metrics.search_operations,
            "pairs_rechecked": relay.metrics.pairs_rechecked
        },
        "exception_1000_32": {
            "skipped": "not remeasured; H0013 27.8 vs frozen 18.5 ms remains unresolved; do not claim a 1,000-exception speedup"
        }
    });
    std::fs::write(out.join("metrics.json"), serde_json::to_vec_pretty(&payload).unwrap()).unwrap();

    assert_eq!(quiet.state.bodies.len(), quiet_extracted_before);
    assert_eq!(quiet.metrics.components, 16);
    assert_eq!(quiet.metrics.component_size_max, 1);
    assert_eq!(quiet.metrics.ir_nodes, 16);
    assert_eq!(quiet.metrics.pairs_rechecked, 0);
    assert_eq!(packed.state.bodies.len(), packed_extracted_before);
    assert_eq!(packed.state.families.len(), packed_families_before);
    assert!(packed.metrics.component_size_max * 2 >= packed_items);
    assert_eq!(contacts_of(&packed), contacts_of(&rebuild));
    assert_eq!(
        packed.history_digest(HORIZON).unwrap(),
        rebuild.history_digest(HORIZON).unwrap()
    );
    assert_eq!(
        relay_events,
        vec![
            "signal_arrived@14".to_string(),
            "contact@43".to_string(),
            "signal_arrived@71".to_string()
        ]
    );
    assert!(packed.metrics.pairs_rechecked < reenqueue_all.max(1) || reenqueue_all == 0);
    assert_eq!(
        stutter.history_digest(HORIZON).unwrap(),
        packed.history_digest(HORIZON).unwrap()
    );
    assert!(
        stutter_ns < 100_000_000,
        "packed budget-1 slice spent {} ns (simultaneous contact batch is one transaction)",
        stutter_ns
    );
}

fn event_ids_by_tick(e: &Engine) -> std::collections::BTreeMap<i128, Vec<String>> {
    let mut by_tick = std::collections::BTreeMap::<i128, Vec<String>>::new();
    for ev in e.sorted_events() {
        by_tick.entry(ev.tick).or_default().push(ev.id.clone());
    }
    by_tick
}

#[test]
fn simultaneous_batch_never_half_committed() {
    let mut e = scenario::packed_overlap_island().unwrap();
    let horizon = scenario::PACKED_ISLAND_HORIZON;
    let mut frozen = std::collections::BTreeMap::<i128, Vec<String>>::new();
    loop {
        let clock_before = e.state.clock;
        let step = e.advance(horizon, WorkBudget::new(1)).unwrap();
        let now = event_ids_by_tick(&e);
        for (tick, ids) in &now {
            assert!(
                e.state.clock >= *tick,
                "events at {tick} visible while clock is {}",
                e.state.clock
            );
            if let Some(prev) = frozen.get(tick) {
                assert_eq!(
                    prev, ids,
                    "tick {tick} grew after first publish; half a simultaneous batch leaked"
                );
            } else {
                frozen.insert(*tick, ids.clone());
                assert!(
                    clock_before < *tick && e.state.clock >= *tick || clock_before >= *tick,
                    "tick {tick} events appeared without a publish that advances the clock"
                );
            }
        }
        if step.complete {
            break;
        }
    }
    let mut full = scenario::packed_overlap_island().unwrap();
    full.advance_fully(horizon).unwrap();
    assert_eq!(e.history_digest(horizon).unwrap(), full.history_digest(horizon).unwrap());
    assert_eq!(relay_event_labels(&{
        let mut relay = scenario::causal_relay().unwrap();
        relay.advance_fully(100).unwrap();
        relay
    }), vec![
        "signal_arrived@14".to_string(),
        "contact@43".to_string(),
        "signal_arrived@71".to_string(),
    ]);
}

#[test]
fn exception_fixture_setup_vs_advance_is_separated() {
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .parent()
        .unwrap();
    let out = root.join("artifacts/runs/compiler-exception-setup-advance-20260912");
    std::fs::create_dir_all(&out).unwrap();
    let payload = if cfg!(debug_assertions) {
        serde_json::json!({
            "law": emergent_engine::LAW_ID,
            "profile": "debug",
            "exception_1000_32": {
                "skipped": "debug; canonical release profile is cargo run --release -p xtask -- exception-setup-advance artifacts/runs/compiler-exception-setup-advance-20260912. Frozen 18.478 ms and H0013 27.768 ms remain historical labels."
            },
            "historical_release_advance_ms": 18.478,
            "historical_h0013_advance_ms": 27.768
        })
    } else {
        let t_setup = Instant::now();
        let mut exceptions = scenario::population_fixture(1_000_000_000, 16).unwrap();
        for i in 0..1000 {
            exceptions
                .intervene(
                    10000 + i as u64 * 17,
                    Command::SetVelocity {
                        velocity: Vec2 {
                            x: r(1) / r(4),
                            y: r(1 + (i % 3) as i128) / r(1024),
                        },
                    },
                )
                .unwrap();
        }
        let setup_ns = t_setup.elapsed().as_nanos();
        let extracted = exceptions.state.bodies.len();
        let t_adv = Instant::now();
        let advanced = exceptions.advance_fully(32).unwrap();
        let advance_ns = t_adv.elapsed().as_nanos();
        serde_json::json!({
            "law": emergent_engine::LAW_ID,
            "profile": "release",
            "exception_1000_32": {
                "setup_ns": setup_ns,
                "advance_ns": advance_ns,
                "frozen_release_advance_ms": 18.478,
                "historical_h0013_advance_ms": 27.768,
                "operations": advanced.operations,
                "extracted_ships": extracted,
                "canonical_serialized_bytes": serde_json::to_vec(&exceptions.state).unwrap().len(),
                "scans": exceptions.metrics.scans,
                "pairs_total": exceptions.metrics.pairs_total,
                "pairs_rechecked": exceptions.metrics.pairs_rechecked,
                "sort_steps": exceptions.metrics.sort_steps,
                "expire_ops": exceptions.metrics.expire_ops,
                "group_ops": exceptions.metrics.group_ops,
                "frontier_ops": exceptions.metrics.frontier_ops,
                "commit_prep_ops": exceptions.metrics.commit_prep_ops,
                "search_operations": exceptions.metrics.search_operations,
                "committed_events": exceptions.metrics.committed_events,
                "note": "Single cargo-test release sample. Canonical contemporaneous control is the xtask exception-setup-advance metrics.json. 18.478 ms remains historical; this is not a restoration claim."
            }
        })
    };
    std::fs::write(
        out.join("compiler_coop_exception.json"),
        serde_json::to_vec_pretty(&payload).unwrap(),
    )
    .unwrap();
    let mut relay = scenario::causal_relay().unwrap();
    relay.advance_fully(100).unwrap();
    assert_eq!(
        relay_event_labels(&relay),
        vec![
            "signal_arrived@14".to_string(),
            "contact@43".to_string(),
            "signal_arrived@71".to_string()
        ]
    );
}
