# Predictions (written before the decisive run)

Run: 20261014-1859-second-20261014-1631-redteam-e8f7-1397. The checker of e8f7 named the
one gold experiment: the positive control on the design's own path — a composed key built
from the shipped `lorentz.rs` integer-shear algebra acting on EVENTS (coefficients at
2^-100 from `Frame::of`'s integer algorithm; event words at ae29's 2^-64 tick), over the
108-cell grid and named rows, planar (nine-shear) arms included, with the child tick
carried by the composed map's time factor. This run does that, on shipped code: an external
probe calls `Frame::of`/`Frame::inverse` (no crate edits), chains them over the doll tree,
and compares against a float64 Lorentz oracle at the engine's own read-back (dyadic-snapped)
parameters. The same probe computes the additive V1/V2 keys (the negative control) on
identical parameters, so both controls live in one instrument.

Instrument validation (already run, SELFTEST mode, single link β 0.5 θ 0.35, offset
(3000,4000)): depth-1 additive err = −4.5e-13 ticks (float noise; the additive key is exact
at depth 1), composed integer key = the oracle bit for bit (err_comp = 0.0 exactly).

## What I expect (derived, not fitted)

Error budget of the composed integer key, derived from the shipped algebra: each link is
nine shears; each shear floors once (≤ 1 word quantum = 2^-64 tick); two links → ≤ 18·2^-64
≈ 9.8e-19 ticks. Coefficient truncation at 2^-100 on values ≤ ~2^81 words contributes
≤ ~2^-84 ticks. So the composed key's real error is ≤ ~1e-18 ticks, and any measured
|err_comp| above that is the f64 oracle's own noise (~1e-11 at t ~ 1e5).

1. **Positive control:** |err_comp| ≤ 1e-9 ticks on EVERY case — the 108-cell grid, the 20
   extended adversarial cells (β₂ ∈ {0.5, 0.9}, θ ∈ {45°, 60°}, plus β₁ 0.99), the 16 planar
   arms with θ₁ ≠ 0 (including θ₂ = 110°, which exercises the rotation flip), the named
   rows, the depth-2..8 chains (collinear and planar), and the t_B channel. That is ≤ 1 tick
   with ≥ 9 orders of margin.
2. **Scaling signature:** on the worst cell at d = 1e4 vs d = 8e4, err_comp scales ~×8
   (oracle-noise-limited), staying ≤ 1e-9. If it stayed constant instead, that constant
   would be the real integer-path error — either way the budget is measured, not assumed.
3. **Negative control (reproduction of the record):** G1 census ≈ 79/108 cells ≥ 1 tick,
   ≈ 52 ≥ 10; worst grid cell (0.9, 0.3, collinear, 1e4) ≈ 4,070/5,067 ticks; named rows
   ≈ 15.2/15.2 (player group), 179/357 (inspiral), 130/140 (high-γ), 0.0/0.0 (perp offset).
   Dyadic parameter snapping (2^-40 words) may move last digits; I predict agreement within
   1% of the record.
4. **The understated worst case, now measured** (the checker's [INFERENCE] extrapolation):
   (β₁ 0.9, β₂ 0.9, θ 45°, d 1e4): from the verified analytic law,
   V2 = [(γ₁−1)sinhη₂ + sinhη₁(γ₂−1)cos45°]·d ≈ 4.56e4 ticks, V1 = (γ₁−1)sinhη₂·d ≈ 2.67e4.
5. **t_B channel:** collinear (0.5, 0.5): t_exact = γ₁γ₂(1+β₁β₂)·t_B = 16,666.67 on t_B =
   1e4 — an additive key that carries the child tick unscaled misses 6,666.7 ticks (66.7%),
   one that carries the per-link product γ₁γ₂ misses 3,333.3 (33%); the composed key errs
   ≤ 1e-9. Perpendicular: t_exact = γ₁γ₂·t_B = 13,333.3 — there γ₁γ₂ is the right carrier
   (miss ≈ 0, ≤ float noise), and the composed key still errs ≤ 1e-9.
6. **Depth:** additive collinear β 0.3/link, d 1e3: ≈ 15 → 78 → 227 → 512 → 995 → 2,921 at
   depths 2/3/4/5/6/8 (the record's 2/3/4 and the checker's 5/6/8); composed ≤ 1e-9 at all
   depths, planar chains included.

## Kill criterion (frozen before the run)

If ANY case shows |err_comp| ≥ 1 tick, the composed-key fix as specified (chained shipped
nine-shear frames on 2^-64 event words) is falsified too, and the re-emit spec needs a
different representation. If any shear leaves the i128 word (an unwrap panic), the word
budget claim is wrong at these offsets. If the additive controls above do NOT reproduce
(within the 1% snapping tolerance), the instrument disagrees with the frozen record and
nothing is claimed until the discrepancy is explained.

## Not claimed here

Key staleness under thrust between re-anchors (adjacent, unmeasured); the Wigner rotation's
effect on the spatial readout (owned by the turn machinery); anything about cost — the
composed key is one map application per event walk, the same order as ae29's chain walk,
but this run measures correctness only.
