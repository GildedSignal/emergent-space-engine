//! Frame-loop levers must not move a bit: `Universe::digest()` at a canonical cut, on scripted flights, whatever the
//! schedule. Each flight is a log of (wall second, keys, level) changes turned into decisions at canonical ticks
//! (`schedule`, never a wall-derived tick), flown as the page flies it (frames of 1/60 s at rtf 100) to a cut and
//! settled there. Three schedules per flight (unlimited budget, a budget of 25 events with the rest left to the cut's
//! settle, and four threads) must give one digest, and the digests are compared before and after a change (the file
//! `artifacts/runs/frame/digests_*.txt` holds each run's lines; `diff` them).
//!
//! cargo run --release -p emergent-universe --example frame_digest [-- <wall seconds per flight> [<only flights whose name contains>]]
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};

const RTF: f64 = 100.0;

type Script = Vec<(f64, u8, u8)>;

/// (name, seed, members, script): keys 1 forward, 2 reverse, 4 left, 8 right.
fn flights() -> Vec<(&'static str, u64, u64, Script)> {
    vec![
        ("coast", 1, 48, vec![]),
        ("reverse L8", 1, 48, vec![(1.0, 2, 8)]),
        ("reverse L15", 1, 48, vec![(1.0, 2, 15)]),
        ("forward L12, turn left", 3, 16, vec![(1.0, 1, 12), (3.0, 5, 12), (4.0, 1, 12)]),
        ("burn, coast, brake L8", 3, 16, vec![(1.0, 2, 8), (6.0, 0, 8), (9.0, 1, 8), (14.0, 0, 8)]),
        ("throttle sweep", 1, 48, (0..32).map(|i| (1.0 + i as f64 * 0.5, 2, if i < 16 { i as u8 } else { 31 - i as u8 })).collect()),
        ("key mashing", 7, 48, (0..120).map(|i| (1.0 + i as f64 * 0.1, [2, 4, 1, 8, 6, 9, 0, 5][i % 8], (i % 16) as u8)).collect()),
        ("turn left, burn L8", 7, 48, vec![(1.0, 4, 8), (2.0, 0, 8), (2.5, 2, 8), (8.0, 0, 8)]),
    ]
}

/// One run to the cut: the digest, the tick the frames reached, and the counters.
fn run(seed: u64, members: u64, script: &Script, cut: i64, budget: Budget, threads: usize) -> (String, i64, u64, u64, u64) {
    let mut p = plane(Config::default(), seed, Order::Sparse, threads, members).unwrap();
    if std::env::var("VERIFY").is_ok() {
        p.u.set_encounters(Box::new(emergent_universe::encounter::PlayerNeighbourhood::verifying()));
    }
    for &(wall, keys, level) in script {
        let t = (wall * RTF / TICK_SECONDS) as i64;
        p.u.schedule(t, word(keys, level)).unwrap();
    }
    for _ in 0..200_000 {
        if p.u.now >= cut {
            break;
        }
        p.u.frame_to(1.0 / 60.0, RTF, budget, cut);
    }
    let reached = p.u.now;
    p.u.settle(cut);
    (p.u.digest(), reached, p.u.stats.kicks, p.u.stats.encounters, p.u.contacts)
}

/// The same, every frame on a wall budget of `ms`: whatever the clock lets through, the digest at the cut is the same.
fn run_wall(seed: u64, members: u64, script: &Script, cut: i64, ms: f64) -> (String, i64, u64, u64, u64) {
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, members).unwrap();
    for &(wall, keys, level) in script {
        let t = (wall * RTF / TICK_SECONDS) as i64;
        p.u.schedule(t, word(keys, level)).unwrap();
    }
    for _ in 0..200_000 {
        if p.u.now >= cut {
            break;
        }
        p.u.frame_to(1.0 / 60.0, RTF, Budget::wall(ms), cut);
    }
    let reached = p.u.now;
    p.u.settle(cut);
    (p.u.digest(), reached, p.u.stats.kicks, p.u.stats.encounters, p.u.contacts)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let seconds: f64 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(20.0);
    let only = args.get(2).cloned().unwrap_or_default();
    let cut = (seconds * RTF / TICK_SECONDS) as i64;
    let mut bad = 0;
    for (name, seed, members, script) in flights().into_iter().filter(|f| f.0.contains(&only)) {
        let t0 = std::time::Instant::now();
        let a = run(seed, members, &script, cut, Budget::unlimited(), 1);
        let b = run(seed, members, &script, cut, Budget::events(25), 1);
        let c = run(seed, members, &script, cut, Budget::unlimited(), 4);
        // A wall budget that bites (3 ms): the scans the player's items hold wait for idle time, and the cut's settle answers them.
        let d = run_wall(seed, members, &script, cut, 3.0);
        let same = a.0 == b.0 && a.0 == c.0 && a.0 == d.0;
        bad += !same as usize;
        println!(
            "{:<26} seed {} members {:>2} | {} | kicks {:>5} encounters {:>4} contacts {:>3} | {}  [{:.1} s]",
            name,
            seed,
            members,
            &a.0[..32],
            a.2,
            a.3,
            a.4,
            if same { "4 schedules agree".to_string() } else { format!("SCHEDULES DISAGREE: {} {} {}", &b.0[..16], &c.0[..16], &d.0[..16]) },
            t0.elapsed().as_secs_f64()
        );
    }
    println!("{}", if bad == 0 { "every flight: one digest on every schedule" } else { "SCHEDULE DEPENDENCE FOUND" });
}
