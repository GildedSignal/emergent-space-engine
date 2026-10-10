//! Autoresearch bench (run 20261010-0920): wall ns per op of `EventCore` on fixed worlds.
//!
//! Behaviour constraint: world + log digests must be identical across code changes.
//! `--tune` (default) runs the tuning worlds; `--heldout` runs the held-out set once.
use emergent_lattice::law::{Response, Tick, World};
use emergent_lattice::Stepper;
use emergent_lattice::worlds;
use emergent_lattice_event::{crowded_axes, EventCore};
use std::time::Instant;

fn tune() -> Vec<(&'static str, World, Tick)> {
    vec![
        ("gas-dense", worlds::gas(20_000, 0.10, 1024, 128, 11), 512),
        ("gas-sparse", worlds::gas(20_000, 0.02, 1024, 128, 22), 512),
        ("crowded", crowded_axes(20_000, 1024, 33).0, crowded_axes(20_000, 1024, 33).1),
        ("random-pass", worlds::random(20_000, 64, 1024, 1, 44, Response::Pass), 2048),
    ]
}

fn heldout() -> Vec<(&'static str, World, Tick)> {
    vec![
        ("h-gas-mid", worlds::gas(40_000, 0.05, 1024, 64, 99), 768),
        ("h-mixed", worlds::mixed(8_192, 512, 77), 2048),
        ("h-crowded", crowded_axes(8_000, 1024, 88).0, crowded_axes(8_000, 1024, 88).1),
        ("h-gas-hot", worlds::gas(5_000, 0.20, 2048, 256, 123), 512),
    ]
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let run_heldout = args.iter().any(|a| a == "--heldout");
    let reps: usize = args
        .iter()
        .position(|a| a == "--reps")
        .and_then(|p| args.get(p + 1))
        .and_then(|v| v.parse().ok())
        .unwrap_or(3);
    let cases = if run_heldout { heldout() } else { tune() };
    let total_ns = 0u128;
    let total_ops = 0u128;
    for (name, world, horizon) in cases {
        let n = world.bodies.len();
        let mut times = Vec::new();
        let mut digest = (String::new(), String::new());
        let mut metrics = None;
        for _ in 0..reps {
            let mut core = EventCore::new(world.clone(), false).expect("world valid");
            let t0 = Instant::now();
            core.run_to(horizon);
            times.push(t0.elapsed().as_nanos());
            digest = core.outcome();
            metrics = Some(core.metrics().clone());
        }
        times.sort();
        let med = times[times.len() / 2];
        let m = metrics.unwrap();
        let ns_per_op = med as f64 / m.ops as f64;
        println!(
            "{name}\tn={n}\th={horizon}\tms={:.2}\tops={}\tfired={}\tsched={}\tns/op={:.3}\tops/fired={:.1}\t{}:{}",
            med as f64 / 1e6,
            m.ops,
            m.fired,
            m.scheduled,
            ns_per_op,
            m.ops as f64 / m.fired as f64,
            digest.0,
            digest.1,
        );
    }
    println!("TOTAL\tmed_ns={total_ns}\tops={total_ops}\tns/op={:.4}", total_ns as f64 / total_ops as f64);
}
