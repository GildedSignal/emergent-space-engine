//! Probe: where does the state-made planet's committed readout refuse, and why?
use emergent_space::orbit::Scalar;
use emergent_universe::num::{from_f64, s};
use emergent_universe::scenario::STAR_RADIUS;
use emergent_universe::universe::Universe;
use emergent_universe::{Config, Kind};

fn main() {
    for beta in [0.5f64, 0.9, 0.99] {
        let mut u = Universe::new(s(STAR_RADIUS), Config::default());
        let planet = u
            .add_body_state(Kind::Planet, 0, [s(500_000), s(0)], [Scalar::ZERO, from_f64(beta)], Scalar::ZERO)
            .unwrap();
        let _ = u.add_doll("fast", planet, -10, Scalar::raw(10, 10).unwrap()).unwrap();
        u.start().unwrap();
        // First refusal tick: scan powers of two.
        let mut first_refusal = None;
        let mut last_ok = 0i64;
        let mut step = 1i64;
        while step < (1i64 << 40) {
            match u.bodies().binding_at(planet, step) {
                Some(b) => match b.cartesian(step) {
                    Ok(_) => last_ok = step,
                    Err(_) => {
                        if first_refusal.is_none() {
                            first_refusal = Some(step);
                        }
                    }
                },
                None => {
                    if first_refusal.is_none() {
                        first_refusal = Some(-step); // history pruned marker
                    }
                }
            }
            step <<= 1;
        }
        println!(
            "beta {beta}: binding_at ok to {:?}, first cartesian refusal at 2^k = {:?} (last ok 2^k = {})",
            first_refusal.map(|t| t.ilog2().to_string()).unwrap_or_else(|| "none".into()),
            first_refusal.map(|t| t.to_string()).unwrap_or_else(|| "none".into()),
            last_ok
        );
    }
}
