//! B9 cost per body (docs/law.md: at most 64 crossings per cycle at m = 16; after that, zero work
//! per orbit until an event). The law reports how many band crossings one radial cycle of each of
//! G1's 256 orbits costs it; the median must be at most 64. Unanswered or NaN seeds fail the gate.
//!
//! The judge also times `advance_per_cycle` on each seed after a first call (which fills any memo)
//! and reports the median and p95 nanoseconds per call. That number is reported, not gated, and it
//! is measured like the player: no pinning, no cooling, no discarded outliers; the machine state
//! is on the lines that surround the gates.
use super::{sample, Gate, Law, BOUND_SEEDS};
use crate::measure::percentile;
use std::hint::black_box;
use std::time::Instant;

/// The gate: the median crossings per cycle over the bound-orbit seeds.
pub const CROSSINGS_MAX: f64 = 64.0;
/// Bands per octave of the reference law (docs/law.md: m = 16; r1 found m = 8 too coarse).
pub const BANDS_PER_OCTAVE: f64 = 16.0;
/// A timed sample lasts about this long, so the clock's own cost is small against it.
const SAMPLE_NS: f64 = 50_000.0;
const REPS_MAX: usize = 256;

/// The reference count `echo` answers: the band boundaries r_k = 2^(k/m) that lie strictly between
/// periapsis p/(1+e) and apoapsis p/(1−e), crossed twice (out and back) in one radial cycle.
pub fn reference_crossings(p: f64, e: f64) -> f64 {
    let (lo, hi) = ((BANDS_PER_OCTAVE * (p / (1.0 + e)).log2()).floor(), (BANDS_PER_OCTAVE * (p / (1.0 - e)).log2()).ceil());
    2.0 * (hi - lo - 1.0).max(0.0)
}

/// Nanoseconds per `advance_per_cycle` call at (p, e): one untimed call, one pilot call that sizes
/// the sample, then the mean over enough calls to last about `SAMPLE_NS`.
fn ns_per_call(law: &dyn Law, p: f64, e: f64) -> f64 {
    black_box(law.advance_per_cycle(black_box(p), black_box(e)));
    let t = Instant::now();
    black_box(law.advance_per_cycle(black_box(p), black_box(e)));
    let pilot = t.elapsed().as_secs_f64() * 1e9;
    let reps = ((SAMPLE_NS / pilot.max(1.0)).ceil() as usize).clamp(1, REPS_MAX);
    let t = Instant::now();
    for _ in 0..reps {
        black_box(law.advance_per_cycle(black_box(p), black_box(e)));
    }
    t.elapsed().as_secs_f64() * 1e9 / reps as f64
}

pub fn b9(law: &dyn Law) -> Gate {
    let orbits = sample::bound_orbits(BOUND_SEEDS);
    let answers: Vec<Option<f64>> = orbits.iter().map(|&(p, e)| law.crossings_per_cycle(p, e).filter(|c| c.is_finite() && *c >= 0.0)).collect();
    let unanswered = answers.iter().filter(|a| a.is_none()).count();
    let mut counts: Vec<f64> = answers.iter().flatten().copied().collect();
    counts.sort_by(f64::total_cmp);
    let median = if counts.is_empty() { f64::NAN } else { percentile(&counts, 0.5) };
    let mut ns: Vec<f64> = orbits.iter().map(|&(p, e)| ns_per_call(law, p, e)).collect();
    ns.sort_by(f64::total_cmp);
    let detail = format!(
        "cost per body: median {median:.1} crossings per cycle (limit {CROSSINGS_MAX}), p95 {:.1}, max {:.1}{}; advance_per_cycle after the first call: median {:.0} ns, p95 {:.0} ns over {} seeds (reported)",
        if counts.is_empty() { f64::NAN } else { percentile(&counts, 0.95) },
        counts.last().copied().unwrap_or(f64::NAN),
        if unanswered > 0 { format!(", {unanswered} of {} unanswered", orbits.len()) } else { String::new() },
        percentile(&ns, 0.5),
        percentile(&ns, 0.95),
        orbits.len()
    );
    // Any unanswered seed fails, whatever the median of the others.
    Gate { id: "B9", pass: unanswered == 0 && median <= CROSSINGS_MAX, detail, secs: 0.0 }
}

#[cfg(test)]
mod tests {
    use super::super::laws::{Echo, Fault, Planted};
    use super::*;

    /// Echo's answers except for the crossings, which come from the closure.
    struct Counting(Box<dyn Fn(f64, f64) -> Option<f64>>);
    impl Law for Counting {
        fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)> {
            Echo.advance_per_cycle(p, e)
        }
        fn deflection(&self, b: f64) -> Option<f64> {
            Echo.deflection(b)
        }
        fn captured(&self, energy: f64, angular: f64) -> bool {
            Echo.captured(energy, angular)
        }
        fn photon_captured(&self, b: f64) -> bool {
            Echo.photon_captured(b)
        }
        fn long_run(&self, p: f64, e: f64, cycles: usize) -> Vec<(f64, f64, f64, f64)> {
            Echo.long_run(p, e, cycles)
        }
        fn crossings_per_cycle(&self, p: f64, e: f64) -> Option<f64> {
            (self.0)(p, e)
        }
    }
    fn counting(f: impl Fn(f64, f64) -> Option<f64> + 'static) -> Counting {
        Counting(Box::new(f))
    }

    #[test]
    fn the_reference_count_is_the_band_lattice_and_echo_sits_well_inside_the_limit() {
        // A circular orbit crosses nothing. One octave of radius holds m = 16 boundaries, crossed twice.
        assert_eq!(reference_crossings(100.0, 0.0), 0.0);
        let (p, e) = (100.0, 1.0 / 3.0); // r from 75 to 150: exactly one octave
        assert!((reference_crossings(p, e) - 2.0 * (BANDS_PER_OCTAVE - 1.0)).abs() <= 2.0, "{}", reference_crossings(p, e));
        let g = b9(&Echo);
        assert!(g.pass, "{}", g.detail);
        let median: f64 = g.detail.split("median ").nth(1).unwrap().split(' ').next().unwrap().parse().unwrap();
        assert!((20.0..50.0).contains(&median), "{}", g.detail);
    }

    #[test]
    fn the_planted_512_crossings_fail() {
        let g = b9(&Planted(Fault::Steps));
        assert!(!g.pass && g.detail.contains("median 512.0"), "{}", g.detail);
    }

    #[test]
    fn the_gate_is_on_the_median_and_every_seed_must_answer() {
        use std::collections::HashSet;
        // `heavy_in_5` of every 5 seeds (by index in G1's list) answer 512, the others 8.
        let heavy_in_5 = |k: usize| {
            let heavy: HashSet<(u64, u64)> = sample::bound_orbits(BOUND_SEEDS).iter().enumerate().filter(|(i, _)| i % 5 < k).map(|(_, &(p, e))| (p.to_bits(), e.to_bits())).collect();
            counting(move |p, e| Some(if heavy.contains(&(p.to_bits(), e.to_bits())) { 512.0 } else { 8.0 }))
        };
        // 40% heavy: the median is 8 and the gate passes, while the max shows the tail.
        let g = b9(&heavy_in_5(2));
        assert!(g.pass && g.detail.contains("median 8.0") && g.detail.contains("max 512.0"), "{}", g.detail);
        // 60% heavy: the median is 512.
        assert!(!b9(&heavy_in_5(3)).pass);
        // Not implemented, a NaN, a negative count and one unanswered seed all fail.
        assert!(!b9(&counting(|_, _| None)).pass);
        assert!(!b9(&counting(|_, _| Some(f64::NAN))).pass);
        assert!(!b9(&counting(|_, _| Some(-1.0))).pass);
        let first = sample::bound_orbits(1)[0];
        let g = b9(&counting(move |p, e| if (p, e) == first { None } else { Some(3.0) }));
        assert!(!g.pass && g.detail.contains("1 of 256 unanswered"), "{}", g.detail);
    }

    #[test]
    fn the_timing_is_taken_after_the_first_call() {
        // A law that memoizes: 1 ms for its first call at each (p, e), nothing after. The timed calls
        // must see the memo, so the reported median is far below the first-call cost.
        use std::collections::HashSet;
        use std::sync::Mutex;
        struct Memo(Mutex<HashSet<(u64, u64)>>);
        impl Law for Memo {
            fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)> {
                if self.0.lock().unwrap().insert((p.to_bits(), e.to_bits())) {
                    std::thread::sleep(std::time::Duration::from_micros(300));
                }
                Some((1.0, 1.0, 1.0))
            }
            fn deflection(&self, _: f64) -> Option<f64> {
                None
            }
            fn captured(&self, _: f64, _: f64) -> bool {
                false
            }
            fn photon_captured(&self, _: f64) -> bool {
                false
            }
            fn long_run(&self, _: f64, _: f64, _: usize) -> Vec<(f64, f64, f64, f64)> {
                Vec::new()
            }
            fn crossings_per_cycle(&self, _: f64, _: f64) -> Option<f64> {
                Some(1.0)
            }
        }
        let g = b9(&Memo(Mutex::new(HashSet::new())));
        let ns: f64 = g.detail.split("first call: median ").nth(1).unwrap().split(' ').next().unwrap().parse().unwrap();
        assert!(g.pass && ns < 100_000.0, "{}", g.detail);
    }
}
