# Predictions (written before the decisive gold run)

Run: 20261010-0352-second-…-7b82 (second author on 20261010-0306-spacex-acb2).
Task = the checker's named gold experiment: ≥5 seeds at ≥4000 pairs/bin under a hi-res
instrument (512 coarse / 24 zoom pts / 6 rounds — the checker's parameters), bin-jackknife
error bars on every headline number, and the closed form either re-derived with the
belt-edge weight or demoted. Shipped record already re-verified bit-identical in this tree
(7.4 s). Everything below is written from the checker's numbers and my Gaussian
conjunction model, before any 4000-ppb hi-res output exists in this folder.

Reference belt (unchanged from the original run): planar, a ∈ [1, 1+W], W=0.02,
e ~ Rayleigh(σ_e), N=1e4, star M*=1, a=1, v_K=1; M_belt ∈ {1e-7, 1e-5}.

- **PG1 (hi-res Λ).** 6-seed means: cold Λ(1e-4) ∈ [0.45, 0.62] and Λ(1e-3) ∈ [4.5, 6.0];
  hot Λ(1e-4) ∈ [0.24, 0.36] and Λ(1e-3) ∈ [2.1, 2.9]. Seed CV on Λ(1e-4) cold ≤ 25%
  (the checker's ×4.5 spread was at 900 ppb; at 4000 it should shrink but not vanish —
  the rate integral is heavy-tailed by construction).
- **PG2 (ρ exponent, 3 points 1e-4→1e-2).** Per-seed decade fit ∈ [0.85, 1.15]; 6-seed
  mean σ ≤ 0.06.
- **PG3 (jackknife bars).** Bin-jackknife σ/Λ: cold Λ(1e-4) ∈ [0.08, 0.60] (top bins
  carry ~40–50% of the rate); cold Λ(1e-3) ≤ 0.15 (better populated). If the Λ(1e-4)
  jackknife bar exceeds the seed spread, the honest error bar is the jackknife one.
- **PG4 (tail correlation).** corr = R_exact/R_product at (M=1e-7, q=1e-4): ln-spread
  σ ≈ 0.4 across seeds (checker's finding); 6-seed mean ∈ [0.8, 2.5]; the shipped 2.2 is
  an upper-tail draw. The design table must be quoted with corr as a seed band, not a point.
- **PG5 (q_v\* and the verdict table survive).** Median-over-seeds q_v* (M=1e-7) ∈
  [4e-7, 1.3e-6]·v_K. Table verdicts unchanged at 10⁹: 2⁻³² breaks by ≥ 500×, q=1e-5
  fits with ≥ 5× margin, q=1e-6 within a factor 2 of the 64-bit budget (still "marginal").
  For M=1e-5 nothing crosses a verdict boundary.
- **PG6 (W-scaling kills the closed form as-is).** K(W) = Λ·W/(N·ρ·σ_e) is NOT constant:
  K(0.1)/K(0.02) ∈ [1.5, 4.5] (checker: 0.16–0.34 measured vs 0.085 closed form at W=0.1;
  my mechanism: the reduced pdf of Δa/σ_e has a heavy tail, so ∫₀^{W/σ} x·p̂(x)dx grows
  ~ln(W/σ)). A two-parameter log-fit K = a + b·ln(W/σ) fitted on W ∈ {0.02, 0.1} predicts
  the held-out W=0.04 within seed error. Outcome either way: the closed form is demoted —
  the stated adoption path becomes the per-belt MC (one ≤ 60 s command per geometry).
- **PG7 (instrument convergence, the missing control).** Ultra-hi-res (2048/48/8) vs
  hi-res Λ(1e-4) cold agree within 5%. If > 10%, the instrument is not converged: VOID the
  rate numbers and escalate resolution instead of publishing.
- **PG8 (re-fit cadence).** At q=1e-5, M=1e-7: median T_refit ∈ [40, 160] sim-days
  (= 10–38 real hours at rtf 100 by 4.17 sim-days/real-hour — fixing the original run's
  "2.6 real hours" slip for 79 sim-days, which is ≈ 19 real hours).
- **Controls.** Blunt sampler undercounts ≥ 5×; widest bins return P = 0, both at hi-res.

Kill criterion: PG7 failure voids the numbers (instrument, not physics). If K(0.1)/K(0.02)
lands below 1.2, the checker's W=0.1 attack does not reproduce and the closed form survives
— that would be reported as the main result. If any verdict row crosses a boundary (PG5),
the dossier reports the new verdicts, not the old ones.
