# Predictions — 20261008-1419-dynamics-5cbd (written before the decisive runs)

Written after: self-tests (drift exact to 1e-15, mu=0 control never diverges, Jacobi
conserved to 1.8e-6 and h^2-convergent) and ONE smoke atlas (mu=1e-3, T=300, 3 phases,
which showed teeth at a≈0.83, 0.86–0.87, 0.91 and a quiet interior a≤0.79).
No cadence run has been executed yet. The decisive experiments are the full atlas
(T=2000, 3 values of mu), the cadence sweep (mu=1e-3), and the held-out cases below.

## Held-out cases (not tuned on)

1. Atlas wall vs mu: for mu in {1e-5, 1e-4}, the outermost fully-quiet bin
   (all 4 phases censored at T=2000) satisfies 1-a_wall ≈ C*mu^beta with
   beta in [0.23, 0.30]; the mu=1e-3 wall lands within 0.02 of 0.80.
   I cannot cleanly separate 1/4 (prior dynamics run 0c67) from Wisdom's 2/7
   over one decade of mu; prediction is the band, not the winner.
2. T_div range at mu=1e-3 over the belt [0.60, 0.98]: >= 2 decades
   (min T_div < 40 orbits inside the teeth, >= 60% of bins censored > 2000),
   and neighbouring bins differ by >= 10x somewhere (teeth intermittency).
3. Cadence floor in the quiet belt (T_div censored, a <= 0.79, e0 Rayleigh
   sigma=0.02): Jacobi error at k=4 is already < 1e-4 (B12's threshold) for
   >= 95% of bodies; i.e. the floor is set by secular resolution, not chaos.
   Prediction: k_req = 4 there (the prior "8 for a belt" runs integrated belts
   closer to their perturber or longer; at e0 = 0.1 the floor rises to 8–16).
4. Transition region (T_div finite, 150 < T_div < 2000 at T_run = 200):
   required cadence rises with 1/T_div; if the split error is amplified by the
   body's own exponent (error ~ h^2 * exp(11.5*T_run/T_div)), then a collapse
   of ln(h_req) against 11.5*T_run/T_div is linear with slope near -1/2.
   If instead conjunction geometry (not chaos) sets the cliff, no such collapse.
5. Bimodality: at fixed k=8, the distribution of per-body max|dC_j| over the
   belt is bimodal — a peak below ~1e-5 (quiet) and a tail above 1e-3
   (chaotic, amplified); the split between them follows the T_div atlas
   (bodies with finite T_div < 200 land in the tail). This predicts B12-style
   exponent statistics conflate the law's error with the ship's own lambda:
   no cadence can bring a chaotic body's Jacobi error to the quiet floor.
6. Held-out scene: mu = 3e-4 with the rule fitted only on mu = 1e-3 data —
   behaviour thresholds still held at the rule's cadence (definitions below).

## Behaviour thresholds (frozen before the sweep)

Per body vs a converged leapfrog truth (hdiv=1024, cross-checked at 2048):
- primary: max |dJacobi| < 1e-4 over the run (B12's frozen threshold);
- secondary: |da|/a < 1e-3, |de| < 5e-3, precession-rate error < 2%.
k_req(a) = smallest k in {2,4,8,16,32,64} holding the primary threshold for
>= 75% of bodies in the bin (secondary reported, not gating). Where no k<=64
holds it, the bin is "unschedulable by cadence" (goes to the dense tier).
Total-kick comparison: sum of k over bodies for the adaptive rule vs the
uniform cadence that holds the primary threshold everywhere it can be held.
