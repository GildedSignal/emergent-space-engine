//! Lab 20261012-0036-quant-115e (quant lens): two measurements on the shipped plane.
//!
//! A. The event's stage budget: settle the default plane scene and split every resolved item's
//!    cost into `step::process` (and its internal stages) against `apply` (+ `root_state`), with
//!    per-What latency percentiles — the mean hides what the frame pays at p99.
//! B. The per-frame scheduler tax: `advance` rekeys every body's deadline each presented frame.
//!    A ladder of N extra Home orbiters (all kicked, all planned) measures the frame's cost with
//!    a zero engine budget — no events resolved at all — plus an inert control (root-doll
//!    haulers, nothing can kick them: pure tubes with no plan).
use emergent_space::orbit::Scalar;
use emergent_universe::fleet::Order;
use emergent_universe::scenario::{plane, AU};
use emergent_universe::{universe, Budget, Config, Kind, OrbitSpec, Universe};
use std::time::Instant;

fn pctl(mut v: Vec<u64>, ps: &[f64]) -> Vec<f64> {
    v.sort_unstable();
    ps.iter()
        .map(|&p| {
            let i = (((v.len() as f64 - 1.0) * p).ceil()) as usize;
            v.get(i).copied().unwrap_or(0) as f64 / 1000.0
        })
        .collect()
}

fn machine() -> String {
    let cpu = std::fs::read_to_string("/proc/cpuinfo").unwrap_or_default();
    let model = cpu
        .lines()
        .find(|l| l.starts_with("model name"))
        .and_then(|l| l.split(':').nth(1))
        .unwrap_or("?")
        .trim()
        .to_string();
    let load = std::fs::read_to_string("/proc/loadavg").unwrap_or_default();
    let avail = std::fs::read_to_string("/proc/meminfo")
        .ok()
        .and_then(|m| m.lines().find(|l| l.starts_with("MemAvailable")).map(|l| l.split_whitespace().nth(1).unwrap_or("?").to_string()))
        .unwrap_or_else(|| "?".into());
    format!("cpu={model}; load={load}; MemAvailable_kB={avail}")
}

fn what_name(c: u8) -> String {
    match c {
        1 => "Crash".into(),
        2 => "Boundary".into(),
        c if (16..32).contains(&c) => format!("Kick({})", c - 16),
        c if (32..48).contains(&c) => format!("Open({})", c - 32),
        _ => format!("code {c}"),
    }
}

fn phase_a() {
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 8).unwrap();
    let horizon = 30_000_000_000i64;
    let t0 = Instant::now();
    p.u.settle(horizon);
    let wall = t0.elapsed();
    let (ev, apply, root_ns, root_n, _rk, _rkn, rq_ns, rq_n) = universe::prof_take();
    let st = step_stages();
    let s = p.u.stats;
    let items = s.kicks + s.opens + s.boundaries;
    println!("== A: stage budget (default plane, settle {horizon} ticks) ==");
    println!("machine: {}", machine());
    println!(
        "wall {:.3?}; items {items} (kicks {}, opens {}, boundaries {}, handoffs {}, lost {}, refused {}); whole-universe {:.1} us/item",
        wall, s.kicks, s.opens, s.boundaries, s.handoffs, s.lost, s.refused,
        wall.as_secs_f64() * 1e6 / items as f64
    );
    println!("digest: {}", p.u.digest());
    let ps = [0.5f64, 0.9, 0.99, 0.999];
    let mut codes: Vec<u8> = ev.iter().map(|(_, c)| *c).collect();
    codes.sort_unstable();
    codes.dedup();
    println!("\n-- step::process per What (us: p50 p90 p99 p99.9 max, n) --");
    for c in codes {
        let sub: Vec<u64> = ev.iter().filter(|(_, w)| *w == c).map(|(n, _)| *n).collect();
        let n = sub.len();
        let mut q = pctl(sub.clone(), &ps);
        q.push(*sub.iter().max().unwrap_or(&0) as f64 / 1000.0);
        println!("{:>10}: {:7.2} {:7.2} {:7.2} {:8.2} {:8.2}  n={n}", what_name(c), q[0], q[1], q[2], q[3], q[4]);
        let ap: Vec<u64> = apply.iter().filter(|(_, w)| *w == c).map(|(n, _)| *n).collect();
        if !ap.is_empty() {
            let mut q = pctl(ap.clone(), &ps);
            q.push(*ap.iter().max().unwrap_or(&0) as f64 / 1000.0);
            println!("{:>10}  apply: {:7.2} {:7.2} {:7.2} {:8.2} {:8.2}", "", q[0], q[1], q[2], q[3], q[4]);
        }
    }
    println!("\n-- kick stages (WH path; us/call and share of kick total) --");
    let kt = st[6] as f64 / 1000.0;
    let names = [
        ("readout", 0usize),
        ("inputs(2nd+tide)", 1),
        ("force", 2),
        ("quantize", 3),
        ("rebind", 4),
        ("kick-post", 5),
    ];
    for (n, i) in names {
        println!("{:>16}: {:7.2} us/call  {:5.1} % of kick", n, st[i] as f64 / 1000.0 / s.kicks.max(1) as f64, 100.0 * st[i] as f64 / st[6].max(1) as f64);
    }
    println!("{:>16}: {:7.2} us/kick (total)", "kick", kt / s.kicks.max(1) as f64);
    println!(
        "{:>16}: {:7.2} us/call  (plan_interval share of boundary: {:5.1} %)",
        "plan_interval",
        st[7] as f64 / 1000.0 / s.boundaries.max(1) as f64,
        100.0 * st[7] as f64 / st[8].max(1) as f64
    );
    println!("{:>16}: {:7.2} us/boundary", "boundary", st[8] as f64 / 1000.0 / s.boundaries.max(1) as f64);
    println!("{:>16}: {:7.2} us/open", "open", st[9] as f64 / 1000.0 / s.opens.max(1) as f64);
    println!("{:>16}: {:7.2} us/call over {} calls (the position cache after every event)", "root_state", root_ns as f64 / 1000.0 / root_n.max(1) as f64, root_n);
    println!(
        "requeue: {:.2} us/call over {} calls; classes: planet {:.1} moon {:.1} ship {:.1} player {:.1} fleet {:.1} us/item (fleet items {})",
        rq_ns as f64 / 1000.0 / rq_n.max(1) as f64,
        rq_n,
        s.cost_ns[0] as f64 / 1000.0 / s.items[0].max(1) as f64,
        s.cost_ns[1] as f64 / 1000.0 / s.items[1].max(1) as f64,
        s.cost_ns[2] as f64 / 1000.0 / s.items[2].max(1) as f64,
        s.cost_ns[3] as f64 / 1000.0 / s.items[3].max(1) as f64,
        s.cost_ns[4] as f64 / 1000.0 / s.items[4].max(1) as f64,
        s.items[4]
    );
    println!("rekey: {} advances in the settle", _rkn);
    let ev_sum: u64 = ev.iter().map(|(n, _)| *n).sum();
    let ap_sum: u64 = apply.iter().map(|(n, _)| *n).sum();
    println!(
        "sums: process {:.1} us/item, apply {:.1} us/item, root_state {:.1} % of apply",
        ev_sum as f64 / 1000.0 / ev.len().max(1) as f64,
        ap_sum as f64 / 1000.0 / ev.len().max(1) as f64,
        100.0 * root_ns as f64 / ap_sum.max(1) as f64
    );
}

fn step_stages() -> [u64; 12] {
    emergent_universe::step::prof_take()
}

struct Lcg(u64);
impl Lcg {
    fn f(&mut self) -> f64 {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        (self.0 >> 11) as f64 / (1u64 << 53) as f64
    }
}

fn phase_b() {
    println!("\n== B: the per-frame scheduler tax (zero engine budget: no events resolved) ==");
    println!("machine: {}", machine());
    println!("{:>8} {:>10} {:>12} {:>12} {:>10} {:>8}", "N_extra", "bodies", "frame_p50", "frame_p99", "rekey", "events");
    for &(k, inert) in &[(0usize, false), (4_000, false), (16_000, false), (64_000, false), (256_000, false), (64_000, true)] {
        let mut p = plane(Config::default(), 1, Order::Sparse, 1, 8).unwrap();
        let mut rng = Lcg(0xC0FFEE_D15EA5);
        let doll = if inert { 0 } else { p.dolls[1] };
        for j in 0..k {
            let spec = if inert {
                let a = (0.5 + 7.5 * rng.f()) * AU as f64;
                OrbitSpec {
                    doll,
                    periapsis: Scalar::raw(a as i128, 0).unwrap(),
                    e_q48: (0.25 * rng.f() * (1u64 << 48) as f64) as u64,
                    clockwise: rng.f() < 0.15,
                    angle: (rng.f() * 4294967296.0) as u32,
                    phase: (rng.f() * 4294967296.0) as u32,
                }
            } else {
                let alt = 1.15 + 0.35 * ((j % 40) as f64) + 0.2 * rng.f();
                OrbitSpec {
                    doll,
                    periapsis: Scalar::raw((4_313.0 * alt * 1024.0) as i128, 8).unwrap(),
                    e_q48: ((0.02 * rng.f()) * (1u64 << 48) as f64) as u64,
                    clockwise: j % 5 == 4,
                    angle: (rng.f() * 4294967296.0) as u32,
                    phase: (rng.f() * 4294967296.0) as u32,
                }
            };
            p.u.add_body(Kind::Ship, spec, Scalar::raw(34, 8).unwrap()).unwrap();
        }
        p.u.start().unwrap();
        let n = p.u.n_bodies();
        let before = p.u.stats.kicks + p.u.stats.opens + p.u.stats.boundaries;
        let mut frames: Vec<u64> = Vec::with_capacity(30);
        for _ in 0..30 {
            let t0 = Instant::now();
            p.u.frame_to(1.0 / 60.0, 1.0, Budget::wall(0.0), i64::MAX);
            frames.push(t0.elapsed().as_nanos() as u64);
        }
        let after = p.u.stats.kicks + p.u.stats.opens + p.u.stats.boundaries;
        let (_, _, _, _, rk, rkn, _, _) = universe::prof_take();
        let q = pctl(frames.clone(), &[0.5, 0.99]);
        println!(
            "{:>8} {:>10} {:>9} us {:>9} us {:>7} us {:>8}",
            if inert { format!("{k} inert") } else { format!("{k}") },
            n,
            format!("{:.1}", q[0]),
            format!("{:.1}", q[1]),
            format!("{:.1}", rk as f64 / 1000.0 / rkn.max(1) as f64),
            after - before
        );
    }
}

fn main() {
    phase_a();
    phase_b();
}
