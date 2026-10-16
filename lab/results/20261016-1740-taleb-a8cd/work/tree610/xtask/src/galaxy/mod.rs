//! `xtask galaxy`: millions to billions of orbiting ships in one doll, seen as a density image.
//! A debug view (a god's view: world frame, positions now), built on `crates/space`.
//!
//! galaxy [--ships N] [--tubes N] [--seed N] [--threads N] [--port 8791] [--family-size N] [--fleets F]
//! galaxy --bench [scene flags] [--frames N] [--pace HZ] [--rtf M_PER_S] [--w W --h H]
//! galaxy --png FILE [scene flags] [--scale M_PER_PX] [--cx X --cy Y] [--t Q20]
mod draw;
mod scene;
mod server;
#[cfg(test)]
mod tests;

use draw::{Opts, Renderer, View};
use scene::{Config, Scene};
use serde_json::json;
use std::time::{Duration, Instant};

fn count(s: &str) -> crate::Result<u64> {
    let f: f64 = s.parse()?;
    if !f.is_finite() || !(0.0..=1e12).contains(&f) {
        return Err(format!("count out of range: {s}").into());
    }
    Ok(f.round() as u64)
}

pub(crate) fn run(args: Vec<String>) -> crate::Result<u8> {
    let mut cfg = Config::default();
    cfg.threads = std::thread::available_parallelism().map_or(4, |n| n.get()).min(4);
    let (mut port, mut bench, mut png) = (8791u16, false, None::<String>);
    let (mut frames, mut pace, mut rtf) = (200usize, 60.0f64, 1000.0f64);
    let (mut w, mut h, mut scale, mut cx, mut cy, mut t) = (960usize, 540usize, None::<f64>, 0.0f64, 0.0f64, 0u64);
    let mut it = args.into_iter();
    while let Some(a) = it.next() {
        let mut val = |name: &str| it.next().ok_or_else(|| format!("missing value for {name}"));
        match a.as_str() {
            "--ships" => cfg.ships = count(&val("--ships")?)?,
            "--tubes" => cfg.tubes = count(&val("--tubes")?)?,
            "--seed" => cfg.seed = val("--seed")?.parse()?,
            "--threads" => cfg.threads = val("--threads")?.parse::<usize>()?.clamp(1, 16),
            "--port" => port = val("--port")?.parse()?,
            "--family-size" => cfg.family_size = count(&val("--family-size")?)?.max(1),
            "--fleets" => cfg.fleets = val("--fleets")?.parse()?,
            "--bench" => bench = true,
            "--png" => png = Some(val("--png")?),
            "--frames" => frames = val("--frames")?.parse()?,
            "--pace" => pace = val("--pace")?.parse()?,
            "--rtf" => rtf = val("--rtf")?.parse()?,
            "--w" => w = val("--w")?.parse()?,
            "--h" => h = val("--h")?.parse()?,
            "--scale" => scale = Some(val("--scale")?.parse()?),
            "--cx" => cx = val("--cx")?.parse()?,
            "--cy" => cy = val("--cy")?.parse()?,
            "--t" => t = val("--t")?.parse()?,
            "--help" => {
                println!("galaxy [--ships 1e9] [--tubes 1e6] [--seed 1] [--threads 4] [--port 8791] [--family-size 1e5] [--fleets 0.1]\ngalaxy --bench [--frames 200] [--pace 60] [--rtf 1000] [--w 960 --h 540]\ngalaxy --png FILE [--scale M_PER_PX] [--cx X --cy Y] [--t Q20]");
                return Ok(0);
            }
            _ => return Err(format!("unknown galaxy argument {a}").into()),
        }
    }
    if port == 8787 || port == 8788 || port == 8790 {
        return Err("ports 8787, 8788 and 8790 are reserved".into());
    }
    let scene = Scene::build(&cfg)?;
    let s = &scene.stats;
    println!(
        "scene: {} ships = {} tubes + {} families · {} cycles compiled for {} key requests (hit rate {:.5}, {:.0} ships per compile) · compile {:.2} s, tubes {:.2} s, total {:.2} s",
        scene.total_ships, scene.tubes.len(), scene.families.len(), s.compiled, s.lookups, s.hit_rate, s.ships_per_compile, s.compile_wall_s, s.tubes_wall_s, s.total_wall_s
    );
    if bench {
        return bench_run(&scene, cfg.threads, frames, pace, rtf, w, h);
    }
    if let Some(path) = png {
        let v = View { w, h, cx, cy, scale: scale.unwrap_or(2.0 * server::R_FAR / h as f64), t };
        let mut out = Vec::new();
        let st = Renderer::new().render(&scene, &v, &Opts::for_size(w, h, cfg.threads), &mut out);
        std::fs::write(&path, server::png(w, h, &out))?;
        println!("{path} {}", server::stats_json(&st, &v));
        return Ok(0);
    }
    server::serve(&scene, port, cfg.threads)
}

fn quantiles(mut v: Vec<f64>) -> (f64, f64, f64) {
    v.sort_by(f64::total_cmp);
    (crate::measure::percentile(&v, 0.5), crate::measure::percentile(&v, 0.99), v.last().copied().unwrap_or(0.0))
}

/// Frame time as the player runs it: paced at `pace` Hz, time advancing at `rtf` M per second, three views
/// (the whole galaxy, 10× in, 100× in at 100 M from the centre). Render only: no HTTP, no browser.
fn bench_run(scene: &Scene, threads: usize, frames: usize, pace: f64, rtf: f64, w: usize, h: usize) -> crate::Result<u8> {
    let extra = |c: &str| std::process::Command::new(c).output().map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string()).unwrap_or_default();
    let before = crate::measure::machine_state("before");
    let (uptime_before, vm_before) = (extra("uptime"), extra("vm_stat"));
    let far = 2.0 * server::R_FAR / h as f64;
    let views = [("far", 0.0, far), ("mid", 0.0, far / 10.0), ("deep", 100.0, far / 100.0)];
    let opts = Opts::for_size(w, h, threads);
    let mut renderer = Renderer::new();
    let mut out = Vec::new();
    let (wall0, cpu0) = (Instant::now(), crate::measure::cpu_seconds());
    let mut results = Vec::new();
    for (name, cx, scale) in views {
        let (mut ms, mut samples, mut ships, mut mat) = (Vec::new(), Vec::new(), Vec::new(), Vec::new());
        let start = Instant::now();
        for n in 0..frames {
            if wall0.elapsed().as_secs_f64() > 52.0 {
                break;
            }
            if pace > 0.0 {
                let due = Duration::from_secs_f64(n as f64 / pace);
                if let Some(wait) = due.checked_sub(start.elapsed()) {
                    std::thread::sleep(wait);
                }
            }
            let t = ((n as f64 / pace.max(1.0)) * rtf * 1048576.0) as u64;
            let v = View { w, h, cx, cy: 0.0, scale, t };
            let st = renderer.render(scene, &v, &opts, &mut out);
            ms.push(st.total_ms);
            samples.push(st.samples as f64);
            ships.push(st.ships_in_view);
            mat.push(st.materialized as f64);
        }
        let over = ms.iter().filter(|&&m| m > 1000.0 / 60.0).count();
        let (med, p99, max) = quantiles(ms.clone());
        let med_samples = quantiles(samples).0;
        let med_ships = quantiles(ships).0;
        results.push(json!({
            "view": name, "scale_m_per_px": scale, "frames": ms.len(),
            "median_ms": med, "p99_ms": p99, "max_ms": max, "over_16_7ms": over,
            "median_samples": med_samples, "median_single_ships": quantiles(mat).0, "median_ships_in_view": med_ships,
            "ns_per_sample": med * 1e6 / med_samples.max(1.0),
            "ns_per_ship_in_view": med * 1e6 / med_ships.max(1.0),
        }));
    }
    let wall = wall0.elapsed().as_secs_f64();
    println!(
        "{}",
        json!({
            "scope": "render only (plan + splat + reduce + tone map); no HTTP, no browser; paced like the player",
            "ships": scene.total_ships.to_string(), "tubes": scene.tubes.len(), "families": scene.families.len(),
            "cycles_compiled": scene.stats.compiled, "memo_hit_rate": scene.stats.hit_rate, "key_requests": scene.stats.lookups,
            "threads": threads, "w": w, "h": h, "pace_hz": pace, "rtf_m_per_s": rtf,
            "tube_cap": opts.tube_cap, "fam_budget": opts.fam_budget,
            "views": results, "wall_s": wall, "cores_used": (crate::measure::cpu_seconds() - cpu0) / wall,
            "peak_rss_mb": crate::measure::peak_rss() as f64 / 1048576.0,
            "machine_before": before, "machine_after": crate::measure::machine_state("after"),
            "uptime_before": uptime_before, "uptime_after": extra("uptime"),
            "vm_stat_before": vm_before, "vm_stat_after": extra("vm_stat"),
        })
    );
    Ok(0)
}
