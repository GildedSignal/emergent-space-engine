# Predictions (written before the decisive runs)

Held-out cases: the seeded ensembles (Random(20261002)) below were not tuned on; all
derivations here are analytic, done before any binary sweep, transfer chain or flyby run.

## eob-doll

- **Precession.** With Darwin (p, e) as effective elements, the exact Schwarzschild advance is
  6pi/p (1 + (4.5 + 0.25 e^2)/p + ...). The 1PN Damour–Deruelle oracle with harmonic turning
  radii (p, e) has J^2 = p + 4 + (2 - nu) e^2 + O(1/p), i.e. 6pi/J^2 = 6pi/p (1 - (4 + (2 - nu) e^2)/p + ...).
  So the candidate runs OVER the oracle by about (8.5 + (2.25 - nu) e^2)/p. The 1% gate then
  needs p >~ 850-930. With p log-uniform in [20, 1000] I predict `precession_pass_fraction`
  ~ 0.02-0.04: **fail**. The candidate is not wrong physics; it is un-truncated (2PN+) where
  the oracle is 1PN.
- **Period.** The 1PN parts should agree (EOB is 1PN-exact; the repo's own test-mass gates say
  the residual is ~300/p^2). Excluding cases with truncation estimate 300/p^2 > 5e-4 (p < ~775,
  ~94% of cases) I predict the remaining ~6% pass within 0.1%: **pass** with heavy exclusions.
- **nu effect.** At e = 0 the map gives T(nu)/T(0) - 1 = nu(E_eff - 1) = -nu q/2, and the oracle
  gives -(3/2)(q1/q0)nu - q0 nu/8 = -nu/(2p) by hand expansion: exact match. At e > 0 I expect
  agreement to a few per cent: **pass** (>= 0.99), sign negative (heavier nu shortens the period).
- **Handoffs.** A symmetric free-return chain has antisymmetric tidal error about each encounter,
  so the per-cycle energy drift may cancel to first order (exponent ~0); if the systematic tide
  inside the planet doll dominates instead, the error grows ~linearly (exponent ~1). I predict an
  exponent in [0, 1]; the <= 0.2 gate is genuinely uncertain. This is the interesting number.
- **Assists.** Patched geodesics vs N-body at b in [1.5, 50] R_p: neglected star tide during the
  encounter ~ 3e-6 relative, neglected planet pull outside the SOI ~ 1e-4 relative. I predict
  `assist_pass_fraction` = 1.0: **pass**.
- **Events.** Binaries are one doll solved by quadrature: 0 events per radial period: **pass**.

## test-mass (negative)

Orbits m1 = (1 + sqrt(1 - 4 nu))/2 with the same absolute p: period scale 1/m1^2 (>= 0.04% even
at nu = 0.01, % at nu = 0.25), advance scale m1. Predicts: precession ~0, period ~0 (fails),
nu term has the WRONG SIGN (T grows with nu via p/m1(nu) while the oracle's shrinks): fails.
Negative must die: **it does**.

## newton-doll (negative)

Advance exactly 0 vs 6pi/J^2: 100% off everywhere: precession fails all cases. Period is Kepler
(1PN corrections of order 15%-0.15% over p in [20,1000] exceed the 0.1% gate nearly everywhere),
nu term is zero: fails sign. **Dies.**

## Verdict

Predicted: eob-doll killed on precession (and possibly handoff exponent); negatives properly
killed; the method (dolls, EOB) survives with the named fix: truncate the effective dynamics at
1PN (or judge against an oracle at matching order / gate at p where 2PN < 1%).

## Addendum (after a 3-case diagnostic probe, before the ensemble)

A spot probe of the ported oracle against the candidate formulas (p=100 e~0, p=100 e=0.5,
p=1000 e=0.3, nu=0.1) falsified two predictions above BEFORE the seeded ensembles ran:
- nu: the oracle's nu term is -2.7e-3 at e~0 (candidate -5.0e-3 per unit nu: ~1.8x off) and
  POSITIVE at e=0.5 (candidate always negative): sign mismatch. The fixed-label identification
  of Darwin (effective) elements with harmonic turning radii is itself nu-dependent at 1PN.
- period: the candidate-vs-oracle difference carries that nu-identification error, so at high e
  it exceeds 0.1% even where the oracle's own 2PN truncation (300/p^2) is small; period may fail
  too, not just precession.
No re-tuning was done: metric definitions are the rung's. These probe values are recorded so the
checker can distinguish prediction from fit.
