//! Gate F1, smooth flight (frozen by the integrator, 12 October): the page's frame loop at a real-time factor (60 frames a
//! second of wall time, `frame_to` with a 12 ms engine budget), 20 s of wall time a flight, every throttle level 0–15 held
//! forward and in reverse, and the older flights. Zero frames over the 12 ms budget after the first second, and a lag of
//! zero, in every flight. One line per flight: the worst frame and the worst lag over the whole flight and after the first
//! second, the frames over the budget after it, and the events a frame carried.
//!
//! cargo run --release -p emergent-universe --example frame_f1 [-- <rtf> <wall seconds per flight> [<only flights whose name contains>]]
use emergent_universe::fleet::Order;
use emergent_universe::num::to_f64;
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};
use std::time::{Duration, Instant};

/// Keys: 1 forward, 2 reverse, 4 left, 8 right. A flight is a list of (wall second, keys, level) changes.
pub fn flights() -> Vec<(String, Vec<(f64, u8, u8)>)> {
    let mut v: Vec<(String, Vec<(f64, u8, u8)>)> = vec![("coast".into(), vec![])];
    for level in 0u8..=15 {
        v.push((format!("forward L{level}"), vec![(1.0, 1, level)]));
    }
    for level in 0u8..=15 {
        v.push((format!("reverse L{level}"), vec![(1.0, 2, level)]));
    }
    for level in [2u8, 8] {
        v.push((format!("turn left then burn L{level}"), vec![(1.0, 4, level), (2.0, 0, level), (2.5, 1, level), (8.0, 0, level)]));
        v.push((format!("burn, coast, brake L{level}"), vec![(1.0, 1, level), (6.0, 0, level), (9.0, 2, level), (14.0, 0, level)]));
    }
    v.push(("throttle sweep 0→15→0".into(), (0..32).map(|i| (1.0 + i as f64 * 0.5, 1, if i < 16 { i as u8 } else { 31 - i as u8 })).collect()));
    v.push(("key mashing".into(), (0..120).map(|i| (1.0 + i as f64 * 0.1, [1, 4, 2, 8, 5, 9, 0, 6][i % 8], (i % 16) as u8)).collect()));
    v
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let rtf: f64 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(100.0);
    let seconds: f64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(20.0);
    let only = args.get(3).cloned().unwrap_or_default();
    let frames = (seconds * 60.0) as usize;
    let budget_ms = 12.0;
    println!("F1 sweep: rtf {rtf}, {seconds} s of wall time per flight ({frames} frames at 60 Hz), engine budget {budget_ms} ms; 'late' = frames over the budget after the first second");
    println!("{:<30} {:>5} {:>6} {:>9} {:>8} {:>8} {:>7} {:>8} {:>5} {:>7} {:>7}  {}", "flight", "alive", "frames", "max|v|/c", "worst ms", "late ms", "lag s", "late lag", "late", "ev p50", "ev max", "fault");
    let mut total_late = 0usize;
    let mut worst_all = Duration::ZERO;
    let mut lag_all = 0f64;
    for (name, script) in flights().into_iter().filter(|(n, _)| n.contains(&only)) {
        let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
        let (mut next, mut worst, mut late_worst, mut lag, mut late_lag, mut vmax) = (0usize, Duration::ZERO, Duration::ZERO, 0f64, 0f64, 0f64);
        let (mut late, mut ran) = (0usize, 0usize);
        let mut events: Vec<u64> = Vec::new();
        for f in 0..frames {
            let wall = f as f64 / 60.0;
            while next < script.len() && script[next].0 <= wall {
                let (_, keys, level) = script[next];
                let t = p.u.now;
                let _ = p.u.input(t, word(keys, level));
                next += 1;
            }
            let start = Instant::now();
            let frame = p.u.frame_to(1.0 / 60.0, rtf, Budget { events: u64::MAX, until: Some(start + Duration::from_millis(12)) }, i64::MAX);
            let took = start.elapsed();
            let l = (frame.target - frame.presented) as f64 * TICK_SECONDS;
            ran += 1;
            events.push(frame.events);
            worst = worst.max(took);
            lag = lag.max(l);
            if wall >= 1.0 {
                late_worst = late_worst.max(took);
                late_lag = late_lag.max(l);
                late += (took > Duration::from_millis(12)) as usize;
            }
            let rec = p.u.rec(p.player);
            if !rec.alive {
                break;
            }
            if let Ok((_, v)) = rec.b.cartesian(frame.presented.max(rec.b.event_time)) {
                vmax = vmax.max((to_f64(v[0]).powi(2) + to_f64(v[1]).powi(2)).sqrt());
            }
        }
        let rec = p.u.rec(p.player);
        let fault = rec.fault.map(|f| format!("{f:?}")).unwrap_or_default();
        events.sort_unstable();
        let (p50, max) = (events[events.len() / 2], events[events.len() - 1]);
        println!(
            "{:<30} {:>5} {:>6} {:>9.6} {:>8.2} {:>8.2} {:>7.3} {:>8.3} {:>5} {:>7} {:>7}  {}",
            name, rec.alive, ran, vmax, worst.as_secs_f64() * 1e3, late_worst.as_secs_f64() * 1e3, lag, late_lag, late, p50, max, fault
        );
        total_late += late;
        worst_all = worst_all.max(late_worst);
        lag_all = lag_all.max(lag);
    }
    println!("F1: {} frames over the budget after the first second; worst late frame {:.2} ms; worst lag {:.3} s", total_late, worst_all.as_secs_f64() * 1e3, lag_all);
}
