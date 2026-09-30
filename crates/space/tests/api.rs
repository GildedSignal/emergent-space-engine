//! Consumer contract: compact records, rebased time, polar velocities, and explicit errors.
use emergent_space::*;

#[test]
fn compact_tube_reads_the_same_generator_at_a_rebased_epoch() {
    assert_eq!(size_of::<Tube>(), 16);
    assert_eq!(align_of::<Tube>(), 4);
    let c = Cycle::compile(Key::darwin(20 << 16, 1 << 29).unwrap()).unwrap();
    let phase = c.increments.t.get() / 7;
    let tube = Tube::new(Words::new(12345), Words::new(phase));
    for t in [0, phase, c.increments.t.get(), c.increments.t.get() * 1000] {
        assert_eq!(
            tube.state(&c, Words::new(12345 + t)).unwrap(),
            c.state(Words::new(phase + t)).unwrap()
        );
    }
    assert_eq!(tube.position(&c, Words::new(12344)), Err(Error::Range));
    let overflow = Tube::new(Words::new(0), Words::new(u64::MAX));
    assert_eq!(overflow.state(&c, Words::new(1)), Err(Error::Range));
}

#[test]
fn polar_velocity_matches_the_invariant_equations_and_readout_derivative() {
    for (p, e) in [(8, 0.5), (20, 0.3), (100, 0.0), (1000, 0.7)] {
        let c = compile(Key::darwin(p << 16, (e * (1u64 << 30) as f64) as u32).unwrap()).unwrap();
        let en = c.key.energy.get() as f64 / (1u64 << 48) as f64;
        let l = c.key.angular.get() as f64 / (1u64 << 32) as f64;
        let period = c.increments.t.get();
        for i in 1..80u64 {
            let t = period * i / 81;
            let s = c.state(Words::new(t)).unwrap();
            let u = s.position.u as f64 / (1u64 << 62) as f64;
            let lapse = 1.0 - 2.0 * u;
            let vr = s.velocity.radial as f64 / (1u64 << 30) as f64;
            let vt = s.velocity.transverse as f64 / (1u64 << 30) as f64;
            let sign = if s.position.outbound { 1.0 } else { -1.0 };
            let want = sign * (en * en - lapse * (1.0 + l * l * u * u)).max(0.0).sqrt() * lapse / en;
            assert!((vr - want).abs() < 2e-7, "p={p} i={i}: {vr} vs {want}");
            assert!((vt - l * u * lapse / en).abs() < 2e-9);
            // Resolve Q20 clock stair steps before taking a numerical derivative.
            let dt = period / 10_000;
            let a = c.position(Words::new(t - dt)).unwrap();
            let b = c.position(Words::new(t + dt)).unwrap();
            let seconds = 2.0 * dt as f64 / (1u64 << 20) as f64;
            let dr = ((1u64 << 62) as f64 / b.u as f64 - (1u64 << 62) as f64 / a.u as f64) / seconds;
            let dp = (b.phi.get() - a.phi.get()) as f64 / (1u64 << 30) as f64 / seconds / u;
            assert!(
                (vr - dr).abs() < 1e-5 && (vt - dp).abs() < 1e-5,
                "p={p} i={i}: ({vr},{vt}) vs ({dr},{dp})"
            );
        }
    }
}

#[test]
fn central_response_accepts_signed_kicks_and_refuses_invalid_probes() {
    let c = compile(Key::darwin(20 << 16, 1 << 29).unwrap()).unwrap();
    let d = Tangent::centered(&c, 1 << 24, 1 << 15).unwrap();
    assert_eq!(d.predict(c.increments, 0, 0).unwrap(), c.increments);
    for (de, dl) in [(1 << 20, 1 << 10), (-(1 << 20), 1 << 10), (1 << 20, -(1 << 10))] {
        let key = Key::new((c.key.energy.get() as i64 + de) as u64, (c.key.angular.get() as i64 + dl) as u64).unwrap();
        let actual = compile(key).unwrap().increments;
        let predicted = d.predict(c.increments, de, dl).unwrap();
        for (a, b) in [(actual.phi, predicted.phi), (actual.t, predicted.t), (actual.tau, predicted.tau)] {
            assert!((a.get() as f64 / b.get() as f64 - 1.0).abs() < 1e-6);
        }
    }
    assert_eq!(Tangent::centered(&c, 0, 1), Err(Error::Range));
    assert_eq!(Tangent::centered(&c, u64::MAX, 1), Err(Error::Range));
    assert!(Tangent::centered(&c, 1 << 47, 1).is_err());
    let edge = compile(Key::darwin(8 << 16, 1 << 29).unwrap()).unwrap();
    assert_eq!(Tangent::centered(&edge, 1 << 25, 1 << 16), Err(Error::Topology));
}

#[test]
fn long_period_mirror_does_not_overflow_twice_the_phase() {
    let key = Key::darwin(8192 << 16, (0.999968 * (1u64 << 30) as f64).round() as u32).unwrap();
    let cycle = compile(key).unwrap();
    let period = cycle.increments.t.get();
    assert!(period > u64::MAX / 2, "this case must exercise the overflowing old 2*r predicate");
    let outbound = cycle.position(Words::new(1)).unwrap();
    let inbound = cycle.position(Words::new(period - 1)).unwrap();
    assert!(outbound.outbound && !inbound.outbound);
    assert_eq!(outbound.u, inbound.u);
    assert_eq!(outbound.phi.get() + inbound.phi.get(), cycle.increments.phi.get());
}
