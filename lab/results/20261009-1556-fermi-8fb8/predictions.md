# Predictions (written before the decisive run)

Revision 2, after instrument bring-up on seed 1 at k ≤ 8 (tuning only):
the first policy-B definition was ill-posed — the joint entropy of
(rank, residual) is identically H(x), because the map is a bijection; a
relabeling cannot compress. It is replaced by the honest decomposition:
reabsorption works through (i) the permutation gauge (interchangeable
bodies give up identity at recompile) and (ii) a 2-param program refit.
A scale bug (double √2 in the program quantiles) was fixed; H_noprog now
matches the analytic value (11.03 vs 11.05 bits).

Question: does H_live — live distinguishing bits per body in a belt stored as
program + scars — stay bounded in steady play, and at what rate is it created
per game-second? Model: encounters are a Poisson stream of impulsive element
kicks; the store keeps state, not history.

Hand estimate: a tied body's deviation from its program is an unbiased random
walk, σ_k = σ₁√k, so per-element scar bits ≈ ½·log₂k + log₂(σ₁√2πe/δ).
The multiset branch (identity given up, program refit) should sit well below
it: reabsorption removes the reshuffle, leaving quantile-coupling residuals.

## Held-out cases (tuned on seed 1 only; seeds 2, 3 held out)

- P1 (growth law, per tied body): H_A slope 0.50 ± 0.08 bits per doubling of
  k over k = 2⁰…2¹³. The Gaussian kernel is its own analytic control:
  H_A(k) ≈ ½log₂k + log₂(2πe)^½ + log₂(σ₁/δ) − (atom correction at k ≤ 2³).
- P2 (units check): H_A(δ/2) − H_A(δ) = +1.00 ± 0.02 bits at every k.
- P3 (Rutherford tail): Pareto-2 kicks (median-calibrated, 100× range)
  inflate H_A by ≤ 3 bits vs Gaussian at k = 2¹³. ≥ 6 bits kills the √k law.
- P4 (reabsorption gap): H_multiset (sorted-match vs 2-param refit, identity
  given up) grows at ≤ 0.35 bits per doubling and sits ≥ 2 bits below H_A at
  k ≥ 2⁶ for both kernels. If H_multiset ≈ H_A (gap < 1 bit), reabsorption
  fails: the belt's memory is the full walk field and the answer flips.
- P5 (dimension): 2-D joint with correlated kicks (ρ = −0.6) ≤ sum of the two
  1-D entropes (penalty 0.3–1.5 bits); never super-additive.
- P6 (control, no program): H_noprog ≈ 11.0 bits flat in k (the value of the
  program at birth; the gold's 0.126 bits replaces this).
- P7 (creation vs retention): kick-stream entropy h_kick ≈ 2–4 bits per
  encounter; created-per-retained ratio at k = 2¹³ ≥ 1000.

## Sizing (applied after the run)

Store per body ≈ H_multiset + f_tie·H_A + ~0.13 program bits + index, where
f_tie is the fraction of bodies whose identity is tied (observed, scarred,
event-recorded). Budget: 8 GB / 10⁹ bodies = 64 bits/body. Pre-estimate for
d = 5 elements, σ₁/δ = 8: the multiset branch stays ≤ ~8 bits; tied bodies
cost 5·(½log₂k + 3 + 2.05). The 10⁹ fit is decided by f_tie and by the
recompile cadence, not by N — pre-estimate: fits for f_tie ≤ 10⁻³ at k = 2¹³.

## What kills the claim

- P1 slope ≥ 0.8 per doubling (chaos amplifies kicks, H2557-style): the belt
  is a dense gas; memory is linear in play time; 10⁹ does not fit.
- P4 gap < 1 bit: reabsorption does not work; same conclusion.
- Estimator bias at N = 2¹⁶ (Miller–Madow applied; plug-in bias ≤ 0.03 bits
  at these bin counts — if exceeded, instrument broken → VOID).
