# Predictions (written before the decisive held-out run)

Change under test: `fast_quad`'s per-node `u64::isqrt` replaced by an f64-seeded,
unit-corrected exact floor sqrt (`num::isqrt_word`, x < 2^62). Tuning corpus:
p ∈ {8..65536} (11 values), e ∈ {0..0.9}; all such keys take the `word_root`
branch (delta ≥ 1/4). Kept on that corpus: compile −6.8% (19.6 → 18.3 µs),
bit-identical hashes. Reverted along the way: div_word swaps (slower), Vec
reserve (no gain), f64-seeded 128-bit isqrt (wrong under Newton-from-below, and
no win).

## Held-out cases (HELDOUT=1: p ∈ {6,7,12,700,9000,262144,1048576}, e ∈ {0.05,0.2,0.8,0.95})

These were never measured while tuning. They include:

- p = 6, 7: strong field. I expect most to be refused (NoBoundOrbit/Range) or,
  when bound, to take the generic (non-word_root) branch that my change does
  not touch.
- p = 262144, 1048576: q ≤ 2^-18 → ShapeKey compactness quantizes to zero →
  `weak_quad` + Taylor clock branch, untouched by my change.
- e = 0.95: near-separatrix dyadic refinement, many small panels.

## Predictions

1. **Bit identity.** compile-hash and rebind-hash on HELDOUT=1 are identical
   between the stock build and the changed build. (isqrt_word returns exactly
   floor(sqrt(x)) for x < 2^62; its only call site guards denominator ≤ 1 < 2^62
   and takes the word_root branch only when denominator ≥ 2^60.)
2. **Latency.** Held-out compile improves by a smaller fraction than the tuning
   corpus, between 2% and 8%, because the weak-branch keys (p ≥ 2^18) never
   enter fast_quad at all and dilute the average; I do NOT expect a regression
   anywhere (the change is inside the same branch the tuning corpus measured).
3. **Refusals unchanged.** The same 22 of 28 held-out keys compile on both
   builds (refusals happen before fast_quad).
4. **Test suite.** `cargo test -p emergent-space` passes unchanged on the
   changed tree (the crate's own quadrature/envelope tests are the behaviour
   gate).
5. **Risk I accept.** If the checker finds any hash mismatch on held-out or
   tuning corpora, the change is wrong and must be reverted, however good the
   timing: the law's contract is exact integer outputs, and one differing bit
   invalidates the whole optimization.
