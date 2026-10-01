//! B9 cost per body (docs/law.md). The law reports how many band crossings one radial cycle of
//! each orbit costs it, and after that cycle costs nothing until an event.
//!
//! - The bound: crossings per cycle ≤ 2m·log₂(r_apo/r_peri) + 8, at m = 16 bands per octave. An orbit
//!   spanning a ratio of radii crosses the band boundaries between its turning points twice (out and
//!   back), so the cost follows the orbit's own extent, not a constant. The first version of this
//!   gate (a median of at most 64) held only to e = 0.6: the law's red-team (1 October) showed that a
//!   flat 64 is a lie at e = 0.99, where the cycle spans 7.6 octaves.
//! - The sample: G1's 256 orbits (e below 0.7, unchanged) then `sample::extreme_orbits(256)`, whose
//!   first 16 sit at e = 0.99 exactly and the rest at e from 0.7 to 0.99.
//! - PASS iff every orbit is answered and within its bound, and the old gate still holds on G1's
//!   256: their median is at most 64 (kept, never loosened). A NaN, a negative count and an
//!   unanswered orbit all fail.
//!
//! The judge also times `advance_per_cycle` on each seed after a first call (which fills any memo)
//! and reports the median and p95 nanoseconds per call. That number is reported, not gated, and it
//! is measured like the player: no pinning, no cooling, no discarded outliers; the machine state
//! is on the lines that surround the gates.
use super::{sample, Gate, Law, BOUND_SEEDS};
use crate::measure::percentile;
use std::hint::black_box;
use std::time::Instant;

/// The old gate, kept on G1's 256 orbits: their median crossings per cycle.
pub const CROSSINGS_MAX: f64 = 64.0;
/// The slack of the log-scaled bound, in crossings.
pub const SLACK: f64 = 8.0;
/// The extreme orbits added to G1's, and the e they reach.
pub const EXTREME_SEEDS: usize = 256;
pub const REACHES_E: f64 = 0.99;
/// Bands per octave of the reference law (docs/law.md: m = 16; r1 found m = 8 too coarse).
pub const BANDS_PER_OCTAVE: f64 = 16.0;
/// A timed sample lasts about this long, so the clock's own cost is small against it.
const SAMPLE_NS: f64 = 50_000.0;
const REPS_MAX: usize = 256;

/// The bound on one cycle's crossings: 2m·log₂(r_apo/r_peri) + 8, where r_apo/r_peri = (1 + e)/(1 − e).
pub fn crossings_bound(e: f64) -> f64 {
    2.0 * BANDS_PER_OCTAVE * ((1.0 + e) / (1.0 - e)).log2() + SLACK
}

/// B9's orbits: G1's 256, then the extreme ones.
pub fn orbits() -> Vec<(f64, f64)> {
    let mut all = sample::bound_orbits(BOUND_SEEDS);
    all.extend(sample::extreme_orbits(EXTREME_SEEDS));
    all
}

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
    let orbits = orbits();
    let answers: Vec<Option<f64>> = orbits.iter().map(|&(p, e)| law.crossings_per_cycle(p, e).filter(|c| c.is_finite() && *c >= 0.0)).collect();
    let unanswered = answers.iter().filter(|a| a.is_none()).count();
    // The old gate: the median over G1's orbits (the first BOUND_SEEDS).
    let mut old: Vec<f64> = answers[..BOUND_SEEDS].iter().flatten().copied().collect();
    old.sort_by(f64::total_cmp);
    let median = if old.is_empty() { f64::NAN } else { percentile(&old, 0.5) };
    // The new gate: every answered orbit within its own bound; the worst margin is the largest count − bound.
    let over: Vec<usize> = (0..orbits.len()).filter(|&i| answers[i].is_some_and(|c| c > crossings_bound(orbits[i].1))).collect();
    let (hi_e, hi_count) = (REACHES_E, answers.iter().zip(&orbits).filter(|(_, o)| o.1 >= 0.99).filter_map(|(a, _)| *a).fold(f64::NAN, f64::max));
    let worst_margin = answers.iter().zip(&orbits).filter_map(|(a, o)| a.map(|c| c - crossings_bound(o.1))).fold(f64::NEG_INFINITY, f64::max);
    let mut ns: Vec<f64> = orbits[..BOUND_SEEDS].iter().map(|&(p, e)| ns_per_call(law, p, e)).collect();
    ns.sort_by(f64::total_cmp);
    let detail = format!(
        "cost per body: {}/{} orbits within 2m·log2(r_apo/r_peri)+8 (worst margin {worst_margin:.1} crossings{}), at e = {hi_e} up to {hi_count:.0} crossings against a bound of {:.1}; on G1's {BOUND_SEEDS} (e < 0.7) median {median:.1} crossings per cycle (limit {CROSSINGS_MAX}), p95 {:.1}, max {:.1}{}; advance_per_cycle after the first call: median {:.0} ns, p95 {:.0} ns over {BOUND_SEEDS} seeds (reported)",
        orbits.len() - over.len() - unanswered,
        orbits.len(),
        if over.is_empty() { String::new() } else { format!("; {} over the bound", over.len()) },
        crossings_bound(hi_e),
        if old.is_empty() { f64::NAN } else { percentile(&old, 0.95) },
        old.last().copied().unwrap_or(f64::NAN),
        if unanswered > 0 { format!(", {unanswered} of {} unanswered", orbits.len()) } else { String::new() },
        percentile(&ns, 0.5),
        percentile(&ns, 0.95),
    );
    // Any unanswered orbit fails, whatever the others.
    Gate { id: "B9", pass: unanswered == 0 && over.is_empty() && median <= CROSSINGS_MAX, detail, secs: 0.0 }
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
    fn the_bound_follows_the_orbit_and_echo_sits_inside_it_to_e_099() {
        assert!((crossings_bound(0.0) - 8.0).abs() < 1e-12);
        // r_apo/r_peri = 199 at e = 0.99: 7.64 octaves, 16 bands each, crossed twice.
        assert!((crossings_bound(0.99) - (32.0 * 199f64.log2() + 8.0)).abs() < 1e-9 && (crossings_bound(0.99) - 252.4).abs() < 0.1);
        let all = orbits();
        assert_eq!(all.len(), 512);
        assert_eq!(all[..256], sample::bound_orbits(256)[..]);
        assert!(all[256..272].iter().all(|o| o.1 == REACHES_E) && all[256..].iter().all(|&(p, e)| (0.7 - 1e-9..=0.99).contains(&e) && p >= 6.5 + 2.0 * e));
        // The count is the lattice's, at most 2·(m·octaves + 1) and so always inside the bound.
        for &(p, e) in &all {
            assert!(cost_margin(p, e) >= 5.0, "p {p} e {e}: margin {}", cost_margin(p, e));
        }
    }
    fn cost_margin(p: f64, e: f64) -> f64 {
        crossings_bound(e) - reference_crossings(p, e)
    }

    #[test]
    fn the_planted_linear_bands_pass_the_old_median_and_fail_the_log_scaled_bound() {
        // Bands a sixteenth of the periapsis apart in r: 32·(r_apo/r_peri − 1) = 64·e/(1 − e) crossings. At G1's
        // median e (0.35) that is about 34, so the old gate's median passes it; at e = 0.99 it is 6300, against a bound of 252.
        let g = b9(&Planted(Fault::Linear));
        assert!(!g.pass && g.detail.contains("over the bound"), "{}", g.detail);
        let median: f64 = g.detail.split("median ").nth(1).unwrap().split(' ').next().unwrap().parse().unwrap();
        assert!(median <= CROSSINGS_MAX, "the old gate's median alone passes it: {}", g.detail);
        assert!(g.detail.contains("up to 6336 crossings against a bound of 252.4"), "{}", g.detail);
        // A law that stops at 64 crossings (cheaper than the bound everywhere) is not a cost failure: whether it
        // can be right with 64 is G1 and G2's question. The gate only bounds what a law spends.
        let flat = counting(|p, e| Some(reference_crossings(p, e).min(64.0)));
        assert!(b9(&flat).pass);
    }

    #[test]
    fn every_orbit_is_inside_its_bound_and_must_answer() {
        use std::collections::HashSet;
        // `heavy_in_5` of every 5 of G1's orbits (by index) answer 512, the others 8; the extreme ones answer 8.
        let heavy_in_5 = |k: usize| {
            let heavy: HashSet<(u64, u64)> = sample::bound_orbits(BOUND_SEEDS).iter().enumerate().filter(|(i, _)| i % 5 < k).map(|(_, &(p, e))| (p.to_bits(), e.to_bits())).collect();
            counting(move |p, e| Some(if heavy.contains(&(p.to_bits(), e.to_bits())) { 512.0 } else { 8.0 }))
        };
        // Even 20% heavy fails now: the median is 8 (the old gate passes) but 512 crossings is over the bound of every orbit below e = 0.99.
        let g = b9(&heavy_in_5(1));
        assert!(!g.pass && g.detail.contains("median 8.0") && g.detail.contains("max 512.0") && g.detail.contains("over the bound"), "{}", g.detail);
        // A law that answers 8 everywhere is within every bound only where 8 is enough: the bound is 8 at e = 0 and grows
        // with e, so 8 passes, and 60% heavy fails on its median as before.
        assert!(b9(&counting(|_, _| Some(8.0))).pass);
        assert!(!b9(&heavy_in_5(3)).pass);
        // Not implemented, a NaN, a negative count and one unanswered orbit all fail.
        assert!(!b9(&counting(|_, _| None)).pass);
        assert!(!b9(&counting(|_, _| Some(f64::NAN))).pass);
        assert!(!b9(&counting(|_, _| Some(-1.0))).pass);
        let first = sample::bound_orbits(1)[0];
        let g = b9(&counting(move |p, e| if (p, e) == first { None } else { Some(3.0) }));
        assert!(!g.pass && g.detail.contains("1 of 512 unanswered"), "{}", g.detail);
        // One extreme orbit over its bound fails everything else being perfect.
        let last = *orbits().last().unwrap();
        let g = b9(&counting(move |p, e| Some(if (p, e) == last { crossings_bound(e) + 1.0 } else { reference_crossings(p, e) })));
        assert!(!g.pass && g.detail.contains("1 over the bound"), "{}", g.detail);
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
