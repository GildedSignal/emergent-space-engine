//! The scaled key must survive the universe's choice of integer state units.
use emergent_space::orbit::Scalar;
use emergent_universe::body::Kind;
use emergent_universe::num::{from_f64, to_f64};
use emergent_universe::scenario::{AU, STAR_RADIUS};
use emergent_universe::{Config, Universe};

#[test]
fn far_flybys_survive_the_universe_adapter() {
    for radius in [3 * AU, 10 * AU, 30 * AU, 100 * AU, 1 << 38, 1 << 39] {
        for energy in [1.001f64, 3.0, 1000.0] {
            let mut u = Universe::new(Scalar::integer(STAR_RADIUS), Config::default());
            let f = 1.0 - 2.0 / radius as f64;
            let speed = (f - f * f / (energy * energy)).sqrt();
            let id = u
                .add_body_state(
                    Kind::Ship,
                    0,
                    [Scalar::integer(radius), Scalar::ZERO],
                    [Scalar::ZERO, from_f64(speed)],
                    Scalar::ZERO,
                )
                .unwrap();
            let digest = u.digest();
            for sign in [-1, 1] {
                let t = (sign as f64 * radius as f64 / speed) as i64;
                let (x, v) = u.rec(id).b.cartesian(t).unwrap();
                // A weak-field straight-flight control: the independent curved
                // reference and the tighter 1e-6 criterion are in space's R1.
                assert!((to_f64(x[0]) / radius as f64 - 1.0).abs() < 1e-5);
                assert!((to_f64(x[1]) / radius as f64 - sign as f64).abs() < 1e-5);
                assert!((to_f64(v[1]) / speed - 1.0).abs() < 1e-5);
            }
            assert_eq!(u.digest(), digest);
            assert_eq!(u.rec(id).refusals, 0);
        }
    }
}
