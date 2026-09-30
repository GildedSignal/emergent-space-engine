# predictions.md — run 20260930-2250-taleb-3d2c (Taleb lens, B14 τ selector)

Written BEFORE the decisive `sweep` and `chatter` runs. Tuned ONLY on:
positive/negative controls and 5 break-zone probes (τ ∈ {0.2, 0.5, 0.7, 0.9, 0.95}
at a few e/directions), plus the integrator controls (resolution 128 vs 512 vs 2048,
Jacobi conservation ≤ 1e-4). Everything below the tuned grid is held out:
the full τ grid × {prograde, retrograde} × e ∈ {0.05, 0.3}, Law F behaviour,
chatter statistics, the S↔F overlap.

Held-out cases (never run before this file): τ ∈ {0.35, 0.40, 0.45, 0.55, 0.60, 0.80}
at any (e, direction); all retrograde cases except τ=0.9/e=0.05; all e=0.3 prograde
except {0.5, 0.7, 0.95}; Law F at every point; all chatter counts.

Model: circular restricted 3-body, GM_planet = 1, GM_sun = 1000 (Jupiter-like),
R_Hill = 0.0693 a_p, horizon 4096 moon orbits (= 45 planet orbits at τ=0.5,
= 700 at τ=0.95), 128 leapfrog steps/orbit, 8 seeds (4 mean anomalies × 2 apsidal
orientations). Truth = full CR3BP; Law F = per-step Hill quadrupole; Law S =
orbit-averaged quadrupole (e ≡ e0 exactly, coplanar).

## P1 — prograde break (e = 0.05)
τ_break(S) = largest τ with 0/8 escapes and max e-pump < 0.1:
PREDICT τ_break(S) ∈ [0.30, 0.45]. At every τ ≥ 0.5 prograde, ≥ 6/8 seeds escape.

## P2 — retrograde asymmetry
PREDICT τ_break(S, retro, e=0.05) ≥ τ_break(S, pro, e=0.05) + 0.25.
At τ = 0.7: retro escapes ≤ 2/8 while prograde escapes 8/8.

## P3 — eccentricity shifts the break at fixed apoapsis
PREDICT τ_break(e=0.3, pro) ∈ [0.25, 0.38] and the two breaks scale roughly as
1/(1+e) (apoapsis-controlled): τ_break(e=0.05)/τ_break(e=0.3) ∈ [1.05, 1.5].

## P4 — Law F (dense quadrupole) tracks truth far past S's break
PREDICT: verdict (bound/escaped) mismatch ≤ 1/8 seeds for τ ≤ 0.7 (both e, both
directions); ≥ 2/8 mismatch appears somewhere in (0.7, 0.95]. For bound seeds,
|final_e(F) − final_e(truth)| < 0.05 at τ ≤ 0.5 and > 0.3 at some τ ≥ 0.7
(chaos amplifies the (a/a_p)² quadrupole truncation).

## P5 — chatter at the boundary
Selector reads τ_apo once per orbit; boundary τ* = measured τ_break(pro, e=0.05);
moons with e=0.3 straddling it. Switches are once-per-orbit samples flipping:
PREDICT median total switches over 4096 orbits ≤ 20, but max ≥ 100 for at least
one (τ, seed) — bursts (consecutive-orbit flip-flopping), not uniform drift.

## P6 — the premise check: τ alone is not a sufficient statistic
In the band τ ∈ [τ_break(pro)+0.05, 0.9]: retrograde truth is bound in ≥ 6/8
while prograde escaped in ≥ 6/8 (same τ). A single τ₀ for both directions
either kills prograde moons (S blind to their escape) or forces retrograde moons
into the expensive Hill/dense regime where averaging was still valid.

## P7 — cost of a prograde-keyed τ₀
If τ₀ must sit at the prograde break (P6), the fraction of the retro grid
(τ < τ₀) where S was still valid — i.e. wasted expensive-regime assignments —
PREDICT ≥ 30% of retro grid points in [0.2, 0.9].

## What would make me wrong
- P1/P2 wrong direction (retro breaks first): my Hill-stability prior (Hamilton &
  Burns 1991, prograde ~0.5, retrograde ~0.7+) is misapplied at this mass ratio.
- P4 failing low (F mismatching verdicts by τ=0.5): the octupole (a/a_p)² is
  bigger than estimated, or the compiled-Hill regime is NOT a drop-in for the
  dense fallback above ~0.7 R_Hill.
- P5 showing no bursts: apoapsis drift is smooth across the boundary; then
  hysteresis is unnecessary and only placement matters.
