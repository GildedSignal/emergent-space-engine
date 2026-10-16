//! Performance evidence for the event core: wall time, cost per fired event and useful-work
//! ratio across world sizes, against the chronon reference where it finishes quickly.
//!
//! cargo run -p emergent-lattice-event --release --offline --example scaling -- [gas|random|crowded]...
use emergent_lattice::{
    chronon::Chronon,
    law::{Response, Tick, World},
    worlds, Stepper,
};
use emergent_lattice_event::{crowded_axes, EventCore};
use std::time::Instant;

fn row(track: &str, w: &World, horizon: Tick, chronon: bool) {
    let n = w.bodies.len() as f64;
    let t = Instant::now();
    let mut e = EventCore::new(w.clone(), false).unwrap();
    e.run_to(horizon);
    let es = t.elapsed().as_secs_f64();
    let m = e.metrics().clone();
    let (cs, same) = if chronon {
        let t = Instant::now();
        let mut c = Chronon::new(w.clone(), false).unwrap();
        c.run_to(horizon);
        (format!("{:.3}", t.elapsed().as_secs_f64()), if c.outcome() == e.outcome() { "yes" } else { "NO" })
    } else {
        ("-".into(), "-")
    };
    let per_fired = if m.fired > 0 { format!("{:.1}", m.ops as f64 / m.fired as f64) } else { "-".into() };
    println!(
        "| {track} | {} | {horizon} | {} | {} | {per_fired} | {:.1} | {:.3} | {es:.3} | {cs} | {same} | {:.1} | {} | {} | {:.2} | {} |",
        w.bodies.len(),
        m.fired,
        m.ops,
        m.ops as f64 / n,
        m.predicates as f64 / m.ops as f64,
        e.cell_side() as f64 / w.q as f64,
        e.rebuilds(),
        m.cell_moves,
        m.invalidated as f64 / m.scheduled.max(1) as f64,
        e.classes(),
    );
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let on = |k: &str| args.is_empty() || args.iter().any(|a| a == k);
    println!("| track | n | horizon | fired | ops | ops/fired | ops/body | pred/ops | event s | chronon s | equal | cell (units) | rebuilds | cell moves | superseded/scheduled | classes |");
    println!("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|");
    if on("gas") {
        for n in [64u64, 256, 1024, 4096, 16384] {
            row("gas fill 0.1", &worlds::gas(n, 0.1, 1024, 256, 1), 1024, n <= 4096);
        }
    }
    if on("random") {
        for n in [256u64, 1024, 4096, 16384, 65536, 262144] {
            row("random Pass", &worlds::random(n, 1_000_000, 1024, 1, 1, Response::Pass), 4096, n <= 4096);
        }
    }
    if on("crowded") {
        for n in [256u64, 4096, 65536] {
            let (w, horizon) = crowded_axes(n, 1024, 1);
            row("crowded axes", &w, horizon, n <= 256);
        }
    }
}
