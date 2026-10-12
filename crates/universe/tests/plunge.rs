use emergent_space::{binding::Trajectory, orbit::Scalar};
use emergent_universe::{universe::Universe, Config, Kind};

#[test]
fn stopping_above_a_surface_falls_and_resolves_one_exact_terminal_event() {
    for r in [64, 1024, 1 << 20] {
        let surface = Scalar::integer(r / 2);
        let mut u = Universe::new(surface, Config::default());
        let body = u.add_body_state(Kind::Player, 0, [Scalar::integer(r), Scalar::ZERO],
            [Scalar::ZERO; 2], Scalar::ZERO).unwrap();
        assert!(matches!(u.rec(body).b.entry.trajectory, Trajectory::Plunge(_)));
        let at = u.rec(body).b.terminal_tick().unwrap().unwrap();
        let exact = u.rec(body).b.readout(0).unwrap();
        assert_eq!(exact.velocity, [0; 2]);
        u.start().unwrap();
        assert_eq!(u.rec(body).plan.len(), 1);
        u.settle(at - 1);
        assert!(u.rec(body).alive);
        assert!(u.rec(body).b.orbit_state(at - 1).unwrap().radius > surface);
        assert_eq!(u.rec(body).b.orbit_state(at).unwrap().radius, surface);
        u.settle(at);
        assert!(!u.rec(body).alive);
        assert_eq!(u.rec(body).events, 1);
        assert!(u.rec(body).plan.is_empty());
        assert!(u.rec(body).b.readout(at + 1).is_err());
    }
}

#[test]
fn a_near_radial_kick_binding_keeps_its_exact_event_and_terminal_clock() {
    use emergent_space::binding::IntegerState;
    use emergent_universe::{bind::{bind_surface, bind_exact}, world::Unit};
    let initial = IntegerState { position: [1 << 50, 0], velocity: [-(1 << 38), 1],
        length_exponent: -40, velocity_exponent: -48 };
    let bound = bind_surface(initial, 123, 0, None, Unit::ONE, Some(Scalar::integer(32))).unwrap();
    let mut binding = bind_exact(bound.entry, bound.tube, 0, bound.units, 123, 0);
    binding.turn = bound.turn;
    binding.residual = bound.residual;
    assert_eq!(binding.readout(123).unwrap(), initial);
    let end = binding.terminal_tick().unwrap().unwrap();
    let expected = binding.readout(end - 1).unwrap();
    for t in [end - 1, 123, (end + 123) / 2, end, end - 1] { binding.readout(t).unwrap(); }
    assert_eq!(binding.readout(end - 1).unwrap(), expected);
}
