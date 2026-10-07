# Predictions addendum (written before rescale2.py; predictions 1–3 of predictions.md already FAILED on rescale.py)

Observed first (rescale.py, rescale_results.json): at fixed per-body kick rate
(perturber channel, λ_p = 0.1475 at every n), the population σ_E of the scar walk
grows with n (4.24e-3 → 7.45e-3 → 7.38e-3 → 1.29e-2 over n = 100…10⁴, spread 205%).
Nothing in the per-body law depends on n, so the σ INSTRUMENT is n-unstable, not the
walk. Diagnosis to test: the impulse kick dv = 2Gm/(b·v_rel) with b = √U·b_max has
p(dv) ∝ dv⁻³ — a log-divergent kick variance — so the empirical population σ is
dominated by the smallest b ever drawn in the sample (an order statistic that grows
with n·t). Physically that tail lives at b below the pair's mutual Hill radius, where
the impulse/no-collision premise is wrong anyway (that regime belongs to the exact
encounter subsystem, m-meso-motion / r8).

## Held-out predictions for rescale2.py (floored instrument + tail diagnostics)

1. **Localization:** in the UNfloored pert channel, bulk order statistics of the
   per-body ΔE (interquartile range) are n-stable (n = 100 vs 10⁴ within ~10%),
   while upper-tail statistics (p99, max) grow with n; and within one n = 10⁴ run,
   σ over the first 100 bodies ≈ the n = 100 value (it is a sample-size effect, not
   a change in the per-body process).
2. **Floor restores stability:** with b floored at the pair's mutual Hill radius,
   R_H = (2m_pair/3M*)^{1/3}·a₀ (perturber: R_H/b_max ≈ 0.13; m = 10⁻¹⁰ pairs:
   ≈ 0.016), the pert-channel σ_E spread across n = 100…10⁴ collapses to < 10%.
3. **Scaling laws return:** floored scan A (fixed m) slope ∈ [0.45, 0.55]; floored
   scan B (fixed total belt mass) slope ∈ [−0.55, −0.45]; σ_E·√n constant within 8%.
4. **Re-anchored verdict survives with floored anchors** (direction unchanged,
   numbers shift by the cutoff, expected ≤ ~3×): fixed-total-mass mutual ceiling at
   10⁹ still ≫ 10⁶ orbits (never inside a game); perturber channel still reaches
   ≥ 90% of the 51.2-bit ceiling within ~10² orbits at any N; an embedded body of
   roughly lunar-to-Pluto class still busts the 32-bit budget within a 30-game-year
   session.

What would falsify the tail diagnosis: floored σ_E still drifting with n (then the
n-coupling is structural in the MC and no N-extrapolation is admissible at all), or
the first-100-bodies σ of the n = 10⁴ run matching the full-run value (then the
per-body process itself changes with n and the model is broken, not the instrument).
