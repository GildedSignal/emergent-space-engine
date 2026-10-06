# predictions.md — 20261006-1135-scout-7a46

Written before the decisive grid. Calibration allowed on ONE case only
(q = 0.1 r_H, v_inf = 0.7 v_H, prograde): the scheme constants (kick count K,
A's step rule) may be chosen there. Everything below is held-out: the rest of
the q-grid, both v_inf, the radial and near-radial cases.

## Claim under test

The (E, L) conic generator refuses or degrades on the conic's singular set
(L = 0, no-turning-point/plunge, near-radial where the turning-point discriminant
approaches 0). A square-root (Levi-Civita) generator covers the whole set in one
closed form: `z = u²`, `dt = |u|² dτ`, `u'' = (E/2) u`. Bound, parabolic,
hyperbolic, radial and r → 0 are one formula (oscillator with κ = E/2; κ < 0
trigonometric, κ > 0 hyperbolic, κ = 0 straight line). No Newton iteration for
the drift; event times come from the closed t(Θ) and one scalar root on
|u|² = r_exit².

## Scene

Planet's doll: mu_p at origin (planetocentric, non-rotating), parent M = 1 on a
circular orbit R = 1, n = 1; r_H = 0.03; entry r0 = 0.98 * r_in with
r_in = 0.4 r_H. Schemes:

- **C** (candidate): exact Levi-Civita drift + tide kicks (parent differential
  gravity) only, Strang D(Δτ/2)·K·D(Δτ/2); K kicks per encounter.
- **A-rt** (today's plane shape): velocity Verlet, planet monopole + tide, step
  re-timed dt = min(cap, alpha·r).
- **A-fix**: same, constant dt (the memo's OM_FIXED_STEP ablation).

Truth: DOP853 rtol 1e-12 on the same inertial ODE.

## Predictions (held-out)

1. **Positive control (instrument check).** C with the tide OFF, on every grid
   case including L = 0, the bound radial fall through r = 0, and the exact
   parabolic radial fall (E = 0): exit-state error vs DOP853 <= 1e-12 relative.
   If this fails my algebra is wrong, not the claim.
2. **Flatness in depth.** C with tide ON at fixed K = 8: exit-state error at
   q = 0.003 r_H is within ~3x of its value at q = 0.3 r_H (error set by the
   tide kick count, not the depth).
3. **A's error growth at fixed rule.** A-rt at the calibration alpha: error at
   q = 0.003 at least 10x its error at q = 0.3.
4. **Cost to match C.** For A-rt or A-fix to reach C's K = 8 error at
   q = 0.003, it needs >= 10x (I expect 30–1000x) more events/force evals.
5. **Radial pass-through.** Bound radial fall (E < 0, L = 0): C exits after
   passing r = 0 with error <= 1e-10 and zero force evaluations. A-rt completes
   too in float (dt = alpha·r is integrable through the centre; addendum), with
   error >= 1e-4 at the calibration alpha. The engine's real behaviour there is
   a refusal, not a stall (NoBoundOrbit: binding.rs 197/210, kicks.rs 168-169,
   orbit.rs 60) — cited from the code, not simulated.
6. **Cost exponent.** A-rt's cost to hold error fixed grows as a power of 1/q
   as q drops 0.3 → 0.003; C's event count is K by construction, independent
   of q.

## Addendum (before any grid run; written while implementing)

Back-of-envelope while coding, correcting my own guess in prediction 6: for
A-rt to hold error as q drops, alpha must shrink like sqrt(q) (angular advance
per step at periapsis is alpha·L/q with L ~ sqrt(2 mu q)), so the cost-to-match
grows like 1/sqrt(q), not 1/q. Amended expectation for the measured exponent
of cost-to-match vs q: in [-1, -0.4], centered near -0.5. Prediction 5 was
amended at the same time (A-rt does not stall; dt = alpha·r is integrable
through r → 0).

## What would falsify the claim

- C's pure-two-body control failing near e = 1 or r → 0 (representation not
  actually regular there), or
- A-rt holding error flat as q → 0.003 at constant cost (then the stepping
  fallback is enough and no generator is needed), or
- C needing K growing with depth to hold error (then the kick cadence, not the
  drift, is the binding term and the generator buys little).

Numbers that decide: error ratios and event counts in results.json; thresholds
above.
