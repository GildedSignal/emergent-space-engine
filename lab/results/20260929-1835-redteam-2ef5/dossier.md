# Dossier — red-team of docs/representation.md (run 20260929-1835-redteam-2ef5)

## Claim

The design's costed perturbation layer — "tidal kicks, with averaging" (§6, from H0190's
114x cut) — cannot represent mean-motion resonance: at an exact 2:1 period ratio it misses
the eccentricity pumping by 2.1–2.6x and turns partial resonant-angle libration into uniform
circulation, while the same kick layer with the conjunction phase kept matches the N-body
truth to ~0.5–2%; averaging dies as a configuration, kicks survive (H0183: kill the
configuration, not the method).

## Bottleneck

Board items 0/2 (representation; stepping vs generators). The §6 cost table's "tidal kicks,
with averaging ~6e4/s" is the load-bearing cheapness claim for undisturbed-and-nearly-
undisturbed bodies. Resonant populations (moons in Laplace-like lockings, asteroid belts,
compact multi-planet systems — the histories a player watches, OC#16 "navigation, knowledge
and dynamics those need to be perfect") must fall back to per-conjunction events; the 114x
averaging cut claimed in H0190's scope (smooth lunar/solar tides) does not extend there.
Gain: none claimed; this is a premise kill worth one rung criterion.

## Evidence

Commands (cloud container, each under 60 s where possible):
- `python3 e1_resonance.py` (~35 s) — two planets about a unit star, e0=0.05, truth =
  Verlet N-body (600 steps/orbit, energy drift 5e-4–2.5e-3); B = exact Kepler cycles +
  densely integrated synodic encounter windows (the doc's generator/event structure);
  A = same cycles with the perturber replaced by its orbit-averaged ring (H0190-style
  averaging), rates refreshed every 10 cycles.

| case | truth max e1 | B (phase kept) | A (averaged) | phi concentration truth/B/A |
|---|---|---|---|---|
| 2:1, m=3e-3, 2000 orbits | 0.175 | 0.173 | 0.067 | 0.266 / 0.306 / 0.005 |
| 2.15, m=3e-3, 2000 orbits | 0.115 | 0.112 | 0.063 | 0.074 / 0.080 / 0.005 |
| 2:1, m=1e-3, 4000 orbits | 0.1355 | 0.1348 | 0.064 | 0.297 / 0.309 / 0.009 |
| 2.55, m=1e-3, 4000 orbits | 0.078 | 0.077 | 0.055 | 0.026 / 0.025 / 0.008 |

Averaging misses the resonant pumping by 2.1x (m=1e-3) to 2.6x (m=3e-3) and erases the
resonant angle's structure (concentration ~0: uniform circulation). Off resonance (2.55)
it is merely ~30% low on max-e (it legitimately drops short-period forcing) — no strawman:
averaging is fine where H0190 measured it (smooth external tides), wrong inside resonance.

- `python3 e3_e4_checks.py` (<1 s):
  - E3: exact Schwarzschild test-body precession vs the 1PN 6*pi/p at e=0.3:
    +71.7% at p=20, +18.6% at p=50, +4.0% at p=200, +0.8% at p=1000. r3's seeds go down
    to p=20, and r3's `prec behaviour >= 0.99` (1%) has **no** truncation exclusion while
    `period` does — at its own seed floor the gate is ~70% contaminated by beyond-1PN truth.
  - E4: Minsky mutual-update rotation carries a systematic prograde bias ~eps^2/24 per
    step; holding r1's 1% precession gate needs eps <= 2.7e-2 at r=1000M (235 steps/cycle)
    and eps <= 8.5e-4 at r=1e6 M (7405 steps/cycle). r1's cost criterion counts band
    crossings (<=512), not in-band steps, so it cannot see this; the bias is one-signed
    (mimics extra central mass — an error *type*, principle 13/OC#42).

## Predictions (predictions.md, written before E1)

Held: truth pumping at 2:1 (e1 gain 2.7–3.5x, resonant angle partially bound:
concentration 0.27–0.30, not the predicted >0.9 clean libration — these resonances are
chaotic, not tidy); averaged model order-of-magnitude miss (predicted >=2x, observed
2.1–2.6x); control same order of magnitude for A. Wrong in detail: predicted A's e1 flat
within 1e-3 — A still has secular e-growth (Laplace–Lagrange exchange) to ~0.06; what it
misses is specifically the resonant part. E3 predicted 2–8% at p=20 — observed +72%
(underestimated, same sign). E4 predicted ~1e2–1e3 steps at r=1000M — observed 235 ✓.

## Ranked attacks (player-visibility order), with the rung that should catch each

1. **Averaging kills mean-motion resonance** (evidence above). Player sees no resonant
   lockings/gaps and wrong belt histories — knowledge/navigation drift. Rung: **none**
   (r2's kick runs are synthetic non-resonant streams; r3 is two-body; r1 is one mass).
   Needed: a three-body resonant case in r2 or r5 judged against N-body truth
   (e.g. `resonance behaviour e_pump_ratio >= 0.8` plus a resonant-angle libration check).
2. **"Exact closed form (Clohessy–Wiltshire)" is the Newtonian linearization.** Not exact
   even Newtonian at sphere-of-influence scale ((dr/R)^2 ~ 1e-4–1e-2 of the tide) and has
   zero GR content: near compact objects the dense doll's tide is the Schwarzschild/Kerr
   electric Weyl part, not CW. Principle 2 drift (exactness overclaimed). Rung: **none**
   (r5 judges bit-identity between orders, not correctness vs the GR oracle). Needed: an
   r5 case with a compact parent judged by gr-oracle behaviours.
3. **r3's `prec` gate is contaminated at its own seed floor** (E3: +72% at p=20). A correct
   1PN configuration can be killed by 2PN truth. Rung: r3 as frozen; fix = extend the
   author-computed truncation exclusion from `period` to `prec` (or raise p's floor).
4. **The view's Newton-from-previous-frame at relativistic approach.** The emission-time
   root moves by ~1/(1 - n.v) per observer displacement: an approaching body at v=0.99c
   makes the previous-frame guess ~100x stale; lensing caustics multiply crossings.
   Cost spikes (p99) exactly during near-c flybys. Rung: **none** (r6 unfrozen; it must
   gate max iterations / fallback rate with approaching-relativistic sources and a near-c
   observer).
5. **Minsky "two additions" as the in-cell law** (E4 numbers above). Survivable via
   memoized exact per-band rotations, but then the first computation uses multiplications
   (fine: it is a surprise) and r1 should count steps, not only crossings.
6. **Sparse/dense bit-identity across the flip.** Plausible on paper (same event graph,
   exact predicates; the c = 1 cell/update bound plus neighbour checks keeps closing speeds
   < 2 cells from tunneling). Ungated: r5 tests both orders, not the sparse->dense
   *transition*; the flip criterion is a heuristic (allowed by principle 22 as scheduling,
   but the flip must be bit-neutral and no criterion says so).
7. **Survived: the 1PN EOB two-body doll.** At 1PN the Buonanno–Damour map is exact:
   relative motion = test body in Schwarzschild with M = m1+m2, nu only in the energy map;
   the 1PN periastron advance is nu-independent and the map preserves it. Scope caveats:
   the effective ISCO at comparable masses is a 1PN artifact (plunge timing needs 2PN+),
   and E3 bounds how close to strong field r3's oracle may be trusted.
8. Minor arithmetic: §4 floors (12–16 B individual, 2–5 B family) vs "billions on 8 GB"
   requires >=99% family membership (1e9 x 13 B = 13 GB); r2's own `bits cost <= 320`
   (40 B) contradicts §4's floor — reconcile before freezing r2.

## What would make it wrong

My truth is 2D Newtonian at Verlet resolution with energy drift up to 2.5e-3 in the
violent m=3e-3 case (the m=1e-3 case drifts 5e-4 and reproduces the same conclusion);
if the engine's resonant behaviour is allowed to differ from Newtonian N-body by design
(determinism != realistic trajectories, OC#48), the *type* failure remains: an averaged
layer has no error budget that can represent a locked angle, at any resolution. If my
reading of "with averaging" is stricter than intended (per-conjunction kicks without
averaging), then attack 1 reduces to a cost note — but §6/H0190's numbers are what the
doc costs, and model B (no averaging) is what matches truth.

## Cost of adoption

One rung criterion (three-body resonant case + oracle), the r3 `prec` exclusion fix, an r5
GR-tide case, and dropping the word "exact" from CW. No new components; the kick layer and
the generator/cycle machinery are untouched — they pass.

## PRINCIPLES fit

- For: "Behaviours matter... error type over error size" (2) — an averaged layer cannot
  even represent the behaviour class "locked angle"; "A failed expectation is not
  automatically a failed method: diagnose which one broke (H0183)" — the configuration
  (averaging) dies, the method (kicks) stands; "Measure before claiming" (10).
- Against/violations found in the doc: "exact closed form (Clohessy–Wiltshire)" overclaims
  (2); §6's cost line inherits an averaging cut whose validity domain excludes resonance
  (3's "compute only surprises" is *not* violated by per-conjunction events — they are the
  surprises — but the advertised price is).

## The lens (what this red-team may have missed)

Premise-first red-teams overweight exotic cases; I ranked by player visibility, but I did
not run: the view gather's actual iteration counts (attack 4 is analytic), the sparse/dense
flip (attack 6 is on paper), AI-decision cost (r7, unfrozen), and the two-body doll's
handoff error growth (r3 covers it). My resonance cases are coplanar two-planet; three-body
resonant chains (Laplace) and secular resonances (nu_6-like) may fail differently or worse.
