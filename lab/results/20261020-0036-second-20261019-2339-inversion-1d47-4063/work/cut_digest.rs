//! The canonical-cut digest at the ladder's burn rungs (the checker's `check_cut` recipe, on 1d47's arms):
//! the plane with N more ships, the burn of `nladder` (forward L8 from 1 s of wall, a decision scheduled at
//! its canonical tick), flown at rtf 1000 to a cut past the first kick wave with `frame_to(limit = cut)`
//! — nothing resolves past the cut — then `settle(cut)` and one digest. The shipped contract
//! (universe.rs, `frame_to`): a digest taken after `settle(limit)` is the same whatever the frames were.
//! Arms come from the environment (the tree's patch): ES_ROOT_SHIPS_TO_QUEUE (1d47's gate),
//! ES_ROOT_SHIPS_REACH=<ticks> (the reach-gated pull); no variable = shipped. ES_FIX_PROBE adds the scan
//! counts. `no-flight` skips the frames entirely (settle from the schedule alone: the law's own order).
//!
//! cargo run --release -p emergent-universe --example cut_digest -- <N> [cut_game_s=17000] [unl|<ms>|noflight] [threads=1]
use emergent_universe::encounter::scan_probe_counts;
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::thrust::word;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};

fn main() {
    let t0 = std::time::Instant::now();
    let args: Vec<String> = std::env::args().collect();
    let n: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(100_000);
    let cut_s: f64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(17_000.0);
    let sched = args.get(3).cloned().unwrap_or_else(|| "12".into());
    let threads: usize = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(1);
    let rtf = 1000.0;
    let cut = (cut_s / TICK_SECONDS) as i64;
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, threads, 48, n).unwrap();
    let (mut frames, mut dolls): (u64, Vec<(u64, u16)>) = (0, Vec::new());
    // The burn's decision at its canonical tick (nladder takes it at the first second of wall).
    p.u.schedule((1.0 * rtf / TICK_SECONDS) as i64, word(1, 8)).unwrap();
    if sched != "noflight" {
        let ms: f64 = sched.parse().unwrap_or(12.0);
        let mut guard = 0u64;
        loop {
            if p.u.now >= cut || guard > 400_000 {
                break;
            }
            // A fresh wall deadline per frame, as nladder gives one (unlimited: no wall at all).
            let until = if sched == "unl" { None } else { Some(std::time::Instant::now() + std::time::Duration::from_micros((ms * 1e3) as u64)) };
            let _ = p.u.frame_to(1.0 / 60.0, rtf, Budget { events: u64::MAX, until }, cut);
            frames += 1;
            guard += 1;
            let doll = p.u.rec(p.player).b.doll;
            if dolls.last().map(|d| d.1) != Some(doll) {
                dolls.push((frames, doll));
            }
        }
    }
    p.u.settle(cut);
    let (scans, cands, stale, stale_max, s_enc, s_ratio, s_age) = scan_probe_counts();
    println!(
        "cut: n={n} cut_game_s={cut_s:.0} sched={sched} threads={threads} frames={frames} digest {} kicks {} encounters {} contacts {} | probe: scans {scans} cands {cands} stale {stale} (max {stale_max}) stale_enc {s_enc} (max ratio {}.{:03} of the window, max age {s_age} ticks) | dolls {dolls:?} [{:.1} s]",
        p.u.digest(),
        p.u.stats.kicks,
        p.u.stats.encounters,
        p.u.contacts,
        s_ratio / 1000,
        s_ratio % 1000,
        t0.elapsed().as_secs_f64()
    );
    if std::env::var_os("ES_DUMP_ENC").is_some() {
        let mut s = String::new();
        for e in &p.u.enc_log {
            s.push_str(&format!("{} {} {} {}\n", e.a, e.b, e.t, e.contact as u8));
        }
        std::fs::write(format!("enc_{n}_{sched}_{}.log", std::env::var("ES_DUMP_TAG").unwrap_or_default()), s).ok();
    }
}
