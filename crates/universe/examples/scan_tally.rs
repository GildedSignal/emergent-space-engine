//! What the player's neighbourhood finder does on a flight: pairs asked about, skipped by the filter, tested exactly, and the
//! pairs it would have skipped had the predicate not wrapped its `i128`s (`kept_by_wrap`: the cost the wrap defect keeps).
//!
//! cargo run --release -p emergent-universe --example scan_tally [-- <wall seconds> <keys> <level> <seed>]
use emergent_universe::ctx::Ctx;
use emergent_universe::encounter::{Encounter, Encounters, Held, PlayerNeighbourhood};
use emergent_universe::fleet::Order;
use emergent_universe::num::Tick;
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};
use std::sync::Arc;

struct Shared(Arc<PlayerNeighbourhood>);
impl Encounters for Shared {
    fn find(&self, c: &Ctx, b: usize, t: Tick, i: Tick) -> Vec<Encounter> {
        self.0.find(c, b, t, i)
    }
    fn capture(&self, c: &Ctx, b: usize, t: Tick, i: Tick) -> Option<Arc<dyn Held>> {
        self.0.capture(c, b, t, i)
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let seconds: f64 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(12.0);
    let keys: u8 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(0);
    let level: u8 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(0);
    let seed: u64 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(1);
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, 48).unwrap();
    let finder = Arc::new(PlayerNeighbourhood::default());
    p.u.set_encounters(Box::new(Shared(finder.clone())));
    if keys != 0 {
        p.u.schedule((1.0 * 100.0 / TICK_SECONDS) as i64, word(keys, level)).unwrap();
    }
    let cut = (seconds * 100.0 / TICK_SECONDS) as i64;
    while p.u.now < cut {
        p.u.frame_to(1.0 / 60.0, 100.0, Budget::unlimited(), cut);
    }
    p.u.settle(cut);
    let t = finder.tally();
    let pct = |n: u64| 100.0 * n as f64 / t.pairs.max(1) as f64;
    println!(
        "keys {keys} level {level} seed {seed}, {seconds} s: {} scans answered, {} pairs asked about: {:.1}% skipped by the filter, {:.1}% tested exactly, and {:.1}% more would be skipped if the predicate did not wrap",
        t.scans,
        t.pairs,
        pct(t.skipped),
        pct(t.tested),
        pct(t.kept_by_wrap),
    );
}
