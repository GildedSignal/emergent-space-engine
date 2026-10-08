//! Lab instrument (run 20261008-2031-constraint-4b27): where the plane frame's view time goes.
//! Drives the same scene and frame loop as `xtask universe --bench`, times `gather_cached`
//! per frame and reads the sub-marks view.rs accumulates (player prologue, bodies loop,
//! fleets loop), plus the readout count and a direct per-`state_rate` timing.
use emergent_universe::fleet::Order;
use emergent_universe::observe::state_rate;
use emergent_universe::scenario::plane;
use emergent_universe::view::{gather, gather_cached, prof, ViewCache};
use emergent_universe::{Budget, Config};
use std::time::Instant;

fn pct(v: &mut [f64], p: f64) -> f64 {
    v.sort_by(f64::total_cmp);
    v.get(((v.len().saturating_sub(1)) as f64 * p).ceil() as usize).copied().unwrap_or(0.0)
}

fn main() {
    let rtf: f64 = std::env::args().nth(1).and_then(|a| a.parse().ok()).unwrap_or(100.0);
    let members: u64 = std::env::args().nth(2).and_then(|a| a.parse().ok()).unwrap_or(48);
    let frames: usize = std::env::args().nth(3).and_then(|a| a.parse().ok()).unwrap_or(1800);
    let seed: u64 = std::env::args().nth(4).and_then(|a| a.parse().ok()).unwrap_or(1);
    let p = plane(Config::default(), seed, Order::Sparse, 1, members).expect("the plane");
    let names = p.names.clone();
    let mut u = p.u;
    let mut cache = ViewCache::default();
    let (mut tot, mut m0, mut m1, mut m2) = (Vec::new(), Vec::new(), Vec::new(), Vec::new());
    let (mut reads_v, mut seen_v) = (Vec::new(), Vec::new());
    let (mut worst_dir, mut worst_ls, mut worst_shift, mut diffs) = (0.0f64, 0.0f64, 0.0f64, 0u64);
    let mut worst_who = String::new();
    let mut gate_counts = [0u64; 4];
    let wall = Instant::now();
    for n in 1..=frames {
        if wall.elapsed().as_secs_f64() >= 80.0 {
            eprintln!("stopping at frame {n}");
            break;
        }
        u.frame_to(1.0 / 60.0, rtf, Budget::wall(5.0), i64::MAX);
        let t0 = Instant::now();
        let v = gather_cached(&u, &names, &mut cache).expect("view");
        let us = t0.elapsed().as_secs_f64() * 1e6;
        let m = prof::take();
        tot.push(us);
        m0.push(m[0] as f64);
        m1.push(m[1] as f64);
        m2.push(m[2] as f64);
        reads_v.push(cache.readouts as f64);
        gate_counts = emergent_universe::view::prof::gate_take();
        seen_v.push(v.seen.len() as f64);
        // Every 100 frames: the exact (cold) gather on the same state, diffed against the gated one.
        if n % 100 == 0 {
            if let Some(x) = gather(&u, &names) {
                let xb: std::collections::HashMap<usize, _> = x.seen.iter().map(|s| (s.id, s)).collect();
                for s in &v.seen {
                    if let Some(e) = xb.get(&s.id) {
                        let dd = (s.direction[0] - e.direction[0]).abs().max((s.direction[1] - e.direction[1]).abs());
                        if dd > worst_dir {
                            worst_who = format!("frame {n} id {} name {} kind {} ls {:.4} vs {:.4} shift {:.4} vs {:.4}", s.id, s.name, s.kind, s.light_seconds, e.light_seconds, s.shift, e.shift);
                        }
                        worst_dir = worst_dir.max(dd);
                        worst_ls = worst_ls.max((s.light_seconds - e.light_seconds).abs() / e.light_seconds.max(1e-9));
                        worst_shift = worst_shift.max((s.shift - e.shift).abs() / e.shift.abs().max(1e-9));
                        diffs += 1;
                    }
                }
            }
        }
    }
    // A cold gather (no memo) on the final state, 30 samples: what the crossing search costs
    // when the guess is not carried, and how many readouts it needs.
    let mut cold = Vec::new();
    let mut cold_reads = 0u64;
    for _ in 0..30 {
        let t0 = Instant::now();
        let _ = gather(&u, &names);
        cold.push(t0.elapsed().as_secs_f64() * 1e6);
    }
    let _ = gather(&u, &names);
    let _ = &mut cold_reads;
    // Direct per-readout cost: state_rate over every live body at the presented tick, 30 rounds.
    let t0 = Instant::now();
    let mut calls = 0u64;
    for _ in 0..30 {
        for i in 0..u.n_bodies() {
            if u.bodies().alive(i) && state_rate(&u.ctx(), i, u.now).is_ok() {
                calls += 1;
            }
        }
    }
    let per_state_rate_us = t0.elapsed().as_secs_f64() * 1e6 / calls as f64;
    // The atoms of state_rate, timed separately over the same bodies (30 rounds each):
    let ctx = u.ctx();
    let (mut t_bind, mut t_cart, mut t_sec, mut t_ramp) = (0u128, 0u128, 0u128, 0u128);
    let mut n = 0u64;
    for _ in 0..30 {
        for i in 0..u.n_bodies() {
            if !u.bodies().alive(i) {
                continue;
            }
            let b0 = ctx.bodies.binding_at(i, u.now);
            let t0 = Instant::now();
            let b = ctx.bodies.binding_at(i, u.now);
            t_bind += t0.elapsed().as_nanos();
            if let Some(b) = b {
                let t0 = Instant::now();
                let _ = b.cartesian(u.now);
                t_cart += t0.elapsed().as_nanos();
                let d = b.doll;
                let t0 = Instant::now();
                let _ = ctx.secondaries(d, u.now, i);
                t_sec += t0.elapsed().as_nanos();
            }
            let t0 = Instant::now();
            let _ = emergent_universe::observe::ramped(&ctx, i, u.now);
            t_ramp += t0.elapsed().as_nanos();
            n += 1;
        }
    }
    println!(
        "atoms (ns each, {n} samples): binding_at {:.0} cartesian {:.0} secondaries {:.0} ramped {:.0}",
        t_bind as f64 / n as f64,
        t_cart as f64 / n as f64,
        t_sec as f64 / n as f64,
        t_ramp as f64 / n as f64
    );
    println!(
        "rtf {rtf} members {members} frames {} bodies_end {}\n\
         gather_us p50 {:.1} p99 {:.1}\n\
         player_prologue_us_p50 {:.1}\n\
         bodies_loop_us_p50 {:.1}\n\
         fleets_loop_us_p50 {:.1}\n\
         readouts_per_frame_p50 {:.1}\n\
         seen_per_frame_p50 {:.1}\n\
         gather_cold_us_p50 {:.1}\n\
         state_rate_us_each {:.3} ({} calls)",
        tot.len(),
        u.n_bodies(),
        pct(&mut tot, 0.5),
        pct(&mut tot, 0.99),
        pct(&mut m0, 0.5),
        pct(&mut m1, 0.5),
        pct(&mut m2, 0.5),
        pct(&mut reads_v, 0.5),
        pct(&mut seen_v, 0.5),
        pct(&mut cold, 0.5),
        per_state_rate_us,
        calls
    );
    println!(
        "display_diff vs exact ({} matched, every 100th frame): max_dir {:.3e} max_rel_ls {:.3e} max_rel_shift {:.3e}",
        diffs, worst_dir, worst_ls, worst_shift
    );
    println!(
        "gate (median frame): mark_changed {} periapsis_changed {} no_root {} checkpoints {}",
        gate_counts[0],
        gate_counts[1],
        gate_counts[2],
        gate_counts[3]
    );
    println!("worst offender: {worst_who}");

}
