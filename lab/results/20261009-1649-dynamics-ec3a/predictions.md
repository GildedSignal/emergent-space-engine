# Predictions — run 20261009-1649-dynamics-ec3a (dynamics lens)

Written BEFORE the decisive runs, after instrument calibration only
(short T=300 main config; controls C1/C2 and held-outs H1-H3 untouched).

## The question

In a belt under the design's own regime (dominant parent, exact compiled
Kepler drift, secondary tide + optional J2 as kicks), how concentrated is the
per-body rate of element-quantum crossings (the law's (E,L) memo re-keys =
distinctions = kicks/recompiles)? If a uniform-tick policy must pay the p99
rate for everyone, its waste is 1 − mean/p99. This feeds q-cadence (the
acknowledged lever: "correctors and higher-order splits buy nothing, so
cadence is the lever") and the unmeasured H_live risk (distinctions per
game-second decide whether 10^9 fit in 8 GB).

## Configurations (decisive set)

- C0 main: m'=0.03, e'=0.05, a' = 1, belt a in [0.28, 0.40], e0 in [0, 0.15],
  N=1024, T=2400 (n'=1 units; ~1700 belt orbits at mid-belt),
  quanta qa=3e-3 (E-native, q_a ~ 1e-3 a) and qe=1e-2, mults {1, 3.16, 10}.
- C1 negative control: m'=0 (pure Kepler). Must give 100% frozen, r=0;
  else the instrument leaks and the verdict is VOID.
- C2 positive control: belt pushed to the stability edge and MMR overlap
  (a in [0.36, 0.46], e'=0.15). Must show strong concentration (S >= 8,
  walkers >= 30%); else the instrument is blind to structure (VOID).
- H1 held-out: m'=0.06 (tide doubled).
- H2 held-out: e'=0.3 (aggressive secondary; large ejection fraction is
  expected and is reported, not hidden).
- H3 held-out: J2 = 0.01, R/a' = 0.1.

## Predictions (held out: none of these configs was used for calibration)

- P1 (C1): frozen = 100%, all rates 0 at every mult.
- P2 (C2): walker fraction >= 0.3, S_key(p99/mean) >= 8, ejected <= 0.15.
- P3 (H1 vs C0): mean key-rate scales with m' within [1.5x, 2.6x];
  S_key within [3, 9]; walker fraction grows but <= 2x C0's.
- P4 (H2 vs C0): e-layer mean rate scales with e' by [3x, 7x]; a-layer S_key
  within a factor 2 of C0; ejected >= 0.3 (the belt crosses the S-type
  stability edge, a_c ~ 0.28 for e' = 0.3, so most of it is expected lost).
- P5 (quantum sweep, all configs): at these law-scale quanta the mean rate
  is NOT proportional to 1/mult (that proportionality is the averaging-leak
  floor seen at sub-floor quanta in calibration); frac_zero grows with mult
  (bodies whose secular range is sub-quantum freeze out); S_key grows or
  stays flat as mult grows, within a factor 3.
- P6 (burstiness): the busiest time-decile of crossings carries <= 3x the
  uniform share in C0/H1/H3 (the secular clock spreads re-keys); C2 may
  exceed that.
- P7 (C0 baseline values, from the physics not the calibration run):
  S_key in [3, 10]; walker fraction in [0.25, 0.75]; frozen fraction
  <= 0.3 at mult 1.

## Kill criterion (decisive)

If C0's S_key < 3 at every mult AND walkers < 0.25 (flat surprise
distribution at law quanta), the concentration premise is dead: a uniform
cadence is already near-optimal for belts, and the dossier says so (a lead,
not a failure of method). If S_key >= 10 anywhere in C0, the claim is
adoption-grade for q-cadence.

## Instrument floor (measured in calibration, reported for honesty)

Below q_a ~ 3e-4 a the crossing counts scale exactly as 1/quantum: that is
leakage of mixed-frequency tide terms (p·n − q·n') through the time-domain
double average, not secular signal. The design's law never sees those terms
(its kicks are orbit-averaged analytically, H0190), so the decisive runs
place quanta above that floor.
