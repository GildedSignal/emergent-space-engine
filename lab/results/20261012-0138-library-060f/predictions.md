# Predictions (written before the probe `probe_b12.py` ran)

Question: can a range-scaling (Hurst-type) classifier `Ĥ` — the slope of log R(k) vs log k,
R(k) = median over windows of (max−min) of the error series, evaluated on the top 3 dyadic
octaves only — separate bounded from compounding error where B12's current statistic (a global
growth exponent of log|e| vs log t, ≤ 0.2 pass) misranks, and where the recurrence ratio
(lab 6 Oct, silver) failed (slow leak vs bounded)?

Calibration classes (amplitudes ~1e-6, floor 1e-12 as in law.md's B12):
- bounded_band, bounded_osc_noise → median Ĥ in [0.00, 0.25]
- diffusive_leak (random walk) → median Ĥ in [0.45, 0.55]
- linear_leak (drift + noise) → median Ĥ in [0.90, 1.05]
- explosive (e^{λt}) → median Ĥ > 1.1
Frozen rule from these: Ĥ ≤ 0.33 → bounded; Ĥ > 0.33 → compounding. Decision = median over seeds.

Held-out cases (not tuned on):
1. bounded_band under the CURRENT B12 statistic: median global exponent > 0.2 (the gate fails a
   bounded error — reproduces H0215's misranking), while Ĥ says bounded.
2. sin_drift (bounded oscillation + drift 2e-5·A per step): current B12 exponent < 0.2 (passes
   the gate, wrongly), Ĥ > 0.65 (flags the leak). If this holds, the misranking is demonstrated
   on a held-out case in both directions.
3. near_unit_root (AR(1), ρ = 0.995, horizon 2^14): median Ĥ in [0.40, 0.60] → reported
   compounding-at-horizon. Correct within the horizon; asymptotically it is bounded, so the
   gate must state its horizon.
4. reflected_rw (random walk, reflecting walls at ±10σ, horizon 2^14): median Ĥ in [0.40, 0.55]
   → compounding-at-horizon. Prediction: NO statistic can call it bounded within this horizon
   (mean hitting time ≈ (B/σ)² = 100 steps << 2^14, so actually walls are hit often — the series
   IS stationary and distinguishable). Risk flagged: if walls are hit often, R(k) saturates and
   Ĥ may come out low. Either way the run tells us which regime the gate is in.
5. bounded_plus_jumps (band + Poisson jumps, rate 5 per series, amplitude 3A, mean-reverting):
   Ĥ ≤ 0.35 → bounded. Risk flagged: jumps add one localized octave of range growth; median over
   windows may keep the slope low, but this could fail.

Kill criterion for the classifier: any calibration class overlapping another's decision band,
or any of 1, 2, 5 coming out opposite to the above.

Noise-floor sensitivity (lesson: sampling under the floor is noise): adding an iid floor at
1e-12 to a bounded band of amplitude 1e-8 changes neither Ĥ (uses the band) nor the verdict,
while the current exponent's estimate on the same series varies by more than its own pass
threshold (0.2) between two subsamplings.
