//! The flip gate's record (lab 20261014-2130, second author on 20261014-2012-system-a669): one ladder
//! flight — the plane with N more ships, flown as the page flies it — reporting the compile stream
//! (`from_keyed`'s fresh compiles and reuses), the digest at the canonical cut, and the map's counters.
//! Run it with and without `ES_KEY_BITS=shape,scale`: unset, the gate compares exact keys (a pure
//! memo, digest-neutral); set, the key is coarsened before the compile and the residual carries what
//! the coarser fit discards.
//!
//! cargo run --release -p emergent-universe --example key_dial [-- <N> <rtf> <wall seconds> [<keys> <level>]]
use emergent_space::binding::keyed_counts;
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::thrust::word;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};
use std::time::Instant;

fn main() {
    let a: Vec<String> = std::env::args().skip(1).collect();
    let n: usize = a.first().and_then(|s| s.parse().ok()).unwrap_or(3000);
    let rtf: f64 = a.get(1).and_then(|s| s.parse().ok()).unwrap_or(1000.0);
    let seconds: f64 = a.get(2).and_then(|s| s.parse().ok()).unwrap_or(20.0);
    let (keys, level): (u8, u8) = (
        a.get(3).and_then(|s| s.parse().ok()).unwrap_or(0),
        a.get(4).and_then(|s| s.parse().ok()).unwrap_or(0),
    );
    let cut = (seconds * rtf / TICK_SECONDS) as i64;
    let t0 = Instant::now();
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, n).unwrap();
    let build = t0.elapsed().as_secs_f64();
    if keys != 0 {
        p.u.schedule((1.0 * rtf / TICK_SECONDS) as i64, word(keys, level)).unwrap();
    }
    for _ in 0..400_000 {
        if p.u.now >= cut {
            break;
        }
        p.u.frame_to(1.0 / 60.0, rtf, Budget::unlimited(), cut);
    }
    p.u.settle(cut);
    let (compiled, reused) = keyed_counts();
    let s = p.u.stats;
    println!(
        "N {} rtf {} cut {} script {} | digest {} | kicks {} encounters {} contacts {} | compiles {} reused {} (reuse {:.3} of cycle fits, {:.2} compiles/kick) | refused {} lost {} handoffs {} boundaries {} | build {:.1}s flight {:.1}s",
        n, rtf, cut, if keys == 0 { "coast".to_string() } else { format!("L{level}") },
        p.u.digest(), s.kicks, s.encounters, p.u.contacts,
        compiled, reused, reused as f64 / (compiled + reused).max(1) as f64, compiled as f64 / s.kicks.max(1) as f64,
        s.refused, s.lost, s.handoffs, s.boundaries, build, t0.elapsed().as_secs_f64() - build,
    );
}
