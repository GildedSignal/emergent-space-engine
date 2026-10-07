# predictions.md — 20261007-1420-library-240c

Written before the probe `probe_b12_stat.py` runs. The requirement (law.md B12, HANDOFF risk
"the instrument"): a statistic that tells a **bounded** error from a **compounding** one on
per-seed Jacobi-error series, including chaotic-but-bounded ships, decided by type (slope
band), not by size. Cases below were chosen adversarially, not tuned on.

Cases (N = 2048 samples, one per doll-edge crossing, 16 seeds each; fixed RNG):
- `bounded-white`: sin + white noise, amplitude 1e-6.
- `bounded-chaotic`: logistic map (r=4) scaled to 1e-6 — deterministic, bounded, the case that
  broke the exponent.
- `leak-rw`: pure random walk, step 2.2e-8 (reaches ~1e-6 at the horizon).
- `leak-slow`: bounded amplitude 1e-7 + random-walk step 2.2e-8 (leak 10× under the bounded
  floor early on, dominant at the horizon — the redteam's separating case).
- `drift`: linear ramp reaching 1e-6.
- `fleet-16`: 15 chaotic-bounded seeds + 1 `leak-slow` seed.

Statistics compared: `expo` = OLS slope of log running-max|e| vs log t (the current gate's
shape: growth exponent on the median seed); `vario` = OLS slope of log variogram
γ(k)=Var(e_t−e_{t−k}) vs log k over dyadic k ∈ [8, 512]; `allan` = same for Allan deviation.

## Predictions

- **P1 (classification).** Variogram slope separates all five single cases into disjoint
  bands: bounded-white and bounded-chaotic ≤ 0.3; leak-rw and leak-slow in [0.7, 1.3] at the
  k-range where the leak dominates; drift ≥ 1.7. Allan slope lands at ≈ half these values
  with the same ordering.
- **P2 (the median fails, the tail catches).** On `fleet-16`, the current rule (median-seed
  exponent ≤ 0.2) PASSES the fleet — median seed is bounded — while the worst-seed variogram
  slope ≥ 0.7 flags the one leaking ship. A gate that judges the median certifies a fleet
  whose determinism is already lost on one seed.
- **P3 (the known miscalibration reproduced).** On `bounded-chaotic`, per-seed `expo`
  exceeds 0.2 on at least 2 of 16 seeds (an extreme-value artifact: the running max of a
  bounded chaotic series keeps creeping in log-log), while its variogram slope stays ≤ 0.3 —
  the inversion that made B12 "rank a bounded error above a compounding error" (H0215).
- **P4 (controls on both sides, else VOID).** Across 16 chaotic-bounded seeds, variogram
  slope never exceeds 0.3 (no false leak); across 16 leak-rw seeds it never falls below 0.7
  (no miss). If either control fails, this statistic is dead too, and the dossier says so.
- **P5 (information floor).** A leak whose accumulated magnitude stays below the bounded
  amplitude at the horizon is invisible to every statistic; the gate's horizon, not the
  statistic, sets the smallest detectable leak. Checked by one `leak-tiny` case (step 2.2e-10
  under amplitude 1e-6): variogram slope must read ≈ 0 (bounded), and that is correct
  behaviour, not a failure — within the scene the leak never reached any threshold a player
  or certificate could see.

## What would make me drop the variogram

Any band overlap between a bounded and a compounding case across all 16 seeds, or the
chaotic control crossing 0.3. Slope bands must also be stable when N doubles (checked at
N = 4096 for leak-rw and bounded-chaotic only).
