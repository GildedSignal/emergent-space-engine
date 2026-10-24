//! The calendar job's hot set over game days: the N ladder's plane (`scenario::plane_extra`), every item resolved in order
//! (`settle`, no frames, no wall budget) up to a horizon of game seconds, the ships' items watched against their own grid
//! ([`emergent_universe::universe::GridWatch`]): how often a root ship's kick plans a step other than the one it had (its next
//! kick is then off the grid `next = last + its step`), by how much, and how far its kicks wander from the grid of its first
//! watched kick. The ladder's 200 s flights (rtf 100, 20,000 game seconds) see almost only each body's first kick (its stub);
//! this sees the second and later ones. Cuts itself at 55 s of wall and says so.
//!
//! cargo run --release -p emergent-universe --example grid [-- <N> <game seconds> [<rtf for the frame unit>]]
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::Config;
use std::time::{Duration, Instant};

fn main() {
    let t_start = Instant::now();
    let args: Vec<String> = std::env::args().collect();
    let n: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(10_000);
    let game_s: f64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(1.0e6);
    let rtf: f64 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(100.0);
    let frame_ticks = rtf / 60.0 / TICK_SECONDS;
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, n).unwrap();
    p.u.watch_grid();
    let horizon = (game_s / TICK_SECONDS) as i64;
    let chunks = 256;
    let mut reached = 0i64;
    let mut truncated = false;
    for k in 1..=chunks {
        if t_start.elapsed() > Duration::from_secs(55) {
            truncated = true;
            break;
        }
        reached = horizon / chunks * k;
        p.u.settle(reached);
    }
    let g = p.u.grid_watch().unwrap();
    let s = p.u.stats;
    let hist = |h: &[u64; 64], label: &dyn Fn(usize) -> String| h.iter().enumerate().filter(|x| *x.1 > 0).map(|(k, c)| format!("{}:{c}", label(k))).collect::<Vec<_>>().join(" ");
    println!(
        "grid: N={n} ({} bodies), {:.3e} game s reached of {game_s:.3e} (truncated {truncated}), wall {:.1} s; kicks {}, boundaries {}, refused {}",
        p.u.n_bodies(),
        reached as f64 * TICK_SECONDS,
        t_start.elapsed().as_secs_f64(),
        s.kicks,
        s.boundaries,
        s.refused
    );
    println!(
        "root ships' kicks after their first (stub) {}: step changed at {} ({:.1}%); planet-doll ships' boundaries {}: changed at {}",
        g.items[0],
        g.off[0],
        100.0 * g.off[0] as f64 / g.items[0].max(1) as f64,
        g.items[1],
        g.off[1]
    );
    println!("bodies with a watched item {}, off their grid at least once {}", g.seen_bodies(), g.off_bodies());
    println!("|dS|/S of the changes: {}", hist(&g.rel_log2, &|k| format!("2^-{k}")));
    println!("|dS| of the changes, ticks: {}", hist(&g.abs_log2, &|k| format!("2^{k}")));
    println!("kicks' distance from the grid of the body's first watched kick, ticks: {}", hist(&g.drift_log2, &|k| format!("2^{k}")));
    let over_frame: u64 = g.drift_log2.iter().enumerate().filter(|(k, _)| (1u64 << k) as f64 >= frame_ticks).map(|x| *x.1).sum();
    let later: u64 = g.drift_log2.iter().sum();
    println!(
        "a frame at rtf {rtf} is {frame_ticks:.3e} ticks: {over_frame} of {later} later kicks ({:.1}%) are at least a frame off the grid of the first",
        100.0 * over_frame as f64 / later.max(1) as f64
    );
}
