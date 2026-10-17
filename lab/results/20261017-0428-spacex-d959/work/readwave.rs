//! The wave's read stream, censused by call site: the plane plus `N` ladder ships, settled straight
//! through the belt's first kick wave (every belt body's first kicks land together at ~13,051-14,534
//! game-s on merged main), with `readstat` armed — so every `Binding::readout` of the settle is
//! bucketed by caller. No page, no view, no scan: the engine's own reads alone.
//!
//! cargo run --release -p emergent-universe --example readwave [-- <N> <end game-s>]
use emergent_universe::bind::readstat;
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::Config;
use std::sync::atomic::Ordering;
use std::time::Instant;

fn main() {
    let n: usize = std::env::args().nth(1).and_then(|s| s.parse().ok()).unwrap_or(100_000);
    let end_gs: f64 = std::env::args().nth(2).and_then(|s| s.parse().ok()).unwrap_or(14_600.0);
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, n).unwrap();
    let bodies = p.u.n_bodies();
    readstat::ARMED.store(true, Ordering::Relaxed);
    let horizon = (end_gs / TICK_SECONDS) as i64;
    let t0 = Instant::now();
    p.u.settle(horizon);
    let wall = t0.elapsed().as_secs_f64();
    println!("readwave: n={n} bodies={bodies} end_gs={end_gs:.0} settle_s={wall:.2} reads/body={:.3}", readstat::total() as f64 / bodies as f64);
    readstat::dump();
}
