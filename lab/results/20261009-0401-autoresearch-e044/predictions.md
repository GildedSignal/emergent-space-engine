# Predictions (written before the loop; 2026-10-09 04:10 UTC)

Metric: ns per `Orbit::compile` (median over the tune bank, 121 keys, reps=200 rounds=5,
`taskset -c 2`), digest = FNV-1a over every knot psi, every knot sum (5 Scalars), crossings,
increments and crossing times. Any digest change reverts the change.

**Held-out set** (not tuned on): `bench heldout` — the weak-branch cut q = 2^-18 ± 2 quanta,
k = HALF+1 and HALF+0x1234 at periapsis exponents 3/12/25/38, circles k = UNIT at exponents
2/6/20/40, strong-field k = 2^47·{2,3} and UNIT−7 at exponent 2, plus 60 keys from a
different seed (0xC0FF_EE11).

1. **R1 (fast_quad divisions):** replacing the four software 128-bit divisions
   (`2^104/root`, `a·g/(1+root)`, `floor·2^62/x`, `rtau·2^62/horizon`) with guarded
   `div_word` (exact, native 64-bit digits; guard `n>>64 < d`, else the old path) cuts the
   **median by ≥ 25%**, digest unchanged. Expected mechanism: 4 × ~20–40 ns software
   division calls per node dominate the ~275 ns/node I infer from the baseline
   (17.6 µs median over ~27 knots × 4 nodes).
2. **R1 tail:** the p99 gains **less than the median** (< 20% relative), because
   near-separatrix compiles are knot-dense and per-panel/per-knot overhead (Scalar
   construction and `Integral::add`) dominates there, not per-node divisions.
3. **R2 (raw fixed-exponent sums):** accumulating the three clock sums as raw i128 with
   per-slot fixed exponents inside `append` (converting to `Scalar` only at each knot)
   cuts a **further ≥ 15%** off the p99, digest unchanged, if slot exponents are constant
   across panels of one shape (they are, by `Scalar::mul`'s exponent arithmetic).
4. **Held-out behaviour:** the best configuration's relative gain on the held-out bank is
   within a factor of 2 of the tune-bank gain, and its digest matches the baseline digest
   there too (exactness is not bank-dependent).
5. **cos is not the lever:** the u64 nested-product `cos` costs < 15% of a compile; I
   expect no measurable win from touching it, so I will not.

If R1 gains < 10%, the division hypothesis is wrong and the cost is in Scalar plumbing —
R2 becomes the primary hypothesis and R1 is reverted and logged.
