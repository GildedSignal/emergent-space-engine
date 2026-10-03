//! Lab bench (run 20261003-1030-autoresearch-dcec): ns per body-chronon for the CPU
//! chronon reference on the standard trapped gas, plus the canonical digests.
//! Usage: lab_bench n fill q vmax seed steps
use emergent_lattice::chronon::Chronon;
use emergent_lattice::worlds;
use emergent_lattice::Stepper;
use std::time::Instant;

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let n: u64 = a[1].parse().unwrap();
    let fill: f64 = a[2].parse().unwrap();
    let q: i64 = a[3].parse().unwrap();
    let vmax: i64 = a[4].parse().unwrap();
    let seed: u64 = a[5].parse().unwrap();
    let steps: usize = a[6].parse().unwrap();
    let mut c = Chronon::new(worlds::gas(n, fill, q, vmax, seed), false).unwrap();
    let t0 = Instant::now();
    for _ in 0..steps {
        c.step();
    }
    let dt = t0.elapsed();
    let (wd, ld) = c.outcome();
    let ns = dt.as_nanos() as f64 / steps as f64;
    println!("ns_per_chronon {:.0}", ns);
    println!("ns_per_body_chronon {:.3}", ns / n as f64);
    println!("world_digest {}", wd);
    println!("log_digest {}", ld);
    let m = c.metrics();
    println!("predicates {} ops {} fired {}", m.predicates, m.ops, m.fired);
}
