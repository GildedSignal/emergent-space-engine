//! How far apart in time the bodies are: after a flight in the page's frame loop, for every body, the age of its last
//! anchoring (now − the tick its current tube was fitted at) and the future its tube already covers (its next item − now),
//! in game seconds, as percentiles (no means), and the backlog (bodies whose next item is already past).
//!
//! cargo run --release -p emergent-universe --example skew [-- <extra bodies> <wall seconds> <keys> <level>]
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::thrust::word;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};
use std::time::{Duration, Instant};

fn pct(v: &mut [f64]) -> String {
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let at = |q: f64| v[((v.len() - 1) as f64 * q) as usize];
    format!("min {:.3e}  p10 {:.3e}  p50 {:.3e}  p90 {:.3e}  p99 {:.3e}  max {:.3e}", v[0], at(0.1), at(0.5), at(0.9), at(0.99), v[v.len() - 1])
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let extra: usize = a.get(1).and_then(|s| s.parse().ok()).unwrap_or(10_000);
    let seconds: f64 = a.get(2).and_then(|s| s.parse().ok()).unwrap_or(20.0);
    let (keys, level): (u8, u8) = (a.get(3).and_then(|s| s.parse().ok()).unwrap_or(0), a.get(4).and_then(|s| s.parse().ok()).unwrap_or(0));
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, extra).unwrap();
    for f in 0..(seconds * 60.0) as usize {
        if f == 60 && keys != 0 {
            let t = p.u.now;
            let _ = p.u.input(t, word(keys, level));
        }
        let start = Instant::now();
        p.u.frame_to(1.0 / 60.0, 100.0, Budget { events: u64::MAX, until: Some(start + Duration::from_millis(12)) }, i64::MAX);
    }
    let now = p.u.now;
    let n = p.u.bodies().len();
    let (mut age, mut ahead, mut backlog, mut none) = (Vec::new(), Vec::new(), 0usize, 0usize);
    for i in 0..n {
        let r = p.u.rec(i);
        if !r.alive {
            continue;
        }
        age.push((now - r.b.event_time) as f64 * TICK_SECONDS);
        match p.u.bodies().next_time(i) {
            Some(t) if t < now => backlog += 1,
            Some(t) => ahead.push((t - now) as f64 * TICK_SECONDS),
            None => none += 1,
        }
    }
    println!("{n} bodies, {seconds} s of wall at rtf 100 (game time now {:.0} s), keys {keys} level {level}", now as f64 * TICK_SECONDS);
    println!("age of the current tube (game s):   {}", pct(&mut age));
    if !ahead.is_empty() {
        println!("future already covered (game s):    {}", pct(&mut ahead));
    }
    println!("next item already past (backlog): {backlog}; no item planned (a pure tube until observed): {none}");
}
