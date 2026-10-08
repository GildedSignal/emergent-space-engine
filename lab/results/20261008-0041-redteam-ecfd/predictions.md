# Predictions — run 20261008-0041-redteam-ecfd

Written before the decisive grid. Tuned on: the pipeline calibration only
(exact-vs-closed-form at fixed turning points; the EOB-2PN machinery's nu->0
limit against the exact Schwarzschild advance, pbar = 50, e = 0.6).
Everything below is held out: I have not run these cases.

## Setup

Compare, at IDENTICAL geometric turning points (u_p, u_a), e = 0.6
(r3 v3's hardest tail), pbar = 2/(u_p+u_a) in {20, 30, 50, 100, 200, 500, 1000}:

- `shipped`: exact Schwarzschild advance (the eob-doll's shape: the compiled
  geodesic is exact Schwarzschild; nu enters only through the 1PN energy map,
  which moves the orbit at fixed real energy only at 2PN order).
- `GR2PN(nu)`: the 2PN effective-one-body Hamiltonian
  A = 1-2u+2*nu*u^3, Dbar = 1+s*6*nu*u^2 (both signs s), F = A^2*Dbar.
- `oracle1PN`: 6*pi/pbar (the 1PN oracle family r3/B11 judges against).

## Predictions

1. **Scale.** rel(nu=0.25) := (shipped - GR2PN)/GR2PN scales as c(nu)/pbar with
   c of order unity: at pbar=20 between 1% and 20% in magnitude; at pbar=100
   between 0.2% and 4%; at pbar=1000 below 0.5%. Sign unknown a priori
   (EOB resummation could put the exact-shape above or below GR).
2. **Monotone in nu.** |rel(0.25)| > |rel(0.1)| > |rel(0.01)| ~ 0, and
   rel(nu->0) -> 0 (machine zero; that is the calibration, but monotonicity
   from 0.01 to 0.25 is held out).
3. **Dbar sign.** Flipping s changes rel(nu=0.25) by < 1e-3 absolute
   (Dbar's 2PN term first moves the periastron at 3PN).
4. **Oracle family.** (oracle1PN - shipped)/shipped = +4.5/pbar + O(1/pbar^2)
   from my integrator: about +30% at pbar=20, +4.8% at 100, +0.45% at 1000,
   and the sign is always positive (published expansion; the integrator
   confirming it is the held-out part).
5. **c2 fit.** Over pbar in {30,40,60,80}: shipped gives c2 = 4.5 +- 0.1;
   GR2PN(0.25) gives c2 in [1, 8]; the gap c2_GR(0.25) - 4.5 is the law's
   leading GR error coefficient.
6. **Gate reach.** B11's precession tolerance (0.01 + 2*8/pbar) exceeds both
   the shipped-vs-GR gap and the oracle-vs-GR gap at pbar <= ~30, so B11 can
   pass both the shipped law and a law with a different 2PN coefficient there
   (arithmetic once 1-5 land, not a free prediction).

## Kill criteria for my own claim

- If rel(nu=0.25) < 0.5% at ALL pbar >= 20 (i.e. c2 gap < 0.1): the premise
  SURVIVES — the shipped construction is closer to GR than anyone measured,
  and I report that as the result (it is still unmeasured by any gate).
- If the machinery's controls (nu->0 limit, Dbar sign, closed form) fail, the
  run is VOID regardless of the numbers.
