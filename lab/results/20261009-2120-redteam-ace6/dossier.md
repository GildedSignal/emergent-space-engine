# Dossier — 20261009-2120-redteam-ace6 (lens: premise red-team)

**Claim.** The design's view gather ("positions are gathered at the observer's past light
cone; lensing takes deflection(b) from the doll's memo", representation.md §2 / law.md
Observation) has no time-transfer law: selecting the emission event by flat light-time
(the original conversation's "retarded observation time t − d/c") misplaces emitters
orbiting within ~50 M of a compact mass by 2–176° of orbital phase on the player's sky —
systematically, worse the farther out the player is — and even the strongest steelman
(deflection applied, flat speed along the bent arc) leaves 1.8–61°; no rung or gate covers
it, because r6 is speced cost-only and B3/B16/B7 judge deflection and rates.

**Bottleneck.** Not a cost bottleneck: a premise of a component about to be built (r6 is
GLM's open rung; "the readout's cost" is in the queue). It is the same class as "gravity
must travel at c… never construct later upon a flawed foundation": the view and AI
perception are one gather (adopted), so a wrong emission event corrupts the map, the
sky and every perception-threshold certificate near a black hole. Adoption deletes
nothing and costs ~one memo entry (below).

## Evidence (float oracle, Schwarzschild 2+1, M = 1)

Circular-geodesic emitter at r_e, static observer at r_o, 12 emission phases, all images
of each scene found as roots of the exact image condition (null geodesics: RK4 on
u″+u = 3u², t and arc carried along; plunging and winding rays included). Gathers:
exact (geodesic time transfer), flat (t − d/c), bent (exact bent path, timed at flat
speed). Error = wrong orbital phase shown to the player.

| scene | primary images: flat err (med/max) | bent err (med/max) | winding images: extra delay / max err | lattice quantum ÷ 1°-need |
|---|---|---|---|---|
| r_e=7M, r_o=500M | 59.4° / 117.6° | 38.9° / 61.2° | 56M (0.48 orbit) / 176° | 67× |
| r_e=8M, r_o=500M | 50.4° / 104.0° | 32.1° / 50.3° | 61M (0.43 orbit) / 172° | 55× |
| r_e=10M, r_o=500M | 27.2° / 84.5° | 21.4° / 36.0° | 38M (0.19 orbit) / 130° | 39× |
| r_e=20M, r_o=500M | 9.8° / 45.1° | 7.5° / 13.3° | 62M (0.11 orbit) / 43° | 14× |
| r_e=50M, r_o=500M | 2.1° / 21.5° | 1.8° / 3.7° | 118M / 20° | 3.5× |
| control r_e=400M, r_o=5000M | 0.06° / 6.6° | 0.06° / 0.23° | — | 1.6× |


Decomposition at the worst r_e=8M grazing image (b = 5.57M, image 0.64° off the hole's
limb): light-time excess over the flat chord 32.7M = coordinate (Shapiro) delay 16.8M +
geometric arc excess 16.0M. Orbit period 142M: the flat gather is wrong by a third of an
orbit. The effect grows with r_o (median 50° → 84° from r_o 500 → 5000): the log term
and chord excess both grow with the lever arm — this is not a near-field artifact.

Controls: deflection of a b=20M ray measured 0.22841/0.22816 rad at dφ = 5e-4/2.5e-4 vs
series 4/b + 15π/4b² = 0.22945 (Δ = 1.3e-3, converged); halving dφ changes reported phase
errors by ≤ 7e-4° over 25 root pairs. Machine (in metrics.json): 8 vCPU, loadavg recorded,
15 GB shared.

Reproduce: `python3 falsifier.py` in this folder (213 s total; one scene ≈ 25 s; numpy
only; < 100 MB). Full per-image rows in `metrics.json`. predictions.md written before the
run. Known coverage gap: the r_e=20M, r_o=5000M scene resolved only 1 root (root-finder
tolerance vs fast residual), and winding-family capture is partial; neither gap hides
small errors — both hide additional large ones.

## Predictions (predictions.md, written before the run)

- P1 (r_e=8: 25–60°) **held on the median** (50.4°); max 104° exceeded my band — the
  grazing-lensed primaries are worse than I estimated.
- P2 (bent ≥ 90% of flat) **failed near the hole**: bent/flat ≈ 64–66% at r_e ≤ 10M —
  for grazing rays the geometric arc excess (~16M) rivals the Shapiro log term (~17M);
  my O(θ²b/8) estimate was wrong there. Holds far away (r_e ≥ 50M).
- P3 (r_e=20: 5–14°, r_e=50: 1–4°) **held** (9.8°, 2.1°).
- P4 (control < 0.5°) **held** (median 0.06°; the 6.6° max is the lensed-through family).
- P5 (lattice 30–70× coarser) **held** (55×; 548× at r_o=5000).
- P6 (winding delay ≥ 1 orbit, err > 90°) **half-held**: extra delay 0.11–0.48 orbit
  periods (overestimated), phase error 130–176° at r_e ≤ 10M (held).
- P7 (integrator controls) **held**.

## What would make it wrong

1. If the design intends the gather to read min-plus cell arrival times instead of a
   per-tube Newton solve — then the error becomes the ring lattice's time quantization:
   one outer cell is ln2/16·r_o of light time, 55× (r_o=500) to 548× (r_o=5000) coarser
   than the 1° phase resolution needed for an r_e=8M emitter. Either reading fails; the
   premise needs an explicit time law either way.
2. If nothing ever orbits inside ~100M of a compact mass in the shipped game — but
   "I want black holes because they create very interesting gameplay" (register, CL 09-27)
   and fleets will orbit them; at r_e=50M the median error is still 2.1°.
3. If the shipped gather already integrates dt/dφ along the bent path (i.e. the deflection
   memo secretly stores arrival time): nothing in representation.md, law.md, plane.md or
   any rung says so; law.md:53 names deflection(b) only.

## Cost of adoption, and fit with PRINCIPLES

The fix is representation-native, not a bandaid: the photon cycle compiler already
integrates dt/dφ = 1/(b·u²(1−2u)) per band to compile deflection(b) (law.md:22); the
memo gains one sibling entry, arrival time Δt(b; u_e, u_o) — the same integral, stored.
The view's Newton solve stays O(1) per visible tube; AI perception (r7) inherits it for
free ("the view and AI perception are one gather", representation.md merge candidate 1).
The rung criterion to add to r6: retarded emission phase within X° of the geodesic oracle
for emitters on circular orbits at 6–50M, plus image count — this falsifier is its seed.

Principles: this is an error of behaviour, not of size — principle 30, "what really
matters is navigation, knowledge and dynamics those need to be perfect": the map is
knowledge, and the map's own formula (t − d/c, original conversation) is the flat gather.
The gates cannot see it because they judge rates (B7) and deflections (B3, B16); principle
34's "oracles are guards" is exactly violated by a view no oracle guards.

## Ranked attacks (the lens deliverable)

1. **[Measured above; no rung] The gather lacks a time-transfer law** (premise 5).
   Should be caught by: r6 — which does not exist as a file and is speced cost-only
   ("Newton iterations and samples per frame", representation.md §7). None does today.
2. **[Open, unbuilt, unpriced] Dense/sparse bit-identity needs root-clock event keys**
   (premise 4). law.md's tie rule keys on root-clock time; the dense order locksteps in a
   doll's own clock; ring-cell time quanta (ln2/16·r) span four decades inside one doll,
   so "same epoch" is undefined across bands until the motion law's step 4 lands. r5 does
   not exist; when written it needs a cross-band same-epoch scene. (HANDOFF already lists
   the simultaneity risk; the view-facing price is attack 1's lattice column.)
3. **[Domain-bounded by others] Kicks and cycle derivatives absorb perturbations**
   (premise 3): averaging killed near resonance (r4 v2/v3), inside 0.17 Hill radii for
   precession (r9), and at belt scale (q-secular-v2); the jet's re-anchor is graded gold
   by one checker, second blind check never ran. No new measurement here — the domain
   boundary is the board's live question (fewer kicks per orbit), not a premise failure.
4. **[Survives, with one untested corner] Two-body doll, 1PN EOB, ν only in the energy
   map** (premise 1): r3 v3 (precession 1024/1024, periods 632/632, ν-effect 500/504,
   assists 64/64) and B11. Untested: the doll's own frame boosts above β = 0.9 (B16's
   moving-lens lesson applied to light, not yet to doll handoffs).
5. **[Survives] Binet/Darwin cycle repetition** (premise 2): G1–G6 pass; per-cycle errors
   identical each cycle (law.md:21) — the right error type; r1's m-sweep bounds the band
   bias (m = 8 too coarse, 16 and 32 pass).
6. **[Survives where averaging is legal] Costs ≈ 0 for undisturbed bodies** (premise 6):
   B9 gates crossings per cycle and zero work between events; the event (kick) rate is
   the board's #1 cost item, queued as cadence work — a cost question, not a false premise.

## The lens (what this red-team may have missed)

Red-teams overweight exotic cases; I mitigated with medians over 12 alignments and a
far-field control that passes (the premise survives at r_e ≥ 400M: 0.05°). Not tested:
eccentric emitters (worse: more time near periapsis, Ω varies), Kerr χ ≠ 0 (B19's
geodesics exist, the gather does not), a moving observer (the player's own β mixes
aberration into the phase error), and occlusion/eclipse timing, which the same missing
delay also corrupts. The winding-family capture is partial. 2D Schwarzschild only, float
only — orders of magnitude, per the lab rules; the integrator re-measures on the M1.
