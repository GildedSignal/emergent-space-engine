//! The stat-free twin of `scanpre` (1ab4): the identical flight with every instrument call
//! removed, so it builds against pristine sources. Flown against the patched build too, it
//! isolates the epoch bookkeeping's always-on cost: patched(scanpre0) − pristine(scanpre0)
//! is the per-flight price of the counters themselves (put/retire/prune bumps, per-doll
//! reg epochs, the per-capture near-list snapshot), with no timing reads anywhere.
//!
//! cargo run --release -p emergent-universe --example scanpre0 [-- <N> <coast|burn> [<wall s> [<rtf> [<budget ms>]]]]
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::thrust::word;
use emergent_universe::{Budget, Config};
use std::time::{Duration, Instant};

fn pct(sorted: &[f64], p: f64) -> f64 {
    sorted[(((sorted.len() - 1) as f64) * p).round() as usize]
}

fn main() {
    let t_start = Instant::now();
    let args: Vec<String> = std::env::args().collect();
    let n: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(30000);
    let flight = args.get(2).cloned().unwrap_or_else(|| "coast".into());
    let mut rows: Vec<f64> = Vec::new();
    let mut late_stats: Option<(emergent_universe::universe::Stats, i64)> = None;
    let seconds: f64 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(20.0);
    let rtf: f64 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(100.0);
    let budget_ms: f64 = args.get(5).and_then(|s| s.parse().ok()).unwrap_or(12.0);
    let frames = (seconds * 60.0) as usize;
    let t0 = Instant::now();
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, n).unwrap();
    let build = t0.elapsed().as_secs_f64();
    let bodies = p.u.n_bodies();
    let mut ran = 0usize;
    let burn = flight == "burn";
    for f in 0..frames {
        if t_start.elapsed() > Duration::from_secs(50) {
            break;
        }
        if f == 60 {
            if burn {
                let t = p.u.now;
                let _ = p.u.input(t, word(1, 8));
            }
            late_stats = Some((p.u.stats, p.u.now));
        }
        let start = Instant::now();
        let _frame = p.u.frame_to(1.0 / 60.0, rtf, Budget { events: u64::MAX, until: Some(start + Duration::from_micros((budget_ms * 1e3) as u64)) }, i64::MAX);
        if f >= 60 {
            rows.push(start.elapsed().as_secs_f64() * 1e3);
        }
        ran += 1;
        if !p.u.rec(p.player).alive {
            break;
        }
    }
    let mut ms = rows.clone();
    ms.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let over = rows.iter().filter(|m| **m > budget_ms).count();
    let (s0, t_first) = late_stats.expect("at least one late frame");
    let last = p.u.stats;
    let game_s = (p.u.now - t_first) as f64 * emergent_universe::view::TICK_SECONDS;
    let settle_to = p.u.now + (p.u.now - t_first).max(1);
    p.u.settle(settle_to);
    let digest = p.u.digest();
    println!(
        "scanarm0: n={n} bodies={bodies} flight={flight} rtf={rtf} frames={ran} build_s={build:.2} | engine ms p50 {:.3} p99 {:.3} max {:.3} over{budget_ms}ms {over} | game_s {game_s:.1} kicks {} events {} encounters {} | digest {digest} wall_s {:.1}",
        pct(&ms, 0.5), pct(&ms, 0.99), pct(&ms, 1.0),
        last.kicks - s0.kicks, last.events() - s0.events(),
        last.encounters - s0.encounters,
        t_start.elapsed().as_secs_f64(),
    );
}
