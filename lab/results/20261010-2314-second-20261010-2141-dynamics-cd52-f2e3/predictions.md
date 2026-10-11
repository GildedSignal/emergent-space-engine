# Predictions (written before the decisive dt×N×μ matrix; anchors already reproduced)

Anchors (bit-exact vs shipped matrix2_raw.log / wm5, so the census leaves the dynamics
untouched) ran first: neg, pos_s1, n200_s1 (mu=1e-4), m5n200_s1, wm5_s1 — all identical
to the shipped record. The decisive blocks below have NOT been piloted at any seed.

The question: is lambda ≈ 3/orbit at mu=1e-5 (P5 cell, fb=0, dH=1.9e-3) REAL belt chaos
(Wisdom–Tremaine dense-ring scattering, lambda/Ω ≈ 0.4–0.5, mass-insensitive) or
MANUFACTURED by sub-resolution conjunctions (then it must fall as spon grows, since the
resolution radius shrinks with dt, and fall with mu at fixed spon)?

Blocks (all --conj, T=50 orbits except N=800 at T=25):
- B: mu=1e-5, {N=50,200} × spon {64,256,1024} × seeds {1,2,3}; N=800 × spon {64,256,1024} × seeds {1,2,3} at T=25.
- C horizon check: N=200, spon {64,1024}, T=25, seeds {1,2,3}.
- D mu-axis: N=200, spon {64,1024}, mu {1e-6, 1e-7}, T=50, seeds {1,2,3}.
- A record completion (mu=1e-4, N=200, T=200, seeds {1,2}): cad64, cad256 — E1's corrected truth base.

Predictions, each falsifiable:

- **P2 (dt-robustness — the decisive one).** Median lambda_exp at N=200, mu=1e-5, T=50
  stays within ±25% from spon 64 → 1024 (ratio in [0.75, 1.30]; checker's pilot:
  2.99 at 64, 3.23–3.40 at 256). Manufactured chaos instead falls monotonically ≥ 30%.
- **P3 (level).** For gate-passing cells (n_sqrt = 0 pairs below sqrt(m·dt)):
  lambda_exp/Ω in [0.35, 0.55] (lambda_exp in [2.2, 3.5] at a=1).
- **P4 (mu-insensitivity, WT prior).** lambda_exp(mu=1e-6)/lambda_exp(mu=1e-5) ≥ 0.6 at
  N=200 spon=1024 (real collective scattering is mass-insensitive at fixed K; manufactured
  scales with the sub-resolution event rate and collapses). At mu=1e-7 (K≈0.72) I allow a
  decline and will report it as the sparse-regime edge rather than a refutation.
- **P5 (N/K axis).** All three N (K = 0.39, 0.155, 0.062) sit in the dense regime, so
  lambda_exp stays in [2.2, 3.8]; no monotone N-trend larger than 25%.
- **P6 (admission gate separates regimes).** mu=1e-5, T=50 cells have n_sqrt = 0 at
  spon ≥ 64 (observed at spon=64 N=200 s1: min r 1.5e-4 > 7.0e-5); the corrupted mu=1e-4
  cell has n_sqrt ≈ 10, m5n200 at T=200 (fb=84k) n_sqrt = 1. Gate failure coincides with
  fb > 0 / dH ≫ 1 corruption.
- **P7 (fallback blindness).** At least one mu=1e-5 cell at spon ≥ 256 shows fb > 0 while
  its spon=64 twin has fb = 0 (coarse cadence misses ejections), or fb = 0 across B; either
  outcome is reported, and both support "fallback is not a cleanliness certificate".
- **P8 (horizon robustness).** lambda_exp(T=25) within ±15% of lambda_exp(T=50) at N=200
  spon {64,1024} — licenses the N=800 T=25 block.

Kill criteria for the silver's mechanism claim:
- CONFIRMED manufactured (dossier right, checker wrong) if median lambda_exp falls ≥ 30%
  monotonically 64 → 1024 at fixed N=200, mu=1e-5, in gate-passing cells.
- REFUTED (real chaos) if dt-robust (P2 holds) AND mu-insensitive (P4 holds): then
  lambda_max ≈ 0.4–0.5 Ω is the belt's physical floor (H_live's floor), and the
  surprise instrument is valid WITHOUT the changeover exactly where the gate passes.
