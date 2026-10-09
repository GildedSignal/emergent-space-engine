# Predictions — run 20261009-2212-dynamics-79ef (dynamics lens)

Tuned ONLY on seed 0, width 0.05, m=1e-7, cold (30-orbit + 28-orbit diagnostics runs).
Observed there: λ (events/body/orbit) plateaus ≈ 0.68 by orbit ~20; e_rms grows 0.038→0.047
from orbit 16→28 (exponent ≈ 0.35, no ceiling visible); energy drift ≤ 2.3e-4.

Decisive runs: N=600, dt=0.02, f=1, g=1.5, T=150 orbits (200 for w=0.30).
Held-out = everything below, run after this file is written.

| # | Case | Prediction (falsifiable) |
|---|------|--------------------------|
| P1 | seeds 1,2,3 cold (w=0.05, m=1e-7) | λ over orbits 50–150 = 0.68 ± 0.05; e_rms still rising at orbit 150 with exponent 0.2–0.5 (no fixed point in e) |
| P2 | hot start, seed 1 (e0=0.15) | λ converges to the SAME plateau 0.68 ± 0.10 (rate independent of e over e∈[0.03,0.15]); e_rms stays ≈0.15 (no damping mechanism exists) |
| P3 | width 0.10, seed 4 | λ_stat ≈ 0.34 ± 0.03 (geometric halving: λ ∝ 1/width) |
| P4 | m=8e-7 (R_H ×2), seed 5 | λ_stat in [1.2, 2.0] (≥ geometric 1.36, focusing adds); b(τ=1 orbit) LARGER than baseline |
| P5 | sparse belt w=0.30, seed 6, T=200 | λ_stat ≈ 0.68/6 = 0.11 ± 0.02 (geometric), rate shape unchanged |
| P6 | branching, baseline seeds 1–3 | b(τ=1 orbit) < 0.2; shuffle control |b_shuf| < 0.03; cluster sizes (gap 0.5 orbit) geometric with ratio < 0.2 |
| P7 | per-body tail (allocator input), seeds 1–3 | events per body per 10-orbit window: p99/median < 3.5, and within 1.5× of a Poisson synthetic stream with the same λ(t) |

Interpretation commitments (what each outcome means):
- P1+P2 hold ⇒ the surprise rate is a precomputable attractor set by geometry (N, width, m);
  the allocator may schedule encounters as Poisson at a generator-computed constant rate.
- P1 fails (λ drifts with e) ⇒ rates must be re-estimated continuously; no static schedule.
- P6 b ≥ 0.5 or non-geometric cluster tail ⇒ avalanches; p99 frame budget needs a ≥10×
  multiplier gate that the plane currently lacks.
- e_rms saturates anywhere (contradicting P1 second half) ⇒ a conserved-quantity/stirring
  ceiling exists; would CHANGE the prediction for old belts (rate depends on age).
- Any run with |dE/E| > 1e-3 ⇒ that run's statistics are VOID (dt too large there).

Kill criterion for the configuration (not the method): if the shuffle control fails
(|b_shuf| ≥ 0.03) the branching estimator is broken and all P6/P7 conclusions are VOID.
