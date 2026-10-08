# predictions.md — second author run 20261008-0458 (before the decisive runs)

Checker's named experiment: re-derive A as median A16 over ≥6 secondary phases at
fixed μ = 1e-3; does the τ-crossing (0.17 < τ* < 0.25) survive? If yes → engine test;
if no → the kill is the deliverable.

I add one instrument audit the checker did not run: the author's `kepler_step` flips
the sign of the radial velocity whenever the advanced mean anomaly wraps past π
(`M1 = (M1+π) % 2π − π` sends f1 negative; the branch `if f1 > π: vr = −vr` then takes
the wrong sign). Measured: fires at 70–75% of the toy's kick steps. The corruption is
2·|vr| ≈ 2·e·v·sin f in velocity (a, e, |h| preserved; e-VECTOR direction rotated).
The toy carries e ≈ 4e-7 while dω is read off that 4e-7 e-vector's direction — so the
scrambling is first-order in the observable, not a small perturbation.

## Predictions (pre-registered)

P1 (control, two-body drift, no tide, e = 1e-3 injected, 300 orbits, K = 16):
the ORIGINAL propagator fails to keep ω constant — |Δω| = O(1) rad over the run;
the FIXED propagator (`vr < 0 branch corrected`) keeps |Δω| ≤ 1e-9 rad.
The original's a and e stay exact throughout (the corruption is a pure mirror state).

P2 (author's φ = 0 grid re-run on the FIXED propagator, 300 orbits):
A16 at τ = 0.05/0.10/0.17/0.25 no longer reproduces 0.45/0.80/0.75/1.68.
Point prediction: the fixed values are all < 1 with no crossing in 0.05–0.25
(batching stays cheap relative to fine sampling at every τ, or the errors collapse
to a scale set by kick quadrature, not by ω scrambling). The 1.68 at τ = 0.25 was
scrambling noise, not shock convexity.

P3 (the named experiment, FIXED propagator, 12 phases kπ/6, μ = 1e-3, 300 orbits):
median A16(τ) does not cross 1 anywhere in 0.05–0.30. Point estimate: median A16
∈ [0.2, 0.9] at every τ; fraction of phases with A16 > 1 at any τ ≤ 1/3.
The author's claimed regime trigger does not survive phase averaging on a sound
instrument → the claim is killed; the cadence rung must not freeze A(τ) criteria.

P4 (horizon, FIXED propagator): median A16(τ) at 150 orbits agrees with the 300-orbit
median within a factor ~2 at every τ (no sign flips of the median). The horizon
fragility the checker saw on the broken instrument disappears with the instrument.

If P3 is wrong — i.e. a phase-robust crossing appears on the FIXED instrument — I will
report it as the claim surviving in corrected form and run the engine test the checker
named (double kick size across r9's Hill ladder, B14 as judge) if time allows.

Kill criterion for my own instrument: if the fixed propagator still fails P1's control
(ω not conserved in pure two-body drift to ≤ 1e-9), my sweep is VOID and I report the
propagator defect only.

---

## Amendment (still before the decisive sweeps)

Validation of the "fixed" harness surfaced two more defects in the author's toy, so
the one-line fix was incomplete and P2–P4 as written were under-specified. The
corrected instrument (v2) is: vr branch fixed (f1<0), om := 0 when e < 1e-14 (the
circular-start roundtrip is otherwise rotated by atan2 of cancellation noise —
measured: a deterministic ~pi teleport at step 1 in every run, author's, checker's
and mine), and dt = 2pi*a^1.5/K, T = n_orb*2pi*a^1.5 (true cadences and orbits; the
author's P = a^1.5 made "K kicks/orbit" actually K/2pi*... — K=1 was 6.28 kicks/orbit,
K=16 was 100.5/orbit, "300 orbits" was 47.7).

Predictions restated for v2 (fixed mu = 1e-3, 12 phases k*pi/6, K in (1,4,16) true):

P2' (phi = 0 grid): the author's row 0.45/0.80/0.75/1.68 does not regenerate; the
v2 A16 values differ by O(1) factors. No prediction on v2's own crossing — that is
the measurement the checker asked for.

P3' (the named experiment): median A16 over 12 phases stays < 1 at every
tau in 0.05–0.30 (point estimate 0.2–0.9); the claimed regime trigger at
0.17 < tau* < 0.25 does not survive. If instead a phase-robust crossing appears,
report it as the claim surviving in corrected form (and run the engine test if
time allows).

P4' (horizon): v2 median A16 at 150 orbits within a factor 2 of the 300-orbit
median at every tau.

Controls for v2 before it counts: (a) pure two-body drift keeps omega to <= 1e-9 rad
from BOTH a generic e=1e-3 start and the exact circular start; (b) vec and scalar v2
agree in domega to <= 1e-4 relative over 300 orbits (the hypersensitivity that made
the broken toy differ at 6e-3 must be gone); (c) truth RK4 converged at 4000 vs 8000
steps/orbit at tau=0.25.
