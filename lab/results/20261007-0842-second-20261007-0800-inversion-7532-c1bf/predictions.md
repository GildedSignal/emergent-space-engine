# Predictions — the checker's named experiment for 20261007-0800-inversion-7532

The checker graded the inversion silver and named the experiment: implement the gold's ACTUAL
watch — k = 4 nearest by current distance (min of both directions, per the gold's own
pre-registered definition, confirmed in its predictions.md #5) — **rebuilt on set-change**, and
measure **misses plus rebuilds** across the inversion's own scenes (B σ_e ∈ {0.005, 0.02, 0.05},
C shear, D bath; A control added for the full record). Same seeds, same `truth_pair`, same ρ as
the inversion: the scenes are regenerated from its code (`make_pop` copied verbatim), and its
`events.csv` must regenerate bit-identically (P0). These predictions are written before the
decisive run. The only code run before them was none; the derivations below are analytic.

Watch semantics measured here:
- **exact policy**: each body's watch = its k = 4 nearest by Euclidean distance at the last
  sample (256 samples/orbit; set changes are resolved at that cadence). An encounter (i, j) at
  t_m is caught iff j ∈ watch(i) or i ∈ watch(j) (either direction, as the gold's rank uses the
  min of both).
- **1-orbit-refresh policy**: the same watch frozen at refresh epochs 1 orbit apart (the lazy
  refresh the inversion tested, now on the correct definition).
- **rebuilds** = watch-entry events (membership changes of the k-set), per body per orbit.
- **lead** = t_m − (last entry of the partner into either watch before t_m): the warning the
  certificate gives.

## P0 — regeneration
`events.csv` (the inversion's format, mean-longitude ranks included) regenerates with md5
`bd310ef82a43dadc2345c466bfc5576b` (the checker's value), and per-scene event counts equal the
inversion's `fleet-out.jsonl`. If not: my rerun is not its record; investigate before claiming.

## P1 — distance rank at t_m (re-verify the checker, extend to A and D)
Distance rank (min of both directions) ≤ 4 at t_m for ≥ 99.9% of events in every scene,
including A and D which the checker did not measure at distance. (Checker: 0.000% > 4 on all
19,140 B + C events.)

## P2 — the decisive miss number: zero under set-change rebuild
Under the exact policy, misses = 0 (to rounding: < 0.1%) in every scene, including σ_e = 0.05,
the shear scene, and the bath (fleet×belt pairs caught by the global watch). Structural reason:
the partner passes rank 4 by continuity before contact, so churn-following rebuild always
acquires it; the k-th-nearest distance (~4·2π/n ≈ 0.04) is ≫ ρ, and no body closes 0.04 → ρ
within one sample (1/256 orbit) at these relative speeds.
**Kill (of the gold):** any scene with > 0.5% exact-policy misses — rank > 4 at t_m really
happens, the certificate is dead on its own definition, and the checker's prediction is wrong.

## P3 — rebuilds follow the churn law
Entries per body per orbit ≈ shear term 2n·δa_max/π + e-spread term ≈ 1.6·σ_e·n (relative
true-longitude oscillation amplitude ~2.5σ_e, each boundary-crossing pair swapping twice per
orbit; factor-2 tolerance):
- A ≈ 0.5 (shear 0.46, e-term 0.1)
- B ≈ 5 / 19 / 48 at σ_e = 0.005 / 0.02 / 0.05 (linear in σ_e; **kill of the cost correction**
  if flat in σ_e)
- C ≈ 12 (shear 1.9 + e-term 9.6)
- D fleet ≈ 4.5, of which belt-driven ≥ 60% (belt stream ~3.8 vs fleet-internal ~0.7);
  D belt ≈ 19 (mostly belt-belt e-spread 12.8 + shear 5.1).

## P4 — the cost crossover (derived from P3; reported, not independently measured)
The gold's O(n·k) base cost per body per orbit is k = 4 watch-checks; churn adds entries.
Crossover at 1.6·σ_e·n = k → σ_e* ≈ 0.004 at n = 600. So B(0.02), B(0.05), C and D's belt are
churn-dominated (up to ~12× the base term at σ_e = 0.05); A, B(0.005), D's fleet are not. The
inversion's "element coherence" inequality 4σ_e·n/(2π) ≤ k survives as a **cost** gate, not a
miss gate.

## P5 — lazy (1-orbit) refresh, the honest replacement of the inversion's lag numbers
Predicted miss fractions under the 1-orbit-refresh policy (lead-time argument: miss iff the
last refresh precedes the partner's last entry, P ≈ 1 − lead/T for lead < T): A < 5% (shear
closure ~1.5·10⁻³ rad/orbit gives leads of tens of orbits); B(0.005) < 15%; B(0.02) 20–60%;
B(0.05) 50–90%; C 10–60% (mixed shear/eccentric closures); D 0–40%. Wide bands on purpose:
this is secondary. The decisive point is the contrast P2 = 0 vs P5 > 0: refresh must follow
churn.

## P6 — lead times
Median lead ≥ 5 orbits in A, ~0.5–1.5 orbits in B(0.05), leads shrink ~1/σ_e across B; in D the
fleet×belt leads are set by the belt crossing speed (~shear at δa ~ 10⁻²).

## Kill criteria for my own run
- P0 fails → VOID my record until regenerated.
- P2 > 0.5% anywhere → clean refutation of the gold's certificate (the strongest outcome).
- P3 flat in σ_e → the churn cost correction dies with the inversion's headline; the gold's
  O(n·k) stands uncorrected.
- If P2 = 0 everywhere AND P5 ≈ 0 everywhere AND P3 holds → the certificate is correct and
  robust even to lazy refresh; the inversion reduces to the churn cost term alone.
