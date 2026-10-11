# Dossier — run 20261011-1917-redteam-fb64 (lens: premise red-team)

## Claim

The view's gather as written ("positions are gathered at the observer's past
light cone. Lensing takes deflection(b) from the doll's memo" —
docs/law.md §Observation, docs/representation.md §2) omits the gravitational
arrival-time delay, so every body orbiting within ~60 M of a black hole is
rendered at the wrong sky position — by 1 pixel at 60 M, 5 pixels at 20 M and
3–8 degrees (33–97 pixels) from 8 M down to the ISCO — and nothing in the
gates or rungs catches it; the fix is one more column in the doll's existing
deflection memo.

## Bottleneck

Not a board bottleneck number: a correctness hole in the view (premise #5 of
the lens), which principle 30 makes load-bearing ("what really matters is
navigation, knowledge and dynamics those need to be perfect"): the sky is the
navigation map (principle 5: "the zoom level is the minimap") and AI
perception uses the same gather (representation.md: "An AI's perception is the
same gather at its own past light cone"). Gain: not speed — truth at the
player's floor in the game's advertised poster scene (black holes are in the
goal; B19 is frozen for rotating holes). What it deletes: nothing; what it
adds: one memo column (see adoption cost).

## Evidence

Float premise probe (lab rule: floats explore, integers decide canonical
outcomes — no canonical outcome touched). Oracle: exact equatorial
Schwarzschild null geodesics, RK4 on the photon Binet equation
u″+u = 3Mu² (b-conservation drift ≤ 5e-7 relative at arrival; median
refinement convergence of the measured error 3.4e-6 rad), source on an exact
circular geodesic (Ω = M^½r^−3/2), static observer at r_o = 4 r_e, 16 frames
per scene spanning one orbit, medians over frames, primary image = the root
whose impact parameter is closest to the flat chord's (the design's own seed).

| r_e (M) | images med | delay (M) | err_design | err_phase (pure timing) | err_fix | px |
|---|---|---|---|---|---|---|
| 6 (ISCO) | 3 | 30.9 | 8.5e-2 | **1.40e-1** | 9.9e-3 | 97 |
| 8 | 3 | 12.3 | 9.0e-2 | **4.85e-2** | 2.4e-2 | 33 |
| 20 | 3 | 4.4 | 1.5e-2 | **7.44e-3** | 1.3e-3 | 5.1 |
| 60 | 2 | 3.9 | 1.6e-3 | **1.53e-3** | 3.9e-5 | 1.1 |
| 200 | 2 | 3.6 | 2.3e-4 | 2.35e-4 | 1.7e-6 | 0.16 |
| 1000 | 1 | 3.9 | 1.7e-5 | 2.37e-5 | 1.6e-7 | 0.02 |

px = err_phase / 1.45e-3 rad (one pixel, 1080p over a 90° FOV — the "finest
spatial distinction the player can see", representation.md §4).

- **err_phase** = |angle between the flat-cone retarded position and the true
  retarded position| — the timing error alone, equivalent to a design whose
  bend memo is perfect (rotation commutes, so a perfect bend applied to both
  leaves exactly this difference).
- **err_design** = the design as written: flat-cone retarded time + the most
  generous per-doll bend memo (the exact finite-path bend of the arrival
  family — better than any "deflection(b)" the text promises).
- **err_fix** = the crossing solved on the delay-corrected cone
  (t_obs − t_e = D_flat + delay(b), delay memoized per family): collapses the
  error 14–150× where lensing is moderate (r_e ≥ 60 → below 4e-5 rad), so the
  delay IS the dominant term. At r_e = 8–20 the per-family delay memo is not
  enough (images med 3): the correction must be image-resolved.
- **Controls** (weak-field calibration scene, r_e = 10,000 M): err_design
  7.4e-7 rad (passes); planted no-deflection law fails at 3.4e-5 (45×);
  planted no-retardation law fails at 5.9e-3 (7,900×). Both sides controlled.
- **Secondary, measured:** image multiplicity is the norm near the hole
  (3 images median at r_e ≤ 20; ≥ 2 at r_e ≤ 200), and the tracked image is
  unstable under oracle refinement in 31% of r_e = 8 frames — rendered images
  will flicker/jump as they merge and split (caustics), with no tracking rule
  in the design and Newton's derivative → 0 at an annihilating image.
- **Secondary, measured:** the flat-cone warm Newton (the design's crossing
  solve) never fails in any orbit scene (≤ 5 iterations), and never fails for
  uniform closing bodies up to β = 0.99 (mean 3 iterations — the convexity
  argument holds; the premise survives). At β = 0.999 it fails 3–8 of 399
  frames, all at closest approach where G′ = −1 − û·v → −0.001 (the near-c
  missile is bottleneck 5's own worst case). The frozen-seed negative control
  fails at the same rate (9/399) as the warm solver: staleness is NOT the
  cause — degeneracy is. The planted wrong-derivative solver fails 399/399
  (the detector sees failure).

Reproduce (each ≤ 60 s; numpy only; 8 vCPU shared cloud runner, load 2.06 at
run time, 1.7 GB RSS used of 15 GB, single-threaded):

```
cd lab/results/20261011-1917-redteam-fb64
python3 attack.py calibrate   # 0.9 s: weak-field controls
python3 attack.py sweep       # 2.7 s: the table above
python3 attack.py converge    # 3.3 s: oracle self-convergence + image stability
python3 attack.py newton      # 2.8 s: uniform-body Newton + negative controls
```

## Predictions

In [predictions.md](predictions.md), written before the sweep (tuned only on
the weak-field calibration). Held: P1–P7 (all six held-out error ranges and
the pixel-floor crossing between 20 M and 60 M), P9 (memo accurate ≥ 60 M),
P11 (≥ 2 images in ≥ 25% of frames at r_e ≤ 20 — actually the median).
Partially held: P8 (err_fix < err_phase/10 held at r_e = 6 and ≥ 60, failed at
8–20: multi-image scenes need an image-resolved delay memo) and P10 (zero
Newton failures held everywhere except β = 0.999 closest approach, 1–2% of
frames). Disclosed instrument fixes forced by the controls before the sweep
was trusted: my own Newton had the derivative sign wrong (−1+û·v instead of
−1−û·v; the wrong-derivative solver is now kept as the planted negative
control), dead photon columns overflowed, and the drift check read
post-arrival garbage. The r_e ≥ 20 sweep rows were unaffected (0 Newton
failures there even before the fix); r_e = 6/8 rows changed and are reported
from the fixed run.

## Ranked attacks (the lens's deliverable)

1. **The view's arrival time has no gravitational delay** (measured above).
   Player-likelihood: highest — the strong-field sky is the advertised core,
   not an exotic case. Rung that should have caught it: **none exists.** r6 is
   named in representation.md §7 ("Newton iterations and samples per frame for
   the gather") but has no file in lab/rungs/, and as sketched it is a cost
   rung, not a correctness one. B3/B16 gate the deflection ANGLE (B16's oracle
   is "a boosted Schwarzschild quadrature" — angle only, effectively static
   source); B7 gates clock RATES; B19 gates Kerr geodesics and clock formulas,
   not apparent positions of moving bodies. Proposed r6 criterion: apparent
   position of orbiting bodies vs a geodesic oracle within one pixel
   (1.45e-3 rad) from the ISCO outward; images counted and tracked stably
   across frames; planted no-delay and no-retardation laws must fail (my
   controls separate 45× and 7,900×).
2. **Dense ≡ sparse bit-identity rests on two different event-discovery
   mechanisms** (premise #4). The sparse order finds contacts through the
   Binet-cone candidate tier; the dense order's broad phase is occupancy bits
   ("an AND, a radix sort of cell keys"). Lab gold 20261006-0346 measured the
   cone tier dropping 4–6% of real contacts under co-orbital concentration;
   an occupancy map cannot drop a same-cell pair. Different discovered events
   ⇒ different event graphs ⇒ different bits: B8 ("bit-identical across …
   sparse and dense orders") is unpassable by construction for formation
   scenes unless ONE discovery law serves both orders — the design never says
   so. Rung: r5 is named in representation.md §7 but has no file; B8 would
   catch it only if its scenes include a concentrated formation (a fleet), not
   just scattered ships. Not re-measured here (the gold already measured the
   miss); the new content is the consequence for B8.
3. **Multi-image skies have no tracking rule** (measured: 3 images median at
   r_e ≤ 20; image identity unstable under refinement in 31% of r_e = 8
   frames). "Each visible tube crosses the observer's past light cone once;
   lensing adds crossings" says images exist but not how the previous-frame
   Newton seed follows one through a caustic (at a fold, two images annihilate
   and the solver's derivative → 0). Player sees: stars flicker, jump or
   double near a black hole. Rung: none (r6 again).
4. **The crossing Newton is ill-conditioned at closest approach of β → 1
   bodies** (measured: 0 fails at β ≤ 0.99; 3–8/399 frames fail at β = 0.999,
   all at closest approach; degeneracy, not staleness). A bracket
   ([t_prev, t_obs] with bisection fallback) removes it — the unique root is
   bracketed for any subluminal body (G is strictly decreasing). Rung: none;
   r6's iteration count would show the cost spike but nothing gates
   convergence.
5. **Premises that survived** (worth reporting, per the lens): the 1PN EOB
   two-body doll (r3 v3, B11 — domain gap remains: e > 0.6, p < 20 are
   ungated); cycle repetition post-Darwin-compile (integrability makes it
   exact; B5); kicks with the re-anchored jet (lab gold 20261006-0346);
   ≈0 cost for undisturbed bodies in the view's solve itself (3 iterations,
   0 failures, at any β ≤ 0.99 — the convexity argument holds).

## Principles

- Violates principle 30 ("what really matters is navigation, knowledge and
  dynamics those need to be perfect"): the sky IS the navigation instrument,
  and AI knowledge inherits the same gather — both are wrong by degrees
  exactly where the player is meant to feel GR.
- Strains principle 3 ("Nothing is evolved that can be derived when looked at
  (clocks, redshift, views)"): deriving-not-evolving is only sound if the
  derivation is exact to the player's floor; the arrival time is derived from
  the undelayed cone.
- Principle 28 ("The view is an instrument… it's a space clock literally"):
  the instrument currently lies near mass.
- No violation found in the dense order's lockstep ticks (principle 14): a
  tick wastes nothing when everything changes every tick — entropy is the
  floor there, consistent with principle 3.

## What would make it wrong

(a) The live view implementation already solves the crossing with light-tube
travel times — the design text contradicts this (law.md §Observation names
only the light cone and deflection(b); "Shapiro" appears nowhere in docs/);
if the implementation is ahead of the text, the TEXT still needs the fix
(the law is the text). (b) The game never renders bodies orbiting within
~60 M of a black hole — contradicted by the goal (black holes named; B19
frozen for rotating holes; Kerr's delay is the same order). (c) An oracle
bug — guarded: weak-field control passes at 7.4e-7, planted negatives fail at
45× and 7,900×, b-conservation ≤ 5e-7, refinement convergence 3.4e-6 median;
the strong-field medians are stable, their tails (single frames flipping
primary image) are disclosed, not hidden.

## Cost of adoption

One column: arrival Δt(b) beside deflection(b) in each doll's memo, compiled
from the light tubes the doll already compiles (law.md §Motion.6: "Light: the
same map without the M/L² term, parameterized by b = L/E" — the travel time
is the same integral). The crossing Newton adds one table lookup per
iteration (cost class unchanged; the gather is already an O(pixels) multiply-
add budget). In the multi-image regime (r_e ≲ 20) the memo must be
image-resolved (per arrival family), which the light-tube compile already
distinguishes. No new component; no law change; integers keep deciding.

## The lens (what this lens may have made me miss)

Red-teams overweight exotic cases; I ranked by player likelihood, and the
strong-field sky is the game's poster scene — but my falsifier is 2D
equatorial, Schwarzschild-only, static observer: Kerr's frame dragging (B19)
reshapes but does not remove the delay, and a fast-moving observer (the
player at β → 1, the plane's own L15 burn) compounds retardation with
aberration — untested here. I did not test the gather's COST (r6's actual
sketch), only its truth. The multi-image instability (attack 3) is measured
only as refinement instability, not as a per-frame animation — the player-
visible flicker rate is inferred, not measured. Attacks on premises 1–3 and 6
rely on cited prior runs rather than fresh probes.
