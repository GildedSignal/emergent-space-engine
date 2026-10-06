# predictions.md — run 20261005-2231-q-cadence-7d0d

Written before the decisive mixed scenes (mixed.py). Tuned on: the replica's
validation (DOP853/RK4 control, classical quadrupole rate), drift exactness,
and the moon frontier grid (f x e). NOT tuned on: the held-out points below.

## The rule under test

N*(body) = ceil2( KAPPA * (1+e)^GAMMA * n / |n - n_p| ), routed out of the
kick layer when |q n - p n_p| < 2 W_pq (resonance) or 1 - a/a_p > mu^(1/4)
(wall). KAPPA ~ 4, GAMMA ~ 3-5 expected from the frontier grid.

## Held-out predictions

1. **Moons at f = 0.225, 0.275, 0.45 (B14 horizon, 50 planet orbits):** the rule
   passes apsidal-10% + e-max + regime on >= 99% of phases at a total kick cost
   4x below the fixed 64 cadence. The frontier grid predicts the fixed 8 fails
   at f >= 0.35 for e0 = 0.3, and 16 fails at f = 0.45.
2. **Retrograde moons (0.3 R_H, e0 = 0.2):** need roughly half the prograde
   cadence (the tide's harmonic content is lower); the rule over-pays there —
   predicted pass with ~2x margin, not optimally.
3. **Belt (a in [0.38, 0.64] sep, e in [0.02, 0.2], 150-300 planet orbits):**
   the rule (synodic term: n/|n - n_J| is 1.3-2 for the interior belt) gives
   N ~ 8-32 per body; the fixed 8 passes out-of-band bodies (27ce's finding),
   the fixed 128 wastes 4-16x. In-band bodies (2:1 at 0.63, 3:1 at 0.48, 5:2,
   7:3 wings): NO fixed cadence up to 64 holds B17 (a9c2); the rule routes them
   (surrogate N=1024 in the replica, cost reported separately).
4. **Resonant pairs (3:2 mu=3e-4 at +-1.5 W, 2:1 mu=1e-3 at +1/3 W):** out-of-
   band (1.5 W): K* <= 4 holds B17 (a9c2's far result); the rule's synodic term
   gives N ~ 4-8 there. In-band (+1/3 W): everything up to 64 fails; routed.
5. **Error type:** at the rule's cadence the apsidal error saturates (does not
   walk) when the synodic term dominates; the Jacobi error on B12 ships walks
   linearly at every cadence (quant-5022), so the ship branch of the rule is
   horizon-sized, not horizon-free — the named gap.
6. **Where the rule breaks:** e -> 0.6+ (harmonics beyond (1+e)^GAMMA), the
   retrograde branch, and mu_p far from 1e-3 (the grid is one-mu).

## What would falsify the rule

A held-out moon point where the rule's N fails the 10% apsidal bar while a
fixed cadence at 4x the cost passes; or the belt out-of-band bodies failing at
the rule's N while passing at 8.
