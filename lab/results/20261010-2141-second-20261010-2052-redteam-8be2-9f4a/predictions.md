# Predictions (written 21:47, before the decisive runs)

Context: checker 2 graded the run silver and named "the one experiment to gold":
re-issue with the corrected Kerr retrograde root, and **measure the winding images'
magnification** to close P2's open branch ("their visibility was not measured").
Everything below is written before `falsifier3.py` (corrected root) or
`magnify.py` (magnification) is run.

## What is replication and what is held out

The corrected retrograde numbers (b_retro = 6.138/6.832/6.997 at χ = 0.5/0.9/0.998,
ratios 1.50/2.41/3.32) were supplied and verified by both checkers, so matching
them is **replication**, not prediction. My held-out additions around it:

- R1: at the corrected (r_ph, b) the radial potential R(r) has a *double* root
  (R = 0 and R′ = 0 to solver tolerance); at the rejected branch's b, R′/|R| at
  r_ph is far from zero (≥ 10³ relative) — i.e. the rejected root is not circular.
- R2: limits a → 1: b_pro → +2, b_retro → −7 (Bardeen's limits), and at a = 0
  both senses → +3√3 (one value, two senses — the degenerate control the author
  wrongly relied on; here it is only a boundary check).
- R3: |b_retro| ≥ 3√3 ≥ b_pro for every a sampled (retrograde cannot be easier
  to capture than Schwarzschild).
- R4 (internal consistency): with b_crit_retro = 6.83 at χ = 0.9, `kerr_alpha(−6)`
  must be capture (no turning point) while `kerr_alpha(−7)` must be a finite bend
  — the original record's own α(−6) = inf was the unnoticed contradiction.

## Held-out: winding-image magnification (the named experiment)

Method (decided before running): exact image positions per branch (family ×
winding k) from the run's own oracle; magnification μ = (sin ψ / sin β)·(dψ/dβ)
per branch, derivative by central differences on the exact map. Scenes: the
dossier's (r_o, r_s) = (50, 200) and (10, 50), checker 1's deep case (6, 30),
and the weak control (5000, 20000) where the textbook point-lens formula applies.

Prior from strong-deflection theory (Bozza/Virbhadra–Ellis): per winding the
suppression is ~e^{−2π} ≈ 0.0019 for Schwarzschild, multiplied by distance
prefactors ~√(r_o·r_s)/b_c ≈ 19.2 (mid scene), 4.3 (near), 4.1 (deep) — these
compete, so I cannot pin the sign of the scene trend a priori. Honest ranges:

- M1 (controls of the instrument): Σ over images of signed μ ≈ 1 within 2% at
  every scene; at the weak control the two primaries match
  μ± = (u² ± 2)/(2u√(u²+4)) + 1/2, u = β/θ_E, within 1%.
- M2 (near scene, the scene the game promises): total winding share
  (Σ|μ| over k ≥ 1 images ÷ Σ|μ| over all images) between **0.1% and 5%**,
  roughly flat as the offset grows from 0.02° to a few degrees (near alignment
  every image's μ ∝ 1/β), then falling as the offset grows past ~10°.
- M3 (mid scene 50/200): winding share 0.1–3% (e^{−2π} dominates; the larger
  √(r_o r_s)/b_c prefactor pulls the other way — direction genuinely uncertain).
- M4 (deep scene 6/30): winding share the largest of the three (observer close
  to the photon sphere weakens the effective suppression), ≥ 0.5%.
- M5 (weak control 5000/20000): winding share < 0.5% (textbook relativistic
  images, ~e^{−2π} demagnified).

Decision rule for P2's open branch (fixed now): the "missing images the player
would see" sub-claim is **confirmed** if some single winding image reaches ≥ 1%
of the brightest image's flux in any promised scene (near/deep/mid); it is
**refuted (harmless in practice)** if every winding image stays < 0.1% of the
brightest everywhere; between those, **borderline**, reported with numbers.
