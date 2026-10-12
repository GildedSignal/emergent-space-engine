# Predictions — second-author run on 20261012-1524-fermi-4b55

Written before any code of mine is run. Context: the checker's verdict names the
gold experiment (fix the sign-flipped Newton in crosscheck §2, regenerate the
10⁹ table, reconcile the record). I therefore know the checker's reported
values; independence here comes from a fresh implementation of the truth
instrument plus controls the original run never had (dt-convergence, a second
seed, window stability under one code path). Cases marked [held-out] are the
ones no one has yet measured in any run.

Units: doll (GM_star=1, a=1, v_K=1, orbit=2π); anchor a=3 AU, M_star=M☉;
T_orbit = 1.64×10⁸ s; quantum q_v = 10⁻⁵ v_K.

## The named experiment

1. **SOI truth by brute force (my own implementation).** Belt 10⁴ bodies,
   σ_e = 5.5×10⁻³, a ∈ [1.0, 1.5], seed 42; planet μ = 10⁻³ at a_p = 1.25,
   circular; R_SOI = 0.0867; episodes counted at rising edges of (dist < R_SOI).
   Predict: rate ∈ [1.0, 1.6]×10⁻² transits/body/orbit at 20 orbits (inside the
   original pre-registered P3 range 0.01–0.05). Reproduces the checker's
   1.30×10⁻² only as a bound, not a target.
2. **[held-out] dt convergence.** dt = 0.3 → 0.15 → 0.075. Predict: rate changes
   by < 5% per halving (episode counting converged; a larger drift means the
   instrument, not the physics, sets the number — then I must say which).
3. **[held-out] second seed.** Same belt, seed 43. Predict: rate within ±10%
   of seed 42 (a 10⁴-body MC over 20 orbits averages ~2600 episodes; Poisson
   scatter ~2%, seed-to-seed belt variation dominates but stays small).
4. **Sign-fixed Newton** (one-line fix `t += dth/dng` in the run's own §2
   machinery, seed 42). Predict: within 15% of the brute force, and strictly
   above the as-shipped 1197 hits.
5. **[held-out] window stability.** 60 and 200 orbits, brute force, seed 42.
   Predict: both within ±10% of the 20-orbit rate (no synodic truncation of
   near-resonant bodies at a ≈ a_p).
6. **Regenerated 10⁹ table** (computed in code from the measured rate — the
   missing code path): rebinds ≈ 7.9×10⁻²/s → H_live(rebinds) ≈ 10 bits/s,
   co-dominant with the player's ~10 bits/s (the original "player nil" flips);
   contacts ≈ 3.4×10⁻³/s × 256 bits ≈ 0.9 bits/s with the 3 AU anchor fixed;
   total H_live ≈ 20–21 bits/s ≈ 2.6 B/s ≈ 9–10 kB per hour of play; singleton
   saturation 1/Γ ≈ 77 orbits ≈ 400 game-years ≈ 4 wall-years at rtf 100.

## What would falsify the corrected claim

- Brute-force rate outside [0.01, 0.05]: the pre-registered range fails for a
  third time and the headline stays unsettled.
- dt non-convergence > 5%: the truth instrument is resolution-limited.
- Sign-fixed Newton disagreeing with brute force by > 25%: the run's machinery
  has a second defect beyond the sign (then brute force alone decides).
- Any 8 GB-scale term other than post-repopulation mixed entropy appearing at
  the corrected rates: the budget conclusion changes.
