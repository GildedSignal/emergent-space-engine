# Predictions — rung-free probe on the cadence law (written before the decisive run)

Question: does a kick cadence triggered by an error quantum (kick when the tidal
acceleration vector has changed by Q = c·mu_p/R^3 since the last kick) beat a
uniform clock cadence at equal behaviour, at equal or lower g-evaluation work?

Setup: 48-particle belt (a in {0.8,1.2,1.6,2.0}, e in {0.05,0.2,0.4,0.6}), circular
perturber (mu_p=1e-3, R=4), T=100. Truth DOP853 rtol 1e-12 (vs 1e-13 control).
Metric: p95 over particles of |delta e| at T (plus |delta varpi| secondary).

Predictions, none tuned on:

- P1 (main): on config A, the threshold law's Pareto front (error vs g-evals)
  dominates the clock law's by >= 2x in g-evals at matched p95 |delta e| in
  the range p95 |delta e| in [1e-3, 5e-2].
- P2 (eccentricity split): gain >= 3x on the e>=0.4 subgroup; gain < 1.5x on
  the e<=0.05 subgroup (near-circular: the tide varies at one slow frequency,
  a clock is already near-optimal).
- P3 (held-out, no retuning): on config B (perturber inclined 30 deg) and
  config C (mu_p=3e-3, R=3), with the same dimensionless quantum list
  c in {0.05,...,4.0} (Q scaled only by the tide scale mu_p/R^3), the >= 2x
  gain at matched error still holds.
- P4: |delta varpi| p95 follows the same ordering as |delta e| (the precession
  error falls with the same cadence law).
- P5 (kill criterion): if at matched p95 |delta e| the threshold law needs
  >= 2/3 of the clock law's g-evals on config A (gain < 1.5x) across the whole
  error range, the error-quantum trigger is dead as the q-cadence lever and the
  dossier says so.
- P6 (compounding check, B12-style): threshold's error at fixed c does not walk
  with T: spot-check config A at T=50 vs T=100 (error scales roughly like the
  number of uncorrected tide turnings, not super-linearly).

Machine state at run: 8 vCPU shared runner, load and free recorded in
machine.txt. Linux/x86 cloud timing: orders of magnitude only.
