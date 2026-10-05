# Predictions — kick-schedule premise probe (written before the decisive sweep)

Controls already run (not tuned on): S0 converges to truth by n=256 (C1: dpre
+2.2e-4 at both n=256 and n=2048 — estimator floor, not drift error; C2-3b
floor +3.2e-3). The decisive sweep (S0/S1/S2a/S2b at n = 2..32 on C1, C2, C3)
has NOT been run. Held-out predictions:

- **P1 (tail shape).** |dv| mass per orbit is heavy-tailed where the
  perturbation is distance-concentrated: C3 (J2, e=0.6) top-decile share
  ≥ 0.5, Gini ≥ 0.4; C2 (third body, e=0.05, R2=3) top-decile share ≤ 0.35
  — the near-circular tide is flat, nothing to concentrate.
- **P2 (positive control, known physics).** S1 (uniform eccentric anomaly)
  beats S0 (uniform time) on C1/C3 at equal n by ≥ 2x in precession error at
  n=8. If this fails, the testbed is suspect and the run flags itself.
- **P3 (accumulation is load-bearing).** S2b (accumulate below the quantum,
  fire at it) beats S2a (drop below the quantum) at every equal event budget,
  by ≥ 5x in precession error: dropped mass is coherent (mostly radial), so
  S2a's error tracks the dropped-mass fraction.
- **P4 (the budget win, and where it fails).** S2b at ~8 events/orbit stays
  within 2x of S0's behaviour at 32 events/orbit on C1 and C3 (≈ 4x fewer
  events at equal behaviour); on C2 no schedule beats S0 by ≥ 2x — when the
  tail is flat, event scheduling buys nothing and cadence is already right.
- **P5 (negative control).** Every schedule at n=2 is off by ≥ 10% somewhere
  (C1/C3), and errors shrink monotonically in n for S0, S2b.

What would make the premise wrong instead: if S2b tracks S0 exactly at every
budget (no concentration gain), then event scheduling adds bookkeeping for
nothing and the fixed phase step stays; if S2a ≈ S2b, then the sub-quantum
tail is weightless and pure deletion (no accumulation state) is enough.
