//! Canonical digest for the band seam: fly the same flight, then `settle` to the exact cut tick and
//! digest there (the shipped `scan_cap` digests at the presented tick, which the record knows wobbles
//! with wall schedule). Args identical to `scan_cap`; one line at the end.

use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra_band;
use emergent_universe::thrust::word;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};
use std::time::Instant;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let extra: usize = args[1].parse().unwrap();
    let level: u8 = args[2].parse().unwrap();
    let seed: u64 = args.get(3).map(|s| s.parse().unwrap()).unwrap_or(1);
    let cut: f64 = args.get(4).map(|s| s.parse().unwrap()).unwrap_or(16_000.0);
    let rtf: f64 = args.get(5).map(|s| s.parse().unwrap()).unwrap_or(100.0);
    let cap = std::env::var("ES_SCAN_STANDING").unwrap_or_else(|_| "off".into());
    let margin: i64 = std::env::var("ES_CANON_MARGIN").ok().and_then(|v| v.parse().ok()).unwrap_or(120);
    let (t0, mut p) = (Instant::now(), plane_extra_band(Config::default(), seed, Order::Sparse, 1, 48, extra).unwrap());
    println!(
        "built in {:.2}s: {} bodies, seed {seed}, L{level}, rtf {rtf}, cut {cut}, cap {cap}, margin {margin}",
        t0.elapsed().as_secs_f64(),
        p.u.n_bodies()
    );
    let cut_tick = (cut / TICK_SECONDS) as i64;
    let mut sent = false;
    let mut frames = 0u64;
    loop {
        if !sent && frames as f64 / 60.0 >= 1.0 {
            let _ = p.u.input(p.u.now, word(1, level));
            sent = true;
        }
        let start = Instant::now();
        let frame = p.u.frame_to(1.0 / 60.0, rtf, Budget { events: u64::MAX, until: Some(start + std::time::Duration::from_millis(12)) }, cut_tick);
        frames += 1;
        if frame.presented >= cut_tick - 2 {
            break;
        }
    }
    let t = Instant::now();
    p.u.settle(cut_tick);
    let settle_s = t.elapsed().as_secs_f64();
    let digest = p.u.digest();
    println!(
        "horizon-limited canonical at tick {cut_tick} (game {:.1}): digest {digest} (settle {settle_s:.2}s, held now {}, encounters {}, decisions {}, frames {frames})",
        cut_tick as f64 * TICK_SECONDS,
        p.u.held_scans(),
        p.u.stats.encounters,
        p.u.stats.decisions
    );
}
