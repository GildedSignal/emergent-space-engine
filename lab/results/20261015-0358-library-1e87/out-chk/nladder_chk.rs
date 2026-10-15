//! Checker 1e87 bisect probe (evidence for check.md; build: cargo build --release -p emergent-universe --example nladder_chk).
//! The shipped loop's calls only (plane_extra, frame_to with budget, held_scans, rec), RSS printed from
//! inside the loop; optional `settle` arg reproduces the author's settle(i64::MAX) after the loop.
//! Arms flown: `10000 100 12 60000` (flat 54 MB, 12 waves); `10000 6000 12 1200` (bounded 159 MB, 13.7 s);
//! `10000 100 12 5400 settle` (loop flat 34 MB, then settle grows ~17 MB/s, never terminates).
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::{Budget, Config};
use std::time::{Duration, Instant};

fn rss_mb() -> f64 {
    std::fs::read_to_string("/proc/self/statm")
        .ok()
        .and_then(|s| s.split_whitespace().nth(1)?.parse::<u64>().ok())
        .map(|p| p as f64 * 4096.0 / 1e6)
        .unwrap_or(0.0)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let n: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(10000);
    let rtf: f64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(100.0);
    let budget_ms = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(12.0);
    let frames: usize = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(60000);
    let settle_too = args.get(5).map(|s| s == "settle").unwrap_or(false);
    let t0 = Instant::now();
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, n).unwrap();
    let bodies = p.u.n_bodies();
    println!("chk n={n} bodies={bodies} rtf={rtf} budget={budget_ms}ms build_rss={:.0}MB", rss_mb());
    let t_first = p.u.now;
    let mut over = 0usize;
    let mut max_ms = 0.0f64;
    for f in 0..frames {
        if t0.elapsed() > Duration::from_secs(80) {
            println!("truncated at frame {f}");
            break;
        }
        let start = Instant::now();
        let frame = p.u.frame_to(1.0 / 60.0, rtf, Budget { events: u64::MAX, until: Some(start + Duration::from_micros((budget_ms * 1e3) as u64)) }, i64::MAX);
        let ms = start.elapsed().as_secs_f64() * 1e3;
        over += (ms > budget_ms) as usize;
        max_ms = max_ms.max(ms);
        let _ = p.u.held_scans();
        let rec = p.u.rec(p.player);
        if f % 120 == 0 {
            println!("f={f} game_s={:.0} rss={:.0}MB over={over} max_ms={max_ms:.1} events={}", (p.u.now - t_first) as f64 / 6e4, rss_mb(), frame.events);
        }
        if !rec.alive {
            println!("player dead at {f}");
            break;
        }
    }
    println!("loop done at frame-check: rss={:.0}MB wall={:.1}s", rss_mb(), t0.elapsed().as_secs_f64());
    if settle_too {
        let ts = Instant::now();
        p.u.settle(i64::MAX);
        println!("after settle: rss={:.0}MB settle_s={:.1}", rss_mb(), ts.elapsed().as_secs_f64());
    }
    println!("digest {}", p.u.digest());
}
