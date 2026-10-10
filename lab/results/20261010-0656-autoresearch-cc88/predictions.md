# Autoresearch predictions (written before the held-out runs; tuning is on seed 1 only)

Artifact: `xtask universe --kick-bench` (deterministic kick replay on the plane's own
scene), pure resolver `step::process`. Metric: `kick_us_all` median (µs per kick).
Behaviour lock: `replay_digest` and universe `digest` bit-identical to the baseline
per seed, `refused == 0`. Tuned set: seed 1. Held-out set: seeds 2, 3, 4 (never
tuned on), each measured once at the end.

Profile (measured, seed 1): per kick, `bind` ≈ 80% of the resolver cost, and inside
`bind`'s `Rebinding::from_state` the `Orbit/Passage::compile` is 84% (≈52–63 µs per
compile): ≈134 Gauss–Legendre panels (≈123 on the weak/integer path), ≈73 `append`
calls per compile, ≈759 `cos`, ≈181 `isqrt`. Exact-key memoization is dead (663
distinct shapes in 663 rebinds), confirming the 5 October taste-log entry.

Hypotheses (in order):
- H-A: `append` recomputes the shape-constant inner cut `√δ/√(qa)·2⁻²` (two `isqrt`
  Newtons with u128/u128 division plus one i128 `Scalar` division) on every append
  (~73×/compile). Hoisting it to `OrbitShape::new` is bit-identical (same formula,
  same inputs, computed once). Prediction: kick_us_all median −10–20% on every seed.
- H-B: `isqrt`'s Newton loop uses u128/u128 division (`__udivti3`). For the operands
  the compiler sees (root < 2^63), the exact `div_word` (u128/u64, word-sized
  quotient) returns the same bits. Prediction: further −5–15%.
- H-C: `knots`/`crossings` `Vec` growth: preallocate from the band ladder.
  Prediction: <5%; keep only if ≥3% on seed 1.

Held-out predictions (seeds 2–4, one run each, after the loop stops):
1. Gain within ±5 percentage points of seed 1's gain (the compile is local to a
   kick; the seed only changes the orbit mix).
2. `replay_digest` and `digest` equal to the baseline values recorded in log.md for
   every seed; `refused == 0`.
3. `kick_us` (plane-made population, ≈35.6 µs baseline) improves by at least half
   the leavers' relative gain (fewer but similar rebinds).

What would make this wrong: any digest change on any seed; total held-out gain
< 10%; or the gain reversing sign between populations. Then the change is reverted
and reported as a lead, not gold.
