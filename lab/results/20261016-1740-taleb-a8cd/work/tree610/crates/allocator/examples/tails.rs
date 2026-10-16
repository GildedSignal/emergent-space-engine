//! Round-3 before/after: a heavy-tailed relativistic scene (one dense gas region beside many
//! small sparse islands, the player among the islands) in the frame harness, each scheduling
//! change enabled in turn in the same build. Prints one table row per configuration and the
//! machine's load and thermal state around the runs.
//!
//!     cargo run -p emergent-allocator --release --offline --example tails
use emergent_allocator::{scenes, Allocator, Config, Factory, FrameConfig, Report};
use emergent_lattice::{chronon::Chronon, law::Law};
use std::sync::Arc;

fn sh(cmd: &str, args: &[&str]) -> String {
    std::process::Command::new(cmd).args(args).output().map(|o| String::from_utf8_lossy(&o.stdout).trim().replace('\n', " | ")).unwrap_or_default()
}

fn run(name: &str, gas: u64, per: u64, cfg: Config) -> Report {
    let q = 256;
    let (scene, observer) = scenes::heavy_tail(q, gas, 8, 12, per, 400, 2500, 5);
    let scene = scenes::with_law(scene, Law::Relativistic);
    let factory: Factory<Chronon> = Arc::new(|w| Chronon::new(w, false).expect("valid region world"));
    let mut a = Allocator::new(scene, factory, Config { p_workers: 3, e_workers: 4, observer, view_radius: 300 * q, ..cfg }).expect("scene");
    let r = a.run_frames(&FrameConfig { hz: 120.0, seconds: 4.0, rate: 600.0, ahead_seconds: 0.25, record: false });
    let (f, s, u) = (r.frames.as_ref().expect("frames"), &r.sched, &r.units);
    println!(
        "| {name:<26} | {:>5.2} | {:>6} | {:>6.2} / {:>6.2} | {:>6.1} | {:>6.3} / {:>6.3} | {:>6.3} | {:>5} | {:>6} | {:>7.0} | {:>5.0} | {:>3} | {:>5} | {:>4.0} | {:>3} |",
        f.work_ms.max,
        f.small_deadline_misses,
        s.latency_small_ms.p50,
        s.latency_small_ms.p99,
        s.latency_giant_ms.p99,
        u.lock_wait_ms.p99,
        s.lock_hold_ms.p99,
        s.lock_hold_ms.max,
        s.steals,
        s.switches,
        r.sim.region_chronons_per_wall_second,
        r.sim.present_chronons_per_wall_second,
        r.regions.rollbacks,
        s.ineligible,
        s.stride_chronons.p50,
        r.regions.initial,
    );
    r
}

fn main() {
    let gas = std::env::args().nth(1).and_then(|a| a.parse().ok()).unwrap_or(8192);
    eprintln!("load before: {}", sh("uptime", &[]));
    eprintln!("thermal before: {}", sh("pmset", &["-g", "therm"]));
    println!("heavy tail: relativistic gas {gas} + 96 islands of 40 (20 for micro rows), 3 P + 4 E workers, 120 Hz, 600 chronons/s target, 4 s each");
    println!("| configuration              | frame max ms | small misses | small latency p50 / p99 ms | giant p99 ms | lock wait p99 / hold p99 ms | hold max | steals | switches | region-chr/s | present/s | rollbacks | ineligible | stride | regions |");
    println!("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|");
    let r2 = Config::round2();
    let fin = Config { fast_finality: true, ..r2.clone() };
    let lanes = Config { lanes: true, ..fin.clone() };
    let queues = Config { queues: true, ..lanes.clone() };
    let aimd = Config { aimd: true, window: 16, stride: 2, stride_max: 16, ..queues.clone() };
    let eev = Config { eligibility: true, hysteresis: true, ..aimd.clone() };
    let no_lanes = Config { queues: true, ..fin.clone() };
    for (name, cfg) in [("round 2 (all off)", r2), ("+ shared-coalesce finality", fin), ("  (queues without lanes)", no_lanes), ("+ SITA lanes", lanes), ("+ queues & stealing", queues), ("+ AIMD strides", aimd), ("+ eligibility & hysteresis", eev.clone())] {
        run(name, gas, 40, cfg);
    }
    // Micro-partitioning: islands of 20 bodies, grouped (min_region 32) or kept apart (8).
    run("all, islands 20, min 32", gas, 20, eev.clone());
    run("all, islands 20, min 8", gas, 20, Config { min_region: 8, ..eev });
    eprintln!("load after: {}", sh("uptime", &[]));
    eprintln!("thermal after: {}", sh("pmset", &["-g", "therm"]));
}
