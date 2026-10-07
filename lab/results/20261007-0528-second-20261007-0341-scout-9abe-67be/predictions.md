# Predictions — second-author run 20261007-0528 (lattice = the checker's named gold experiment)

Written BEFORE the decisive run (`python3 lattice.py full`). Tuned on nothing
from the new lattice: policy set and kappa grid copied verbatim from the
original run; the only calibration runs were (a) the original's own scenes
(S2d, S3: bit-identical reproduction of the shipped record through my
instrumented layer), (b) a pilot at the exact 2:1 centre (phase 0) used to
shake out harness bugs, which is one of the 60 lattice rows.

## Measured before this file (context, not predictions)

- **The shipped "2:1 centre" S2c is mislabeled.** `n=1.0/2**(2/3)**1.5` in
  cadence.py parses as `2**((2/3)**1.5)`, giving n_per = 0.6857, not 0.5. The
  scene is a rotating forcing with n_b/n_per = 1.459, i.e. 2.3 W outside a
  3:2 commensurability, not at any resonance centre. The shipped numbers
  regenerate bit-for-bit; the label does not transfer. The checker's "3:2
  inversion" contrasted their correct 3:2 against this mislabeled scene.

## Pre-registered gate (fixed before the run)

A policy row HOLDS on a scene iff: not unbound, epump = e_layer/e_truth in
[0.8, 1.25] (B17's band), and da_rel <= 0.05 — at BOTH horizons (100 and 200
orbits; 30 and 60 for S1). Baseline per row = cheapest holding FIXED-n in
tide evals (1 eval/kick; TRIG*/TRIG2G cost 3 evals/kick). The mixed set =
60 lattice rows + S3 + S1.

## Predictions

- **P1 (first-order centres, 2:1 and 3:2, |Delta_1|/W = 0):** no policy in
  the set holds both gates at either horizon for >= 2 of 3 phases. The truth's
  coherent e-libration (pilot at 2:1: e 0.02 -> 0.100 at 100 orbits) is not
  representable by any impulsive midpoint-quadrature cadence; the layer is
  uncertified there independent of cadence. Consequence: no cadence rule,
  frequency-derived or not, can claim any cut on a mixed set containing
  first-order centres.
- **P2 (first-order edges, |Delta_1|/W = 2/3):** mostly uncertified as well;
  possibly FIXED-64 scrapes inside the gates on some phases. No cheap policy
  holds.
- **P3 (second-order centres, 3:1 and 5:3):** benign. Coarse de-phased
  cadences (GOLD, DEPH-2.5, TRIG2-2.0) hold both gates at <= 3.5 evals/orbit;
  cheapest holding FIXED is FIXED-4 or FIXED-8, so the eval cut is 1.5-3x,
  under 4x.
- **P4 (far detuning, |Delta_1|/W = 2, all resonances):** quiet. Same winners
  and same < 4x cut as P3.
- **P5 (global verdict):** no frequency-derived cadence rule reaches >= 4x
  total eval cut at held behaviour on the mixed set: first-order rows are
  uncertifiable at any cost, and on certifiable rows the cheapest holding
  FIXED is already coarse while the trigger pays 3 evals/kick. The local
  trigger is killed as a global cadence law on this layer; what survives is
  (i) the frequency selector — first-order commensurability within ~1 W
  forces the handoff to the resonant representation (law.md's doll), and
  (ii) ~1.5-3x eval cuts from de-phased coarse cadences on certifiable
  scenes. The engine's integer accounting (trigger = one compare, ~0 extra
  evals) would turn the kick cut (~2-5x) into the real number — to be
  re-measured there, not claimed here.
- **P6 (the inversion dissolves):** with correctly-built scenes there is no
  "2:1 vs 3:2 inversion" — at both first-order centres every cadence fails
  (P1), and away from centres de-phased coarse holds alongside dense fixed.
  The published inversion was an artifact of the mislabeled S2c.
- **P7 (quiet S1):** one global kappa cannot beat the fixed baseline in
  evals (TRIG2-0.125 ~ 28.5 evals/orbit vs FIXED-16's 16); its epump (1.48
  at 60 orbits) sits outside the band. The quiet-regime cut survives only in
  the engine's integer accounting.
