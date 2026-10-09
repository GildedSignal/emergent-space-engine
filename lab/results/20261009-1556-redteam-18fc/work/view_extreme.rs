// What the view's gather does at the closing speeds the design's worst case names (bottleneck 5: a near-c
// missile; the queue's "γ to 10⁶"): emitters toward the observer at β up to 0.99999, and the mutual case
// (observer 0.9c × emitter 0.9999c, closing at 0.999994). `view_rel` stops at 0.99 toward; from 0.9999 up,
// the arrival rate 1/(1−β) meets and passes the gather's slope clamp (1e4 in `ViewCache::put`), and the
// crossing tick advances by frame/(1−β) per frame. Cold and memo views are compared per emitter (counted,
// not asserted), drops are counted against the emitter list, and readouts per emitter per frame reported.
// `view_extreme [RTF] [FRAMES]`.
use emergent_universe::scenario::{stream, Stream};
use emergent_universe::view::{gather, gather_cached, ViewCache, TICK_SECONDS};

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let rtf: f64 = args.first().map(|s| s.parse().unwrap()).unwrap_or(1.0);
    let frames: usize = args.get(1).map(|s| s.parse().unwrap()).unwrap_or(600);
    let frame = (rtf / 60.0 / TICK_SECONDS) as i64;
    println!("rtf {rtf}: {frame} ticks per 60 Hz frame, {frames} frames, 24 emitters at 1e6 ticks");
    println!("{:<30} {:>8} {:>8} {:>6} {:>6} {:>6}", "case", "reads/em", "max/fr", "drops", "disagr", "seen");
    use Stream::*;
    let cases: [(&str, f64, f64, Stream); 8] = [
        ("control: slow across", 0.0, 1e-4, Across),
        ("control: 0.9c across", 0.0, 0.9, Across),
        ("0.9c toward (view_rel)", 0.0, 0.9, Toward),
        ("0.999c toward", 0.0, 0.999, Toward),
        ("0.9999c toward", 0.0, 0.9999, Toward),
        ("0.99995c toward", 0.0, 0.99995, Toward),
        ("0.99999c toward", 0.0, 0.99999, Toward),
        ("obs 0.9c x 0.9999c toward", 0.9, 0.9999, Toward),
    ];
    for (name, bo, b, kind) in cases {
        let (mut u, ids, _p) = stream(bo, b, kind, 24, 1.0e6, 1_200_000_000).unwrap();
        let mut cache = ViewCache::default();
        let (mut reads, mut worst, mut drops, mut dis, mut seen_ok) = (0u64, 0u64, 0u64, 0u64, 0usize);
        let start = 1_200_000_000i64;
        let mut n_frames = 0u64;
        for f in 0..frames {
            let t = start + f as i64 * frame;
            u.settle(t);
            u.now = t;
            let cold = gather(&u, &[]);
            let warm = gather_cached(&u, &[], &mut cache);
            let (Some(cold), Some(warm)) = (cold, warm) else { continue };
            n_frames += 1;
            if f >= 1 {
                reads += cache.readouts;
                worst = worst.max(cache.readouts);
                for &id in &ids {
                    let c = cold.seen.iter().find(|s| s.id == id);
                    let w = warm.seen.iter().find(|s| s.id == id);
                    match (c, w) {
                        (None, None) => drops += 1,
                        (Some(c), Some(w)) => {
                            seen_ok += 1;
                            if c.offset != w.offset || c.light_seconds != w.light_seconds {
                                dis += 1;
                            }
                        }
                        _ => dis += 1,
                    }
                }
            }
        }
        let em = 24.0;
        println!(
            "{:<30} {:>8.2} {:>8} {:>6} {:>6} {:>6}   ({} frames)",
            name,
            reads as f64 / n_frames.max(1) as f64 / em,
            worst,
            drops,
            dis,
            seen_ok / n_frames.max(1) as usize,
            n_frames
        );
    }
}
