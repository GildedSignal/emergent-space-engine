// The frame's tail: every item the engine resolves, one at a time (a budget of one event), timed, and the slowest listed
// with what it was. `tail [SECONDS] [RTF] [SEED] [MEMBERS] [THRESHOLD_US]`. Resolving one item per call changes nothing the
// law decides (a budget moves when work is done, never what), so the digest it prints is the bench's.
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};
use std::time::Instant;

fn main() {
    let a: Vec<String> = std::env::args().skip(1).collect();
    let seconds: f64 = a.first().map(|s| s.parse().unwrap()).unwrap_or(20.0);
    let rtf: f64 = a.get(1).map(|s| s.parse().unwrap()).unwrap_or(1.0);
    let seed: u64 = a.get(2).map(|s| s.parse().unwrap()).unwrap_or(1);
    let members: u64 = a.get(3).map(|s| s.parse().unwrap()).unwrap_or(48);
    let thr: f64 = a.get(4).map(|s| s.parse().unwrap()).unwrap_or(1000.0);
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, members).unwrap();
    let frames = (seconds * 60.0) as usize;
    let mut slow: Vec<(f64, usize, String)> = Vec::new();
    let mut per_frame: Vec<f64> = Vec::new();
    let names = ["planet", "moon", "ship", "player", "fleet"];
    for f in 0..frames {
        let want = (rtf / 60.0 / TICK_SECONDS) as i64;
        let target = p.u.now + want.max(1);
        let fr = Instant::now();
        let mut horizon = p.u.now;
        loop {
            let before = p.u.stats;
            let t0 = Instant::now();
            let adv = p.u.advance(target, Budget::events(1));
            let us = t0.elapsed().as_secs_f64() * 1e6;
            horizon = adv.horizon;
            let s = p.u.stats;
            if adv.events == 0 {
                break;
            }
            if us > thr {
                let k = (0..5).find(|&k| s.items[k] > before.items[k]).map(|k| names[k]).unwrap_or("?");
                slow.push((us, f, format!("{k}: kicks {} opens {} bounds {} handoffs {} slices {} leavers {} dissolved {} lost {} refused {}", s.kicks - before.kicks, s.opens - before.opens, s.boundaries - before.boundaries, s.handoffs - before.handoffs, s.slices - before.slices, s.leavers - before.leavers, s.dissolved - before.dissolved, s.lost - before.lost, s.refused - before.refused)));
            }
        }
        p.u.now = horizon.max(p.u.now);
        per_frame.push(fr.elapsed().as_secs_f64() * 1e3);
    }
    slow.sort_by(|a, b| b.0.total_cmp(&a.0));
    println!("{} items above {thr} us; frames above 5 ms: {}", slow.len(), per_frame.iter().filter(|&&m| m > 5.0).count());
    for (us, f, what) in slow.iter().take(25) {
        println!("  frame {f:>5} {us:>9.0} us  {what}");
    }
    p.u.settle(p.u.now);
    println!("digest {}", p.u.digest());
}
