//! What a held throttle's frame spends: one flight at a real-time factor, the page's frame loop, and for every frame its
//! wall time, the events it carried and the cost by kind (planet, moon, ship, player, fleet) from the universe's own
//! counters, and with `--features prof` the stages inside (the rekey, the position walk, the requeue, the kick's readout,
//! sources, field, quantize, rebind and replan). The distribution of frames, then the worst ones.
//!
//! cargo run --release -p emergent-universe --features prof --example frame_cost [-- <rtf> <wall seconds> <keys> <level> [<worst frames shown>]]
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::{Budget, Config};
use std::time::{Duration, Instant};

fn pct(sorted: &[f64], p: f64) -> f64 {
    sorted[(((sorted.len() - 1) as f64) * p).round() as usize]
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let rtf: f64 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(100.0);
    let seconds: f64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(20.0);
    let keys: u8 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(1);
    let level: u8 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(8);
    let shown: usize = args.get(5).and_then(|s| s.parse().ok()).unwrap_or(8);
    let budget_ms: f64 = args.get(6).and_then(|s| s.parse().ok()).unwrap_or(12.0);
    let frames = (seconds * 60.0) as usize;
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
    println!("rtf {rtf}, {seconds} s, keys {keys} level {level} from 1 s, engine budget {budget_ms} ms, {} bodies", p.u.n_bodies());
    let mut rows: Vec<(usize, f64, u64, [u64; 5], [u64; 5], u64)> = Vec::new();
    let mut total = Duration::ZERO;
    let (mut stage_ns, mut stage_calls) = ([0u64; emergent_universe::prof::N], [0u64; emergent_universe::prof::N]);
    let mut stage_rows: Vec<(usize, [u64; emergent_universe::prof::N])> = Vec::new();
    for f in 0..frames {
        if f == 60 {
            let t = p.u.now;
            let _ = p.u.input(t, word(keys, level));
        }
        let s0 = p.u.stats;
        let _ = emergent_universe::prof::take();
        let start = Instant::now();
        let frame = p.u.frame_to(1.0 / 60.0, rtf, Budget { events: u64::MAX, until: Some(start + Duration::from_micros((budget_ms * 1e3) as u64)) }, i64::MAX);
        let took = start.elapsed();
        total += took;
        let s1 = p.u.stats;
        let mut cost = [0u64; 5];
        let mut items = [0u64; 5];
        for k in 0..5 {
            cost[k] = s1.cost_ns[k] - s0.cost_ns[k];
            items[k] = s1.items[k] - s0.items[k];
        }
        let kicks = s1.kicks - s0.kicks;
        rows.push((f, took.as_secs_f64() * 1e3, frame.events, cost, items, kicks));
        if std::env::var("TIMELINE").is_ok() && (58..120).contains(&f) {
            let r = p.u.rec(p.player);
            let (_, v) = r.b.cartesian(frame.presented.max(r.b.event_time)).map(|(x, v)| (x, v)).unwrap_or(([emergent_space::orbit::Scalar::ZERO; 2], [emergent_space::orbit::Scalar::ZERO; 2]));
            let sp = (emergent_universe::num::to_f64(v[0]).powi(2) + emergent_universe::num::to_f64(v[1]).powi(2)).sqrt();
            println!("  f{:>4} {:>7.3} ms ev {:>4} kicks {:>3} doll {} step {:>10} |v| {:.3e} lag {:>9} ticks", f, took.as_secs_f64() * 1e3, frame.events, kicks, r.b.doll, r.step, sp, frame.target - frame.presented);
        }
        let (ns, calls) = emergent_universe::prof::take();
        if f >= 60 {
            for k in 0..emergent_universe::prof::N {
                stage_ns[k] += ns[k];
                stage_calls[k] += calls[k];
            }
            stage_rows.push((f, ns));
        }
        if !p.u.rec(p.player).alive {
            println!("the player was lost at frame {f}");
            break;
        }
    }
    let late: Vec<_> = rows.iter().filter(|r| r.0 >= 60).collect();
    let mut ms: Vec<f64> = late.iter().map(|r| r.1).collect();
    ms.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let mut ev: Vec<f64> = late.iter().map(|r| r.2 as f64).collect();
    ev.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let kicks: u64 = late.iter().map(|r| r.5).sum();
    println!("frames after 1 s: {}  ms p50 {:.3} p90 {:.3} p99 {:.3} max {:.3} mean {:.3}   events p50 {} p99 {} max {}   kicks {} ({:.2}/frame)  over budget {}",
        late.len(), pct(&ms, 0.5), pct(&ms, 0.9), pct(&ms, 0.99), pct(&ms, 1.0), ms.iter().sum::<f64>() / ms.len() as f64, pct(&ev, 0.5), pct(&ev, 0.99), pct(&ev, 1.0), kicks, kicks as f64 / late.len() as f64,
        late.iter().filter(|r| r.1 > budget_ms).count());
    let sum = |k: usize| late.iter().map(|r| r.3[k]).sum::<u64>() as f64 / 1e3;
    let it = |k: usize| late.iter().map(|r| r.4[k]).sum::<u64>();
    let all_ms: f64 = late.iter().map(|r| r.1).sum::<f64>() * 1e3;
    println!("by kind over the {} frames (µs total, items): planet {:.0} ({}), moon {:.0} ({}), ship {:.0} ({}), player {:.0} ({}), fleet {:.0} ({}); frames total {:.0} µs", late.len(), sum(0), it(0), sum(1), it(1), sum(2), it(2), sum(3), it(3), sum(4), it(4), all_ms);
    if emergent_universe::prof::ENABLED {
        println!("stages (µs per frame, calls per frame, ns per call), over the {} frames:", late.len());
        for k in 0..emergent_universe::prof::N {
            if stage_calls[k] > 0 {
                println!("  {:<38} {:>9.1} {:>8.2} {:>10.0}", emergent_universe::prof::NAMES[k], stage_ns[k] as f64 / 1e3 / late.len() as f64, stage_calls[k] as f64 / late.len() as f64, stage_ns[k] as f64 / stage_calls[k] as f64);
            }
        }
    }
    let mut worst: Vec<_> = late.clone();
    worst.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    println!("the {} worst frames: frame, ms, events, kicks | µs by kind planet moon ship player fleet | items by kind", shown);
    for r in worst.iter().take(shown) {
        println!("{:>5} {:>7.3} {:>5} {:>5} | {:>7.0} {:>7.0} {:>7.0} {:>7.0} {:>7.0} | {:?}", r.0, r.1, r.2, r.5, r.3[0] as f64 / 1e3, r.3[1] as f64 / 1e3, r.3[2] as f64 / 1e3, r.3[3] as f64 / 1e3, r.3[4] as f64 / 1e3, r.4);
    }
    if emergent_universe::prof::ENABLED {
        println!("stages of the worst frames (µs): rekey, walk, apply, requeue, process, fit | scans answered, capture | fleet run, fleet advance, hand-out | hand-out: pull, bind, replan");
        for r in worst.iter().take(shown) {
            let ns = stage_rows.iter().find(|x| x.0 == r.0).map(|x| x.1).unwrap_or([0; emergent_universe::prof::N]);
            use emergent_universe::prof::*;
            let us = |k: usize| ns[k] as f64 / 1e3;
            println!(
                "{:>5} {:>7.3} | {:>7.0} {:>7.0} {:>7.0} {:>7.0} {:>7.0} {:>7.0} | {:>7.0} {:>7.0} | {:>7.0} {:>7.0} {:>7.0} | {:>7.0} {:>7.0} {:>7.0}",
                r.0, r.1, us(REKEY), us(ROOT), us(APPLY), us(REQUEUE), us(PROCESS), us(FIT), us(SCANS), us(ENCOUNTERS), us(F_RUN), us(F_ADV), us(HANDOUT), us(H_PULL), us(H_BIND), us(H_REPLAN)
            );
        }
    }
    println!("total engine wall {:.3} s", total.as_secs_f64());
}
