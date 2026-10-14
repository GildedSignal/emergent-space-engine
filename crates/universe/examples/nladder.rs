//! The N ladder: how many real bodies the plane holds. The plane with `N` more ships (`scenario::plane_extra`: a few hundred
//! about Home and the Moon, the rest a belt between 2 and 3 AU, each on its own exact orbit from integers and a seed), flown the
//! way the page flies it (60 frames a second of wall time at a real-time factor, `frame_to` with a 12 ms engine budget), the player
//! coasting or burning forward at level 8 from the first second. One run is one rung and one flight, and must fit in 60 s: it
//! reports the build (wall, resident memory, bytes a body), the frames after the first second (engine wall p50 / p99 / worst,
//! frames over 12 ms, the presented time's lag), events and kicks per body per game-second, refusals, the view's cost for one
//! gather, and with `--features prof` the stage profile. One `ladder:` line holds every number (key=value) for the tables.
//!
//! cargo run --release -p emergent-universe --example nladder [-- <N> <coast|burn> [<wall seconds of flight> [<rtf> [<engine budget ms>]]]]
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::thrust::word;
use emergent_universe::view::{gather_cached, ViewCache, TICK_SECONDS};
use emergent_universe::{Budget, Config};
use std::time::{Duration, Instant};

extern "C" {
    fn proc_pid_rusage(pid: i32, flavor: i32, buffer: *mut u64) -> i32;
}

/// (physical footprint now, its peak over the process's life) in bytes: the memory the process holds, compressed pages
/// included (the resident size alone drops pages the machine has compressed or swapped, and this machine does under load).
fn footprint() -> (u64, u64) {
    let mut buf = [0u64; 64];
    // flavor 4: rusage_info_v4; ri_phys_footprint is word 9, ri_lifetime_max_phys_footprint word 30.
    let ok = unsafe { proc_pid_rusage(std::process::id() as i32, 4, buf.as_mut_ptr()) };
    if ok != 0 {
        return (0, 0);
    }
    (buf[9], buf[30])
}

fn pct(sorted: &[f64], p: f64) -> f64 {
    if sorted.is_empty() {
        return 0.0;
    }
    sorted[(((sorted.len() - 1) as f64) * p).round() as usize]
}

fn main() {
    let t_start = Instant::now();
    let args: Vec<String> = std::env::args().collect();
    let n: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(0);
    let flight = args.get(2).cloned().unwrap_or_else(|| "coast".into());
    let seconds: f64 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(10.0);
    let rtf: f64 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(100.0);
    let budget_ms: f64 = args.get(5).and_then(|s| s.parse().ok()).unwrap_or(12.0);
    let burn = flight == "burn";
    let frames = (seconds * 60.0) as usize;
    let (_, rss0) = footprint();
    let t0 = Instant::now();
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, n).unwrap();
    let build = t0.elapsed().as_secs_f64();
    let (now1, rss1) = footprint();
    let bodies = p.u.n_bodies();
    println!("rung N={n} ({bodies} bodies), {flight}, rtf {rtf}, {seconds} s of wall time, engine budget {budget_ms} ms; build {build:.2} s, peak footprint {:.0} MB (now {:.0} MB)", rss1 as f64 / 1e6, now1 as f64 / 1e6);
    let mut rows: Vec<(usize, f64, u64, f64)> = Vec::new(); // frame, ms, events, lag s
    let mut stage_ns = [0u64; emergent_universe::prof::N];
    let mut stage_calls = [0u64; emergent_universe::prof::N];
    let (mut held_max, mut truncated) = (0usize, false);
    let mut late_stats: Option<(emergent_universe::universe::Stats, i64)> = None;
    let mut last_stats = p.u.stats;
    let mut alive = true;
    let mut ran = 0usize;
    let mut doll_at: Vec<(usize, u16)> = Vec::new(); // (frame, doll) each time the player's doll changes
    for f in 0..frames {
        if t_start.elapsed() > Duration::from_secs(55) {
            truncated = true;
            break;
        }
        if f == 60 {
            if burn {
                let t = p.u.now;
                let _ = p.u.input(t, word(1, 8));
            }
            late_stats = Some((p.u.stats, p.u.now));
            let _ = emergent_universe::prof::take();
        }
        let start = Instant::now();
        let frame = p.u.frame_to(1.0 / 60.0, rtf, Budget { events: u64::MAX, until: Some(start + Duration::from_micros((budget_ms * 1e3) as u64)) }, i64::MAX);
        let took = start.elapsed();
        let (ns, calls) = emergent_universe::prof::take();
        if f >= 60 {
            for k in 0..emergent_universe::prof::N {
                stage_ns[k] += ns[k];
                stage_calls[k] += calls[k];
            }
        }
        rows.push((f, took.as_secs_f64() * 1e3, frame.events, (frame.target - frame.presented) as f64 * TICK_SECONDS));
        held_max = held_max.max(p.u.held_scans());
        last_stats = p.u.stats;
        ran += 1;
        let rec = p.u.rec(p.player);
        if doll_at.last().map(|d| d.1) != Some(rec.b.doll) {
            doll_at.push((f, rec.b.doll));
        }
        if !rec.alive {
            alive = false;
            break;
        }
    }
    let (now2, rss2) = footprint();
    let late: Vec<_> = rows.iter().filter(|r| r.0 >= 60).collect();
    let mut ms: Vec<f64> = late.iter().map(|r| r.1).collect();
    ms.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let mut ev: Vec<f64> = late.iter().map(|r| r.2 as f64).collect();
    ev.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let over = late.iter().filter(|r| r.1 > budget_ms).count();
    let lag = late.iter().map(|r| r.3).fold(0.0, f64::max);
    let late_frames_lagging = late.iter().filter(|r| r.3 > 0.0).count();
    let (s0, t_first) = late_stats.unwrap_or((p.u.stats, p.u.now));
    let game_s = (p.u.now - t_first) as f64 * TICK_SECONDS;
    let (kicks, evs) = (last_stats.kicks - s0.kicks, last_stats.events() - s0.events());
    let per = |x: u64| if game_s > 0.0 { x as f64 / bodies as f64 / game_s } else { 0.0 };
    // refusals: the engine's count (a body refused an item) and what the bodies hold; the dead.
    let (mut refusals, mut dead) = (0u64, 0usize);
    for i in 0..bodies {
        let r = p.u.rec(i);
        refusals += r.refusals;
        dead += (!r.alive) as usize;
    }
    // the view: one gather from a cold cache and one from the warm one, wall (skipped when the run is near its 60 s).
    let mut cache = ViewCache::default();
    let (mut cold, mut warm, mut seen) = (-1.0f64, -1.0f64, 0usize);
    // (a cold gather costs about 30 us a body: it runs only when it fits in the run's 60 s)
    if t_start.elapsed().as_secs_f64() + bodies as f64 * 3.0e-5 < 55.0 {
        let tv = Instant::now();
        seen = gather_cached(&p.u, &p.names, &mut cache).map_or(0, |v| v.seen.len());
        cold = tv.elapsed().as_secs_f64() * 1e3;
        if t_start.elapsed() < Duration::from_secs(45) {
            let tv = Instant::now();
            let _ = gather_cached(&p.u, &p.names, &mut cache);
            warm = tv.elapsed().as_secs_f64() * 1e3;
        }
    }
    println!(
        "frames after 1 s: {}  engine ms p50 {:.3} p90 {:.3} p99 {:.3} max {:.3}; over {budget_ms} ms: {over}; frames behind: {late_frames_lagging}, worst lag {lag:.3} s; events/frame p50 {} p99 {} max {}; scans held max {held_max}",
        late.len(), pct(&ms, 0.5), pct(&ms, 0.9), pct(&ms, 0.99), pct(&ms, 1.0), pct(&ev, 0.5), pct(&ev, 0.99), pct(&ev, 1.0)
    );
    println!(
        "game {game_s:.1} s after the first second: kicks {kicks} ({:.3e}/body/game-s), events {evs} ({:.3e}/body/game-s), stats {{opens {}, boundaries {}, handoffs {}, lost {}, refused {}, slices {}}}; refusals held {refusals}, dead {dead}, alive(player) {alive}",
        per(kicks), per(evs), last_stats.opens - s0.opens, last_stats.boundaries - s0.boundaries, last_stats.handoffs - s0.handoffs, last_stats.lost - s0.lost, last_stats.refused - s0.refused, last_stats.slices - s0.slices
    );
    println!("memory: peak footprint {:.0} MB at the build's end, {:.0} MB at the flight's end (now {:.0} MB); {:.0} B a body from the build; dashboard bytes/body {}; view gather {cold:.1} ms cold, {warm:.1} ms warm ({seen} seen); catalogue {} entries", rss1 as f64 / 1e6, rss2 as f64 / 1e6, now2 as f64 / 1e6, (rss1.saturating_sub(rss0)) as f64 / n.max(1) as f64, p.u.bytes_per_body(), p.u.catalogue_live());
    if emergent_universe::prof::ENABLED {
        println!("stages (µs per frame, calls per frame, ns per call), over the {} frames:", late.len());
        for k in 0..emergent_universe::prof::N {
            if stage_calls[k] > 0 {
                println!("  {:<38} {:>9.1} {:>8.2} {:>10.0}", emergent_universe::prof::NAMES[k], stage_ns[k] as f64 / 1e3 / late.len().max(1) as f64, stage_calls[k] as f64 / late.len().max(1) as f64, stage_ns[k] as f64 / stage_calls[k] as f64);
            }
        }
    }
    let mut worst: Vec<_> = late.clone();
    worst.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    let mut over_at: Vec<usize> = late.iter().filter(|r| r.1 > budget_ms).map(|r| r.0).collect();
    over_at.truncate(12);
    println!("frames over the budget (first 12): {over_at:?}; the player's doll (frame, doll): {doll_at:?}");
    println!("worst frames (frame, ms, events, lag s): {}", worst.iter().take(5).map(|r| format!("({}, {:.2}, {}, {:.3})", r.0, r.1, r.2, r.3)).collect::<Vec<_>>().join(" "));
    println!(
        "ladder: n={n} bodies={bodies} flight={flight} rtf={rtf} frames={ran} build_s={build:.2} foot_build_mb={:.0} foot_end_mb={:.0} b_per_body={:.0} p50_ms={:.3} p99_ms={:.3} max_ms={:.3} over={over} lag_s={lag:.3} kicks_per_body_gs={:.3e} events_per_body_gs={:.3e} refusals={refusals} dead={dead} held_max={held_max} view_ms={warm:.1} truncated={truncated} wall_s={:.1}",
        rss1 as f64 / 1e6, rss2 as f64 / 1e6, (rss1.saturating_sub(rss0)) as f64 / n.max(1) as f64, pct(&ms, 0.5), pct(&ms, 0.99), pct(&ms, 1.0), per(kicks), per(evs), t_start.elapsed().as_secs_f64()
    );
}
