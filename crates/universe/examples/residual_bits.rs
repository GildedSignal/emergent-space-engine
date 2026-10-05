// What the binding's residual (4 x i128: the exact state less the turned tube, per component) has to absorb: the histogram of the bit
// lengths of its components over every binding of a plane run, positions and velocities apart. `residual_bits [TICKS] [SEED]`.
use emergent_universe::fleet::Order;
use emergent_universe::scenario::{plane, restricted};
use emergent_universe::Config;
use std::collections::BTreeSet;

fn bits(x: i128) -> usize {
    128 - x.unsigned_abs().leading_zeros() as usize
}

fn report(name: &str, mut pos: Vec<usize>, mut vel: Vec<usize>) {
    for (what, v) in [("position", &mut pos), ("velocity", &mut vel)] {
        v.sort();
        let n = v.len().max(1);
        let q = |p: f64| v[((n as f64 * p) as usize).min(n - 1)];
        let mut hist = [0usize; 12];
        for &b in v.iter() {
            hist[(b / 8).min(11)] += 1;
        }
        println!("{name} {what:<8}: {} components; bit length median {}, p90 {}, p99 {}, max {}; share by octet of bits {:?}", v.len(), q(0.5), q(0.9), q(0.99), v.last().copied().unwrap_or(0), hist.iter().enumerate().filter(|h| *h.1 > 0).map(|(i, c)| format!("{}-{}:{:.1}%", i * 8, i * 8 + 7, 100.0 * *c as f64 / n as f64)).collect::<Vec<_>>());
    }
}

fn main() {
    let ticks: i64 = std::env::args().nth(1).map(|s| s.parse().unwrap()).unwrap_or(2_000_000_000);
    let seed: u64 = std::env::args().nth(2).map(|s| s.parse().unwrap()).unwrap_or(1);
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, 24).unwrap();
    p.u.settle(ticks);
    let (mut pos, mut vel, mut total) = (Vec::new(), Vec::new(), 0usize);
    for i in 0..p.u.n_bodies() {
        let mut seen = BTreeSet::new();
        let mut take = |b: &emergent_universe::bind::Binding| {
            if seen.insert(b.event_time) {
                total += 1;
                for c in 0..2 {
                    pos.push(bits(b.residual.position[c]));
                    vel.push(bits(b.residual.velocity[c]));
                }
            }
        };
        take(&p.u.rec(i).b);
        for k in 0..400 {
            if let Some(b) = p.u.bodies().binding_at(i, ticks / 400 * k) {
                take(&b);
            }
        }
    }
    println!("plane seed {seed}, {ticks} ticks: {total} bindings, {} kicks, {} handoffs", p.u.stats.kicks, p.u.stats.handoffs);
    report("plane", pos, vel);
    // The restricted problem: ships that pass the planet (handoffs).
    let sep = 527_000_000i64;
    let hill = sep as f64 * (2f64.powi(-10) / 3.0).cbrt();
    let ships: Vec<(i64, u32)> = (0..12).map(|i| ((sep as f64 + if i % 2 == 0 { 1.0 } else { -1.0 } * hill * (1.5 + 0.1 * i as f64)) as i64, (i as u32).wrapping_mul(0x9E37_79B9))).collect();
    let mut w = restricted(-10, sep, 49_000, &ships, 1).unwrap();
    let period = 2.0 * std::f64::consts::PI / ((1.0 + 2f64.powi(-10)).sqrt() / (sep as f64).powf(1.5));
    let end = (20.0 * period) as i64;
    w.u.settle(end);
    let (mut pos, mut vel, mut total) = (Vec::new(), Vec::new(), 0usize);
    for &i in &w.ships {
        let mut seen = BTreeSet::new();
        for k in 0..2000 {
            if let Some(b) = w.u.bodies().binding_at(i, end / 2000 * k) {
                if seen.insert(b.event_time) {
                    total += 1;
                    for c in 0..2 {
                        pos.push(bits(b.residual.position[c]));
                        vel.push(bits(b.residual.velocity[c]));
                    }
                }
            }
        }
    }
    println!("restricted, 12 ships, 20 planet periods: {total} bindings, {} kicks, {} handoffs", w.u.stats.kicks, w.u.stats.handoffs);
    report("restricted", pos, vel);
}
