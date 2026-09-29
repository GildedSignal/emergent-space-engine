# Predictions (written before the 2,000,000-step run)

Case is frozen: e = 0.5, a = 1, h = T/200, 10^4 orbits, float64. Nothing was tuned.

## leapfrog (kick-drift-kick velocity Verlet)

- `energy_growth_exponent` ≈ 0, certainly ≤ 0.2. Symplectic at fixed h: |dE| oscillates
  bounded near its h² amplitude (I expect max|dE| somewhere in 1e-5…1e-3), with no secular
  trend; the 20 window maxima should be flat in ln t, so the least-squares slope is noise
  around 0. Rounding accumulation over 2e6 steps random-walks at ~1e-13, far under the
  systematic oscillation, so it cannot fake a trend.
- `bound_fraction` = 1.0 exactly (E stays near -0.5, never crosses 0).
- `steps_per_orbit` = 200 exactly (2e6 steps / 1e4 orbits, no substeps).
- Verdict: PASS on E1, B1, C1 — as this PASS-canary expects.

## euler (forward Euler, negative control)

- Energy is injected every step at O(h²), accumulating secularly → the orbit spirals
  outward and unbinds. I predict first E >= 0 within the first ~500 orbits, i.e.
  `bound_fraction` < 0.05 (likely ~0.005–0.05). B1 FAILS.
- After escape the force dies as 1/r² and E plateaus at E∞ > 0, so |dE| saturates at
  |E∞ + 0.5| ≳ 0.5. Since unbinding lands well before t = 0.1·t_end (orbit 1000), all 20
  windows sit on that plateau and `energy_growth_exponent` may come out ≈ 0 — E1 could
  accidentally pass. The discriminator for this negative is B1, not E1. If it instead
  unbinds after orbit ~1000, the windows catch the linear drift and E1 ≈ 1.
- `steps_per_orbit` = 200 (C1 passes trivially).
- Verdict: FAIL overall, via B1 at minimum — the control must fail.

## What would surprise me

leapfrog showing slope > 0.2 (would mean a real secular leak at this h, e.g. a bug in the
KDK order), or euler staying bound for all 10^4 orbits (would mean the step is somehow
symplectic, which forward Euler is not).
