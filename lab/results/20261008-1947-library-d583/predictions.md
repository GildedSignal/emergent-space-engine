# Predictions — 20261008-1947-library-d583

Written before the decisive run. The probe tests the board's own unexplored lead (r8 v2 "Next"): *a pair's miss distance at successive conjunctions is quasi-periodic, so its next close conjunction is predictable — each pair paid once per element change, not once per orbit* (the premise behind "steady-state work per orbit → 0").

Setup (not tuned on): coplanar two-body ellipses around one primary, with secular apsidal precession ϖ(t) = ϖ₀ + g·t (the analytic-generator regime; g emulates J2/third-body secular rates). Truth: brute-force root-finding of every conjunction over 150 synodic cycles; miss distance d_k at conjunction k. Model: Fourier series (3 harmonics) of one per-conjunction phase advance Δ, fit on conjunctions 0–99 (the "paid once" observations), predicting held-out conjunctions 100–149. Close threshold τ = 3 × min(d) over the full sequence.

Cases I have NOT tuned on, and what I expect:

1. **Random non-resonant pairs** (8 seeds, a₂/a₁ ∈ [1.03, 1.25], e ∈ [0, 0.3], g ∈ [0, 0.003]·n): the phase advance per conjunction is nearly constant, so a 1-frequency model should hold. Expect: median held-out misclassification of close/far ≤ 1 per 50 conjunctions; next-close-conjunction index error ≤ 1; held-out RMS ≪ (max−min)/2 of d.
2. **Positive control (g₁ = g₂)**: sequence exactly periodic in k. Expect fit residual ~0 and perfect held-out prediction (instrument check — if this fails, VOID).
3. **Near-resonant pair (n₂/n₁ = 1 + 1/301 style, tiny synodic rate)**: few conjunctions, long horizon per conjunction; secular drift accumulates over each long synodic period. Expect the 1-frequency model to degrade (misclassification > 1 per 50) — I predict partial failure here and will report it as such (resonance kills averaging, r4 v2 lesson).
4. **High-eccentricity pair (e ≈ 0.5)**: waveform of d_k vs phase is non-sinusoidal; expect the 3-harmonic fit to still capture shape, index error ≤ 2. If it fails, the model class (not the premise) is too small.

Kill criterion for the premise (written before the run): the pay-once premise dies at this rung if case 1 (non-resonant, the belt's regime) shows median misclassification > 1/50 held-out conjunctions OR median next-close-conjunction index error > 2. It survives with a named cost if case 3 fails (resonant pairs need their own certificate), and that cost is reported.

Work accounting predicted: pay-once = 100 paid observations per element change amortized over horizon → 0 per additional orbit; vs re-examination per orbit (r8 v2 measured 786 work per encounter for element-sort). Expect the amortized observation count per conjunction to fall below 1 after ~100 conjunctions without element change (i.e. steady-state per-orbit candidate work → 0).
