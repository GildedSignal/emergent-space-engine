//! Lab run 20261017-1447-components-5eb2 (lens: first principles, one component).
//! The belt kick, priced from the inside on shipped code (feature `prof` adds the instrument):
//! the wall-clock decomposition of `kick_clock` (secondaries rebuild, fit, its nested readouts)
//! and the `(doll, tick)` multiplicity of `Ctx::secondaries` — the redundancy a shared field
//! read would delete, which decides read-stream's open direction 1. Then, on the flown state:
//! `bind_surface` on real belt states (the refit at its true inputs) and `Orbit::compile` on
//! the same bodies' keys (the quadrature alone). Linux-safe (no proc_pid_rusage).
//!
//! cargo run --release -p emergent-universe --features prof --example refit_probe [-- <N> <wall s> <rtf>]
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};
use std::hint::black_box;
use std::time::{Duration, Instant};

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let n: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(30_000);
    let seconds: f64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(30.0);
    let rtf: f64 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(600.0);
    let budget_ms = 12.0;
    let frames = (seconds * 60.0) as usize;
    let t_start = Instant::now();
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, n).unwrap();
    let bodies = p.u.n_bodies();
    let sources0 = p.u.sources[0].len();
    println!("N={n} ({bodies} bodies, doll 0 sources {sources0}), rtf {rtf}, {seconds} s wall, budget {budget_ms} ms");
    let mut stage_ns = [0u64; emergent_universe::prof::N];
    let mut stage_calls = [0u64; emergent_universe::prof::N];
    let mut census = (0usize, 0u64, [0u64; 5]);
    let mut events = 0u64;
    for f in 0..frames {
        if t_start.elapsed() > Duration::from_secs(52) {
            println!("truncated at frame {f}");
            break;
        }
        if f == 60 {
            let _ = emergent_universe::prof::take();
            let _ = emergent_universe::prof::secstat::take();
        }
        let start = Instant::now();
        let frame = p.u.frame_to(1.0 / 60.0, rtf, Budget { events: u64::MAX, until: Some(start + Duration::from_micros((budget_ms * 1e3) as u64)) }, i64::MAX);
        events += frame.events;
        let (ns, calls) = emergent_universe::prof::take();
        let c = emergent_universe::prof::secstat::take();
        if f >= 60 {
            for k in 0..emergent_universe::prof::N {
                stage_ns[k] += ns[k];
                stage_calls[k] += calls[k];
            }
            census.0 += c.0;
            census.1 += c.1;
            for i in 0..5 {
                census.2[i] += c.2[i];
            }
        }
    }
    let game_s = p.u.now as f64 * TICK_SECONDS;
    println!("game {game_s:.0} s, events {events}");
    println!("stages (µs per frame, calls per frame, ns per call):");
    for k in 0..emergent_universe::prof::N {
        if stage_calls[k] > 0 {
            println!("  {:<42} {:>9.1} {:>8.2} {:>10.0}", emergent_universe::prof::NAMES[k], stage_ns[k] as f64 / 1e3 / (frames as f64 - 60.0).max(1.0), stage_calls[k] as f64 / (frames as f64 - 60.0).max(1.0), stage_ns[k] as f64 / stage_calls[k] as f64);
        }
    }
    let (distinct, total, at) = census;
    println!(
        "secondaries census: {total} calls at {} distinct (doll, tick) keys; calls at multiplicity >=2 {}/>=4 {}/>=8 {}/>=16 {}/>=64 {}: {:.1}% of all calls share a key",
        distinct, at[0], at[1], at[2], at[3], at[4], if total > 0 { at[0] as f64 * 100.0 / total as f64 } else { 0.0 }
    );
    // The refit at its true inputs: real belt states, the binding the next rebind would fit.
    let now = p.u.now;
    let mut belt = Vec::new();
    for i in 0..bodies {
        let r = p.u.rec(i);
        if r.b.doll == 0 && r.alive && belt.len() < 512 {
            if let Ok(st) = r.b.readout(now) {
                belt.push((i, st, r.b.clock_exp, r.b.entry.clone()));
            }
        }
        if belt.len() >= 512 {
            break;
        }
    }
    println!("belt states captured: {}", belt.len());
    let mut ns = Vec::new();
    for _ in 0..3 {
        let t = Instant::now();
        for (_, st, clock_exp, entry) in belt.iter() {
            let _ = black_box(emergent_universe::bind::bind(black_box(*st), black_box(now), *clock_exp, None, entry.unit)).unwrap();
        }
        ns.push(t.elapsed().as_nanos() as f64 / belt.len() as f64);
    }
    ns.sort_by(|a, b| a.partial_cmp(b).unwrap());
    println!("bind (Rebinding::from_state, edge None) on real belt states: {:.0} ns/call median", ns[1]);
}
