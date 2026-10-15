//! The lazy entry seam: `ES_LAZY` demotes settled bindings to their re-mintable key (the compiled
//! orbit is a cache). The certificate is digest identity at a canonical cut (`frame_to` limited to
//! the cut, `settle`, `digest`) on the ladder scene, control (seam off, shipped verbatim) versus
//! seam on, past the belt's first-kick wave.
//!
//! cargo run --release -p emergent-universe --example lazyfly [-- <N> <seed> <coast|burn> <game seconds> [<rtf>]]
use emergent_universe::bind::{DEMOTIONS, PROMOTIONS};
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::thrust::word;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};
use std::time::Instant;

fn hwm() -> u64 {
    std::fs::read_to_string("/proc/self/status")
        .ok()
        .and_then(|s| {
            s.lines()
                .find(|l| l.starts_with("VmHWM:"))
                .and_then(|l| l.split_whitespace().nth(1).and_then(|v| v.parse().ok()))
        })
        .unwrap_or(0)
        * 1024
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let n: usize = a.get(1).and_then(|s| s.parse().ok()).unwrap_or(10_000);
    let seed: u64 = a.get(2).and_then(|s| s.parse().ok()).unwrap_or(1);
    let burn = a.get(3).map_or(false, |s| s == "burn");
    let game_s: f64 = a.get(4).and_then(|s| s.parse().ok()).unwrap_or(16_000.0);
    let rtf: f64 = a.get(5).and_then(|s| s.parse().ok()).unwrap_or(100.0);
    let t0 = Instant::now();
    let mut p = plane_extra(Config::default(), seed, Order::Sparse, 1, 48, n).unwrap();
    let build = t0.elapsed().as_secs_f64();
    let cut = p.u.now + (game_s / TICK_SECONDS) as i64;
    if burn {
        let t = (1.0 * rtf / TICK_SECONDS) as i64;
        p.u.schedule(t, word(1, 8)).unwrap();
    }
    let t1 = Instant::now();
    let mut frames = 0u64;
    while p.u.now < cut {
        p.u.frame_to(1.0 / 60.0, rtf, Budget::unlimited(), cut);
        frames += 1;
        if frames > 2_000_000 {
            break;
        }
    }
    let reached = p.u.now;
    p.u.settle(cut);
    let digest = p.u.digest();
    let (dem, pro) = (
        DEMOTIONS.load(std::sync::atomic::Ordering::Relaxed),
        PROMOTIONS.load(std::sync::atomic::Ordering::Relaxed),
    );
    let bpb = p.u.bytes_per_body();
    println!(
        "lazyfly N={n} seed={seed} {} game_s={game_s:.0} cut_reached={reached} build={build:.2}s fly={:.1}s frames={frames} digest={digest} kicks={} opens={} boundaries={} encounters={} contacts={} bpb={bpb} demotions={dem} promotions={pro} per_dem={:.1} rss={:.0}MB",
        if burn { "burn" } else { "coast" },
        t1.elapsed().as_secs_f64(),
        p.u.stats.kicks,
        p.u.stats.opens,
        p.u.stats.boundaries,
        p.u.stats.encounters,
        p.u.contacts,
        if dem > 0 { pro as f64 / dem as f64 } else { 0.0 },
        hwm() as f64 / 1e6,
    );
}
