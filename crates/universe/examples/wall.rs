//! Total engine wall of a held throttle's 20 s flight (frames of 1/60 s at rtf 100, 12 ms budget and unlimited), for A/B between two engines.
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::{Budget, Config};
use std::time::{Duration, Instant};
fn main() {
    for (name, keys, level) in [("coast", 0u8, 0u8), ("forward L8", 1, 8), ("reverse L8", 2, 8), ("reverse L12", 2, 12), ("reverse L15", 2, 15)] {
        let mut out = format!("{name:<12}");
        for demand in [false, true] {
            let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
            let (mut total, mut worst) = (Duration::ZERO, Duration::ZERO);
            for f in 0..1200 {
                if f == 60 && keys != 0 {
                    let t = p.u.now;
                    let _ = p.u.input(t, word(keys, level));
                }
                let start = Instant::now();
                let until = if demand { None } else { Some(start + Duration::from_millis(12)) };
                p.u.frame_to(1.0 / 60.0, 100.0, Budget { events: u64::MAX, until }, i64::MAX);
                let took = start.elapsed();
                total += took;
                worst = worst.max(took);
                if !p.u.rec(p.player).alive {
                    break;
                }
            }
            out += &format!(" | {}: total {:6.0} ms, worst frame {:6.1} ms", if demand { "demand" } else { "12 ms budget" }, total.as_secs_f64() * 1e3, worst.as_secs_f64() * 1e3);
        }
        println!("{out}");
    }
}
