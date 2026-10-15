//! Flight certificate for the fit-only bind: the plane's canonical digest and counters must not
//! move when `bind_in` stops paying the dead residual readout.
//! cargo run --release -p emergent-universe --example bindflight [-- <N> <cut ticks>]
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::{Budget, Config};

fn main() {
    let n: usize = std::env::args().nth(1).and_then(|s| s.parse().ok()).unwrap_or(1000);
    let cut: i64 = std::env::args().nth(2).and_then(|s| s.parse().ok()).unwrap_or(4_000_000_000);
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, n).unwrap();
    // Fly at rtf 100 in 1/60 s frames to a canonical cut, unlimited budget, then settle there:
    // the digest after settle(limit) is the same whatever the frames were (frame_to's contract).
    let mut frames = 0u64;
    loop {
        let f = p.u.frame_to(1.0 / 60.0, 100.0, Budget::unlimited(), cut);
        frames += 1;
        if f.presented >= cut || frames > 400_000 {
            break;
        }
    }
    p.u.settle(cut);
    let s = &p.u.stats;
    println!("digest {}", p.u.digest());
    println!("kicks {} opens {} boundaries {} encounters {} frames {}", s.kicks, s.opens, s.boundaries, s.encounters, frames);
}
