use emergent_space::{binding::{IntegerState, Rebinding}, orbit::{OrbitKey, Scalar}, plunge::{End, Plunge}, Error};

fn f(s: Scalar) -> f64 { s.significand() as f64 * 2f64.powi(s.exponent() as i32 - 62) }
fn s(x: f64) -> Scalar { Scalar::raw((x * (1u64 << 48) as f64) as i128, -48).unwrap() }
fn state(r: i64, vr: f64, vt: f64) -> IntegerState {
    IntegerState { position: [r, 0], velocity: [(vr * (1u64 << 50) as f64) as i64, (vt * (1u64 << 50) as f64) as i64],
        length_exponent: 0, velocity_exponent: -50 }
}

#[test]
fn a_surface_deadline_does_not_set_the_motion_scale() {
    let input = state(1024, -0.02, 0.0);
    let far = Plunge::from_state(input, End::Surface(Scalar::integer(32))).unwrap();
    let near = Plunge::from_state(input, End::Surface(Scalar::integer(1023))).unwrap();
    assert_eq!(far.motion_period().unwrap(), near.motion_period().unwrap());
    assert!(near.motion_period().unwrap() > near.arrival().coordinate_time.unwrap().scale(10).unwrap());
}

#[test]
fn rest_fall_has_an_exact_surface_event_and_the_schwarzschild_radial_clock() {
    for r in [8, 32, 1024, 1 << 24] {
        let input = state(r, 0.0, 0.0);
        assert!(matches!(Rebinding::from_state(input, Scalar::ZERO, None), Err(Error::NoBoundOrbit)));
        let inner = Scalar::integer(r / 2);
        let p = Plunge::from_state(input, End::Surface(inner)).unwrap();
        let a = p.arrival();
        // Exact GR radial fall from rest: tau = sqrt(r0^3/2)(acos sqrt(x) + sqrt(x(1-x))).
        let expected = ((r as f64).powi(3) / 2.0).sqrt() * (std::f64::consts::FRAC_PI_4 + 0.5);
        assert!((f(a.proper_time) / expected - 1.0).abs() < 2e-9, "r={r} {:?}", a);
        let end = p.at_coordinate(a.coordinate_time.unwrap()).unwrap();
        assert_eq!(end.radius, inner);
        assert!(end.terminal);
        assert_eq!(p.at_affine(p.affine_duration()).unwrap(), end);
        assert_eq!(p.at_coordinate(a.coordinate_time.unwrap().scale(1).unwrap()), Err(Error::Range));
        let first = p.at_coordinate(Scalar::ZERO).unwrap();
        assert_eq!(first.radius, Scalar::integer(r));
        assert_eq!(first.radial_momentum, Scalar::ZERO);
        for n in [7, 1, 6, 2, 5, 3, 4] {
            let t = a.coordinate_time.unwrap().mul(Scalar::raw(n, -3).unwrap()).unwrap();
            assert_eq!(p.at_coordinate(t).unwrap(), p.clone().at_coordinate(t).unwrap());
            assert!(p.at_coordinate(t).unwrap().radial_momentum < Scalar::ZERO);
        }
    }
}

#[test]
fn horizon_is_finite_in_falling_clocks_and_not_in_schwarzschild_time() {
    let p = Plunge::from_state(state(32, 0.0, 0.0), End::Horizon).unwrap();
    let a = p.arrival();
    assert_eq!(a.coordinate_time, None);
    let x: f64 = 2.0 / 32.0;
    let expected = (32f64.powi(3) / 2.0).sqrt() * (x.sqrt().acos() + (x*(1.0-x)).sqrt());
    assert!((f(a.proper_time) / expected - 1.0).abs() < 2e-9);
    let end = p.at_affine(a.proper_time).unwrap();
    assert_eq!(end.radius, Scalar::integer(2));
    assert!(end.terminal && a.advanced_time > Scalar::ZERO);
    assert_eq!(p.at_coordinate(Scalar::ZERO), Err(Error::Range));
}

#[test]
fn near_radial_sign_and_whole_interval_barriers() {
    for vt in [0.0, 1e-9, -1e-9, 0.001, -0.001, 0.01] {
        let p = Plunge::from_state(state(64, -0.02, vt), End::Horizon).unwrap();
        assert_eq!(p.arrival().angle.significand().signum(), if vt == 0.0 { 0 } else { vt.signum() as i64 });
        let mut prev = p.initial_radius();
        for n in 1..=10 {
            let a = p.at_affine(p.affine_duration().mul(Scalar::integer(n)).unwrap().div(Scalar::integer(10)).unwrap()).unwrap();
            assert!(a.radius < prev);
            prev = a.radius;
        }
    }
    // At an apoapsis with a centrifugal barrier before the surface: NOT capture.
    assert!(Plunge::from_state(state(64, 0.0, 0.10), End::Horizon).is_err());
    assert!(Plunge::from_state(state(64, 0.02, 0.0), End::Horizon).is_err());
    assert!(Plunge::from_state(state(64, -1.0, 0.0), End::Horizon).is_err());
    assert!(Plunge::from_state(state(2, 0.0, 0.0), End::Horizon).is_err());
    assert!(Plunge::from_state(state(64, 0.0, 0.0), End::Surface(Scalar::integer(2))).is_err());
}

#[test]
fn null_capture_uses_the_exact_existing_predicate_and_has_zero_proper_time() {
    for impact in [0.0, 1.0, 4.0, 5.0, 5.19, 5.20, 6.0] {
        let b = s(impact);
        let captured = OrbitKey::photon(b).unwrap().is_none();
        let p = Plunge::photon(b, Scalar::integer(32), End::Horizon).unwrap();
        assert_eq!(p.is_some(), captured);
        if let Some(p) = p {
            assert_eq!(p.arrival().proper_time, Scalar::ZERO);
            assert_eq!(p.at_affine(p.affine_duration()).unwrap().radius, Scalar::integer(2));
            assert_eq!(p.arrival().coordinate_time, None);
            if impact == 0.0 {
                assert_eq!(p.arrival().advanced_time, Scalar::ZERO);
                assert!((f(p.affine_duration()) / 30.0 - 1.0).abs() < 2e-9);
            }
        }
    }
}

/// A state the turning inverse takes keeps its turning orbit whatever its periapsis: one that dips under the surface is ended
/// where its tube meets the surface by the engine (`next_impact`), and the arcs' exact interval predicate (milliseconds) is paid
/// only by states with no periapsis to turn at (a fall or a rise: the tests around this one).
#[test]
fn a_turning_orbit_inside_the_star_stays_a_turning_orbit() {
    let input = state(64, -0.02, 0.10);
    let original = Rebinding::from_state(input, Scalar::ZERO, None).unwrap();
    assert!(original.trajectory.key().unwrap().periapsis < Scalar::integer(32));
    let fit = Rebinding::ending_at(input, Scalar::integer(123), None, Scalar::integer(32)).unwrap();
    assert_eq!(fit.reconstruct().unwrap(), input);
    assert!(fit.trajectory.key().is_some_and(|k| k.periapsis < Scalar::integer(32)), "a turning orbit, not an arc");
}

#[test]
fn energy_and_angular_momentum_hold_on_the_inward_arc() {
    for r in [16, 64, 1024, 1 << 20] {
        for vt in [-0.001, 0.0, 0.001] {
            let input = state(r, -0.02, vt);
            let p = Plunge::from_state(input, End::Surface(Scalar::integer(r/2))).unwrap();
            let [_, _, l2, energy, _] = p.coefficients();
            for j in 0..=16 {
                let t = p.arrival().coordinate_time.unwrap().mul(Scalar::raw(j, -4).unwrap()).unwrap();
                let st = p.orbit_state(t).unwrap();
                let (rr, vr, vt) = (f(st.radius), f(st.radial_velocity), f(st.transverse_velocity));
                let lapse = 1.0 - 2.0/rr;
                let den = lapse - vr*vr/lapse - vt*vt;
                assert!((lapse/den.sqrt()/f(energy)-1.0).abs() < 1e-12);
                if f(l2) != 0.0 { assert!(((rr*vt).powi(2)/den/f(l2)-1.0).abs() < 1e-12); }
            }
        }
    }
}
