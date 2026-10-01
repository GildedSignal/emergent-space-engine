//! Null guards independent of the compiler: metric, clocks and asymptotic limits.
use emergent_space::orbit::{OrbitKey, Passage, Scalar};
fn s(x: f64) -> Scalar {
    let e = x.abs().log2().floor() as i32;
    Scalar::raw((x * 2f64.powi(60 - e)).round() as i128, e - 60).unwrap()
}
fn d(x: Scalar) -> f64 {
    x.significand() as f64 * 2f64.powi(x.exponent() as i32 - 62)
}
#[test]
fn photons_have_zero_length_and_follow_the_null_metric_at_retarded_times() {
    for b in [5.197, 6.0, 10.0, 1000.0, 1e12] {
        let p = Passage::photon(s(b), s(b * 1024.0)).unwrap().unwrap();
        let half = p.duration().unwrap().scale(-1).unwrap();
        for fraction in [0.01, 0.1, 0.7, 1.0] {
            let t = half.mul(s(fraction)).unwrap();
            let a = p.state(t).unwrap();
            let incoming = p.state(t.negate()).unwrap();
            assert_eq!(a.radius, incoming.radius);
            assert_eq!(a.radial_velocity, incoming.radial_velocity.negate());
            assert_eq!(a.proper_time, Scalar::ZERO);
            let (r, vr, vt) = (d(a.radius), d(a.radial_velocity), d(a.transverse_velocity));
            let lapse = 1.0 - 2.0 / r;
            assert!(
                (vr * vr / (lapse * lapse) + vt * vt / lapse - 1.0).abs() < 3e-8,
                "b={b} r={r}"
            );
            // Readout is pure: an intervening observation cannot change an earlier one.
            p.state(half).unwrap();
            assert_eq!(p.state(t).unwrap(), a);
        }
        let r = s(b * 16.0);
        let (t, a) = p.at_radius(r).unwrap();
        assert!((d(p.state(t).unwrap().radius) / d(r) - 1.0).abs() < 1e-7);
        assert_eq!(a.proper_time, Scalar::ZERO);
    }
}
#[test]
fn capture_and_weak_bending_retain_information_across_exponents() {
    let critical = 27f64.sqrt();
    for side in [-1.0, 1.0] {
        for gap in [1e-3, 1e-6, 1e-10] {
            assert_eq!(
                OrbitKey::photon(s(critical * (1.0 + side * gap)))
                    .unwrap()
                    .is_none(),
                side < 0.0
            );
        }
    }
    for exponent in [20, 40, 80, 200] {
        let b = Scalar::power_of_two(exponent);
        let p = Passage::photon(b, b.scale(80).unwrap()).unwrap().unwrap();
        let deflection = p.deflection().unwrap();
        assert!((d(deflection.mul(b).unwrap()) / 4.0 - 1.0).abs() < 4e-6);
        let t = p.duration().unwrap().scale(-2).unwrap();
        assert!(p.state(t).unwrap().radius > b);
    }
}
#[test]
fn captured_light_has_native_exterior_readout_and_the_radial_schwarzschild_clock() {
    use emergent_space::light::Capture;
    for b in [0.0, 3.0, 5.19] {
        let impact = if b == 0.0 { Scalar::ZERO } else { s(b) };
        let c = Capture::compile(impact, s(100.0), s(2.01))
            .unwrap()
            .unwrap();
        let end = c.duration().unwrap();
        for fraction in [0.0, 0.2, 0.8, 1.0] {
            let t = end
                .mul(if fraction == 0.0 {
                    Scalar::ZERO
                } else {
                    s(fraction)
                })
                .unwrap();
            let a = c.state(t).unwrap();
            let (r, vr, vt) = (d(a.radius), d(a.radial_velocity), d(a.transverse_velocity));
            let lapse = 1.0 - 2.0 / r;
            assert_eq!(a.proper_time, Scalar::ZERO);
            assert!(vr < 0.0 && r >= 2.00999);
            assert!((vr * vr / (lapse * lapse) + vt * vt / lapse - 1.0).abs() < 2e-10);
            if b == 0.0 {
                let exact = 100.0 - r + 2.0 * ((100.0 - 2.0) / (r - 2.0)).ln();
                assert!((d(t) - exact).abs() < 1e-5, "{t:?} {exact}");
            }
        }
        assert!(Capture::compile(impact, s(100.0), s(2.0)).is_err());
    }
    assert!(
        Capture::compile(s(6.0), s(100.0), s(2.01))
            .unwrap()
            .is_none()
    );
}
#[test]
fn aberration_is_a_reversible_lorentz_map_and_preserves_null_directions() {
    use emergent_space::light::{aberrate, moving_deflection};
    for beta in [0.0, 0.3, 0.9, 0.999] {
        let b = if beta == 0.0 { Scalar::ZERO } else { s(beta) };
        for angle in [0.0, 0.3, 1.0, 2.4, std::f64::consts::PI] {
            let signed = |x: f64| {
                if x == 0.0 {
                    Scalar::ZERO
                } else if x > 0.0 {
                    s(x)
                } else {
                    s(-x).negate()
                }
            };
            let n = [signed(angle.cos()), signed(angle.sin())];
            let lens = aberrate(n, b).unwrap();
            assert!((d(lens[0]).powi(2) + d(lens[1]).powi(2) - 1.0).abs() < 1e-12);
            let back = aberrate(lens, b.negate()).unwrap();
            for i in 0..2 {
                assert!((d(back[i]) - d(n[i])).abs() < 1e-12);
            }
            let positive = moving_deflection(n, b, s(100.0)).unwrap();
            let mirrored = moving_deflection([n[0], n[1].negate()], b, s(100.0).negate()).unwrap();
            assert!((d(positive) + d(mirrored)).abs() < 1e-12);
        }
    }
    assert!(aberrate([Scalar::ONE, Scalar::ZERO], Scalar::ONE).is_err());
}
#[test]
fn moving_lenses_do_not_erase_subquantum_bends() {
    use emergent_space::light::moving_deflection;
    let beta = s(0.9);
    let factor = ((1.0 + 0.9f64) / (1.0 - 0.9)).sqrt();
    for exponent in [40, 80, 200] {
        let b = Scalar::power_of_two(exponent);
        let deflection = moving_deflection([Scalar::integer(-1), Scalar::ZERO], beta, b).unwrap();
        assert!((d(deflection.mul(b).unwrap()) / (4.0 * factor) - 1.0).abs() < 1e-10);
    }
}
