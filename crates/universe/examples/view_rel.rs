// What the view's gather costs on relativistic content (the 0.9c stream of B15's scene is the content the game exists
// for): a player and emitters that are bare tubes (no force, so no events) moving at speed β in the star's doll, in
// every geometry that sets the arrival rate dt_e/dT = 1/(1 + n·β): across the line of sight, toward the observer,
// away from it, and the same with the observer itself at 0.9c. Every frame is gathered cold (a search from the
// present) and from the memo (the last frame's crossing); the views are asserted equal (a cache changes how a
// crossing is found, never what it is) and the readouts per emitter and the wall time of the memo's gather are
// reported. `view_rel [FRAMES] [RTF]`.
use emergent_universe::scenario::{stream, Stream};
use emergent_universe::view::{gather, gather_cached, ViewCache, TICK_SECONDS};
use std::time::Instant;

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let frames: usize = args.first().map(|s| s.parse().unwrap()).unwrap_or(100);
    let rtf: f64 = args.get(1).map(|s| s.parse().unwrap()).unwrap_or(100.0);
    let frame = (rtf / 60.0 / TICK_SECONDS) as i64;
    println!("rtf {rtf}: {frame} ticks per 60 Hz frame, {frames} frames, 24 emitters per case at 1e6 ticks");
    println!("{:<34} {:>9} {:>9} {:>11} {:>11}", "case", "reads/em", "max/frame", "cold us", "memo us");
    use Stream::*;
    let cases: [(&str, f64, f64, Stream); 9] = [
        ("static: slow (1e-4) across", 0.0, 1e-4, Across),
        ("static: 0.9c across", 0.0, 0.9, Across),
        ("static: 0.9c toward", 0.0, 0.9, Toward),
        ("static: 0.9c away", 0.0, 0.9, Away),
        ("static: 0.99c across", 0.0, 0.99, Across),
        ("static: 0.99c toward", 0.0, 0.99, Toward),
        ("observer 0.9c: 0.9c across", 0.9, 0.9, Across),
        ("observer 0.9c: 0.9c toward", 0.9, 0.9, Toward),
        ("observer 0.9c: 0.9c away", 0.9, 0.9, Away),
    ];
    for (name, bo, b, kind) in cases {
        let (mut u, ids, _p) = stream(bo, b, kind, 24, 1.0e6, 1_200_000_000).unwrap();
        let mut cache = ViewCache::default();
        let (mut reads, mut worst, mut cold_s, mut memo_s, mut n_frames, mut seen_ok) = (0u64, 0u64, 0.0f64, 0.0f64, 0, 0usize);
        let start = 1_200_000_000i64; // the observer is at the middle of the cloud then (see `stream`)
        for f in 0..frames {
            let t = start + f as i64 * frame;
            u.settle(t);
            u.now = t;
            let t0 = Instant::now();
            let cold = gather(&u, &[]);
            let c = t0.elapsed().as_secs_f64();
            let t0 = Instant::now();
            let warm = gather_cached(&u, &[], &mut cache);
            let w = t0.elapsed().as_secs_f64();
            let (Some(cold), Some(warm)) = (cold, warm) else { continue };
            assert_eq!(cold, warm, "{name}: a cache changed the view at frame {f}");
            if f >= 3 {
                let em = cold.seen.iter().filter(|s| s.id < u.n_bodies()).count();
                seen_ok = em.max(seen_ok);
                reads += cache.readouts;
                worst = worst.max(cache.readouts);
                cold_s += c;
                memo_s += w;
                n_frames += 1;
                let _ = &ids;
            }
        }
        let em = seen_ok.max(1) as f64;
        println!("{:<34} {:>9.2} {:>9} {:>11.1} {:>11.1}   ({} emitters seen)", name, reads as f64 / n_frames.max(1) as f64 / em, worst, cold_s / n_frames.max(1) as f64 * 1e6, memo_s / n_frames.max(1) as f64 * 1e6, seen_ok);
    }
}
