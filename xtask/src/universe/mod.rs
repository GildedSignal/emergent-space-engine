//! `xtask universe`: the plane, flown. One star system, whole: serves a debug view of what arrives at
//! the player's past light cone (port 8792), or prints the smoothness dashboard headless.
//!
//! universe [--seed N] [--rtf R] [--port 8792] [--threads N] [--members N]
//! universe --bench [--seed N] [--rtf R] [--seconds S] [--threads N] [--unpaced] [--engine-ms MS]
//! universe --describe
//! universe --kick-bench [--seed N] [--rtf R] [--seconds S]
//!
//! The frame loop is the one a player runs: every frame spends a wall budget on the engine in
//! causal-deadline order, gathers the view, serialises it; its wall time is the frame time.
mod http;
mod kick_bench;
mod session;

use serde_json::json;
use session::Session;
use std::time::{Duration, Instant};

pub(crate) fn run(args: Vec<String>) -> crate::Result<u8> {
    let (mut seed, mut rtf, mut port, mut threads, mut members) = (1u64, 1.0f64, 8792u16, 1usize, 48u64);
    let (mut bench, mut seconds, mut paced, mut describe) = (false, 30.0f64, true, false);
    let mut engine_ms = session::ENGINE_BUDGET_MS;
    let mut kicks = false;
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
            "--kick-bench" => kicks = true,
            "--unpaced" => paced = false,
            "--engine-ms" => engine_ms = val("--engine-ms")?.parse()?,
            "--describe" => describe = true,
            "--help" => {
                println!("universe [--seed N] [--rtf R] [--port 8792] [--threads N] [--members N]\nuniverse --bench [--seed N] [--rtf R] [--seconds S] [--threads N] [--unpaced] [--engine-ms MS]\nuniverse --kick-bench [--seed N] [--rtf R] [--seconds S]\nuniverse --describe");
                return Ok(0);
            }
            _ => return Err(format!("unknown universe argument {a}").into()),
        }
    }
    if !(rtf.is_finite() && (0.01..=1e7).contains(&rtf)) || !(1.0..=55.0).contains(&seconds) {
        return Err("rtf outside [0.01, 1e7], or seconds outside [1, 55] (every test and probe is at most a minute)".into());
    }
    let mut s = Session::new(seed, threads, members, rtf)?;
    s.engine_ms = engine_ms;
    if kicks {
        return kick_bench::run(s, seconds);
    }
    if describe {
        println!("{}", s.describe());
        return Ok(0);
    }
    if bench {
        return benchmark(s, seconds, paced);
    }
    http::serve(s, port)
}

/// The scripted player of the benchmark: a short burn every four seconds of game time (forward, forward and right,
/// reverse, left), coasting between. Short, because a long burn from low orbit ends in the planet. The script is a
/// function of the frame's *nominal* place (60 Hz of game time at the session's rtf), and so becomes a list of
/// decisions at canonical ticks ([`canonical_log`]): the wall's own frames never move a decision.
fn script(frame: usize) -> u8 {
    let slot = frame / 240;
    if frame % 240 < 20 {
        [1, 9, 2, 4, 1, 1 | 4, 2, 8][slot % 8]
    } else {
        0
    }
}

/// The script's decisions at canonical ticks: the key state at nominal frame `n` takes effect at tick `(n−1)·F`, `F`
/// the ticks of one nominal 60 Hz frame at `rtf`. Written before the run; the run takes them at those ticks.
fn canonical_log(frames: usize, rtf: f64) -> Vec<(i64, u8)> {
    let per_frame = rtf / 60.0 / emergent_universe::view::TICK_SECONDS;
    let (mut log, mut keys) = (Vec::new(), 0u8);
    for n in 1..=frames {
        if script(n) != keys {
            keys = script(n);
            log.push((((n - 1) as f64 * per_frame).round() as i64, keys));
        }
    }
    log
}

fn benchmark(mut s: Session, seconds: f64, paced: bool) -> crate::Result<u8> {
    let before = crate::measure::machine_state("before");
    let uptime = |c: &str| std::process::Command::new(c).output().map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string()).unwrap_or_default();
    let load_before = uptime("uptime");
    let frames = (seconds * 60.0) as usize;
    // The canonical cut: the game time the run is for (`seconds` at `rtf`), a tick of the root clock. No frame goes past it,
    // the digest is taken there whatever the wall did, and it is printed with the digest.
    let cut = (frames as f64 * s.rtf / 60.0 / emergent_universe::view::TICK_SECONDS).round() as i64;
    s.cut = Some(cut);
    let log = canonical_log(frames, s.rtf);
    for &(t, k) in &log {
        s.p.u.schedule(t, k).map_err(|e| format!("schedule: {e:?}"))?;
    }
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
        s.step(None, if paced { dt } else { 1.0 / 60.0 })?;
    }
    let d = s.dash.summary();
    let wall_s = wall.elapsed().as_secs_f64();
    let presented_at_end = s.p.u.now;
    let st = s.stats();
    let cost: Vec<_> = ["planet", "moon", "ship", "player", "fleet"]
        .iter()
        .enumerate()
        .map(|(i, k)| json!({"kind": k, "items": st.items[i], "total_ms": st.cost_ns[i] as f64 / 1e6, "us_per_item": if st.items[i] > 0 { st.cost_ns[i] as f64 / 1e3 / st.items[i] as f64 } else { 0.0 }}))
        .collect();
    // What the paced frames did is read before the cut's settle (which does the budget's leftover work unpaced).
    let (player_alive, lost, bytes_per_body, bodies, catalogue_live, stats_s) = (s.player_alive(), s.lost_bodies(), s.bytes_per_body(), s.n_bodies(), s.catalogue_live(), format!("{:?}", s.stats()));
    let (cut_tick, digest) = s.digest_at_cut();
    let report = json!({
        "scope": "engine advance (budgeted, causal-deadline order) + view gather + JSON serialisation; paced at 60 Hz; no browser or HTTP",
        "paced": paced, "frames": d.frames, "wall_seconds": wall_s, "rtf_target": s.rtf, "seed": s.seed,
        "frame_ms": {"p50": d.p50, "p95": d.p95, "p99": d.p99, "p99.9": d.p999},
        "frame_cpu_ms": {"p50": d.cpu.0, "p99": d.cpu.1, "p99.9": d.cpu.2, "worst": d.cpu.3, "note": "the thread's CPU time per frame: the work without the waiting; a hitch in frame_ms that is not here was a stall (descheduled or paged), not computed", "hitch_counts": d.cpu_hitch_counts},
        "hitches_per_gameplay_hour": {"above_16.7ms": d.hitches_per_hour[0], "above_33ms": d.hitches_per_hour[1], "above_50ms": d.hitches_per_hour[2]},
        "hitch_counts": d.hitch_counts,
        "worst_hitch_ms": d.worst_ms, "worst_hitch_at_frame": d.worst_at_frame,
        "where_the_time_goes_ms": {"engine": {"p50": d.parts[0].0, "p99": d.parts[0].1, "max": d.parts[0].3, "share": d.parts[0].2}, "view_gather": {"p50": d.parts[1].0, "p99": d.parts[1].1, "max": d.parts[1].3, "share": d.parts[1].2}, "view_json": {"p50": d.parts[2].0, "p99": d.parts[2].1, "max": d.parts[2].3, "share": d.parts[2].2}, "wire": {"p50": d.parts[3].0, "p99": d.parts[3].1, "max": d.parts[3].3, "share": d.parts[3].2}},
        "rtf": {"median": d.rtf_median, "lowest_1pct": d.rtf_low1, "overflow_frames": d.overflow_frames},
        "events_per_second": d.events_per_second,
        "player_alive": player_alive, "lost_bodies": lost,
        "bytes_per_body": bytes_per_body, "bodies": bodies, "catalogue_live": catalogue_live,
        "stats": stats_s,
        "engine_cost_by_kind": cost,
        "engine_budget_ms": s.engine_ms,
        "decisions": {"logged": log, "taken": s.p.u.inputs, "note": "scheduled at canonical ticks before the run; taken at those ticks, never at a wall-derived one"},
        "presented_tick_at_end": presented_at_end,
        "digest_note": "the digest is taken at the canonical cut (cut_tick, a tick of the root clock): no frame advanced past it, and everything up to it is resolved (settle); two runs with one input log, one seed and one cut give one digest, paced or not, on any budget",
        "cut_tick": cut_tick,
        "digest": digest,
        "machine_before": before, "machine_after": crate::measure::machine_state("after"),
        "uptime_before": load_before, "uptime_after": uptime("uptime"),
    });
    println!("{}", serde_json::to_string_pretty(&report)?);
    Ok(0)
}
