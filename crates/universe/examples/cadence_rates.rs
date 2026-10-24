//! Events per body per game-second by class, on the N ladder's population (`scenario::plane_extra`), with each ship of the root doll
//! on its own clock and on the clock of 7 October (`own_clock = false`): the locals on the Moon's orbit and about Home (a planet's
//! doll: `2^step_log2` kicks per their own radial period, the split of docs/law.md, unchanged), the belt (the root doll's clock: an
//! event is a kick or a boundary, so its kicks are half its events) and the plane's own ships. A doll body's events are its kicks,
//! its boundaries and, near the Moon, the changeover's opens and sub-level kicks.
//!
//! cargo run --release -p emergent-universe --example cadence_rates -- <N> <game seconds>
use emergent_universe::fleet::Order;
use emergent_universe::scenario::{ladder_locals, plane_extra};
use emergent_universe::Config;
use emergent_universe::view::TICK_SECONDS;
use std::time::Instant;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let n: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(600);
    let game: f64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(86_400.0);
    for own in [false, true] {
        let t0 = Instant::now();
        let mut p = plane_extra(Config { own_clock: own, ..Config::default() }, 1, Order::Sparse, 1, 48, n).unwrap();
        let locals = ladder_locals(n as u64) as usize;
        let base = p.player - n;
        let classes: [(&str, Vec<usize>); 4] = [
            ("locals on the Moon's orbit", (base..base + locals / 4).collect()),
            ("locals about Home", (base + locals / 4..base + locals).collect()),
            ("belt (root doll)", (base + locals..base + n).collect()),
            ("the plane's own ships", p.ships.iter().copied().filter(|&i| i < base).collect()),
        ];
        let before: Vec<u64> = classes.iter().map(|(_, ids)| ids.iter().map(|&i| p.u.rec(i).events).sum()).collect();
        p.u.settle((game / TICK_SECONDS) as i64);
        println!("own_clock = {own}: {n} ladder ships over {game:.0} game-s ({:.1} s of wall)", t0.elapsed().as_secs_f64());
        for ((name, ids), b) in classes.iter().zip(&before) {
            let after: u64 = ids.iter().map(|&i| p.u.rec(i).events).sum();
            let per = (after - b) as f64 / ids.len().max(1) as f64 / game;
            println!("  {name:<28} {:>6} bodies: {per:.3e} events/body/game-s", ids.len());
        }
    }
}
