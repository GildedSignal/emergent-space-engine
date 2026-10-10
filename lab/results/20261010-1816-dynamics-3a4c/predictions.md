# Predictions (written before the ladder runs; smoke test only ran 8 orbits)

Scene: Sun + circular Jupiter (a=5.204 AU, mu_J=9.5459e-4) + massless belt,
the engine's own split: exact Kepler drift (the tube) + full Jupiter tide as
one impulse per kick. Cadence K = kicks per Jupiter orbit, powers of two,
shared boundaries (block steps). Truth = top ladder cadence. Behaviour of a
body = (mean e, std e, max e) of its e(t) history over 120 Jupiter orbits,
sampled every 4 orbits. Sufficient cadence K* = min K with all three scalars
within max(10-15% relative, absolute floors 2e-3/1.5e-3/3e-3).

Predictor zeta: from BIRTH elements only (what the compiler holds: the body's
n and the perturber's n_J, both compiled before any integration):
zeta = min over (p<=8, q in {1,2}) of |p*n - (p+q)*n_J| / (n_res * C * sqrt(mu_J) * e0^(q/2)),
one scalar C calibrated on belt A only, then frozen for B and C.

Held-out cases (not tuned on): belt B = a in [3.6,4.6], e Rayleigh(0.12)
(different resonance set, 3x the eccentricity); belt C = belt A's range but
mu_J x3 (fresh seed).

- P1 (concentration): on belt A, K* spreads >= 8x between median and p90;
  uniform-cadence-at-p99 costs >= 5x sum(K*) over the belt.
- P2 (tuning belt): Spearman rho(log K*, log zeta) <= -0.6 on belt A.
- P3 (held-out B): with C frozen, rho <= -0.6 AND the calibrated K*(zeta)
  map lands within a factor 2 of measured K* for >= 75% of bodies.
- P4 (held-out C, mu x3): rho <= -0.6 with the same C; median finite-time
  Lyapunov exponent (truth run, shadow renormalized every half orbit) rises
  by 1.4-3.5x vs belt A (libration-frequency scaling ~ mu^(1/2)).
- P5 (the cliff): bodies that fail even at the top cadence (the phase-feedback
  regime r4 found) concentrate at small zeta: >= 70% of never-sufficient
  bodies have zeta < 1 (calibrated units).
- P6 (mechanism): on bodies with lambda > 2e-3 /yr (above the 120-orbit
  detection floor), Spearman rho(log lambda, -log zeta) >= 0.5.

Kill branch: if P2 fails (rho > -0.4 on belt A), then birth frequencies alone
cannot schedule kick cadence; q-cadence must measure surprise (FTLE probes or
phase feedback), not predict it from the memo. That negative is itself the
deliverable.

# Addendum: predictions for experiment 2 (written BEFORE running exp2)

Diagnostics after experiment 1 (120 orbits, belt A): e_std is ~0 for all
bodies (no resonant pumping unfolds); the FTLE is shear-dominated (uniform
~7e-3/yr baseline = ln(1+s*6yr)/6yr with synodic shear s; resonant excess
only ~10%, concentrated at the 4:1). So at this horizon behaviours are
cadence-insensitive and P1/P2 fail AS STATED - the horizon, not the kick
rate, sets the bill. P4's lambda-ratio will also read ~1 for the same
instrument reason (shear baseline, not chaos).

Experiment 2 (pre-registered now): belt C physics (mu_J x3, fresh seed, same
a-range, e Rayleigh 0.05), horizon 600 Jupiter orbits, two 250-body subsets
chosen from BIRTH elements only: NEAR = smallest zeta_raw (resonance-proximal),
FAR = largest zeta_raw. Ladder {4,16,64,256}, truth 512.

- P7: at 600 orbits NEAR bodies develop e-excitation (median e_std > 3x the
  120-orbit belt A level) while FAR bodies stay flat (e_std < 1e-3 median).
- P8: cadence bites in NEAR only: median K*(NEAR) >= 16 while median
  K*(FAR) <= 4 (ladder floor); a uniform cadence covering NEAR's p90 costs
  >= 4x the scheduled sum over both subsets.
- P9: the NEAR/FAR split is a threshold in zeta alone (one number from the
  compiled frequencies): >= 90% of bodies needing K* >= 16 have zeta below
  the belt median of zeta.
- Kill branch: if NEAR and FAR behave alike at 600 orbits, then kick cadence
  in this regime is a non-lever below 64/orbit even resonance-adjacent, and
  the cadence question must be re-derived from what the certificate checks
  (event horizons), not from belt dynamics.
