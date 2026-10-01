//! Native polar readout checked against independent invariant equations and derivatives.
use emergent_space::orbit::{Orbit, OrbitKey, Scalar};
fn d(x: Scalar) -> f64 {
    x.significand() as f64 * 2f64.powi(x.exponent() as i32 - 62)
}
#[test]
fn polar_velocity_matches_invariants_and_the_readout_derivative() {
    for (p, e) in [(8, 0.5), (20, 0.3), (100, 0.0), (1000, 0.7)] {
        let key = OrbitKey::bound(Scalar::integer(p), (e * 2f64.powi(48)).round() as u64).unwrap();
        let c = Orbit::compile(key).unwrap();
        let en = (((p as f64 - 2.0).powi(2) - 4.0 * e * e) / (p as f64 * (p as f64 - 3.0 - e * e)))
            .sqrt();
        let l = p as f64 / (p as f64 - 3.0 - e * e).sqrt();
        let period = c.period().unwrap();
        for i in 1..80 {
            let t = period
                .mul(Scalar::integer(i))
                .unwrap()
                .div(Scalar::integer(81))
                .unwrap();
            let s = c.state(t).unwrap();
            let u = 1.0 / d(s.radius);
            let lapse = 1.0 - 2.0 * u;
            let (vr, vt) = (d(s.radial_velocity), d(s.transverse_velocity));
            let want = (en * en - lapse * (1.0 + l * l * u * u)).max(0.0).sqrt() * lapse / en
                * if s.outbound { 1.0 } else { -1.0 };
            assert!((vr - want).abs() < 2e-7);
            assert!((vt - l * u * lapse / en).abs() < 2e-9);
            let dt = period.div(Scalar::integer(10_000)).unwrap();
            let (a, b) = (
                c.state(t.sub(dt).unwrap()).unwrap(),
                c.state(t.add(dt).unwrap()).unwrap(),
            );
            let angle = |s: emergent_space::orbit::OrbitState| {
                s.radial_angle as f64 / 2f64.powi(61) + d(s.advance)
            };
            let dr = (d(b.radius) - d(a.radius)) / (2.0 * d(dt));
            let dp = (angle(b) - angle(a)) / (2.0 * d(dt) * u);
            assert!(
                (vr - dr).abs() < 1e-5 && (vt - dp).abs() < 1e-5,
                "p={p} i={i} ({vr},{vt}) vs ({dr},{dp})"
            );
        }
    }
}
