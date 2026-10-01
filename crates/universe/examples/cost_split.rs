// Where a ship's kick goes: the pure resolve (readouts, force, rebinding) against the universe's own
// overhead (applying, the queue, the root-position cache, pulling the planets).
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::Config;
use std::time::Instant;
fn main() {
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 8).unwrap();
    let ship = p.ships[14]; // an orbiter about Home
    let n = 3000;
    // pure process on clones of one record: kicks and boundaries alternate
    let ctx = p.u.ctx();
    let rec = p.u.rec(ship);
    let t0 = Instant::now();
    let mut kicks = 0;
    for _ in 0..n {
        let mut r = rec.clone();
        // advance to the first Kick item
        while !matches!(r.plan.first().map(|i| i.what), Some(emergent_universe::body::What::Kick(0))) { r.plan.remove(0); }
        let u = emergent_universe::step::process(&ctx, ship, r);
        kicks += matches!(u.kind, emergent_universe::step::Resolved::Kick) as u32;
        std::hint::black_box(&u);
    }
    let per = t0.elapsed().as_secs_f64() * 1e6 / n as f64;
    println!("pure kick (resolve) {per:.1} us ({kicks} kicks of {n})");
    // pieces
    let t = rec.b.event_time + 1000;
    let t0 = Instant::now();
    for _ in 0..n { std::hint::black_box(rec.b.readout(t).unwrap()); }
    println!("own readout {:.2} us", t0.elapsed().as_secs_f64() * 1e6 / n as f64);
    let t0 = Instant::now();
    for _ in 0..n { std::hint::black_box(ctx.secondaries(rec.b.doll, t, ship).unwrap()); }
    println!("secondaries (moon) {:.2} us", t0.elapsed().as_secs_f64() * 1e6 / n as f64);
    let t0 = Instant::now();
    for _ in 0..n { std::hint::black_box(ctx.tide(rec.b.doll, t).unwrap()); }
    println!("tide {:.2} us", t0.elapsed().as_secs_f64() * 1e6 / n as f64);
    let t0 = Instant::now();
    for _ in 0..n { std::hint::black_box(emergent_universe::observe::root_state(&ctx, ship, t).unwrap()); }
    println!("root_state (the position cache after every event) {:.2} us", t0.elapsed().as_secs_f64() * 1e6 / n as f64);
    let t0 = Instant::now();
    for _ in 0..n { std::hint::black_box(p.u.rec(ship)); }
    println!("rec() clone {:.2} us", t0.elapsed().as_secs_f64() * 1e6 / n as f64);
    drop(ctx);
    // whole universe
    let t0 = Instant::now();
    let h = 30_000_000_000i64;
    p.u.settle(h);
    let s = p.u.stats;
    let ev = s.kicks + s.opens + s.boundaries;
    println!("whole universe over {h} ticks: {:.1} us per kick/open/boundary ({ev} items), ships {:.1} us per item", t0.elapsed().as_secs_f64() * 1e6 / ev as f64, s.cost_ns[2] as f64 / 1e3 / s.items[2].max(1) as f64);
}
