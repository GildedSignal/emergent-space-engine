# Predictions — second-author run 20261011-2028

Written BEFORE the decisive runs (corrected sweep + image-resolved memo
prototype). Instrument setup already run: reproduction of the silver record
from the shipped attack.py (bit-identical JSON, both calibrate and sweep).

Two classes of predictions, honestly labelled:

- **[REPRO]** Not held out: the checker already published these numbers
  (converged table dφ=7.5e-4, 4000 α). My prediction is that MY fix
  (substep re-integration of the arrival step, dφ=3e-3 global, h=dφ/128
  local) lands within a few % of them. This is a double-check of the
  checker, not a held-out claim.
- **[OUT]** Held out: never measured by anyone (checker or author).

## Instrument (quad validation, [OUT] for the bound only)

- Q1 The fixed table's A_t agrees with an independent u-space Gauss–Legendre
  quadrature (sin²ψ substitution at turning points and grazing launches) to
  better than 1e-5 relative and 1e-3 M absolute at EVERY arrived column of
  every scene r_e ∈ {6, 8, 20, 60, 200, 1000}. A_phi to better than 1e-5 rad.
- Q2 The ORIGINAL table's A_t (linear interpolation across the arrival step)
  exceeds 1 M error somewhere in the b range of the scenes (checker: +24 M at
  r_e=1000, b=20–77; +14 M at r_e=60; +1.1 M at r_e=6), concentrated at small
  b (nearly radial out-family columns). Reproducing the checker's finding.

## Corrected sweep ([REPRO] with my numbers)

- S1 r_e=6: delay 30.9 → ~38 M, err_phase ~0.14–0.17, err_design ~0.09–0.12,
  err_fix ~0.05–0.11 (the silver's 9.9e-3 "14×" was an artifact). The
  per-family delay memo does NOT reach err_phase/10 at the ISCO — P8's
  r_e=6 clause flips from held to FAILED on the converged record.
- S2 r_e=8: err_fix stays ~2e-2 (per-family fails), err_design ~0.06.
- S3 r_e=20: err_fix ~1e-3 ±40% (per-family marginal-to-failing vs the
  1.45e-3 floor; the <1e-4 clause of P8 fails).
- S4 r_e ≥ 60 rows change <2% (the silver's fix claim for the single-image
  regime stands: err_fix/err_phase ≥ 25×).
- S5 P8 re-derived on the converged record: "err_fix < err_phase/10 at every
  r_e ≤ 20" FAILS at all of 6, 8, 20; "<1e-4 at r_e ≥ 20" holds only at
  r_e ≥ 60. The delay is still the dominant error term (err_fix collapses
  25–150× at r_e ≥ 60), but the per-family memo is insufficient at ≤ 20 M.

## Image-resolved delay memo prototype at r_e ∈ {6, 8, 20} ([OUT])

The memo keyed per image (arrival family + winding segment + local α window
±0.35 rad), travel time dt_img(b) and bend_img(b) from the same light-tube
table; crossing solved as te = t_obs − dt_img(b(te)) with b from the bent
arrival direction; tracked image followed across frames by (σ, branch,
α-continuity ≤ 0.35 rad).

- I1 r_e=8: median err_img ≤ 1.45e-3 rad (one pixel) — the floor the
  per-family memo misses by ~15×. Estimate ~1e-4.
- I2 r_e=6: median err_img ≤ 1.45e-3 but with tails above it (photon-ring
  winding images, table interpolation through A_phi ~ 2π segments);
  disclose the tail fraction.
- I3 r_e=20: median err_img ≤ 1.45e-3 (easily; single-image-dominated).
- I4 Ablation (same image-resolved memo, b from the UNBENT flat chord):
  at r_e=8 the residual err_img_flat ≥ err_img_bent × 3 (the bent-b lookup
  matters in strong lensing); at r_e=20 they are within 2×. Uncertain —
  this is a genuinely held-out number.
- I5 Frames where the tracker jumps (no α-continuity match) are ≤ 35% of
  frames at r_e=8 (the author measured 31% refinement instability there);
  for jumped frames the memo is still evaluated against the frame's own
  tracked root, and disclosed separately.

## Kill criterion for the gold attempt (pre-registered)

If median err_img > 1.45e-3 rad at r_e = 8 (the image-resolved memo does
not reach the player floor where the per-family memo provably cannot), the
silver's proposed fix is INSUFFICIENT as stated and I report that as a
partial refutation: the delay column is necessary (S1–S5 still stand) but
not sufficient in the multi-image regime.
