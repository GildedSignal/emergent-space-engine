// The player's decision as a market order: one twin plane (this process, one arm) runs the frame
// loop at a fixed rtf with the plane's wall engine budget; at frame F0 the player either holds a
// level-15 burn (mode burn), or takes a word-0 no-op decision (mode noop), or nothing (mode coast).
// Per frame: engine wall ms, events, presented tick, overflow, per-kind deltas, per-kind cost deltas.
// The shell runs arms in ABBA order and compares. `wake SEED MODE [SECONDS] [RTF] [ENGINE_MS]`.
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::universe::Stats;
use emergent_universe::{Budget, Config};
use std::io::Write as _;
use std::time::Instant;

fn delta(a: &Stats, b: &Stats) -> [u64; 12] {
    [
        a.kicks - b.kicks,
        a.opens - b.opens,
        a.boundaries - b.boundaries,
        a.handoffs - b.handoffs,
        a.slices - b.slices,
        a.decisions - b.decisions,
        a.encounters - b.encounters,
        a.refused - b.refused,
        a.leavers - b.leavers,
        a.dissolved - b.dissolved,
        a.items[2], // ship items (cumulative per frame: ships resolve in waves of all ships)
        a.items[3], // player items
    ]
}

fn main() {
    let a: Vec<String> = std::env::args().skip(1).collect();
    let seed: u64 = a.first().map(|s| s.parse().unwrap()).unwrap_or(1);
    let mode = a.get(1).cloned().unwrap_or_else(|| "burn".into());
    let seconds: f64 = a.get(2).map(|s| s.parse().unwrap()).unwrap_or(30.0);
    let rtf: f64 = a.get(3).map(|s| s.parse().unwrap()).unwrap_or(100.0);
    let engine_ms: f64 = a.get(4).map(|s| s.parse().unwrap()).unwrap_or(5.0);
    let (f0, f1) = (600usize, 1200usize);
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, 48).unwrap();
    let player = p.player;
    let mut out = std::io::stdout().lock();
    let _ = writeln!(out, "# mode={mode} seed={seed} rtf={rtf} engine_ms={engine_ms} seconds={seconds} load={}", std::fs::read_to_string("/proc/loadavg").unwrap_or_default().trim());
    let frames = (seconds * 60.0) as usize;
    let mut prev = p.u.stats;
    // Both decisions at FIXED canonical ticks (6/12 wall-seconds at nominal rtf), submitted before
    // the loop: the input history must not depend on the wall-clock schedule the budget chose.
    let level: u8 = mode.strip_prefix("burn").and_then(|l| l.parse().ok()).unwrap_or(15);
    let is_burn = mode.starts_with("burn");
    let (tb, tr) = (338_375i64 * f0 as i64, 338_375i64 * f1 as i64);
    if mode != "coast" {
        p.u.schedule(tb, if is_burn { word(1, level) } else { word(0, 0) }).unwrap();
    }
    if is_burn {
        p.u.schedule(tr, word(0, 0)).unwrap();
    }
    for f in 0..frames {
        let t0 = Instant::now();
        let fr = p.u.frame(1.0 / 60.0, rtf, Budget::wall(engine_ms));
        let ms = t0.elapsed().as_secs_f64() * 1e3;
        let s = p.u.stats;
        let d = delta(&s, &prev);
        prev = s;
        let cols: Vec<String> = std::iter::once(format!("{f}"))
            .chain(std::iter::once(format!("{ms:.4}")))
            .chain([
                fr.events, fr.presented as u64, fr.overflow as u64, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9],
                s.cost_ns[0], s.cost_ns[1], s.cost_ns[2], s.cost_ns[3], s.cost_ns[4],
            ].iter().map(|x| x.to_string()))
            .collect();
        let _ = writeln!(out, "{}", cols.join(","));
    }
    // The canonical cut at the run's full target: same tick in every arm, so digests compare.
    let end: i64 = std::env::var("WAKE_END").ok().and_then(|s| s.parse().ok()).unwrap_or_else(|| p.u.now + 1);
    p.u.settle(end);
    let s = p.u.stats;
    let _ = writeln!(
        out,
        "# digest={} now={} periapsis={:?} refused={} kicks={} opens={} boundaries={} handoffs={} slices={} decisions={} encounters={}",
        p.u.digest(), p.u.now, p.u.rec(player).b.entry.trajectory.key().periapsis, s.refused, s.kicks, s.opens, s.boundaries, s.handoffs, s.slices, s.decisions, s.encounters
    );
}
