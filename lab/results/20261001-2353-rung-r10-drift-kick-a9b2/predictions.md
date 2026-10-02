# Predictions (written before the decisive run)

Design constants fixed a priori from the geometry (never tuned on a graded case):
changeover outer edge R0 = 1.3 R_H (covers the 0.9 R_H, e0 = 0.3 births' apoapsis 1.17 R_H),
inner edge R0/3, smoothstep window; sub-stepping while the local planet period < 40 sub-steps,
factor 3, depth cap 9; base step P/128 for ships and moons, P_ship/128 for the resonant cases.
Only the self-test and three probe moons (0.5/0.3/0.6 R_H, e0 = 0/0.2/0.15, 5-20 periods) were
looked at before this file; none is a graded seed.

## Held-out expectations

1. **B12 Jacobi, soi-switch (negative control):** median growth exponent above the 1e-12 floor
   in [0.4, 1.0] — events3 measured 0.83; the hard switch injects a same-sense jump per crossing
   and there are >= 20 crossings per ship. It must fail `jacobi`.
2. **B12 Jacobi, wh-fixed:** close passes unresolved (the kick sees the planet at one instant of
   a fast transit): random-walk error, median exponent in [0.3, 0.8]; fails.
3. **B12 Jacobi, symba:** bounded: exponent in [-0.05, 0.2]; max |dC_J/C_J| over a ship's series
   in [1e-6, 1e-4] (the changeover's edge kicks at base cadence set the level, not growth).
4. **B14 class:** symba >= 0.97 of judged moons in the reference's class (the gate needs 0.99 —
   called narrow); wh-fixed in [0.4, 0.7] (inner moons destroyed by star-drift); soi-switch
   >= 0.9 (planet-drift is the right dominant body inside, its cost is at the switch).
5. **B14 apsides:** symba within 10% of the reference's rate on >= 0.95 of rated bound moons;
   the risk sits at a in [0.7, 0.9] R_H where the window is half-open and the sub-step rule no
   longer subdivides (local period ~ 40-90 base steps). wh-fixed fails outright (< 0.5).
6. **Resonance:** the changeover never engages (ship inside, min separation >= 23 vs R_H <= 10),
   so symba, wh-fixed and soi-switch are the same map at P_ship/128: libration ratio >= 0.9 in
   every librating case, identical to the last bit across the three; excursion-metric borderline
   cases (within 20% of 2pi) excluded per B17's rule.
7. **Cost:** symba median force evals per orbit in [110, 160] (moons dominate: 3-9 sub-steps per
   base step of P/128); wh and soi near 26-128; truth's real count ~1e4-1e5 per orbit (reported
   separately, 0 in the metrics by the rung's convention).
8. **Truth's own drift:** below the 1e-12 floor on most ships (no exponent to judge), and the
   reference converged (1e-12 vs 1e-13) on >= 90% of the 16 frozen ships.

## What would change my mind

If symba's B12 exponent comes out > 0.2, the smooth changeover's edge kicks have a systematic
sign per crossing — the DLL98 anti-term balance is wrong somewhere, and the rung kills it.
