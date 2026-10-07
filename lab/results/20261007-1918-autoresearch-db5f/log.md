# Autoresearch log (lens: something that works)

Artifact: `crates/space` — the Darwin geodesic compiler of `es-space-v2`
(`Orbit::compile`), the live plane's kick path (board: "kicks dominate the
engine's cost"; taste log: the plane recompiles an orbit on ~99% of kicks).
Metric: **geomean ns per `Orbit::compile`** over a 44-key corpus (weak-ecc,
weak-circ, strong-fast, near-separatrix), min-of-5 pinned to one core;
constraint: bit-identical digest of every compiled answer (knots, crossings,
period/advance/proper period, crossing times, 9 phase states, table read,
reflection), on tuning and held-out corpora.

Machine note: GitHub Actions runner, 8 vCPU shared; load rose from 0.65 to
1.2 during the run, so all keep/revert decisions were re-measured as
interleaved A/B (same window), not across time.

Baseline (pristine): geomean 16546-16576 ns/compile; digest
`d6b70f94…` (tuning). Attribution measured with temporary counters +
standalone op probes: cos() = 42 ns = 26-31% of ns/compile; div_word 18 ns;
u128 `/` 25 ns; isqrt 91 ns; a weak panel ≈ 331 ns of arithmetic vs ~650 ns
per knot wall-clock; knots per orbit ≈ bands ≈ 16·log2((1+e)/(1-e)) clamped
by compactness.

| # | Hypothesis | Change | Result | Verdict |
|---|---|---|---|---|
| R1 | isqrt's Newton division (128/128) can use the crate's exact word division (y ≥ √x > x>>64) | `num.rs` isqrt: `x/y` → div_word when y fits u64 | 16460 vs 16553 min-of-5: +0.6%, inside noise; ratio_sqrt operands are often small so the big-isqrt saving is rarer than modelled | **reverted** (no measured gain) |
| R2 | per-compile Vec growth (96 B/knot, ~3-6 mallocs) is visible at µs scale | `orbit.rs` bound(): count bands, `knots.reserve(bands+8)`, `crossings.reserve(bands+2)` | interleaved A/B: 16373 vs 16567 = **−1.2%**, digest identical | **kept** |
| R3 | fast path's four u128 divisions per node → word division where provably exact (root ≥ 2^46; x ≥ floor > floor>>2) | `orbit.rs` fast_quad: 2 of 4 divisions via div_word | 18183-18186 reproducible vs 16383 = **+11% slower**; the ops probe had sampled only large roots (2^61+), real shapes hit small roots where div_word's correction loop and the new branch mispredict | **reverted** (regression; microbench distribution mismatch) |

Stop rule hit: three consecutive rounds under 10% (0.6%, 1.2%, −11%).

Held-out (after predictions.md written): 160 randomized keys, seed
0x5eed_1234_5678_9abc, log-uniform periapsis [4, 2^40], e mixture 70%
U[0, 0.995] / 30% U[0.995, 0.9999].

- digest `c8c103c7…` identical pristine vs patched (160/160 digested;
  prediction 1 held);
- ns/compile 66980 (patched) vs 67374/68250 (pristine): −0.6…−1.8%
  (prediction 2 held);
- mean knots/key 70.8, inside the predicted [44, 85] (prediction 3 held);
  per-knot cost ≈ 946 ns on this mix — ~45% above the tuning corpus's ~650,
  because the mix reaches the compact non-fast branch (general path with
  `node()`), which the tuning corpus barely sampled.

The one idea that carried the gain: allocation shape, not arithmetic — the
compiler was already word-division-optimised by its author; the remaining
bit-identical headroom is small.

Observation for the law's owner (identical on pristine, part of the digest):
`at_phase(period·f/20, f = 1..9)` returns `Err(Range)` on compact non-weak
keys (e.g. k ≈ 0.68, periapsis ≈ 2^9 M) while `signed_state` and
`crossing_state` succeed — first-decile phase reads fail there.
