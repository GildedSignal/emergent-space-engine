//! Decompose the plane's view gather: where its time goes, what it scales with, and how much of the
//! view actually changes between frames (its surprise rate). Same frame loop as the xtask bench
//! (`frame_to`, 5 ms engine budget), same scenario (`scenario::plane`).
use emergent_universe::scenario::plane;
use emergent_universe::universe::Budget;
use emergent_universe::view::{gather_cached, Seen, ViewCache};
use serde_json::json;
use std::time::Instant;

fn pct(mut v: Vec<f64>, q: f64) -> f64 {
    if v.is_empty() {
        return 0.0;
    }
    v.sort_by(|a, b| a.total_cmp(b));
    v[((v.len() - 1) as f64 * q).round() as usize]
}

/// The perceptible quanta, fixed before the run (predictions.md): 1 px at 1080p for direction and
/// angular radius, one 8-bit colour step, 1% relative luminosity.
fn changed_beyond_quantum(a: &Seen, b: &Seen) -> bool {
    let d = [a.direction[0] - b.direction[0], a.direction[1] - b.direction[1]];
    if (d[0] * d[0] + d[1] * d[1]).sqrt() > 2e-3 {
        return true;
    }
    if (a.angular_radius - b.angular_radius).abs() > 2e-3 {
        return true;
    }
    if (a.color[0] - b.color[0]).abs() > 1.0 / 255.0
        || (a.color[1] - b.color[1]).abs() > 1.0 / 255.0
        || (a.color[2] - b.color[2]).abs() > 1.0 / 255.0
    {
        return true;
    }
    (a.luminosity - b.luminosity).abs() / a.luminosity.max(1e-30) > 0.01
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let arg = |i: usize, d: &str| args.get(i).cloned().unwrap_or_else(|| d.to_string());
    let members: u64 = arg(1, "48").parse().unwrap();
    let frames: usize = arg(2, "600").parse().unwrap();
    let rtf: f64 = arg(3, "100").parse().unwrap();
    let seed: u64 = arg(4, "1").parse().unwrap();
    let mut p = plane(Default::default(), seed, emergent_universe::fleet::Order::Sparse, 1, members).expect("plane");
    let mut cache = ViewCache::default();
    let mut gather_ms: Vec<f64> = Vec::new();
    let mut readouts: Vec<u64> = Vec::new();
    let mut entries: Vec<usize> = Vec::new();
    let mut changed: Vec<usize> = Vec::new();
    let mut prev: Vec<Seen> = Vec::new();
    for f in 1..=frames {
        let _ = p.u.frame_to(1.0 / 60.0, rtf, Budget::wall(5.0), i64::MAX);
        let t0 = Instant::now();
        let v = gather_cached(&p.u, &p.names, &mut cache).expect("view");
        gather_ms.push(t0.elapsed().as_secs_f64() * 1e3);
        readouts.push(cache.readouts);
        entries.push(v.seen.len());
        if f > 1 {
            let c = v
                .seen
                .iter()
                .zip(prev.iter())
                .filter(|(a, b)| a.id == b.id && changed_beyond_quantum(a, b))
                .count();
            changed.push(c);
        }
        prev = v.seen;
    }
    // A pure readout's cost: `state_rate` on random alive bodies at random ticks (the Newton eval).
    let ctx = p.u.ctx();
    let n = p.u.n_bodies();
    let mut per_readout_ns: Vec<f64> = Vec::new();
    let mut seed2: u64 = seed.wrapping_mul(0x9E3779B97F4A7C15) | 1;
    for _ in 0..400 {
        seed2 = seed2.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        let i = (seed2 >> 33) as usize % n;
        if i == p.player || !p.u.bodies().alive(i) {
            continue;
        }
        seed2 = seed2.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        let t = ((seed2 >> 33) % (p.u.now.max(1) as u64)) as i64;
        let t0 = Instant::now();
        let _ = emergent_universe::observe::state_rate(&ctx, i, t);
        per_readout_ns.push(t0.elapsed().as_nanos() as f64);
    }
    let mean_changed = changed.iter().sum::<usize>() as f64 / changed.len().max(1) as f64;
    let mean_entries = entries.iter().sum::<usize>() as f64 / entries.len().max(1) as f64;
    println!(
        "{}",
        json!({
            "members": members, "frames": frames, "rtf": rtf, "seed": seed, "bodies": n,
            "gather_ms": {"p50": pct(gather_ms.clone(), 0.5), "p99": pct(gather_ms.clone(), 0.99), "max": gather_ms.iter().cloned().fold(f64::MIN, f64::max)},
            "readouts_per_gather": {"median": pct(readouts.iter().map(|&x| x as f64).collect(), 0.5), "max": *readouts.iter().max().unwrap_or(&0)},
            "us_per_readout_direct": {"median": pct(per_readout_ns.clone(), 0.5) / 1e3, "samples": per_readout_ns.len()},
            "seen_entries_mean": mean_entries,
            "surprise": {"mean_changed_per_frame": mean_changed, "fraction_of_entries": mean_changed / mean_entries.max(1.0),
                          "note": "entries whose direction moved >2e-3 rad, or a colour channel >1/255, or luminosity >1% rel, or angular radius >2e-3 rad, between consecutive frames"},
        })
    );
}
