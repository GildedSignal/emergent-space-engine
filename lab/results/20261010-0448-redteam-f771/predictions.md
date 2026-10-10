# Predictions — 20261010-0448-redteam-f771

Written before the decisive run. Held-out domain: outside r1's frozen seed set
(e ∈ [0, 0.7] bound only). Cases here: bound e ∈ [0.75, 0.99] with periapsis
r_p ∈ {7, 8, 10} M, plus massive hyperbolic flybys (E ∈ [1.05, 2.0], r_p ∈
{8, 10, 15} M). r1's own tolerance bands are applied unchanged: precession 1%,
period 0.1%, shape 1%, crossings ≤ 512.

## P1 — precession (r1 `prec` band, 1%)
The linearization error per band is second order in band width (~4.4% in r at
m=16) but periapsis passages grow stronger with e. I expect the 1% band to
hold through e ≈ 0.9 and to break somewhere in e ∈ [0.93, 0.99] at r_p = 7–8 M.
Prediction: precession error ≥ 1% for at least one case with e ≥ 0.93 and
r_p ≤ 8 M; < 1% for all cases with e ≤ 0.9.

## P2 — coordinate-time period (r1 `period` band, 0.1%)
dt/dφ is the exact rule on both sides; only u(φ) differs, so period error
tracks shape error, which is smaller than precession error. Prediction: within
0.1% for all e ≤ 0.9; marginal (0.1–1%) at e ≥ 0.95, r_p ≤ 8 M.

## P3 — loop shape (r1 `shape` band, 1%)
Turning points are where the band model is worst. Prediction: apoapsis error
< 0.5% everywhere; periapsis error < 1% up to e = 0.95, ≥ 1% only at e = 0.99
with r_p = 7 M, if anything.

## P4 — crossings per cycle (r1 `cost` band, ≤ 512)
Band crossings scale like the number of octaves in r_a/r_p ≈ (1+e)/(1−e).
Prediction: ~40 at e = 0.7, ~100 at e = 0.9, ~250 at e = 0.99; all ≤ 512.

## P5 — exact cycle repetition (r1 `repeat` criterion, 1e-12)
Structural, not statistical: the band dynamics is reversible and the loop in
(u, u′) retraces, so Δφ and Δt per cycle repeat identically at any e — error
type is "fixed function of (E, L)", non-compounding (principle 13). Prediction:
cycle-to-cycle variation of Δφ at the 1e-12 level (float noise only) at e = 0.95
over 100 cycles. This one I expect to SURVIVE.

## P6 — massive hyperbolic deflection (no r1 criterion exists — held out entirely)
No frozen band for massive-particle scattering; I use the light-gate band (1%)
as the reference. Prediction: banded deflection within 1% of the exact
Schwarzschild value for r_p ≥ 10 M at all E ≤ 2; error ≥ 1% at r_p = 8 M once
E ≥ 1.4 (the relativistic slingshot regime a player will actually fly).

## What would make each prediction matter
- P1/P2/P3 failing at e ≥ 0.9: r1's PASS is envelope-limited; player-visible
  (eccentric transfer orbits and near-mass flybys are the navigation core,
  principle 30); the seed set must be re-frozen wider.
- P5 holding: positive evidence — the band error cannot compound by
  construction; worth stating in the design.
- P6 failing at moderate E: a whole regime (massive scattering) ungated.
