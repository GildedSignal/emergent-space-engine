use emergent_space::events::{Calendar, Clock, CyclePool, Doll, LogMass, TimeBasis, Tube};
use emergent_space::{
    Error,
    binding::{IntegerState, Trajectory},
    orbit::{OrbitKey, Scalar},
};
use std::collections::BTreeMap;
fn s(n: i64) -> Scalar {
    Scalar::integer(n)
}

#[test]
fn compact_records_use_native_shapes_at_planetary_and_extreme_scale() {
    assert_eq!(size_of::<Tube>(), 16);
    for exponent in [0, 29, 2000, 20000] {
        let mut pool = CyclePool::default();
        let key = OrbitKey::bound(s(20).scale(exponent).unwrap(), 1 << 47).unwrap();
        let id = pool.intern(key).unwrap();
        assert_eq!(pool.intern(key).unwrap(), id);
        let tube = Tube::new(id, 0, 0);
        let clock_exponent = (3 * exponent / 2 - 20) as i16;
        assert!(
            tube.state(&pool.catalogue, 42, clock_exponent)
                .unwrap()
                .radius
                .is_positive()
        );
        assert_eq!(pool.len(), 1);
    }
}
#[test]
fn calendar_matches_an_independent_sorted_map_across_scales() {
    let mut heap = Calendar::new(97);
    let mut reference = BTreeMap::new();
    let mut seed = 17u64;
    for i in 0..20_000 {
        seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1);
        let slot = (seed >> 32) as usize % 97;
        let time =
            (seed & 63 != 0).then(|| s((seed % 101) as i64).scale((i % 4000) - 2000).unwrap());
        heap.set(slot, time).unwrap();
        if let Some(t) = time {
            reference.insert(slot, t);
        } else {
            reference.remove(&slot);
        }
        let first = reference.iter().map(|(&slot, &t)| (t, slot)).min();
        assert_eq!(heap.peek(), first);
        assert_eq!(heap.len(), reference.len());
        if i % 13 == 0 {
            assert_eq!(heap.pop(), first);
            if let Some((_, slot)) = first {
                reference.remove(&slot);
            }
        }
    }
    assert_eq!(heap.set(97, Some(s(1))), Err(Error::Range));
}
#[test]
fn derived_clock_never_undershoots_at_planetary_scale() {
    let mut pool = CyclePool::default();
    let id = pool
        .intern(OrbitKey::bound(s(527_527_527), 1 << 46).unwrap())
        .unwrap();
    let clock = Clock {
        centre: Tube::new(id, 0, 0),
        basis: TimeBasis { exponent: 16 },
        coordinate_epoch: 0,
        proper_epoch: s(0),
    };
    for tick in [1, 10, 1000, 10_000_000, 1_000_000_000] {
        let tau = clock.proper_time(&pool, tick).unwrap();
        let inverse = clock.parent_time(&pool, tau).unwrap().fixed(-16).unwrap() as i64;
        assert!(inverse <= tick);
        assert!(clock.proper_time(&pool, inverse).unwrap() >= tau);
        if inverse > 0 {
            assert!(clock.proper_time(&pool, inverse - 1).unwrap() < tau);
        }
    }
}
#[test]
fn logarithmic_mass_and_soi_do_not_have_an_absolute_radius_cap() {
    for exponent in [-20000, 0, 20000] {
        let parent = Doll::root(LogMass(0));
        let child = Doll::child(LogMass(-10 << 24), 0, Tube::new(0, 0, 0));
        assert_eq!(
            child
                .edge_radius(&parent, s(1600).scale(exponent).unwrap())
                .unwrap(),
            s(100).scale(exponent).unwrap()
        );
    }
    assert_eq!(
        LogMass::factor(100 << 24).unwrap(),
        Scalar::power_of_two(100)
    );
}
#[test]
fn native_handoffs_reconstruct_after_repeated_translations_and_kicks() {
    use emergent_space::{
        events::handoff::{bind, rebind, slow},
        tube::Catalogue,
    };
    let mut catalogue = Catalogue::default();
    let mut exact = IntegerState {
        position: [100_000_000 << 20, 0],
        velocity: [0, 107374],
        length_exponent: -20,
        velocity_exponent: -30,
    };
    let mut event = bind(exact, 0, 10, None, &mut catalogue).unwrap();
    let zero = IntegerState {
        position: [0; 2],
        velocity: [0; 2],
        ..exact
    };
    let other = IntegerState {
        position: [12345, -67890],
        velocity: [1, -2],
        ..exact
    };
    for _ in 0..40 {
        event = rebind(&event, &mut catalogue, zero, other, None).unwrap();
        event = rebind(&event, &mut catalogue, other, zero, None).unwrap();
        assert_eq!(event.reconstruct(&catalogue).unwrap(), exact);
        exact.velocity[0] += 1;
        event = bind(exact, 0, 10, None, &mut catalogue).unwrap();
    }
    let fast = IntegerState {
        velocity: [1 << 28, 1 << 28],
        ..zero
    };
    assert!(!slow(fast).unwrap());
    assert!(bind(fast, 0, 0, None, &mut catalogue).is_err());
}
#[test]
fn queue_and_nested_clocks_use_scaled_root_deadlines() {
    use emergent_space::events::{Event, EventKind, EventQueue, Hierarchy};
    let mut pool = CyclePool::default();
    let key = pool.intern(OrbitKey::bound(s(100), 0).unwrap()).unwrap();
    let mut hierarchy = Hierarchy::new(Doll::root(LogMass(0))).unwrap();
    for parent in 0..2 {
        hierarchy
            .add(
                Doll::child(
                    LogMass(-((parent as i32 + 1) << 24)),
                    parent,
                    Tube::new(key, 0, 0),
                ),
                TimeBasis { exponent: -10 },
                s(0),
                &pool,
            )
            .unwrap();
    }
    let root = hierarchy.root_time(&pool, 2, s(10)).unwrap();
    let mut queue = EventQueue::new(3);
    for slot in (0..3).rev() {
        queue
            .schedule(Event {
                time: root,
                slot,
                kind: EventKind::Edge { destination: 0 },
            })
            .unwrap();
    }
    for slot in 0..3 {
        assert_eq!(queue.pop_through(root).unwrap().unwrap().slot, slot);
    }
    assert!(
        queue
            .pop_through(Scalar::power_of_two(20000))
            .unwrap()
            .is_none()
    );
    assert!(
        queue
            .schedule(Event {
                time: root,
                slot: 0,
                kind: EventKind::Horizon
            })
            .is_err()
    );
}
#[test]
fn tide_selector_and_full_parent_force_have_the_expected_limits() {
    use emergent_space::events::kicks::{Regime, parent_tide, regime, tau0, tidal_ratio};
    let tau = tidal_ratio(s(1), s(1).scale(-10).unwrap(), s(1), s(32)).unwrap();
    assert_eq!(tau, s(1).scale(-4).unwrap());
    assert_eq!(regime(tau, true, false).unwrap(), Regime::Averaged);
    assert_eq!(regime(tau0().unwrap(), true, false).unwrap(), Regime::Dense);
    assert_eq!(regime(tau, false, false).unwrap(), Regime::Arc);
    assert_eq!(regime(tau, true, true).unwrap(), Regime::Dense);
    assert_eq!(
        parent_tide(s(1), [s(32), s(0)], [s(0), s(0)]).unwrap(),
        [s(0), s(0)]
    );
    let force = parent_tide(s(1), [s(32), s(0)], [s(1), s(1)]).unwrap();
    assert!(force[0].is_positive() && force[1] < s(0));
}
#[test]
fn edge_is_the_first_outgoing_population_tick() {
    use emergent_space::events::edge::next_exit;
    let mut pool = CyclePool::default();
    let id = pool
        .intern(OrbitKey::bound(s(100_000_000), 1 << 47).unwrap())
        .unwrap();
    let tube = Tube::new(id, 0, 0);
    let edge = s(100_000_000);
    let at = next_exit(pool.get(id).unwrap(), tube, &pool.catalogue, 0, 10, edge)
        .unwrap()
        .unwrap();
    assert!(tube.state(&pool.catalogue, at, 10).unwrap().radius >= edge);
    assert!(tube.state(&pool.catalogue, at - 1, 10).unwrap().radius < edge);
    assert!(matches!(pool.get(id).unwrap(), Trajectory::Cycle(_)));
}
#[test]
fn signed_sigma_delta_conserves_every_native_increment() {
    use emergent_space::events::handoff::Carry;
    let mut carry = Carry::new(97).unwrap();
    let (mut input, mut output, mut seed) = (0i128, 0i128, 41u64);
    for _ in 0..100_000 {
        seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1);
        let increment = (seed % 10007) as i64 - 5003;
        input += increment as i128;
        output += carry.add(increment).unwrap() as i128;
        assert!(carry.remainder().abs() < 97);
        assert_eq!(input, output * 97 + carry.remainder() as i128);
    }
    let mut negative = Carry::new(97).unwrap();
    assert_eq!(negative.add(-96).unwrap(), 0);
    assert_eq!(negative.add(-1).unwrap(), -1);
}

#[test]
fn binary_test_mass_limit_is_exact_and_clock_map_uses_the_same_energy() {
    use emergent_space::{events::binary::Binary, orbit::Orbit};
    let b = Binary {
        energy: Scalar::integer(-1).scale(-10).unwrap(),
        angular: s(20),
        nu: 0,
    };
    let c = Orbit::compile(b.key().unwrap()).unwrap();
    assert_eq!(b.period(&c).unwrap(), c.period().unwrap());
    let equal = Binary { nu: 1 << 28, ..b };
    assert!(equal.effective_binding().unwrap() > b.effective_binding().unwrap());
    let cycle = Orbit::compile(equal.key().unwrap()).unwrap();
    assert!(equal.period(&cycle).unwrap() < cycle.period().unwrap());
    assert_eq!(equal.period(&c), Err(Error::Topology));
    assert_eq!(
        Binary {
            nu: (1 << 28) + 1,
            ..b
        }
        .key(),
        Err(Error::Range)
    );
    // Much weaker than the former Q48 binding-energy quantum.
    for exponent in [40, 80, 120, 200] {
        let weak = Binary {
            energy: Scalar::integer(-1).scale(-exponent).unwrap(),
            angular: Scalar::integer(2).scale(exponent / 2 - 2).unwrap(),
            nu: 1 << 28,
        };
        let key = weak.key().unwrap();
        assert!(key.periapsis.exponent() > exponent as i16 - 4);
        let c = Orbit::compile(key).unwrap();
        assert!(weak.period(&c).unwrap().is_positive());
    }
}

#[test]
fn dense_order_is_independent_of_observation_and_keeps_the_full_tide() {
    use emergent_space::events::dense::{ONE, Scene, Stepper};
    let scene = Scene {
        mu: ONE / 1000,
        radius: ONE / 10000,
        edge: ONE / 16,
        speed_unit: Scalar::power_of_two(-20),
    };
    let initial = [ONE / 30, 0, 0, ONE / 6];
    let mut a = Stepper::new(scene, initial).unwrap();
    let mut b = a.clone();
    for i in 1..100 {
        a.at(i * ONE / 1000).unwrap();
    }
    let end = a.at(ONE / 10).unwrap();
    assert_eq!(end, b.at(ONE / 10).unwrap());
    assert_eq!(a.time, b.time);
    assert_eq!(a.state, b.state);
    assert_eq!(a.counts.steps, b.counts.steps);
    let unsupported = Scene { radius: 0, ..scene };
    assert!(Stepper::new(unsupported, initial).is_err());
}

#[test]
fn physical_evolution_consumes_the_remainder_before_the_next_binding() {
    use emergent_space::{
        events::handoff::{advance, bind},
        tube::Catalogue,
    };
    let mut catalogue = Catalogue::default();
    let mut oracle = IntegerState {
        position: [100_000_000 << 20, 1000],
        velocity: [107, 107374],
        length_exponent: -20,
        velocity_exponent: -30,
    };
    let mut event = bind(oracle, 0, 10, None, &mut catalogue).unwrap();
    assert!(event.residual.position != [0; 2] || event.residual.velocity != [0; 2]);
    for time in 1..41 {
        // A supplied exact drift/kick is an independent transport oracle. The
        // production force resolver can use the same consuming interface.
        oracle.position[0] += oracle.velocity[0];
        oracle.velocity[0] += 3;
        event = advance(&event, &mut catalogue, time, None, |mut state| {
            state.position[0] += state.velocity[0];
            state.velocity[0] += 3;
            Ok(state)
        })
        .unwrap();
        assert_eq!(event.reconstruct(&catalogue).unwrap(), oracle);
    }
}

#[test]
fn arc_work_uses_the_compiled_path_and_kicks_preserve_position() {
    use emergent_space::{
        events::{
            handoff::bind,
            kicks::{Kick, apply, integrate_arc},
        },
        orbit::Orbit,
        tube::Catalogue,
    };
    let orbit = Orbit::compile(OrbitKey::bound(s(100_000_000), 1 << 47).unwrap()).unwrap();
    let dt = orbit.period().unwrap().scale(-4).unwrap();
    let zero = integrate_arc(
        &Trajectory::Cycle(orbit),
        0,
        false,
        Scalar::ZERO,
        dt,
        8,
        (-20, -50),
        |_, _| Ok([Scalar::ZERO; 2]),
    )
    .unwrap();
    assert_eq!(
        zero,
        Kick {
            energy: Scalar::ZERO,
            angular: Scalar::ZERO
        }
    );
    let mut catalogue = Catalogue::default();
    let exact = IntegerState {
        position: [100_000_000 << 20, 1000],
        velocity: [1000, 107374],
        length_exponent: -20,
        velocity_exponent: -30,
    };
    let event = bind(exact, 0, 10, None, &mut catalogue).unwrap();
    let next = apply(
        &event,
        &mut catalogue,
        Kick {
            energy: Scalar::power_of_two(-40),
            angular: Scalar::ZERO,
        },
        None,
    )
    .unwrap();
    assert_eq!(
        next.reconstruct(&catalogue).unwrap().position,
        exact.position
    );
    assert!(next.reconstruct(&catalogue).unwrap().velocity[0] >= exact.velocity[0]);
}

#[test]
fn c_quarter_refusal_keeps_subquantum_transverse_speed_and_overflow_is_explicit() {
    use emergent_space::events::handoff::{slow, translate};
    let exact = IntegerState {
        position: [0; 2],
        velocity: [1 << 60, 0],
        length_exponent: 10000,
        velocity_exponent: -62,
    };
    assert!(slow(exact).unwrap());
    assert!(
        !slow(IntegerState {
            velocity: [1 << 60, 1],
            ..exact
        })
        .unwrap()
    );
    let zero = IntegerState {
        position: [0; 2],
        velocity: [0; 2],
        ..exact
    };
    assert!(
        translate(
            IntegerState {
                position: [i64::MAX, 0],
                ..zero
            },
            IntegerState {
                position: [1, 0],
                ..zero
            },
            zero
        )
        .is_err()
    );
}

#[test]
fn dense_readout_reduces_phase_before_rotation_and_preserves_length() {
    use emergent_space::events::dense::{ONE, inertial};
    for t in [0, 1, 1000, i64::MAX / ONE] {
        let time = t * ONE;
        let want = (t as f64).sin_cos();
        let out = inertial([ONE, 0, 0, ONE], time).unwrap();
        assert!((out[0] as f64 / ONE as f64 - want.1).abs() < 1e-12);
        assert!((out[1] as f64 / ONE as f64 - want.0).abs() < 1e-12);
        assert_eq!(out[2], -out[1]);
        assert_eq!(out[3], out[0]);
    }
}

#[test]
fn dense_c_quarter_guard_uses_the_exact_dyadic_product() {
    use emergent_space::events::dense::{ONE, Scene, Stepper};
    let scene = Scene {
        mu: ONE / 1000,
        radius: ONE / 10000,
        edge: ONE / 16,
        speed_unit: Scalar::ONE,
    };
    // The parent centre's physical speed itself is outside the low-c contract.
    assert!(Stepper::new(scene, [ONE, 0, 0, 0]).is_err());
    let scene = Scene {
        speed_unit: Scalar::power_of_two(-2),
        ..scene
    };
    assert!(Stepper::new(scene, [ONE, 0, ONE, 0]).is_err()); // diagonal barycentric velocity
    assert!(Stepper::new(scene, [ONE, 0, 0, 0]).is_ok());
    assert!(Stepper::new(scene, [ONE, 0, 0, ONE]).is_err());
    let tiny = Scene {
        radius: 1,
        speed_unit: Scalar::power_of_two(-20),
        ..scene
    };
    let mut body = Stepper::new(tiny, [512, 0, 0, 0]).unwrap();
    assert!(body.at(ONE).is_err()); // an unrepresentable force is refused without a panic
}

#[test]
fn resonance_comes_from_the_compiled_frequencies() {
    use emergent_space::{events::kicks::resonant, orbit::Orbit};
    let inner = Orbit::compile(OrbitKey::bound(s(100), 0).unwrap()).unwrap();
    let outer = Orbit::compile(OrbitKey::bound(s(10000), 0).unwrap()).unwrap();
    assert!(resonant(&inner, &inner).unwrap());
    assert!(!resonant(&inner, &outer).unwrap());
}
