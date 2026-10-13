//! Bind-word probe (20261013-0037-components-009b): how often a bind's word transition
//! discards the first compiled trajectory, and what that costs. Args: [game-seconds] [members]
//! [seed]; prints the universe stats, the probe counters and the canonical digest.
use emergent_universe::bind::probe;
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::Config;
use std::time::Instant;

fn main() {
    let secs: f64 = std::env::args().nth(1).map(|s| s.parse().unwrap()).unwrap_or(600.0);
    let members: u64 = std::env::args().nth(2).map(|s| s.parse().unwrap()).unwrap_or(48);
    let seed: u64 = std::env::args().nth(3).map(|s| s.parse().unwrap()).unwrap_or(1);
    let t0 = Instant::now();
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, members).unwrap();
    println!("built in {:.2}s: {} bodies", t0.elapsed().as_secs_f64(), p.u.n_bodies());
    let ticks = (secs / 4.926e-6) as i64;
    let t0 = Instant::now();
    p.u.settle(ticks);
    println!(
        "settled {secs}s game ({ticks} ticks) in {:.2}s: {:?}",
        t0.elapsed().as_secs_f64(),
        p.u.stats
    );
    println!("{}", probe::dump());
    println!("digest {}", p.u.digest());
}
