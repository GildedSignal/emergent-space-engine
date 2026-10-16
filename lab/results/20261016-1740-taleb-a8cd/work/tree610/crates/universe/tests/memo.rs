//! The kick's rebind against the law's cycle memo (docs/law.md: "keyed by quantized (E, L)").
//!
//! **What was measured, and what it corrects.** Five lab runs reported that the plane compiles a fresh
//! exact orbit on about 99% of its kicks while the memo would serve them. One of them (b139) read
//! "24 distinct exact shapes in 13,801 compiles" and concluded that wiring the exact `ShapeMemo` into
//! the rebind deletes the compile at bit-identical digests. That count was taken by re-timing the same
//! pending kick at every frame: the same state, so the same shape, over and over. Over *distinct*
//! kicks, an exact key never recurs (a kick moves the exact (E, L) by an integer), and only the
//! law's quantized 12+12-bit cell does. So an exact memo in the rebind is a lookup that always misses;
//! the memo that pays is the quantized one, which changes the orbit between events (its period by up to
//! 2^-11) and therefore the digest: a law-level choice, behind B1, B2 and B9 re-judged on memo keys.
//!
//! This test keeps the measurement honest and standing: if the rebind ever keys its orbits by the
//! quantized cell, the exact recurrence below rises and the test says so.
use emergent_space::{
    binding::Trajectory,
    orbit::{MemoCode, ShapeKey},
};
use emergent_universe::body::What;
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::{step, Budget, Config, Kind};
use std::collections::HashSet;

#[test]
fn the_exact_shape_never_recurs_and_the_laws_memo_cell_does() {
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
    let mut last: Vec<Option<i64>> = Vec::new();
    let (mut cycles, mut exact, mut quantized) = (0u64, HashSet::new(), HashSet::new());
    for _ in 0..900 {
        last.resize(p.u.n_bodies(), None);
        for i in 0..p.u.n_bodies() {
            let rec = p.u.rec(i);
            if rec.kind != Kind::Ship || !rec.alive {
                continue;
            }
            let Some(item) = rec.plan.first().copied() else { continue };
            // Distinct kicks only: the same pending kick is one state, however often it is looked at.
            if !matches!(item.what, What::Kick(_)) || last[i] == Some(item.t) {
                continue;
            }
            last[i] = Some(item.t);
            let upd = step::process(&p.u.ctx(), i, rec);
            let Some(Trajectory::Cycle(c)) = upd.new_entry.as_ref().map(|e| &e.trajectory) else { continue };
            cycles += 1;
            exact.insert(ShapeKey::for_orbit(c.key()).unwrap());
            quantized.insert(MemoCode::encode(c.key()).unwrap().bits());
        }
        p.u.frame(1.0 / 60.0, 100.0, Budget::unlimited());
        p.u.settle(p.u.now);
    }
    let hit = |n: usize| 1.0 - n as f64 / cycles as f64;
    println!("{cycles} distinct cycle rebinds: exact shapes {} (hit {:.3}), quantized cells {} (hit {:.3})", exact.len(), hit(exact.len()), quantized.len(), hit(quantized.len()));
    assert!(cycles > 300, "the stream is real: {cycles}");
    assert!(hit(exact.len()) < 0.05, "the exact shape recurs: {:.3}", hit(exact.len()));
    assert!(hit(quantized.len()) > 0.9, "the law's cell does not recur: {:.3}", hit(quantized.len()));
    assert!(quantized.len() < 200, "memory is bounded by distinct cells, not bodies: {}", quantized.len());
}
