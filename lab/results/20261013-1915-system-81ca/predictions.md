# Predictions (written before the first run of carlson_probe.rs)

Formula under test (derived, not yet run): `advance = 2π·(RF(0, B, A) − 1)`, with
`A = 1 − q(8k−2)`, `B = 1 − q(4k+2)`, `q = compactness = 1/p_periapsis`, `k` Q48 —
all dyadic, no division (RF homogeneity absorbs the √A). First order is 6π/p exactly
(hand-checked). The shipped truth is `Orbit::compile(key).advance()`.

## Tuning grid (I may look at these)

p_slr ∈ {6·2^j, j=0..16}, e ∈ {0, 0.1, …, 0.9, 0.99}. Strong branch only (q > 2⁻¹⁸).

## Held-out cases (written before running them)

Keys I will not tune on, predicted to behave like the grid:
- (p, e) = (7.3, 0.05), (100.7, 0.55), (4192.9, 0.95), (37, 0.985), (99991, 0.3)
- near-circular strong: (5, 0.0); high-e deep: (8, 0.995)
- near-separatrix B→0 corner: (5.5, 0.9999) — if compile refuses, record the refusal.

## Predictions

- **P1 (positive):** on every strong key that compiles, relerr(f64 closed form vs
  shipped advance) ≤ 1e-9 (≈ the walk's own Q30 output quantum 2⁻³⁰ = 9.3e-10).
- **P2 (positive):** my integer RF (floor-rounding duplication, certified stop at
  spread ≤ 2⁻¹⁶, Carlson bound |δ| ≤ 0.3·spread²·(1−2e)^{−3/2}) lands within
  1.5 Q30 quanta (1.4e-9) of the f64 closed form on every strong key.
- **P3 (cost, both sides):** integer RF iterations to certified stop ≤ 10 on the whole
  strong domain; if any key needs > 14, the B→0 corner needs the complementary form
  (that would bound the claim, not kill it — flagged in the dossier).
- **P4 (cost):** one RF call < 1/3 of that key's full `Orbit::compile` wall at e ≤ 0.5,
  and < 1/20 at e ≥ 0.99 (the compile explodes in e via band cuts; RF is flat).
- **P5 (negative control, must NOT match):** on weak keys (q ≤ 2⁻¹⁸) the shipped walk
  is itself first-order truncated, so relerr(f64 CF vs shipped) should be ~q-level,
  ≥ 1e-6 somewhere in the sweep. If it were ≤ 1e-9 there, either my formula or my
  reading of the branch structure is wrong.
- **P6 (unification price):** a co-precessing per-pair Δφ update = 2 RF calls
  (one per tube), i.e. ~2×(P4 cost), vs 2 full compiles — ≥ 10× cheaper per pair
  at e ≤ 0.5 and ≥ 40× at e ≥ 0.99.

## What would make the claim wrong

- Any strong key with relerr > 1e-9: the reduction (or my A/B normalization) is wrong.
- Integer/f64 gap > 1.5 quanta anywhere: my rounding or the Carlson bound handling is
  unsound.
- Iteration counts growing with 1/B unboundedly: the O(1)-in-e claim dies at the
  separatrix without complementary forms.
