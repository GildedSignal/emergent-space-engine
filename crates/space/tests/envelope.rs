//! Independent limiting formulas and direct GR quadrature judge the scaled representation.
use emergent_space::orbit::{Orbit, OrbitKey, Passage, Scalar, ShapeMemo};
use std::f64::consts::{PI, TAU};
fn decode(x: Scalar) -> f64 {
    x.significand() as f64 * 2f64.powi(x.exponent() as i32 - 62)
}
fn encode(x: f64) -> Scalar {
    let exp = x.abs().log2().floor() as i32;
    Scalar::raw((x * 2f64.powi(60 - exp)).round() as i128, exp - 60).unwrap()
}
fn key(p: f64, e: f64) -> OrbitKey {
    OrbitKey::bound(encode(p), (e * 2f64.powi(48)).round() as u64).unwrap()
}

#[test]
fn weak_field_sweep_preserves_advance_and_kepler_plus_1pn() {
    let mut worst = [0f64; 3];
    for j in 0..=32 {
        let p = 10f64.powf(4.0 + j as f64 / 4.0);
        for i in 0..=18 {
            let e = i as f64 / 20.0;
            let orbit = Orbit::compile(key(p, e)).unwrap();
            let advance = decode(orbit.advance().unwrap());
            let a = p / (1.0 - e * e);
            let expected = TAU * a.powf(1.5);
            let errors = [
                (advance / (6.0 * PI / p) - 1.0).abs(),
                (decode(orbit.period().unwrap()) / (expected * (1.0 + 3.0 / a)) - 1.0).abs(),
                (decode(orbit.proper_period().unwrap()) / (expected * (1.0 + 1.5 / a)) - 1.0).abs(),
            ];
            assert!(
                advance > 0.0 && errors[0] < 0.01 && errors[1] < 0.001 && errors[2] < 0.001,
                "p={p} e={e}: {errors:?}"
            );
            for n in 0..3 {
                worst[n] = worst[n].max(errors[n]);
            }
            let coarse = Orbit::compile(key(p, e).memo_key().unwrap()).unwrap();
            let coarse_t = decode(coarse.period().unwrap());
            assert!((coarse_t / (expected * (1.0 + 3.0 / a)) - 1.0).abs() < 0.001, "memo width p={p} e={e}");
        }
    }
    println!("weak sweep: 627 orbits p=1e4..1e12 e=0..0.9; worst advance/period/proper={worst:?}");
}

#[test]
fn exponent_ladder_has_identical_shapes_and_positive_resolved_precession() {
    let mut memo = ShapeMemo::default();
    for exp in [40, 100, 1000, 10000, 20000] {
        let c = memo.get(OrbitKey::bound(Scalar::power_of_two(exp), 1 << 47).unwrap()).unwrap();
        assert!(c.advance().unwrap().is_positive());
        assert!(c.period().unwrap().is_positive());
        let phase = Scalar::integer(1);
        let early = c.at_phase(0, phase).unwrap();
        let late = c.at_phase(1_000_000, phase).unwrap();
        assert_eq!(
            (early.radius, early.psi, early.radial_velocity, early.transverse_velocity),
            (late.radius, late.psi, late.radial_velocity, late.transverse_velocity)
        );
    }
    assert_eq!(memo.len(), 1);
    assert_eq!(memo.hits, 4);
}

// Composite midpoint reference of the smooth continuum integrands, independently written.
fn reference(p: f64, e: f64) -> [f64; 3] {
    let mut sums = [0.0; 3];
    let l = p / (p - 3.0 - e * e).sqrt();
    let energy = (((p - 2.0).powi(2) - 4.0 * e * e) / (p * (p - 3.0 - e * e))).sqrt();
    for i in 0..16384 {
        let psi = PI * (i as f64 + 0.5) / 16384.0;
        let u = (1.0 + e * psi.cos()) / p;
        let g = (p / (p - 6.0 - 2.0 * e * psi.cos())).sqrt();
        sums[0] += g - 1.0;
        sums[1] += energy * g / (l * u * u * (1.0 - 2.0 * u));
        sums[2] += g / (l * u * u);
    }
    sums.map(|s| s * TAU / 16384.0)
}
#[test]
fn strong_field_and_near_separatrix_match_gr_and_velocity() {
    for e in [0.0, 0.001, 0.1, 0.5, 0.9] {
        for p in [6.0 + 2.0 * e + 0.0001, 10.0, 100.0, 1000.0] {
            let c = Orbit::compile(key(p, e)).unwrap();
            let expected = reference(p, e);
            let got = [
                decode(c.advance().unwrap()),
                decode(c.period().unwrap()),
                decode(c.proper_period().unwrap()),
            ];
            for j in 0..3 {
                assert!(
                    (got[j] / expected[j] - 1.0).abs() < if j == 0 { 0.01 } else { 0.001 },
                    "p={p} e={e} {got:?} vs {expected:?}"
                );
            }
            for j in [1, 3, 8, 13] {
                let s = c
                    .state(c.period().unwrap().mul(Scalar::integer(j)).unwrap().div(Scalar::integer(31)).unwrap())
                    .unwrap();
                let u = 1.0 / decode(s.radius);
                let l = p / (p - 3.0 - e * e).sqrt();
                let en = (((p - 2.0).powi(2) - 4.0 * e * e) / (p * (p - 3.0 - e * e))).sqrt();
                let vr = (en * en - (1.0 - 2.0 * u) * (1.0 + l * l * u * u)).max(0.0).sqrt() * (1.0 - 2.0 * u) / en;
                assert!((decode(s.radial_velocity).abs() - vr).abs() < 1e-7, "{p} {e}: {s:?}");
                assert!((decode(s.transverse_velocity) - l * u * (1.0 - 2.0 * u) / en).abs() < 1e-8);
            }
        }
    }
}

#[test]
fn hyperbolic_and_parabolic_passages_have_finite_times_and_symmetric_readouts() {
    for rp in [1e6, 1e10, 1e16] {
        for e in [1.0, 1.001, 1.5, 3.0, 30.0] {
            let k = (2f64.powi(48) / (1.0 + e)).round() as u64;
            let p = Passage::compile(OrbitKey::new(encode(rp), k).unwrap(), encode(20.0 * rp)).unwrap();
            let bend = decode(p.deflection().unwrap());
            let want = 2.0 * (1.0 / e).asin();
            assert!((bend / want - 1.0).abs() < 1e-4, "{rp} {e}: {bend} vs {want}");
            let half = decode(p.duration().unwrap()) / 2.0;
            let time = if e == 1.0 {
                let d = 19.0f64.sqrt();
                (2.0 * rp.powi(3)).sqrt() * (d + d.powi(3) / 3.0)
            } else {
                let a = rp / (e - 1.0);
                let h = ((20.0 * rp / a + 1.0) / e).acosh();
                a.powf(1.5) * (e * h.sinh() - h)
            };
            assert!((half / time - 1.0).abs() < 1e-4, "time {rp} {e}: {half} vs {time}");
            for j in 1..10 {
                let t = p.duration().unwrap().mul(Scalar::integer(j)).unwrap().div(Scalar::integer(21)).unwrap();
                let a = p.state(t).unwrap();
                let b = p.state(t.negate()).unwrap();
                assert_eq!(a.radius, b.radius);
                assert_eq!(a.radial_velocity, b.radial_velocity.negate());
                assert_eq!(a.transverse_velocity, b.transverse_velocity);
                assert_eq!(a.advance, b.advance.negate());
            }
        }
    }
}

#[test]
fn inverse_with_residual_is_an_exact_identity_through_repeated_event_frame_changes() {
    use emergent_space::binding::{cartesian, Rebinding};
    for p in [20.0, 1e4, 5e8, 3e10, 1e12] {
        for e in [0.0, 0.3, 0.9] {
            let c = Orbit::compile(key(p, e)).unwrap();
            for fraction in [3, 17] {
                let time = c
                    .period()
                    .unwrap()
                    .mul(Scalar::integer(fraction))
                    .unwrap()
                    .div(Scalar::integer(23))
                    .unwrap();
                let s = c.state(time).unwrap();
                let units = (s.radius.exponent() - 50, -52);
                let original = cartesian(s, 0x539abe21, false, units).unwrap();
                let mut current = original;
                for i in 0..40 {
                    // 20 round-trip handoffs and kicks. The transformation is integer;
                    // every new fit must return all four original components exactly.
                    let sign = if i % 2 == 0 { 1 } else { -1 };
                    current = current.translate([sign * 1234567, -sign * 987654], [sign * 4321, sign * 7654]).unwrap();
                    let fit =
                        Rebinding::from_state(current, Scalar::ZERO, None).unwrap_or_else(|err| panic!("p={p} e={e} f={fraction} i={i}: {err:?}"));
                    assert_eq!(fit.reconstruct().unwrap(), current);
                    let decoded = fit.decoded_event().unwrap();
                    // Residuals must also be small: an arbitrary fit plus the whole input
                    // would pass the identity while failing to represent this geodesic.
                    let position_scale = original.position.iter().map(|v| v.unsigned_abs()).max().unwrap() as f64;
                    let velocity_scale = original.velocity.iter().map(|v| v.unsigned_abs()).max().unwrap() as f64;
                    for j in 0..2 {
                        assert!(
                            ((decoded.position[j] as i128 - current.position[j] as i128).unsigned_abs() as f64) < position_scale * 1e-5 + 8.0,
                            "bad position fit {p} {e}: {:?}",
                            fit.residual
                        );
                        assert!(
                            ((decoded.velocity[j] as i128 - current.velocity[j] as i128).unsigned_abs() as f64) < velocity_scale * 1e-5 + 8.0,
                            "bad velocity fit {p} {e}: {:?}",
                            fit.residual
                        );
                    }
                    current = fit.reconstruct().unwrap();
                }
                assert_eq!(current, original);
            }
        }
    }
}

#[test]
fn public_tube_has_key_orientation_and_one_time_and_carries_its_inverse_rounding() {
    use emergent_space::{
        binding::{cartesian, Rebinding},
        tube::{Catalogue, TubeEvent},
        Tube,
    };
    assert_eq!(size_of::<Tube>(), 16);
    assert_eq!(align_of::<Tube>(), 4);
    for p in [20.0, 1e12] {
        let orbit = Orbit::compile(key(p, 0.3)).unwrap();
        for clockwise in [false, true] {
            let state = orbit.state(orbit.period().unwrap().div(Scalar::integer(7)).unwrap()).unwrap();
            let original = cartesian(state, 0xbeeffeed, clockwise, (state.radius.exponent() - 48, -52)).unwrap();
            let fit = Rebinding::from_state(original, Scalar::ZERO, None).unwrap();
            let clock_exp = fit.periapsis_time.abs().exponent() - 50;
            let mut catalogue = Catalogue::default();
            let bound = TubeEvent::bind(fit, &mut catalogue, clock_exp).unwrap();
            assert_eq!(bound.reconstruct(&catalogue).unwrap(), original);
            assert_eq!(catalogue.len(), 1);
            assert_ne!(bound.tube.periapsis_angle, 0);
            assert!(bound.tube.state(&catalogue, 0, clock_exp).unwrap().radius.is_positive());
        }
    }
}

#[test]
fn packed_keys_round_trip_and_shared_shapes_do_not_alias_different_inputs() {
    use emergent_space::orbit::{MemoCode, QuantizedMemo};
    let mut memo = QuantizedMemo::default();
    for p in [10.0, 100.0, 1e6, 1e10, 1e12] {
        for e in [0.0, 0.1, 0.7, 0.9, 0.999999] {
            let key = key(p, e).memo_key().unwrap();
            let code = MemoCode::encode(key).unwrap();
            assert_eq!(code.decode().unwrap(), key);
            assert!(code.bits() < 1 << 44);
            let a = memo.get(key).unwrap();
            let b = Orbit::compile(key).unwrap();
            assert_eq!(a.advance().unwrap(), b.advance().unwrap());
            assert_eq!(a.period().unwrap(), b.period().unwrap());
        }
    }
    assert_eq!(memo.hits, 10); // five eccentricities, two repeated weak scales
                               // Exercise every shape exponent and both signs of the full scale exponent.
                               // Encoding need not compile these shapes: their code is independent of dynamics.
    for radius_exp in [i16::MIN, -30000, -1, 0, 40, 20000, i16::MAX] {
        for gap_exp in -47..=0 {
            for mantissa in [2048, 2049, 3071, 4095] {
                let gap = Scalar::raw(mantissa, gap_exp - 11).unwrap().fixed(48).unwrap() as u64;
                if gap > 1 << 48 {
                    continue;
                }
                let raw = OrbitKey::new(Scalar::power_of_two(radius_exp), ((1 << 48) + gap) / 2).unwrap();
                let quantized = raw.memo_key().unwrap();
                let code = MemoCode::encode(raw).unwrap();
                assert!(code.bits() < 1 << 44);
                assert_eq!(code.decode().unwrap(), quantized);
            }
        }
    }
}

#[test]
fn unbound_inverse_preserves_incoming_and_outgoing_integer_states() {
    use emergent_space::binding::{cartesian, Rebinding, Trajectory};
    for e in [1.001, 1.5, 10.0] {
        let p = Passage::compile(
            OrbitKey::new(encode(1e10), (2f64.powi(48) / (1.0 + e)).round() as u64).unwrap(),
            encode(2e11),
        )
        .unwrap();
        for sign in [-1, 1] {
            let time = p.duration().unwrap().div(Scalar::integer(7 * sign)).unwrap();
            let state = p.state(time).unwrap();
            let input = cartesian(state, 0x198abcdf, sign < 0, (state.radius.exponent() - 48, -52)).unwrap();
            let fit = Rebinding::from_state(input, Scalar::ZERO, Some(encode(2e11))).unwrap();
            assert!(matches!(fit.trajectory, Trajectory::Passage(_)));
            assert_eq!(fit.reconstruct().unwrap(), input);
        }
    }
}

#[test]
fn strong_passages_match_an_independent_binet_ode_including_time() {
    // RK4 in azimuth: u''=1/L²-u+3u². No Darwin phase or compiler helper is used.
    for (rp, e) in [(3.3, 2.4), (4.5, 1.001), (6.0, 1.5), (10.0, 3.0), (20.0, 10.0)] {
        let p = rp * (1.0 + e);
        let l = p / f64::sqrt(p - 3.0 - e * e);
        let en = f64::sqrt(((p - 2.0) * (p - 2.0) - 4.0 * e * e) / (p * (p - 3.0 - e * e)));
        let edge = 20.0 * rp;
        let passage = Passage::compile(
            OrbitKey::new(encode(rp), (2f64.powi(48) / (1.0 + e)).round() as u64).unwrap(),
            encode(edge),
        )
        .unwrap();
        let derivative = |s: [f64; 3], clock: bool| {
            [
                s[1],
                1.0 / (l * l) - s[0] + 3.0 * s[0] * s[0],
                if clock { en / (l * s[0] * s[0] * (1.0 - 2.0 * s[0])) } else { 0.0 },
            ]
        };
        let step = |s: [f64; 3], h: f64, clock: bool| {
            let a = derivative(s, clock);
            let b = derivative(std::array::from_fn(|i| s[i] + h * a[i] / 2.0), clock);
            let c = derivative(std::array::from_fn(|i| s[i] + h * b[i] / 2.0), clock);
            let d = derivative(std::array::from_fn(|i| s[i] + h * c[i]), clock);
            std::array::from_fn(|i| s[i] + h * (a[i] + 2.0 * b[i] + 2.0 * c[i] + d[i]) / 6.0)
        };
        let h = 2e-5;
        let mut state = [1.0 / rp, 0.0, 0.0];
        let mut phi = 0.0;
        let mut crossing = None;
        let mut bend = None;
        for _ in 0..2_000_000 {
            let next = step(state, h, crossing.is_none());
            if crossing.is_none() && next[0] <= 1.0 / edge {
                let f = (state[0] - 1.0 / edge) / (state[0] - next[0]);
                crossing = Some(state[2] + f * (next[2] - state[2]));
            }
            if next[0] <= 0.0 {
                bend = Some(2.0 * (phi + h * state[0] / (state[0] - next[0])) - PI);
                break;
            }
            state = next;
            phi += h;
        }
        let time = crossing.expect("finite edge crossed");
        let bend = bend.expect("reached infinity in the Binet coordinate");
        let got_time = decode(passage.duration().unwrap()) / 2.0;
        let got_bend = decode(passage.deflection().unwrap());
        assert!((got_time / time - 1.0).abs() < 1e-5, "rp={rp} e={e} time {got_time} vs {time}");
        assert!((got_bend / bend - 1.0).abs() < 1e-5, "rp={rp} e={e} bend {got_bend} vs {bend}");
    }
}
