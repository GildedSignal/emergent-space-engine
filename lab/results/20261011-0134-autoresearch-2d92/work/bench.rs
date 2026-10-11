//! Autoresearch bench: the event core's cost per event on the contact-heavy track,
//! with the full metric breakdown and the outcome digests (identity must hold).
//!
//! cargo run -p emergent-lattice-event --release --offline --example bench -- [tune|heldout|all]
use emergent_lattice::{law::{Tick, World}, worlds, Stepper};
use emergent_lattice_event::EventCore;
use std::time::Instant;

fn row(tag: &str, w: &World, horizon: Tick) {
    let n = w.bodies.len() as f64;
    let t = Instant::now();
    let mut e = EventCore::new(w.clone(), false).unwrap();
    e.run_to(horizon);
    let s = t.elapsed().as_secs_f64();
    let m = e.metrics().clone();
    let (d1, d2) = e.outcome();
    println!(
        "{tag:>14} n={n:>6} fired={fired:>7} ops={ops:>9} opf={opf:>7.1} \
         ns/fired={nsf:>8.0} ns/body={nsb:>7.0} pred/ops={po:.3} \
         sched/f={sf:>6.1} inval/sched={is:.3} moves={mv} digest={d1:>16},{d2:>10}",
        fired = m.fired,
        ops = m.ops,
        opf = m.ops as f64 / m.fired.max(1) as f64,
        nsf = s * 1e9 / m.fired.max(1) as f64,
        nsb = s * 1e9 / n,
        po = m.predicates as f64 / m.ops as f64,
        sf = m.scheduled as f64 / m.fired.max(1) as f64,
        is = m.invalidated as f64 / m.scheduled.max(1) as f64,
        mv = m.cell_moves,
    );
    println!("      {d1} {d2}");
}

fn main() {
    let which = std::env::args().nth(1).unwrap_or_else(|| "tune".into());
    let reps: usize = std::env::args().nth(2).and_then(|a| a.parse().ok()).unwrap_or(1);
    for _ in 0..reps {
    run(&which);
    }
}

fn run(which: &str) {
    if which == "tune" || which == "all" {
        for n in [256u64, 1024, 4096] {
            row("gas", &worlds::gas(n, 0.1, 1024, 256, 1), 1024);
        }
    }
    if which == "heldout" || which == "all" {
        row("gas-held", &worlds::gas(64, 0.1, 1024, 256, 1), 1024);
        row("gas-held", &worlds::gas(16384, 0.1, 1024, 256, 1), 1024);
        row("gas-hi-fill", &worlds::gas(1024, 0.3, 1024, 256, 1), 1024);
        row("random", &worlds::random(4096, 1_000_000, 1024, 1, 1, emergent_lattice::law::Response::Pass), 4096);
        let (w, h) = emergent_lattice_event::crowded_axes(4096, 1024, 1);
        row("crowded", &w, h);
    }
}
