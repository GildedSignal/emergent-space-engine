use emergent_space::events::{Calendar, Clock, CyclePool, Doll, LogMass, TimeBasis, Tube};
use emergent_space::{Cycle, Error, Key, Words};
use std::collections::BTreeMap;

#[test]
fn compact_records_read_the_shared_exact_key_and_refuse_lossy_offsets() {
    assert_eq!(size_of::<Tube>(), 16);
    assert_eq!(align_of::<Tube>(), 4);
    let mut pool = CyclePool::default();
    let key = Key::darwin(20 << 16, 1 << 29).unwrap();
    let id = pool.intern(key).unwrap();
    assert_eq!(pool.intern(key).unwrap(), id);
    let basis = TimeBasis(Words::new(1 << 40));
    let tube = Tube::new(3, 7, id, basis.0.get() + 42, 123, basis).unwrap();
    let period = pool.get(id).unwrap().increments.t.get();
    for n in [0, 1, 1000, 1_000_000] {
        let t = basis.0.get() + 42 + n * period;
        assert_eq!(
            tube.state(&pool, basis, Words::new(t)).unwrap(),
            pool.get(id).unwrap().state(Words::new(123 + n * period)).unwrap()
        );
    }
    assert_eq!(pool.len(), 1);
    assert_eq!(Tube::new(0, 0, id, basis.0.get() - 1, 0, basis), Err(Error::Range));
    assert_eq!(Tube::new(0, 0, id, basis.0.get() + (1 << 32), 0, basis), Err(Error::Range));
    assert_eq!(Tube::new(0, 0, id, basis.0.get(), 1 << 32, basis), Err(Error::Range));
}

#[test]
fn heap_matches_an_independent_sorted_calendar_under_replacements_and_ties() {
    let mut heap = Calendar::new(97);
    let mut reference = BTreeMap::new();
    let mut seed = 17u64;
    for i in 0..20_000 {
        seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1);
        let slot = (seed >> 32) as usize % 97;
        let time = (seed & 63 != 0).then_some(seed % 101);
        heap.set(slot, time).unwrap();
        if let Some(t) = time {
            reference.insert(slot, t);
        } else {
            reference.remove(&slot);
        }
        let first = reference.iter().map(|(&s, &t)| (t, s)).min();
        assert_eq!(heap.peek(), first);
        assert_eq!(heap.len(), reference.len());
        if i % 13 == 0 {
            assert_eq!(heap.pop(), first);
            if let Some((_, s)) = first {
                reference.remove(&s);
            }
        }
    }
    while let Some((t, s)) = heap.pop() {
        assert_eq!(Some((t, s)), reference.iter().map(|(&s, &t)| (t, s)).min());
        reference.remove(&s);
    }
    assert!(reference.is_empty() && heap.is_empty());
    assert_eq!(heap.pop(), None);
    assert_eq!(heap.set(97, Some(1)), Err(Error::Range));
    assert_eq!(heap.set(0, Some(u64::MAX)), Err(Error::Range));
}

#[test]
fn child_clock_uses_cycles_and_crossing_brackets_and_never_undershoots() {
    for (p, e) in [(8, 1 << 29), (20, 1 << 29), (100, 0)] {
        let c = Cycle::compile(Key::darwin(p << 16, e).unwrap()).unwrap();
        let phase = c.increments.t.get() / 7;
        let clock = Clock {
            centre: emergent_space::LegacyTube::new(Words::new(1234), Words::new(phase)),
            proper_epoch: Words::new(987),
        };
        let mut previous = 0;
        for i in 0..100u64 {
            let child = 987 + i * c.increments.tau.get() / 17;
            let t = clock.parent_time(&c, Words::new(child)).unwrap().get();
            assert!(t >= previous);
            assert!(clock.proper_time(&c, Words::new(t)).unwrap().get() >= child);
            if i > 0 {
                assert!(clock.proper_time(&c, Words::new(t - 1)).unwrap().get() < child);
            }
            previous = t;
        }
        assert_eq!(clock.parent_time(&c, Words::new(986)), Err(Error::Range));
    }
}

#[test]
fn logarithmic_mass_and_soi_are_integer_and_dimensionless() {
    assert_eq!(LogMass::scale(123, 0, false).unwrap(), 123);
    assert_eq!(LogMass::scale(123, 1 << 24, false).unwrap(), 246);
    assert_eq!(LogMass::scale(123, -(1 << 24), true).unwrap(), 62);
    let centre = Tube::new(0, 0, 0, 0, 0, TimeBasis::default()).unwrap();
    let parent = Doll::root(LogMass(0));
    let child = Doll::child(LogMass(-10 << 24), 0, centre).unwrap();
    // (2^-10)^(2/5) = 2^-4 exactly.
    assert_eq!(child.edge_radius(&parent, Words::new(1600)).unwrap().get(), 100);
    assert_eq!(Doll::child(LogMass(0), 1, centre), Err(Error::Topology));
    assert_eq!(parent.edge_radius(&parent, Words::new(1600)), Err(Error::Topology));
    assert_eq!(LogMass::scale(u64::MAX, 1 << 24, false), Err(Error::Range));
}

#[test]
fn same_scene_twice_has_identical_records_queue_and_readouts() {
    let run = || {
        let mut pool = CyclePool::default();
        let key = pool.intern(Key::darwin(20 << 16, 1 << 29).unwrap()).unwrap();
        let c = pool.get(key).unwrap();
        let period = c.increments.t.get();
        let mut calendar = Calendar::new(8);
        let tubes: Vec<_> = (0..8)
            .map(|slot| {
                calendar.set(slot, Some((slot as u64 % 3 + 1) * period)).unwrap();
                Tube::new(0, 0, key, 0, slot as u64, TimeBasis::default()).unwrap()
            })
            .collect();
        let mut states = Vec::new();
        while let Some((t, slot)) = calendar.pop() {
            states.push((t, slot, tubes[slot].state(&pool, TimeBasis::default(), Words::new(t)).unwrap()));
        }
        (tubes, states)
    };
    assert_eq!(run(), run());
}

#[test]
fn frozen_jupiter_scene_is_outside_the_current_compiler_envelope() {
    // Adapter-boundary quantizations, retained as an explicit consumer falsifier.
    // sep/Mstar=5.275275275e8, sqrt(r)/(sqrt(1-3/r))=22967.967...
    let key = Key::new(281474976443869, 98646669216336);
    assert_eq!(key, Err(Error::Range)); // L exceeds 4096, independently of time/radius.
                                        // Even extending Key's L alone would not extend its u>=2^-28 or Q20 period limits.
}

#[test]
fn root_queue_composes_nested_clocks_and_has_no_observation_events() {
    use emergent_space::events::{Event, EventKind, EventQueue, Hierarchy};
    let mut pool = CyclePool::default();
    let key = pool.intern(Key::darwin(20 << 16, 0).unwrap()).unwrap();
    let basis = TimeBasis::default();
    let mut hierarchy = Hierarchy::new(Doll::root(LogMass(0))).unwrap();
    let mut clocks = Vec::new();
    for parent in 0..2u16 {
        let centre = Tube::new(parent, 0, key, 0, 0, basis).unwrap();
        let child = Doll::child(LogMass(-((parent as i32 + 1) << 24)), parent, centre).unwrap();
        assert_eq!(hierarchy.add(child, basis, Words::new(0), &pool).unwrap(), parent + 1);
        clocks.push(Clock {
            centre: centre.generator(basis).unwrap(),
            proper_epoch: Words::new(0),
        });
    }
    let local = 1024;
    let one = clocks[1].parent_time(pool.get(key).unwrap(), Words::new(local / 2)).unwrap();
    let expected = clocks[0].parent_time(pool.get(key).unwrap(), Words::new(one.get().div_ceil(2))).unwrap();
    let root = hierarchy.root_time(&pool, 2, Words::new(local)).unwrap();
    assert_eq!(root, expected);
    let mut q = EventQueue::new(3);
    for slot in (0..3).rev() {
        q.schedule(Event {
            time: root,
            slot,
            kind: EventKind::Edge { destination: 0 },
        })
        .unwrap();
    }
    assert_eq!(q.pop_through(Words::new(root.get() - 1)).unwrap(), None);
    for slot in 0..3 {
        assert_eq!(q.pop_through(root).unwrap().unwrap().slot, slot);
    }
    assert_eq!(q.pop_through(Words::new(1 << 40)).unwrap(), None);
    assert!(q.is_empty());
    assert_eq!(
        q.schedule(Event {
            time: root,
            slot: 0,
            kind: EventKind::Horizon
        }),
        Err(Error::Range)
    );
    assert_eq!(hierarchy.root_time(&pool, 4, Words::new(0)), Err(Error::Topology));
}

#[test]
fn event_translations_are_reversible_and_refuse_diagonal_high_c() {
    use emergent_space::events::handoff::{translate, Cartesian};
    let body = Cartesian {
        position: [12345, -654321],
        velocity: [111, -222],
    };
    let old = Cartesian {
        position: [-92345, 321321],
        velocity: [303, -404],
    };
    let new = Cartesian {
        position: [8294571, -264582],
        velocity: [-505, 606],
    };
    let mut state = body;
    for _ in 0..10_000 {
        state = translate(translate(state, old, new).unwrap(), new, old).unwrap();
    }
    assert_eq!(state, body);
    let fast = Cartesian {
        position: [0, 0],
        velocity: [1 << 28, 1 << 28],
    };
    assert_eq!(translate(body, old, fast), Err(Error::Range));
    let edge = Cartesian {
        position: [0, 0],
        velocity: [1 << 28, 0],
    };
    assert!(translate(Cartesian::ZERO, Cartesian::ZERO, edge).is_ok());
    assert!(translate(edge, edge, Cartesian::ZERO).is_err());
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
fn kick_key_changes_are_authoritative_and_refusals_are_atomic() {
    use emergent_space::events::kicks::KeyCarry;
    let mut pool = CyclePool::default();
    let id = pool.intern(Key::darwin(20 << 16, 1 << 29).unwrap()).unwrap();
    let mut carry = KeyCarry::new(1024, 1024).unwrap();
    assert_eq!(carry.apply(&mut pool, id, 1000, 1000).unwrap(), id);
    assert_eq!(pool.len(), 1);
    let new = carry.apply(&mut pool, id, 1048, 1048).unwrap();
    assert_eq!(pool.get(new).unwrap().key.energy.get(), pool.get(id).unwrap().key.energy.get() + 2);
    assert_eq!(pool.get(new).unwrap().key.angular.get(), pool.get(id).unwrap().key.angular.get() + 2);
    let saved = carry;
    assert!(carry.apply(&mut pool, new, i64::MAX, 0).is_err());
    assert_eq!(carry, saved);
    assert_eq!(pool.len(), 2);
}

#[test]
fn linear_tide_stretches_radially_and_compresses_transversely() {
    use emergent_space::events::kicks::linear_tide;
    assert_eq!(linear_tide(1 << 20, [1 << 30, 0], [1 << 20, 1 << 20]).unwrap(), [2 << 20, -(1 << 20)]);
    assert_eq!(linear_tide(1 << 20, [0, 0], [1 << 20, 0]), Err(Error::Range));
}

#[test]
fn binary_test_mass_limit_is_exact_and_clock_map_uses_the_same_energy() {
    use emergent_space::events::binary::Binary;
    let key = Key::darwin(200 << 16, 1 << 29).unwrap();
    let b = Binary {
        energy: key.energy.get() as i64 - (1 << 48),
        angular: key.angular,
        nu: 0,
    };
    assert_eq!(b.key().unwrap(), key);
    let c = Cycle::compile(key).unwrap();
    assert_eq!(b.period(&c).unwrap(), c.increments.t);
    let equal = Binary { nu: 1 << 28, ..b };
    assert!(equal.key().unwrap().energy.get() > key.energy.get());
    let cycle = Cycle::compile(equal.key().unwrap()).unwrap();
    let mapped = equal.period(&cycle).unwrap().get();
    assert!(mapped < cycle.increments.t.get());
    assert_eq!(equal.period(&c), Err(Error::Topology));
    assert_eq!(Binary { nu: (1 << 28) + 1, ..b }.key(), Err(Error::Range));
}

#[test]
fn edge_prediction_is_an_exact_first_exit_and_skips_arbitrary_whole_cycles() {
    use emergent_space::events::edge::next_exit;
    let cycle = Cycle::compile(Key::darwin(20 << 16, 1 << 29).unwrap()).unwrap();
    let tube = emergent_space::LegacyTube::new(Words::new(123), Words::new(0));
    let edge = Words::new(20 << 20);
    let at = next_exit(&cycle, tube, Words::new(123), edge).unwrap().unwrap().get();
    let outside = |t| tube.position(&cycle, Words::new(t)).unwrap().u as u128 * edge.get() as u128 <= 1u128 << 82;
    assert!(outside(at) && !outside(at - 1));
    let n = 1_000_000 * cycle.increments.t.get();
    assert_eq!(next_exit(&cycle, tube, Words::new(n + 123), edge).unwrap().unwrap().get(), n + at);
    assert_eq!(next_exit(&cycle, tube, Words::new(at), edge).unwrap(), Some(Words::new(at)));
    assert_eq!(next_exit(&cycle, tube, Words::new(123), Words::new(100 << 20)).unwrap(), None);
}

#[test]
fn clock_is_monotone_at_mirrors_cuts_and_adjacent_integer_times() {
    for (p, e) in [(8, 1 << 29), (20, 1 << 29), (1000, 3 << 28)] {
        let c = Cycle::compile(Key::darwin(p << 16, e).unwrap()).unwrap();
        let clock = Clock {
            centre: emergent_space::LegacyTube::new(Words::new(0), Words::new(0)),
            proper_epoch: Words::new(0),
        };
        let period = c.increments.t.get();
        let mut cuts = vec![0, period / 2, period];
        for cut in &c.crossings {
            cuts.extend([cut.at.t.get(), period - cut.at.t.get()]);
        }
        for cut in cuts {
            let mut before = 0;
            for t in cut.saturating_sub(5)..=cut + 5 {
                let tau = clock.proper_time(&c, Words::new(t)).unwrap().get();
                assert!(tau >= before, "p={p} cut={cut} t={t}: tau={tau} before={before}");
                let inverse = clock.parent_time(&c, Words::new(tau)).unwrap().get();
                assert!(inverse <= t, "p={p} t={t} tau={tau} inverse={inverse}");
                before = tau;
            }
        }
    }
}

#[test]
fn polar_cartesian_accessor_preserves_handedness_and_refuses_invalid_states() {
    use emergent_space::events::handoff::cartesian;
    let c = Cycle::compile(Key::darwin(20 << 16, 1 << 29).unwrap()).unwrap();
    let state = c.state(Words::new(0)).unwrap();
    let a = cartesian(state, false, 0).unwrap();
    let b = cartesian(state, true, 0).unwrap();
    assert_eq!(a.position, b.position);
    assert!(a.position[0] > 0 && a.position[1] == 0);
    assert_eq!(a.velocity[0], 0);
    assert_eq!(a.velocity[1], -b.velocity[1]);
    let mut bad = state;
    bad.position.u = 1;
    assert_eq!(cartesian(bad, false, 0), Err(Error::Range));
}
