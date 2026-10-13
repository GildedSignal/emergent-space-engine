//! The N ladder's digests: `Universe::digest()` at a canonical cut on the ladder's populations (the plane with N more ships), scripted
//! flights flown as the page flies them, on four schedules (unlimited budget, 25 events a frame, four threads, a 3 ms wall budget) that
//! must agree; recorded before a change to the frame's bookkeeping and compared after it (`diff` the output files): the bookkeeping
//! (queues, prune, scans) must not move a bit. The belt flights burn through the star's doll, so the player's scans meet the belt.
//!
//! cargo run --release -p emergent-universe --example ladder_digest [-- <only cases whose name contains>]
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::thrust::word;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};

type Script = Vec<(f64, u8, u8)>;

/// (name, N, rtf, wall seconds to the cut, script of (wall second, keys, level)).
fn cases() -> Vec<(String, usize, f64, f64, Script)> {
    let mut v = Vec::new();
    for n in [100usize, 1000, 3000] {
        v.push((format!("N={n} coast"), n, 100.0, 20.0, vec![]));
        v.push((format!("N={n} forward L8"), n, 100.0, 20.0, vec![(1.0, 1, 8)]));
        v.push((format!("N={n} key mashing"), n, 100.0, 12.0, (0..120).map(|i| (1.0 + i as f64 * 0.1, [2, 4, 1, 8, 6, 9, 0, 5][i % 8], (i % 16) as u8)).collect()));
    }
    // Through the belt: forward L10 from 1 s to 4 s at rtf 3000, then coast to the cut (the player is in the star's doll among the belt's bodies).
    for n in [1000usize, 3000] {
        v.push((format!("N={n} belt crossing L10"), n, 3000.0, 8.0, vec![(1.0, 1, 10), (4.0, 0, 10)]));
    }
    v
}

fn run(n: usize, rtf: f64, script: &Script, cut: i64, budget: Budget, threads: usize) -> (String, u64, u64, u64) {
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, threads, 48, n).unwrap();
    for &(wall, keys, level) in script {
        let t = (wall * rtf / TICK_SECONDS) as i64;
        p.u.schedule(t, word(keys, level)).unwrap();
    }
    for _ in 0..400_000 {
        if p.u.now >= cut {
            break;
        }
        p.u.frame_to(1.0 / 60.0, rtf, budget, cut);
    }
    p.u.settle(cut);
    (p.u.digest(), p.u.stats.kicks, p.u.stats.encounters, p.u.contacts)
}

fn main() {
    let only = std::env::args().nth(1).unwrap_or_default();
    let mut bad = 0;
    for (name, n, rtf, seconds, script) in cases().into_iter().filter(|c| c.0.contains(&only)) {
        let t0 = std::time::Instant::now();
        let cut = (seconds * rtf / TICK_SECONDS) as i64;
        let a = run(n, rtf, &script, cut, Budget::unlimited(), 1);
        let b = run(n, rtf, &script, cut, Budget::events(25), 1);
        let c = run(n, rtf, &script, cut, Budget::unlimited(), 4);
        let d = run(n, rtf, &script, cut, Budget::wall(3.0), 1);
        let same = a.0 == b.0 && a.0 == c.0 && a.0 == d.0;
        bad += !same as usize;
        println!(
            "{:<28} | {} | kicks {:>6} encounters {:>6} contacts {:>3} | {}  [{:.1} s]",
            name,
            &a.0[..32],
            a.1,
            a.2,
            a.3,
            if same { "4 schedules agree".to_string() } else { format!("SCHEDULES DISAGREE: {} {} {}", &b.0[..16], &c.0[..16], &d.0[..16]) },
            t0.elapsed().as_secs_f64()
        );
    }
    println!("{}", if bad == 0 { "every case: one digest on every schedule" } else { "SCHEDULE DEPENDENCE FOUND" });
}
