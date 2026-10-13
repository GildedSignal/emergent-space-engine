# Predictions — 20261013-1249-spacex-5b98 (the Λ* map)

## Disclosure (order of work)

The controls (0e79's D row at alt 1.0), the r/R bisections (L0–L4), the retro bisect (L2) and the
e-bisections (L2, e ∈ {0.3, 0.6, 0.9}) all ran as one grid invocation BEFORE this file was
written (the grid finished in 99 s, inside the window where I intended to stop it before the
held-out axes). Everything above is therefore **post-hoc** and is reported as such in the
dossier. What is genuinely held out: the three cases below, chosen to test the empirical law
extracted from the post-hoc grid, at grid points it has never evaluated. The law:
**Λ* = C(r/R)·(1+e)^p / √(1−R/r₀)**, with C drifting 1.83→2.47 as r/R falls 2.86→1.19 and
p = 2.7–2.9 read off the e-ladder at matched r/R.

## Held-out predictions (frozen before the flights)

- **P-H1 (the law off-grid, e-axis at another level).** L1, e = 0.6, bisect alt in [1.5, 6]:
  predicted alt* ∈ [3.6, 3.95] (central 3.75), i.e. Λ* ≈ 9.4–10.0. The law must hold at a level
  whose e = 0 boundary (alt* 1.969) is far from the e = 0.6 solution.
- **P-H2 (mirror symmetry with eccentricity).** L2, retro, e = 0.6, bisect [1.2, 5]: predicted
  alt* = 2.5791 **bit-exactly** the pro row's (identical fate classes and world times at every
  alt), because retrograde prograde-brake is a mirror of the prograde case and the only symmetry
  breakers (the Moon, the star's tides) moved nothing at 0.3% resolution in the e = 0 retro row.
- **P-H3 (the law off-grid, e-axis at L0).** L0, e = 0.3, bisect alt in [2, 8]: predicted
  alt* ∈ [3.55, 3.75] (central 3.65), Λ* ≈ 4.5. A second independent extrapolation, at the
  weakest thrust where flights are longest.
- **P-H4 (no reachable crash basin at L ≥ 5).** L5 and L6 at alt 1.01 (r/R = 1.110, the lowest
  practical start): both ESCAPE — the boundary curve at r/R ≥ 1.10 requires Λ ≤ Λ(alt 1.01, L5)
  = 10.9 > 6.6 = the near-surface asymptote of the e = 0 curve, so no altitude above the surface
  can crash at L5+. If either crashes, the near-surface asymptote (or my C-drift extrapolation)
  is wrong.

## Scorecard (filled after the held-out runs)
- P-H1: **FALSIFIED.** Measured alt\* = 3.3296 (Λ\* 7.42, r\*/R 3.659) against the predicted
  [3.6, 3.95] (Λ\* 9.4–10.0): the law over-predicted Λ\* by 26%.
- P-H2: **HELD, bit-exactly.** alt\* = 2.5791, Λ\* 8.91, and every flight in the bisect
  matches the pro e=0.6 row's fate class and world time (t = 82.6 / 6693.5 / 1404.8 / 6858.8 /
  6941.4 / 7024.1 / 1570.1 / 1652.7 / 7106.7 s …).
- P-H3: **FALSIFIED (borderline).** Measured alt\* = 3.4983 (Λ\* 4.10) against the predicted
  [3.55, 3.75] (Λ\* ≈ 4.5): missed by 1.4% in alt, 9% in Λ\*.
- P-H4: **HELD.** L5 and L6 at alt 1.01 both ESCAPE (minR/R 1.027 / 1.071) — no crash basin
  reachable from above the surface at L5+, as the near-surface asymptote predicts.
