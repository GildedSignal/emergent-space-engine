# predictions.md — 20261010-2220-autoresearch-2fe1

Written before the first change, after baselines were recorded.

## Metric and artifact

Artifact: `crates/space` orbit compile (`Orbit::compile` → `OrbitShape::bound` quadrature)
plus the per-kick inverse `Rebinding::from_state` (fit_key + compile + readout + residual).
Scalar metric: **ns per compile event** (`lab_bench compile-main`), ns per rebind event as the
consumer-visible metric. Behaviour constraint: **bit-identical outputs** (checksums over
compiled increments / rebinding residuals, all four bench modes) and the crate's test suite green.

## Tuned-on set

`compile-main` only (q ∈ [2^-14, 2^-4], e ∈ [0, 0.9], 512 keys, seed 0x853c...).

## Held-out set (run once at the end, never tuned on)

- `compile-deep`: q ∈ [2^-6, 2^-4], e ∈ [0.7, 0.95] (60.8 knots/orbit — more panels, eccentric).
- `compile-circ`: e ∈ [0, 0.05] (6 knots/orbit — panel count minimal, per-orbit overhead dominant).
- `rebind`: fit+readout dominated (near-circular synthetic states, r ∈ 2^5..2^13 M).
- `cargo test -p emergent-space --release` (the frozen gates' unit/envelope tests).

## Hypotheses and predictions (before measuring any change)

- **R1 — replace `u64::isqrt` (measured 22.3 ns) with an f64-seeded exact fixup** in
  `fast_quad`'s word-root path and as the seed of `num::isqrt` (u128, measured 86.8 ns).
  The fixup loops restore floor(sqrt(x)) exactly, so bits are identical by construction.
  Predict: compile-main −4…−8% (isqrt ≈ 22 of ~280 ns/node × ~107 nodes);
  compile-deep −6…−12% (same per-node saving over more nodes); compile-circ −15…−25%
  (per-node cost dominates over fixed overhead at 5 nodes/orbit... wait, circ has ~5 panels →
  ~20 nodes over 5.7 µs = 285 ns/node; same share, so −4…−8% too). Corrected prediction:
  compile-circ −4…−8%. rebind −2…−4% (compile is ~half of it).
- **R2 — `append()` loop**: most panels take the n==1 path but still evaluate two
  i128 divisions per panel (`(hi-lo)*i/n`, `(hi-lo)*(i+1)/n`) plus the `(span+CAP-1)/CAP`
  division; i128 division measured 26 ns. Predict a dedicated n==1 branch plus hoisting buys
  compile-main −2…−5%; deep doubles it in absolute ns (60 knots).
- **R3 — `fit_key`'s `poly` closure** recomputes `z*z` twice and `q.scale(1)` per bisection
  iteration (up to ~63 iterations × ~8 Scalar ops). Hoist both. Predict rebind −2…−5%;
  compile modes unchanged.
- Stop rule: three consecutive rounds each < 10% on their target metric → stop (I expect to hit
  it: the per-node cost is ~95 ns of wide divisions that have no bit-identical cheaper form).

## What would make it wrong

- Any checksum change in any mode, or any test failure: revert, the round is void.
- Gains outside the predicted bands by >2×: suspect measurement noise (shared 8-vCPU runner);
  re-run 3× and take the median-of-medians before logging "kept".
- Machine noise: timings on this shared runner swing; orders of magnitude only per lab rules.
