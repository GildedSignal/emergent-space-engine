# predictions.md — run 20261012-0036-autoresearch-e3ca

Written BEFORE the decisive held-out run. Tuned only on the `main` corpus
(300 belt-like keys, p ∈ [4, 512] M, e ∈ [0, 0.95)).

Baseline (main, 3×30 reps, this Linux box): mean 36.1 µs/compile, median 29.5 µs,
p99 114.7 µs; ~30.3 knots/compile; every key takes the `fast_quad` path.
Kernel micro-bench: `isqrt` 97.5 ns, u128/u128 div 24.2 ns, `div_word` 47.0 ns
(div_word REJECTED: slower than the compiler's `__udivti3` here).

## Change under test

`num::isqrt`: replace the top-64 `u64::isqrt` seed with an f64 sqrt seed plus a
provable at-or-above-root margin (`est + (est>>40) + 16`, x ≥ 2^40 branch; exact
u64 path below that). The Newton-from-above descent and its termination check are
untouched, so the returned bits are provably identical (same invariant, same loop).

## Held-out predictions (not tuned on)

Corpus `heldout`: 120 keys p ∈ [3, 50] M, e ∈ [0.90, 0.99) (near-separatrix,
near-parabolic) + 120 keys p ∈ [30, 2000] M, e ∈ [0, 0.3) (far field).

1. **Bit-identity:** the output hash on BOTH corpora is exactly the baseline hash
   (main `7932a7d0de3d965919763c10a2a780f2`, heldout `1d3ac9118d67781bcccee07d5fc617e2`).
   Any difference: revert, the change is a law change, not an optimization.
2. **Speed carries over:** mean ns/compile drops by 10–20% on heldout (its
   near-separatrix half has more non-word-root nodes, i.e. more isqrt calls per
   compile, so the relative gain should be ≥ the main corpus gain; the far-field
   half is word_root-dominated and gains little).
3. **p99:** the p99 key (close-in, high-e, most panels AND most non-word-root
   nodes) gains the most: I predict p99 drops by 15–25%.
4. **`cut` and `Scalar::sqrt` benefit too** (both call isqrt): cut ns/call drops
   by ≥ 20%.
5. **Stop rule:** if the heldout mean gain is < 10%, the loop stops there (three
   sub-10% rounds rule); I predict it will not stop.
