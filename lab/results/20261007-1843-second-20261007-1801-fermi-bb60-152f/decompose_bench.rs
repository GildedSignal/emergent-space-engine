// Decomposition bench v2: the plane's distinct kicks (same replay as xtask universe
// --kick-bench, same input script); for every kick that rebinds, time a fresh
// `Orbit::compile` on the exact key the new entry holds (the recompile the kick
// paid or cached), plus the whole-kick cost. No shipped file is edited.
use emergent_space::binding::Trajectory;
use emergent_space::orbit::Orbit;
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::{body::What, step, Budget, Config, Kind};
use std::time::Instant;

fn script(frame: usize) -> u8 {
    let slot = frame / 240;
    if frame % 240 < 20 { [1, 9, 2, 4, 1, 1 | 4, 2, 8][slot % 8] } else { 0 }
}

#[derive(Default)]
struct Pop {
    kicks: u64,
    kick_ns: u128,
    rebinds: u64,
    compile_ns: u128,
    cycles: u64,
    passages: u64,
    compile_err: u64,
}

fn main() {
    let seed = std::env::args().nth(1).and_then(|s| s.parse().ok()).unwrap_or(1);
    let seconds = 30.0f64;
    let rtf = 100.0f64;
    let p = plane(Config::default(), seed, Order::Sparse, 1, 48).expect("the plane");
    let mut u = p.u;
    let made_n = u.n_bodies();
    let mut last: Vec<Option<i64>> = vec![None; made_n];
    let mut keys = 0u8;
    let (mut made, mut leavers) = (Pop::default(), Pop::default());
    let mut ship_seconds: f64 = 0.0;
    let wall = Instant::now();
    let mut frames = 0usize;
    for n in 1..=(seconds * 60.0) as usize {
        if wall.elapsed().as_secs_f64() >= 55.0 { eprintln!("cut at frame {n}"); break; }
        let now = u.now;
        if keys != script(n) { keys = script(n); u.input(now, keys).expect("input"); }
        last.resize(u.n_bodies(), None);
        let mut live = 0usize;
        for (i, seen) in last.iter_mut().enumerate() {
            let rec = u.rec(i);
            if rec.kind != Kind::Ship || !rec.alive { continue; }
            live += 1;
            let Some(item) = rec.plan.first().copied() else { continue };
            if !matches!(item.what, What::Kick(_)) || *seen == Some(item.t) { continue; }
            *seen = Some(item.t);
            let t0 = Instant::now();
            let upd = step::process(&u.ctx(), i, rec);
            let el = t0.elapsed().as_nanos();
            let pop = if i < made_n { &mut made } else { &mut leavers };
            pop.kicks += 1;
            pop.kick_ns += el;
            if let Some(e) = &upd.new_entry {
                pop.rebinds += 1;
                match &e.trajectory {
                    Trajectory::Cycle(_) => pop.cycles += 1,
                    Trajectory::Passage(_) => pop.passages += 1,
                }
                // Fresh compile of the exact key (cold; what a memo miss pays).
                let t1 = Instant::now();
                let r = Orbit::compile(e.trajectory.key());
                pop.compile_ns += t1.elapsed().as_nanos();
                if r.is_err() { pop.compile_err += 1; }
            }
        }
        u.frame(1.0 / 60.0, rtf, Budget::unlimited());
        ship_seconds += live as f64 * rtf / 60.0;
        u.settle(u.now);
        frames = n;
    }
    for (name, p) in [("made", &made), ("leavers", &leavers)] {
        println!("{name}: kicks {} {:.1} us/kick | rebinds {} (cycles {} passages {}) | fresh-compile {:.1} us/rebind ({:.0}% of kick time) err {}",
            p.kicks, p.kick_ns as f64 / p.kicks.max(1) as f64 / 1000.0,
            p.rebinds, p.cycles, p.passages,
            p.compile_ns as f64 / p.rebinds.max(1) as f64 / 1000.0,
            100.0 * p.compile_ns as f64 / p.kick_ns.max(1) as f64, p.compile_err);
    }
    let kicks = made.kicks + leavers.kicks;
    println!("cadence: {} distinct kicks / {:.0} ship-game-seconds = {:.2e} kicks/s/game-s/body",
        kicks, ship_seconds, kicks as f64 / ship_seconds);
    println!("frames {} wall {:.2}s seed {}", frames, wall.elapsed().as_secs_f64(), seed);
}
