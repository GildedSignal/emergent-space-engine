//! The flight sweep: the player's path, flown the way the page flies it (60 frames a second of wall time at a real-time
//! factor, `frame_to` with the frame's budget), under scripted keys. One line per flight: alive or the fault, refusals,
//! the speed reached, the lowest it flew (radius over the planet's), the first impact warning's lead on the loss, the worst
//! frame's CPU time and the presented time's worst lag behind the frame's target. A flight is a script of keys at wall seconds
//! or a pilot that reads the view (brake until the nose-ward speed is gone, burn on).
//!
//! cargo run --release -p emergent-universe --example flight_sweep [-- <rtf> <wall seconds per flight> [<only flights whose name contains>]]
use emergent_universe::fleet::Order;
use emergent_universe::num::to_f64;
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::view::{gather_cached, View, ViewCache, TICK_SECONDS};
use emergent_universe::{Budget, Config};
use std::time::{Duration, Instant};

/// A pilot: from the wall second and the view of the frame, the decision word's keys and level, if it changes.
type Pilot = Box<dyn FnMut(f64, &View) -> Option<(u8, u8)>>;

/// Keys: 1 forward, 2 reverse, 4 left, 8 right. A script is a list of (wall second, keys, level) changes.
fn script(changes: Vec<(f64, u8, u8)>) -> Pilot {
    let mut next = 0;
    Box::new(move |wall, _| {
        let mut out = None;
        while next < changes.len() && changes[next].0 <= wall {
            out = Some((changes[next].1, changes[next].2));
            next += 1;
        }
        out
    })
}

/// The speed along the nose against the planet (the doll's frame): positive while the ship still moves the way it points.
fn along(v: &View) -> f64 {
    v.doll_beta[0] * v.heading[0] + v.doll_beta[1] * v.heading[1]
}

/// Brake (reverse at `level`) from the first second until the nose-ward speed is gone (the ship is at rest against the planet,
/// to within a kick), then `then`: coast, or burn forward at the same level until the speed is the starting speed again.
fn brake(level: u8, burn_out: bool) -> Pilot {
    let (mut phase, mut v0) = (0u8, 0f64);
    Box::new(move |wall, v| match phase {
        0 if wall >= 1.0 => {
            phase = 1;
            v0 = along(v);
            Some((2, level))
        }
        1 if along(v) <= 0.0 => {
            phase = 2;
            Some(if burn_out { (1, level) } else { (0, level) })
        }
        2 if burn_out && along(v) >= v0 => {
            phase = 3;
            Some((0, level))
        }
        _ => None,
    })
}

fn flights() -> Vec<(String, Pilot)> {
    let mut v: Vec<(String, Pilot)> = vec![("coast".into(), script(vec![]))];
    for level in [0u8, 2, 4, 6, 8, 10, 12, 15] {
        v.push((format!("forward L{level} (prograde)"), script(vec![(1.0, 1, level)])));
    }
    for level in [0u8, 2, 4, 8] {
        v.push((format!("reverse L{level} (held)"), script(vec![(1.0, 2, level)])));
    }
    for level in [2u8, 4, 8] {
        v.push((format!("brake to rest L{level}"), brake(level, false)));
        v.push((format!("brake to rest, burn out L{level}"), brake(level, true)));
    }
    for level in [2u8, 8] {
        v.push((format!("turn left then burn L{level}"), script(vec![(1.0, 4, level), (2.0, 0, level), (2.5, 1, level), (8.0, 0, level)])));
        v.push((format!("burn, coast, brake L{level}"), script(vec![(1.0, 1, level), (6.0, 0, level), (9.0, 2, level), (14.0, 0, level)])));
    }
    v.push(("throttle sweep 0→15→0".into(), script((0..32).map(|i| (1.0 + i as f64 * 0.5, 1, if i < 16 { i as u8 } else { 31 - i as u8 })).collect())));
    v.push(("key mashing".into(), script((0..120).map(|i| (1.0 + i as f64 * 0.1, [1, 4, 2, 8, 5, 9, 0, 6][i % 8], (i % 16) as u8)).collect())));
    v
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let rtf: f64 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(100.0);
    let seconds: f64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(20.0);
    let only = args.get(3).cloned().unwrap_or_default();
    let frames = (seconds * 60.0) as usize;
    println!("rtf {rtf}, {seconds} s of wall time per flight ({frames} frames at 60 Hz)");
    println!("{:<34} {:>6} {:>8} {:>10} {:>8} {:>9} {:>8} {:>8}  {}", "flight", "alive", "refusals", "max |v|/c", "min r/R", "warned s", "worst ms", "lag s", "fault, or the loss");
    for (name, mut pilot) in flights().into_iter().filter(|(n, _)| n.contains(&only)) {
        let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
        let mut cache = ViewCache::default();
        let (mut worst, mut lag, mut vmax, mut rmin) = (Duration::ZERO, 0f64, 0f64, f64::MAX);
        let mut warned = None;
        let mut lost_at = None;
        for f in 0..frames {
            let wall = f as f64 / 60.0;
            if let Some(view) = gather_cached(&p.u, &p.names, &mut cache) {
                if let Some((keys, level)) = pilot(wall, &view) {
                    let t = p.u.now;
                    let _ = p.u.input(t, word(keys, level));
                }
                if warned.is_none() && view.impact.is_some() {
                    warned = Some(view.tick);
                }
            }
            let start = Instant::now();
            let frame = p.u.frame_to(1.0 / 60.0, rtf, Budget { events: u64::MAX, until: Some(start + Duration::from_millis(12)) }, i64::MAX);
            worst = worst.max(start.elapsed());
            lag = lag.max((frame.target - frame.presented) as f64 * TICK_SECONDS);
            let rec = p.u.rec(p.player);
            if !rec.alive {
                lost_at = Some(frame.presented);
                break;
            }
            if let Ok((x, v)) = rec.b.cartesian(frame.presented.max(rec.b.event_time)) {
                vmax = vmax.max((to_f64(v[0]).powi(2) + to_f64(v[1]).powi(2)).sqrt());
                if rec.b.doll != 0 {
                    rmin = rmin.min((to_f64(x[0]).powi(2) + to_f64(x[1]).powi(2)).sqrt() / to_f64(p.u.dolls[rec.b.doll as usize].surface));
                }
            }
        }
        let rec = p.u.rec(p.player);
        let end = match (rec.alive, lost_at) {
            (false, Some(t)) => gather_cached(&p.u, &p.names, &mut cache).and_then(|v| v.loss).unwrap_or_else(|| format!("lost at tick {t}")),
            _ => rec.fault.map(|f| format!("{f:?}")).unwrap_or_default(),
        };
        let warn = match (warned, lost_at) {
            (Some(w), Some(l)) => format!("{:.0}", (l - w) as f64 * TICK_SECONDS),
            (Some(_), None) => "yes".to_string(),
            _ => "-".to_string(),
        };
        let rmin = if rmin == f64::MAX { "-".to_string() } else { format!("{rmin:.3}") };
        println!("{:<34} {:>6} {:>8} {:>10.6} {:>8} {:>9} {:>8.2} {:>8.3}  {}", name, rec.alive, rec.refusals, vmax, rmin, warn, worst.as_secs_f64() * 1e3, lag, end);
    }
}
