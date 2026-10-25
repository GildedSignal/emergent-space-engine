//! A shared readout must preserve the exact event and be independent of memo history.
use emergent_space::{
    binding::{cartesian, Rebinding, Trajectory},
    orbit::{clear_shape_cache, Orbit, OrbitKey, Scalar, ShapeGrid},
};
const GRID: ShapeGrid = ShapeGrid { bits: 10, order: 1 };

#[test]
fn exact_geometry_survives_the_circle_and_parabolic_grid_edges() {
    for gap in [2, 4, 1 << 20, (1 << 47) - 2, 1 << 47, (1 << 47) + 2,
        (1 << 48) - 2, 1 << 48] {
        let key = OrbitKey::new(Scalar::power_of_two(30), ((1 << 48) + gap) / 2).unwrap();
        let orbit = Orbit::compile_interpolated(key, GRID).unwrap();
        assert_eq!(orbit.key(), key);
        let first = orbit.at_phase(0, Scalar::power_of_two(-10)).unwrap();
        for cycles in [1, 10_000, 1_000_000] {
            let late = orbit.at_phase(cycles, Scalar::power_of_two(-10)).unwrap();
            assert_eq!((late.radius, late.psi, late.radial_velocity),
                (first.radius, first.psi, first.radial_velocity));
            assert_eq!(late.advance, first.advance.add(orbit.advance().unwrap()
                .mul(Scalar::integer(cycles as i64)).unwrap()).unwrap());
        }
    }
}

#[test]
fn eviction_reordered_reads_and_other_threads_do_not_select_answers() {
    let key = OrbitKey::bound(Scalar::power_of_two(30), (1 << 48) * 7 / 10).unwrap();
    let mut orbit = Orbit::compile_interpolated(key, GRID).unwrap();
    let period = orbit.period().unwrap();
    let times = [period.scale(-3).unwrap(), period, period.mul(Scalar::integer(13)).unwrap()];
    let expected: Vec<_> = times.iter().map(|&t| orbit.state(t).unwrap()).collect();
    orbit.make_evictable();
    for i in [2, 0, 1, 0] {
        clear_shape_cache();
        // Exact and interpolated recipes for the same key cannot alias.
        let mut exact = Orbit::compile(key).unwrap();
        exact.make_evictable();
        let _ = exact.state(times[i]).unwrap();
        assert_eq!(orbit.state(times[i]).unwrap(), expected[i]);
    }
    std::thread::spawn(move || {
        for (t, expected) in times.into_iter().zip(expected) {
            assert_eq!(orbit.state(t).unwrap(), expected);
        }
    }).join().unwrap();
}

#[test]
fn integer_event_state_is_reconstructed_after_interpolated_rebinding() {
    for i in 0..64u64 {
        let key = OrbitKey::bound(Scalar::power_of_two(30), ((1 << 48) - 1) * i / 65).unwrap();
        let exact = Orbit::compile(key).unwrap();
        let st = exact.state(exact.period().unwrap().scale(-3).unwrap()).unwrap();
        let input = cartesian(st, (i as u32).wrapping_mul(0x1234567), i % 2 == 0,
            (st.radius.exponent() - 60,
             st.radial_velocity.abs().max(st.transverse_velocity.abs()).exponent() - 60)).unwrap();
        let mut fit = Rebinding::from_state_grid(input, Scalar::ZERO, None, Some(GRID)).unwrap();
        assert_eq!(fit.reconstruct().unwrap(), input);
        if let Trajectory::Cycle(orbit) = &mut fit.trajectory { orbit.make_evictable(); }
        clear_shape_cache();
        assert_eq!(fit.reconstruct().unwrap(), input);
    }
}
