# Predictions — 20261018-1237-components-271c

Component: the compiled cycle's quadrature node (read-stream open direction 2, the slices
d4ce left unpriced: the two `isqrt` implementations — `num::isqrt`'s wide Newton with
software `u128/128` division on the `word_root = false` side, and std's `u64::isqrt` on the
`word_root = true` side that every belt/planet-class key takes).

Lever: division-free exact `isqrt` (f64 seed + multiplicative reciprocal-root refinement +
bounded exact-floor correction). `floor(sqrt)` is a unique integer, so any exact
implementation is bit-identical by construction — no law change, no digest risk.

## Before the decisive run

- **P1 (exactness, control both sides).** `isqrt_mul == num::isqrt` on ≥10⁶ random u128
  and ≥10⁶ gate-shaped operands (`denominator << 62` swept across the word_root/fast gate
  decades); compile-output hashes (knot psis, period/advance/proper period, crossing times,
  8-phase states) identical across arms on the whole key ladder; `cargo test -p
  emergent-space` green under both arms. Kill the arm if any bit moves.
- **P2 (census).** Belt/planet-class keys (periapsis ≳ 10⁵ M) are ~100% `fast +
  word_root = true` (std `u64::isqrt` per node); the wide `num::isqrt` fires only on the
  near-separatrix rungs (delta < 2⁻²), a small case fraction but the rungs where d4ce's
  checker saw the panel time move (R2/R5).
- **P3 (in-situ, the decisive number).** On `word_root = false` rungs the arm cuts panel
  time ≥ 25% (the root is on the dependency chain of g/g1/rtau/rt, and the shipped wide
  Newton pays 2–3 software `u128` divisions per node). Kill criterion: if the interleaved
  paired median is < 10% on every rung, the slice joins d4ce's division slice as
  OoO-hidden and read-stream od 2's arithmetic half closes with "no bit-exact arithmetic
  lever ≥ 10% remains in the node".
- **P4 (the belt side, where the flight's compile actually spends its time).** Std
  `u64::isqrt`'s share of the belt-class node is unknown to the page (never priced): I
  predict ≤ 8% of panel time on belt-class keys. If it measures ≥ 20%, that is a finding
  against my own prediction and the page's "arithmetic is not the lever" reading.

## Held-out (not tuned on)

- The census numbers (P2) are read once, before any timing arm.
- Seed 2 ladder and a 10× finer near-separatrix sweep run only after the decisive pairs.
