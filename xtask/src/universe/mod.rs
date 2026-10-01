//! `xtask universe`: the plane, flown. One star system, whole: serves a debug view of what arrives at
//! the player's past light cone (port 8792), or prints the smoothness dashboard headless.
//!
//! universe [--seed N] [--rtf R] [--port 8792] [--threads N] [--members N]
//! universe --bench [--seed N] [--rtf R] [--seconds S] [--threads N] [--unpaced]
//! universe --describe
//!
//! The frame loop is the one a player runs: every frame spends a wall budget on the engine in
//! causal-deadline order, gathers the view, serialises it; its wall time is the frame time.
mod http;
mod session;

use serde_json::json;
use session::Session;
use std::time::{Duration, Instant};

pub(crate) fn run(args: Vec<String>) -> crate::Result<u8> {
    let (mut seed, mut rtf, mut port, mut threads, mut members) = (1u64, 1.0f64, 8792u16, 1usize, 48u64);
    let (mut bench, mut seconds, mut paced, mut describe) = (false, 30.0f64, true, false);
    let mut it = args.into_iter();
    while let Some(a) = it.next() {
        let mut val = |n: &str| it.next().ok_or_else(|| format!("missing value for {n}"));
        match a.as_str() {
            "--seed" => seed = val("--seed")?.parse()?,
            "--rtf" => rtf = val("--rtf")?.parse()?,
            "--port" => port = val("--port")?.parse()?,
            "--threads" => threads = val("--threads")?.parse::<usize>()?.clamp(1, 16),
            "--members" => members = val("--members")?.parse::<u64>()?.clamp(4, 400),
            "--seconds" => seconds = val("--seconds")?.parse()?,
            "--bench" => bench = true,
            "--unpaced" => paced = false,
            "--describe" => describe = true,
            "--help" => {
                println!("universe [--seed N] [--rtf R] [--port 8792] [--threads N] [--members N]\nuniverse --bench [--seed N] [--rtf R] [--seconds S] [--threads N] [--unpaced]\nuniverse --describe");
                return Ok(0);
            }
            _ => return Err(format!("unknown universe argument {a}").into()),
        }
    }
    if !(rtf.is_finite() && (0.01..=1e7).contains(&rtf)) || !(1.0..=55.0).contains(&seconds) {
        return Err("rtf outside [0.01, 1e7], or seconds outside [1, 55] (every test and probe is at most a minute)".into());
    }
    let mut s = Session::new(seed, threads, members, rtf)?;
    if describe {
        println!("{}", s.describe());
        return Ok(0);
    }
    if bench {
        return benchmark(s, seconds, paced);
    }
    http::serve(s, port)
}

/// The scripted player of the benchmark: a short burn every four seconds (forward, forward and right,
/// reverse, left), coasting between. Short, because a long burn from low orbit ends in the planet.
fn script(frame: usize) -> u8 {
    let slot = frame / 240;
    if frame % 240 < 20 {
        [1, 9, 2, 4, 1, 1 | 4, 2, 8][slot % 8]
    } else {
        0
    }
}

fn benchmark(mut s: Session, seconds: f64, paced: bool) -> crate::Result<u8> {
    let before = crate::measure::machine_state("before");
    let uptime = |c: &str| std::process::Command::new(c).output().map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string()).unwrap_or_default();
    let load_before = uptime("uptime");
    let frames = (seconds * 60.0) as usize;
    let wall = Instant::now();
    let mut last = Instant::now();
    for n in 1..=frames {
        if paced {
            let due = Duration::from_secs_f64(n as f64 / 60.0);
            if let Some(wait) = due.checked_sub(wall.elapsed()) {
                std::thread::sleep(wait);
            }
        }
        let dt = last.elapsed().as_secs_f64().min(0.1);
        last = Instant::now();
        s.step(script(n), if paced { dt } else { 1.0 / 60.0 })?;
    }
    let d = s.dash.summary();
    let wall_s = wall.elapsed().as_secs_f64();
    let st = s.stats();
    let cost: Vec<_> = ["planet", "moon", "ship", "player", "fleet"]
        .iter()
        .enumerate()
        .map(|(i, k)| json!({"kind": k, "items": st.items[i], "total_ms": st.cost_ns[i] as f64 / 1e6, "us_per_item": if st.items[i] > 0 { st.cost_ns[i] as f64 / 1e3 / st.items[i] as f64 } else { 0.0 }}))
        .collect();
    let report = json!({
        "scope": "engine advance (budgeted, causal-deadline order) + view gather + JSON serialisation; paced at 60 Hz; no browser or HTTP",
        "paced": paced, "frames": d.frames, "wall_seconds": wall_s, "rtf_target": s.rtf, "seed": s.seed,
        "frame_ms": {"p50": d.p50, "p95": d.p95, "p99": d.p99, "p99.9": d.p999},
        "hitches_per_gameplay_hour": {"above_16.7ms": d.hitches_per_hour[0], "above_33ms": d.hitches_per_hour[1], "above_50ms": d.hitches_per_hour[2]},
        "hitch_counts": d.hitch_counts,
        "worst_hitch_ms": d.worst_ms, "worst_hitch_at_frame": d.worst_at_frame,
        "where_the_time_goes_ms": {"engine": {"p50": d.parts[0].0, "p99": d.parts[0].1, "max": d.parts[0].3, "share": d.parts[0].2}, "view_gather": {"p50": d.parts[1].0, "p99": d.parts[1].1, "max": d.parts[1].3, "share": d.parts[1].2}, "view_json": {"p50": d.parts[2].0, "p99": d.parts[2].1, "max": d.parts[2].3, "share": d.parts[2].2}, "wire": {"p50": d.parts[3].0, "p99": d.parts[3].1, "max": d.parts[3].3, "share": d.parts[3].2}},
        "rtf": {"median": d.rtf_median, "lowest_1pct": d.rtf_low1, "overflow_frames": d.overflow_frames},
        "events_per_second": d.events_per_second,
        "player_alive": s.player_alive(), "lost_bodies": s.lost_bodies(),
        "bytes_per_body": s.bytes_per_body(), "bodies": s.n_bodies(), "catalogue_live": s.catalogue_live(),
        "stats": format!("{:?}", s.stats()),
        "engine_cost_by_kind": cost,
        "digest_note": "the digest is taken at a canonical cut (after settle); this is the digest of the benchmark's universe after resolving everything up to the presented tick",
        "digest": s.digest_at_cut(),
        "machine_before": before, "machine_after": crate::measure::machine_state("after"),
        "uptime_before": load_before, "uptime_after": uptime("uptime"),
    });
    println!("{}", serde_json::to_string_pretty(&report)?);
    Ok(0)
}
