//! Flight past γ ≈ 2,000 (the lens `b-high-gamma`): a ship under the top throttle must reach
//! γ = 10⁶ and coast there. This file starts as the probe that finds where the range breaks;
//! it becomes the frozen test once the range is extended.
use emergent_space::orbit::Scalar;
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::view::gather;
use emergent_universe::{thrust, Budget, Config};

fn to_f64(s: Scalar) -> f64 {
    emergent_universe::num::to_f64(s)
}

#[test]
fn probe_where_a_top_throttle_burn_breaks() {
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
    p.u.input(0, thrust::word(1, 15)).unwrap();
    let mut target: i64 = 1 << 26;
    let mut best = 1.0f64;
    loop {
        p.u.settle(target);
        let v = gather(&p.u, &p.names).unwrap();
        let b = (v.beta[0].powi(2) + v.beta[1].powi(2)).sqrt();
        let g = 1.0 / (1.0 - b * b).sqrt();
        let rec = p.u.rec(p.player);
        let (x, vel) = rec.b.cartesian(rec.b.event_time).unwrap();
        let r = to_f64(x[0].mul(x[0]).unwrap().add(x[1].mul(x[1]).unwrap()).unwrap().sqrt().unwrap());
        println!(
            "t={:>13} event={:>13} r={:11.3e} beta={:.9} gamma={:11.3e} rate={:.9e} alive={} refusals={} fault={:?} loss={:?} events={}",
            p.u.now, rec.b.event_time, r, b, g, v.rate, rec.alive, rec.refusals, rec.fault, v.loss, p.u.stats.events()
        );
        best = best.max(g);
        if !rec.alive || rec.refusals > 0 {
            panic!("broke at gamma {g:.3e}: {:?}", rec.fault);
        }
        if g >= 1.0e6 {
            break;
        }
        target = target.saturating_mul(2);
        if target <= 0 {
            panic!("out of ticks at gamma {g:.3e}");
        }
    }
    println!("reached gamma {best:.3e}");
}
