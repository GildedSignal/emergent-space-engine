# Predictions — second-author run on 20261007-0528-fermi-aab3

Written BEFORE the decisive integration (`enc3.py`). The checker (silver verdict) named two
unpinned quantities: f_emb (embryo fraction — the headline creation rate spans 6 orders on
it) and the impulse accounting (their ×57 conjunction-speed correction). Neither the author
(v_rel = v_K) nor the checker (v_rel = 0.0175·v_K, the epicyclic median) used the right
relative speed at large conjunction distance: for b >> e·a the conjunction is
shear-dominated, v_rel ≈ 1.5·b·n, so the impulse kick scales 2μ/(b·v_rel) ∝ μ/b², not μ/b.
I integrate the exact restricted three-body problem (Sun + perturber on a circular orbit +
massless belt-0 rock, DOP853 rtol 1e-12) to measure the true per-conjunction element kick
δ vs measured closest approach b, and recompute the 8 GB gate with the f_emb uncertainty
replaced by a total-perturber-mass bound.

## P1 — strong-scatter radius (control against known physics)

The b where the integrated median kick reaches δv/v = 1e-3 for a 1e22 kg perturber lies
within a factor 2 of 3 Hill radii, r_H = (μ/3)^{1/3}·a = 1.2e-3 AU at a = 1.25, i.e. in
[1.8e-3, 7.2e-3] AU. (The author had 1e-5, the checker 5.7e-4; if my integration lands at
either, the Hill-scaling expectation is wrong.)

## P2 — the kick law beyond the epicyclic scale

For b ∈ [0.03, 0.15] AU (>> e·a ≈ 0.0125, << annulus), the median integrated kick follows
the shear law δv/v ≈ (4/3)·μ/b² within a factor 3, and the log-slope of δv/v vs b lies in
[−2.6, −1.6]. Both the author's 2μ/b and the checker's 2μ/(0.0175 b) (slope −1) would then
overestimate by 30–100× at 0.1 AU. If instead the slope is ≈ −1 at the checker's
normalization, adiabatic shielding does not operate and the checker's numbers stand.

## P3 — the 1-bit radius

b_bits (integrated median δv/v = 1e-6) for 1e22 kg lies in [0.03, 0.2] AU (shear-law point
estimate 0.082). The author said 0.01, the checker ~0.5.

## P4 — the f_emb collapse under a mass budget

In the shear regime the creation rate is C ≈ k·(M_pert/M_star)·bits per 1e9 rocks,
independent of how M_pert splits into embryos (rate ∝ b_bits² ∝ μ cancels f_emb = M_pert/(μ·N)).
Predicted: with M_pert ≤ 1e-3 M_star (a disk heavier than that is unphysical — the star
dominates), C < 100 bits/s game-time at 1e9 bodies spread at belt-0 local density, i.e.
≥ 1 order below any ~1e3 bits/s tube-filling floor, and the stated scenario (1e25 kg =
5e-6 M_star) gives C ≤ 1 bit/s. The 6-order f_emb uncertainty collapses to ≤ 2 orders
(sensible disk masses 1e-6..1e-3 M_star).

## P5 — honest r8 v2 claim check (frozen parameters)

At frozen N = 1e4 with (σ_e, ρ) drawn log-uniform from the rung bands (σ_e ∈ [1e-3, 3e-2],
ρ ∈ [1e-5, 3e-4]), my reimplemented rate model matches belt 0's (1.7e6 candidates, 427
encounters/20 orbits) within a factor 2 only for σ_e ≲ 5e-3 (a low draw, ~25% of the band);
at σ_e = 1e-2 (the author's assumption) the encounter count misses by ≥ 3×. Prediction: I
reproduce the checker's in-band match (σ_e = 3e-3, ρ = 1e-5) within ×1.3 on both numbers.

## What would kill the run's claim

If P2 fails toward no-shielding (slope ≈ −1 at the checker's normalization) AND P4's mass
bound is ignored, creation at f_emb ≳ 1e-3 would sit at or above the floor: the dossier's
priority call ("gate f_ind, build nothing for encounter memory") would need the mass
argument stated, not just f_emb.
