//! The flight sweep: the player's path, flown the way the page flies it (60 frames a second of wall time at a real-time
//! factor, `frame_to` with the frame's budget), under scripted keys. One line per flight: alive or the fault, refusals,
//! the speed reached, the worst frame's CPU time and the presented time's worst lag behind the frame's target.
//!
//! cargo run --release -p emergent-universe --example flight_sweep [-- <rtf> <wall seconds per flight>]
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::{fleet::Order, num::to_f64, Budget, Config};
use std::time::{Duration, Instant};

/// Keys: 1 forward, 2 reverse, 4 left, 8 right. A flight is a list of (wall second, keys, level) changes.
fn flights() -> Vec<(String, Vec<(f64, u8, u8)>)> {
    let mut v: Vec<(String, Vec<(f64, u8, u8)>)> = vec![("coast".into(), vec![])];
    for level in [0u8, 2, 4, 6, 8, 10, 12, 15] {
        v.push((format!("forward L{level}"), vec![(1.0, 1, level)]));
    }
    for level in [0u8, 2, 4, 8] {
        v.push((format!("reverse L{level} (brake)"), vec![(1.0, 2, level)]));
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
    let frames = (seconds * 60.0) as usize;
    println!("rtf {rtf}, {seconds} s of wall time per flight ({frames} frames at 60 Hz)");
    println!("{:<30} {:>8} {:>9} {:>11} {:>10} {:>10}  {}", "flight", "alive", "refusals", "max |v|/c", "worst ms", "max lag s", "fault");
    for (name, script) in flights() {
        let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
        let (mut next, mut worst, mut lag, mut vmax) = (0usize, Duration::ZERO, 0f64, 0f64);
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
            worst = worst.max(start.elapsed());
            lag = lag.max((frame.target - frame.presented) as f64 * emergent_universe::view::TICK_SECONDS);
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
        println!("{:<30} {:>8} {:>9} {:>11.6} {:>10.2} {:>10.3}  {}", name, rec.alive, rec.refusals, vmax, worst.as_secs_f64() * 1e3, lag, fault);
    }
}
