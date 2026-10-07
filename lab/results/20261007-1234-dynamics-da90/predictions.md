# Predictions — run 20261007-1234-dynamics-da90

Written BEFORE the decisive full run (ensembles of ≥400 pairs, K=3000 conjunctions).
Smoke (30 pairs, K=600, seed 1) informed code correctness only; these predictions are
about ensemble behaviours I have not tuned on.

Instrument control (must hold or the run is VOID):
- C1: the first_hit port matches brute force on 300 random instances.

Configurations and my expectations:

1. **generic** (absorb policy): work_ratio (cert-touched conjunctions / all conjunctions)
   ≤ 0.03; late = 0; every truth encounter is found by the certificate path (hits +
   invalidator-triggered regrants = encounters). Median first-hit ≥ 20 conjunctions.

2. **precession** (g_rel ≈ 7e-4 rad/yr, absorb + slide-margin 0.15 rad): late = 0, but
   slide re-grants dominate: grants per pair ≥ 5× generic. This is the honest cost of
   relative apsidal drift IF absorption is not enough on its own.

3. **precessionNoM** (absorb, no slide re-grant): uncertain, and this is the deliberate
   held-out bet. Absorption treats the window slide as a rigid translation of D(u),
   which is exact only to first order (D depends on u and u+Δϖ separately). Over a
   certified span of ~30 conjunctions with ~0.05 rad/conjunction of relative drift
   (~1.5 rad total), I expect the shape mismatch to break the window: late > 0 on at
   least a few percent of encounters. If late = 0 anyway, absorption + window safety 2
   suffices and precession costs nothing — the strongest possible result for the design.

4. **noabsorb** (negative control): window frozen at grant time, slide ignored entirely.
   Must fail: late > 0 substantially. If it does not fail, my slide model is wrong.

5. **snaps**: sub-quantum accumulator with a 2nd-harmonic phasor. Generic pairs:
   bounded accumulator, snap rate ≤ 0.2 per pair per K=3000. Near-resonant pairs
   (2α within the same band): linear drift, snap rate ≥ 10× generic.

6. **resonant** (α seeded within 3/q² of p/q, 7 ≤ q ≤ 64): encounter spacing clusters
   at multiples of q (coherent recurrence; the keyhole/resonant-return structure);
   median first-hit < generic median (the phase where certificate work stops
   amortizing). Work ratio per pair still low overall but the per-encounter work
   (touches/encounter) is ≥ 2× generic.

7. **kicks**: exogenous flyby kicks (Δa/a up to ~0.15). Prediction: regrants ≈ kicks
   (each kick invalidates its pair's certificate once); growth of total grants with
   kicks is linear (branching ratio ≤ 1, no cascade); late = 0 still (kicks are
   truth events the cert re-grants on).

8. **resonance fraction** (generic ensemble): with the correct criterion
   min_{q≤64} ||qα|| < window half-width (~0.02 turns), a large fraction of pairs
   (≥ 30%) sit within one window width of some low-order resonance, but only those
   with small q (≤ 20) produce coherent recurrence. Report both fractions; the
   q ≤ 20 fraction is the one that needs a promotion gate.

Kill criteria (self-imposed):
- late > 0 in generic/snaps/kicks/precession(absorb) → the certificate policy fails
  the completeness contract → that configuration is killed, not the method.
- noabsorb passing clean → my negative control cannot fail → VOID for the slide claim.
- snap rate generic ≈ resonant → coherence claim dead.
