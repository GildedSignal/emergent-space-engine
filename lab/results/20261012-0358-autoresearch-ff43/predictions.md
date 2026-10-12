# predictions.md — 20261012-0358-autoresearch-ff43

Written before the decisive optimization runs. Tuned on: seed 1, rtf 100, seconds 30
(bench `xtask universe --kick-bench`). Held out: seeds 3, 4, 5 (never run before this
file is written), rtf 1 (real-time pacing) seconds 55, and seed 2 at rtf 100.

## Baseline (tuned set, seed 1 rtf 100, clean binary)

- kick_us_all median ≈ 76–80 µs, p99 ≈ 380–440 µs, n ≈ 1158.
- Per kick: Orbit::compile ≈ 49 µs (≈ 66 quad panels × 4 nodes), passage compile ≈ 9.5 µs
  (3% of kicks at ≈ 330 µs each), fit_key ≈ 4.2 µs, decoded_event ≈ 3.7 µs.
- Op counts per kick: div_word ≈ 595, isqrt ≈ 113, cos ≈ 437.

## Hypotheses to test (in order)

1. **H1 div_word**: the base-2^32 two-division Knuth path is replaceable by a
   Granlund–Montgomery reciprocal-multiply (or one native 64-bit divide) that returns the
   same integer quotient. Expected: div_word avg 25–45 ns → ≤ 15 ns; kick median −8…−15%.
2. **H2 isqrt**: Newton's `x / y` is a u128/u128 `__udivti3` call; `y < 2^64` always here,
   so the same integer comes from one div_word-class division. Expected: isqrt avg
   ~80–110 ns → ≤ 40 ns; kick median −5…−10%.
3. **H3 cos**: the 13 nested factors are already one mul+shift each; I expect < 5% and
   will revert if so.
4. **H4 passage compile** (3% of kicks, ≈ 330 µs each): if it repeats OrbitShape work that
   a cycle compile also does, factor the shared part; expect −5…−9% on the all-kicks
   median only if the p99 tail is passage-dominated. Check before touching.
5. **H5 outbound_at Newton loop** in reads: count iterations; if most reads run the full
   72, the loop's early-exit quantum rarely triggers and I expect no bit-exact win
   (iteration count is part of the definition) — measure only, revert.

## What must hold everywhere (the certificate)

- `replay_digest` and `digest` bit-identical to baseline for every seed and rtf.
- `refused` = 0, sample counts identical (same kicks fired).

## Held-out predictions

- On seeds 3/4/5 and rtf 1/55 s: digests differ from seed 1's (different scenes) but each
  seed's digest under the optimized binary equals that seed's digest under the baseline
  binary, and its median kick falls by the same fraction as seed 1's (within run-to-run
  noise, ±20% of the gain).
- The p99 improves more than the median in relative terms if H4/H1 land, because the tail
  kicks are the eccentric orbits with the most panels and divisions.
- No seed's median gets worse than baseline (a regression on any held-out seed reverts the
  change that caused it).
