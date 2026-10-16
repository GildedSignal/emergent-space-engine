//! Unit-time attribution: drive one ladder world in units of 4096 ops (as ladder v5 does),
//! time every unit, and for the slowest units report CPU time, page faults, context
//! switches and container reallocations, to separate hidden work from machine contention.
//!
//! cargo run -p emergent-lattice-event --release --offline --example units -- <gas|random|mixed|crowded|horizon> <n> [horizon]
use emergent_lattice::{law::Response, worlds, Stepper};
use emergent_lattice_event::{crowded_axes, EventCore};
use std::time::Instant;

#[repr(C)]
#[derive(Default, Clone, Copy)]
struct Timeval {
    sec: i64,
    usec: i32,
}

/// Darwin `struct rusage`.
#[repr(C)]
#[derive(Default, Clone, Copy)]
struct Rusage {
    utime: Timeval,
    stime: Timeval,
    longs: [i64; 14],
}

extern "C" {
    fn getrusage(who: i32, usage: *mut Rusage) -> i32;
}

fn usage() -> Rusage {
    let mut u = Rusage::default();
    // SAFETY: getrusage fills the struct; RUSAGE_SELF = 0.
    unsafe { getrusage(0, &mut u) };
    u
}

fn cpu_ms(u: &Rusage) -> f64 {
    (u.utime.sec + u.stime.sec) as f64 * 1e3 + (u.utime.usec + u.stime.usec) as f64 / 1e3
}

const SEED: u64 = 2718281828;

fn main() {
    let a: Vec<String> = std::env::args().skip(1).collect();
    let n: u64 = a.get(1).and_then(|s| s.parse().ok()).unwrap_or(1024);
    let (w, mut horizon) = match a.first().map(String::as_str).unwrap_or("gas") {
        "gas" => (worlds::gas(n, 0.1, 1024, 256, SEED), 1024),
        "random" => (worlds::random(n, 1_000_000, 1024, 1, SEED, Response::Pass), 4096),
        "horizon" => (worlds::random(4096, 1_000_000, 1024, 1, SEED, Response::Pass), n as i64),
        "mixed" => (worlds::mixed(n, 512, SEED), 2048),
        "crowded" => crowded_axes(n, 1024, SEED),
        other => panic!("unknown world {other}"),
    };
    if let Some(h) = a.get(2).and_then(|s| s.parse().ok()) {
        horizon = h;
    }
    let mut e = EventCore::new(w, false).unwrap();
    struct Unit {
        ms: f64,
        cpu: f64,
        ops: u64,
        minflt: i64,
        majflt: i64,
        vcsw: i64,
        ivcsw: i64,
        ticks: (i64, i64),
        grew: bool,
    }
    let mut units = Vec::new();
    let t0 = Instant::now();
    while e.tick() < horizon && t0.elapsed().as_secs_f64() < 60.0 {
        let (u0, f0, tick0, ops0) = (usage(), e.footprint(), e.tick(), e.metrics().ops);
        let t = Instant::now();
        e.advance(horizon, 4096);
        let ms = t.elapsed().as_secs_f64() * 1e3;
        let (u1, f1) = (usage(), e.footprint());
        let grew = f1.calendar_cap != f0.calendar_cap || f1.cells_cap != f0.cells_cap;
        units.push(Unit {
            ms,
            cpu: cpu_ms(&u1) - cpu_ms(&u0),
            ops: e.metrics().ops - ops0,
            minflt: u1.longs[4] - u0.longs[4],
            majflt: u1.longs[5] - u0.longs[5],
            vcsw: u1.longs[12] - u0.longs[12],
            ivcsw: u1.longs[13] - u0.longs[13],
            ticks: (tick0, e.tick()),
            grew,
        });
    }
    let total = t0.elapsed().as_secs_f64();
    let mut ms: Vec<f64> = units.iter().map(|u| u.ms).collect();
    ms.sort_by(|a, b| a.total_cmp(b));
    let q = |p: f64| ms[((ms.len() - 1) as f64 * p) as usize];
    let m = e.metrics();
    println!(
        "{} units, {total:.2} s, tick {} of {horizon}; unit ms p50 {:.3} p99 {:.3} p99.9 {:.3} max {:.3}; ops/fired {:.1}, pred/ops {:.3}, rebuilds {}, classes {}",
        units.len(),
        e.tick(),
        q(0.5),
        q(0.99),
        q(0.999),
        q(1.0),
        m.ops as f64 / m.fired.max(1) as f64,
        m.predicates as f64 / m.ops as f64,
        e.rebuilds(),
        e.classes()
    );
    let worst_cpu = units.iter().map(|u| u.cpu).fold(0.0, f64::max);
    let quiet = units.iter().filter(|u| u.ivcsw == 0 && u.minflt == 0).map(|u| u.ms).fold(0.0, f64::max);
    println!(
        "worst unit CPU {worst_cpu:.3} ms; worst wall among units with no involuntary switch or fault {quiet:.3} ms; units with a capacity change: {}",
        units.iter().filter(|u| u.grew).count()
    );
    let mut idx: Vec<usize> = (0..units.len()).collect();
    idx.sort_by(|&a, &b| units[b].ms.total_cmp(&units[a].ms));
    println!("slowest: ms cpu_ms ops minflt majflt vcsw ivcsw ticks realloc");
    for &i in idx.iter().take(12) {
        let u = &units[i];
        println!(
            "  #{i}: {:.3} {:.3} {} {} {} {} {} {:?} {}",
            u.ms, u.cpu, u.ops, u.minflt, u.majflt, u.vcsw, u.ivcsw, u.ticks, u.grew
        );
    }
    println!("footprint {:?}, peak RSS {} MB", e.footprint(), usage().longs[0] >> 20);
}
