//! Galaxy-shaped layout (journal H0173): ship clusters on two log-spiral arms over a disc of
//! radius 2^span light-chronons, Pareto cluster sizes, ~10% fill inside clusters, one 0.9c
//! stream of 256 aimed at the largest cluster, Q = 256, relativistic law. The world generator
//! is the probe's (artifacts/evidence/quanta-probes-20260926/galaxy.rs), unchanged, so numbers
//! stay comparable; this runs the event core only and prints its cell sizing and cost.
//!
//! cargo run -p emergent-lattice-event --release --example galaxy -- 16384 16 <span> 256 1
//! cargo run -p emergent-lattice-event --release --example galaxy -- 262144 64 30 1024 1
//! cargo run -p emergent-lattice-event --release --example galaxy -- gas [n] [horizon]
use emergent_lattice::{law::Response, worlds, worlds::Rng, Body, Law, Stepper, World};
use emergent_lattice_event::EventCore;
use std::time::Instant;

fn galaxy(total: usize, clusters: usize, span: u32, dscale: f64) -> World {
    let q = 256i64;
    let mut rng = Rng(12345);
    let u = |r: &mut Rng| (r.next() >> 11) as f64 / (1u64 << 53) as f64;
    // Pareto(α=1.2) sizes normalised to `total`.
    let raw: Vec<f64> = (0..clusters).map(|_| (1.0 - u(&mut rng)).powf(-1.0 / 1.2)).collect();
    let s: f64 = raw.iter().sum();
    let mut sizes: Vec<usize> = raw.iter().map(|x| ((x / s) * total as f64).max(16.0) as usize).collect();
    sizes.sort_unstable_by(|a, b| b.cmp(a));
    let rdisc = (1i64 << span) as f64;
    let mut bodies: Vec<Body> = Vec::new();
    let mut id = 1u64;
    let mut centres = Vec::new();
    for (i, &n) in sizes.iter().enumerate() {
        let r = rdisc * (0.05 + 0.9 * u(&mut rng));
        let th = (i % 2) as f64 * std::f64::consts::PI + (r / rdisc * 20.0).ln() / 0.25_f64.tan() + 0.3 * (u(&mut rng) - 0.5);
        let c = [r * th.cos(), r * th.sin()];
        let rc = (n as f64 * 30.0 / std::f64::consts::PI).sqrt(); // ~10% fill with radius 1
        let drift = [(u(&mut rng) - 0.5) * 0.5 * q as f64 * dscale, (u(&mut rng) - 0.5) * 0.5 * q as f64 * dscale];
        centres.push((c, rc));
        for _ in 0..n {
            let (rr, ph) = (rc * u(&mut rng).sqrt(), u(&mut rng) * std::f64::consts::TAU);
            let x = [((c[0] + rr * ph.cos()) * q as f64) as i64, ((c[1] + rr * ph.sin()) * q as f64) as i64];
            let k = [(drift[0] + (u(&mut rng) - 0.5) * q as f64 / 8.0) as i64, (drift[1] + (u(&mut rng) - 0.5) * q as f64 / 8.0) as i64];
            bodies.push(Body::new(id, x, k, 1, q, Response::Bounce));
            id += 1;
        }
    }
    // Near-c stream: 256 ships at 0.9c toward the largest cluster, starting 600 light-chronons out.
    let (c0, rc0) = centres[0];
    for j in 0..256 {
        let x = [((c0[0] - rc0 - 600.0) * q as f64) as i64 - (j % 16) * 4 * q, ((c0[1] + (j / 16 - 8) as f64 * 6.0) * q as f64) as i64];
        bodies.push(Body::new(id, x, [(0.9 * q as f64) as i64, 0], 1, q, Response::Bounce));
        id += 1;
    }
    // Overlapping genesis pairs are dropped (keep the first).
    bodies.sort_by_key(|b| (b.x[0] >> 12, b.x[1] >> 12));
    let n0 = bodies.len();
    let mut grid: std::collections::HashMap<(i64, i64), Vec<[i64; 2]>> = Default::default();
    bodies.retain(|b| {
        let key = (b.x[0].div_euclid(4 * q), b.x[1].div_euclid(4 * q));
        for dx in -1..=1 {
            for dy in -1..=1 {
                if let Some(v) = grid.get(&(key.0 + dx, key.1 + dy)) {
                    if v.iter().any(|p| {
                        let d = [(p[0] - b.x[0]) as i128, (p[1] - b.x[1]) as i128];
                        d[0] * d[0] + d[1] * d[1] <= 4 * q as i128 * q as i128
                    }) {
                        return false;
                    }
                }
            }
        }
        grid.entry(key).or_default().push(b.x);
        true
    });
    bodies.sort_by_key(|b| b.id);
    let w = World::new(q, None, bodies).expect("ranges").with_law(Law::Relativistic).unwrap();
    let maxc = w.bodies.iter().map(|b| b.x[0].abs().max(b.x[1].abs())).max().unwrap();
    println!(
        "galaxy: {} ships ({} dropped as overlapping) in {clusters} clusters (largest {}, smallest {}), disc radius 2^{span} light-chronons, max |x| = 2^{:.1} units of 1/{q}",
        w.bodies.len(),
        n0 - w.bodies.len(),
        sizes[0],
        sizes[clusters - 1],
        (maxc as f64).log2()
    );
    w
}

fn run(w: World, horizon: i64) {
    let q = w.q as f64;
    let t = Instant::now();
    let mut e = EventCore::new(w, false).unwrap();
    let setup = t.elapsed().as_secs_f64();
    // Genesis indexing happens in the first advance: report the side it chose.
    e.advance(1, u64::MAX);
    let genesis = e.cell_side();
    e.run_to(horizon);
    let run = t.elapsed().as_secs_f64() - setup;
    let m = e.metrics().clone();
    let fp = e.footprint();
    let (wd, ld) = e.outcome();
    println!(
        "event: setup {setup:.2} s, run {run:.2} s to {horizon}, contacts {}, genesis cell {:.2} light-chronons, final {:.2}, rebuilds {}, ops {}, predicates {}, max unit ops {}, cells cap {}",
        e.log().contacts,
        genesis as f64 / q,
        e.cell_side() as f64 / q,
        e.rebuilds(),
        m.ops,
        m.predicates,
        m.max_unit_ops,
        fp.cells_cap
    );
    println!("outcome world {wd} log {ld}");
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    if a.get(1).map(String::as_str) == Some("gas") {
        let n: u64 = a.get(2).and_then(|s| s.parse().ok()).unwrap_or(65_536);
        let horizon: i64 = a.get(3).and_then(|s| s.parse().ok()).unwrap_or(1024);
        println!("gas: worlds::gas({n}, 0.1, 1024, 256, 1), horizon {horizon}");
        run(worlds::gas(n, 0.1, 1024, 256, 1), horizon);
        return;
    }
    let total: usize = a.get(1).and_then(|s| s.parse().ok()).unwrap_or(262_144);
    let clusters: usize = a.get(2).and_then(|s| s.parse().ok()).unwrap_or(64);
    let span: u32 = a.get(3).and_then(|s| s.parse().ok()).unwrap_or(30);
    let horizon: i64 = a.get(4).and_then(|s| s.parse().ok()).unwrap_or(1024);
    let dscale: f64 = a.get(5).and_then(|s| s.parse().ok()).unwrap_or(1.0);
    let w = galaxy(total, clusters, span, dscale);
    run(w, horizon);
}
