//! When the ladder's bodies first have something to do: the first planned item of each ladder ship at the start (the locals about
//! Home and the belt about the star), in game seconds. The belt's bodies are stepped by the root doll's clock (2^step_log2 kicks per
//! period of the doll's shortest secondary), and all are born at tick 0 with one Δs: their first kicks come as one wave.
//!
//! cargo run --release -p emergent-universe --example belt_first [-- <N>]
use emergent_universe::fleet::Order;
use emergent_universe::scenario::{ladder_locals, plane_extra};
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::Config;

fn main() {
    let n: usize = std::env::args().nth(1).and_then(|s| s.parse().ok()).unwrap_or(3000);
    let p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, n).unwrap();
    let locals = ladder_locals(n as u64) as usize;
    // The ladder's ships come after the plane's own bodies and before the player.
    let base = p.player - n;
    let (mut belt, mut loc) = (Vec::new(), Vec::new());
    for k in 0..n {
        let r = p.u.rec(base + k);
        let t = r.plan.iter().map(|it| it.t).min().map_or(f64::INFINITY, |t| t as f64 * TICK_SECONDS);
        if k < locals {
            loc.push(t)
        } else {
            belt.push(t)
        }
    }
    for (name, v) in [("locals", &mut loc), ("belt", &mut belt)] {
        v.sort_by(|a, b| a.partial_cmp(b).unwrap());
        if v.is_empty() {
            continue;
        }
        let q = |p: f64| v[((v.len() - 1) as f64 * p) as usize];
        println!("{name}: {} bodies, first item (game s) min {:.0} p01 {:.0} p50 {:.0} p99 {:.0} max {:.0}", v.len(), q(0.0), q(0.01), q(0.5), q(0.99), q(1.0));
    }
}
