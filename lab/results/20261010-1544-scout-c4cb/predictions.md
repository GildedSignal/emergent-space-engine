# Predictions — run 20261010-1544-scout-c4cb

Written after calibration (seed 1, nb=256, D=12L, grid in `grid_calib.json`),
BEFORE any held-out run below. Frozen pass rule: final observer position
error <= 1e-3 (in units of D) AND |dE_final| <= max(0.01*|work_true|,
1e-6*|E0|), scene non-vacuous. Frozen minimal passing news config from the
calibration grid: lmax=2, rate=8 per P_ref (innermost heavy planet's
period), bits=32, per-l quantization scale from kinematic bounds only.

Notation: config (lmax, rate, bits).

## H1 — body-count scaling (the aggregation claim, K1)
Scenes: nb = 64 and nb = 1024 light bodies (nested draws, same seed 1,
same planet phases, disk total mass fixed at 2.0), D=12, e=0.1, 8.37 obs
orbits. Config (2, 8, 32).
- PREDICT: PASSES at both nb, with the same live-channel count (8 reals)
  and the same news bits/time (8 reals x 32 bits x 8 / P_ref = 2048 bits
  per P_ref). The required config does not get finer as the body count
  grows 16x. (If either nb needs finer rate or bits, aggregation dies:
  news cost would track body count, not mass-distribution bandwidth.)
- PREDICT: the news channel's quantization error contribution from the
  light disk SHRINKS with nb (incoherent power ~ m_tot^2/nb); pos_err at
  nb=1024 <= pos_err at nb=64.

## H2 — distance grading
Scene: seed 3, nb=1024, D=24L (2x farther), e_obs=0.2.
- PREDICT: (2, 8, 32) PASSES (easier: quadrupole/monopole ~ (L/D)^2
  shrinks 4x).
- PREDICT: (1, 8, 32) FAILS — the dipole (star wobble) is not enough even
  at 24L; the tide's work is quadrupolar. Grading cuts higher l with
  distance, but never below l=2 for a system whose internal structure
  does work on the observer.

## H3 — independent seed
Scene: seed 2, nb=1024, D=12, e=0.1. Config (2, 8, 32).
- PREDICT: PASSES (calibration did not see this seed's phases).

## H4 — error type at 4x window (compounding, K2)
Scene: seed 1, nb=256, D=12, e=0.1, 32.37 obs orbits (4x window). Config
(2, 8, 32).
- PREDICT: the position-error trajectory grows at most LINEARLY in time
  (fitted exponent <= 1.0 over the 8 checkpoints), no exponential
  divergence; bounded field error with a linear readout random-walks the
  position, it does not compound. Energy error stays within the frozen
  rule extended to the longer window.

## H5 — adversarial fast heavy mass (bandwidth tracks the distribution)
Scene: seed 4, nb=256 light + one intruder m=0.3 (3% of orbiting mass) at
a=0.12L, e=0.4 (period ~ P_ref/3.9). Base stream rate 64 per P_ref.
- PREDICT: (2, 8, 32) FAILS — one fast heavy body raises the channel's
  required bandwidth; news rate tracks the mass distribution, not the
  count or the distance.
- PREDICT: (2, 32, 32) PASSES (~8 samples per intruder period). This is
  the engine's hierarchical fix arriving by measurement: the intruder
  needs its own faster channel (its own doll), the rest keeps rate 8.

## What would make the whole premise wrong
- H1 failing at nb=1024 (or needing finer news): aggregation false.
- H4 showing exponent > 1 or energy error growing secularly beyond the
  rule: the channel's error compounds (principle 13 violated) — news
  cannot be absorbed by a plain integrator.
- H5 passing at rate 8: bandwidth would NOT track the mass distribution;
  the grading rule (fast light mass below the quantum, fast heavy mass
  above) would be wrong.
