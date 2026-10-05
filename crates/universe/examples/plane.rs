use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::Config;
use std::time::Instant;
fn main() {
    let secs: f64 = std::env::args().nth(1).map(|s| s.parse().unwrap()).unwrap_or(3600.0);
    let t0 = Instant::now();
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
    println!("built in {:.2}s: {} bodies, {} dolls", t0.elapsed().as_secs_f64(), p.u.n_bodies(), p.u.dolls.len());
    let ticks = (secs / 4.926e-6) as i64;
    let t0 = Instant::now();
    p.u.settle(ticks);
    let s = p.u.stats;
    println!("settled {secs}s game ({ticks} ticks) in {:.2}s: {s:?}", t0.elapsed().as_secs_f64());
    let dead: Vec<_> = (0..p.u.n_bodies()).filter(|&i| !p.u.rec(i).alive).map(|i| (i, p.names[i].clone(), p.u.rec(i).fault)).collect();
    println!("dead: {dead:?}");
    println!("fleet: tick {} contacts {} epochs {} anchors {}", p.u.fleets[0].tick(), p.u.fleets[0].contacts(), p.u.fleets[0].epochs(), p.u.fleets[0].anchors());
    println!("bytes/body {}", p.u.bytes_per_body());
    println!("digest {}", p.u.digest());
}
