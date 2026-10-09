# Dossier — redteam-2320: the gather cannot see a light-cone crossing being born

## Claim

representation.md §2's view premise ("Each visible tube crosses the observer's
past light cone once; Newton's method finds the crossing, starting from the
previous frame's. Lensing adds crossings, from each doll's memoized
deflection(b).") has no mechanism that *finds* the added crossings: a
continuation-only gather never discovers images born at a caustic, and in a
plain star-transit — no black hole, no exotic case — it misses a 41–78%-as-bright
companion image at 4.7–5.1° separation for 100% of the frames in which it
exists.

## Bottleneck

Not a current board bottleneck row; it is premise 5 of the lens list (the view
gathered at the past light cone), and the view is the product's core promise
("feel what living at high c would feel like"; "navigation, knowledge and
dynamics those need to be perfect", OC#16). Expected gain of fixing now: zero
compute, one sentence of design + one rung criterion; expected cost of NOT
fixing: r6 (view) gets frozen as a cost-only rung on top of a gather that is
structurally blind to image birth, and the blindness is in "knowledge", which
Julien named as must-be-perfect.

## Evidence

Truth = backward ray tracing on the design's own photon law (Binet
u″ + u = 3Mu², float RK4, M = 1, 2D). Scene: observer at (0,0), source at
(10⁴, 0), lens star (M=1, r\* = 50) transits the line of sight from η = 400 to
20 and back, 59 frames. Gather = per-image warm-started secant on the arrival
angle, seeded with the truth at frame 0 (generous), exactly the doc's sentence.

- **Control (outside caustic): continuation == truth.** 1 image, tracked,
  converged, ≤ 3 iterations, at every frame with η ≥ 85.5, both directions.
- **Birth**: bisected caustic edge η_crit = 81.6. Inside it the truth has 2
  images; the second is born at the star's limb (r_min ≈ r\*), just outside it.
- **Miss**: all 9 two-image frames show n_continuation = 1; miss fraction
  1.000. The missed image sits 0.082–0.089 rad (4.7–5.1°) from the tracked one
  (e.g. k=25, η=72.4: truth {−0.0262, +0.0630}, tracked {−0.0262}), with
  relative magnification 0.412 at birth rising to 0.776 at best alignment
  (1/|ds/dθ|, the 2D lens Jacobian).
- **Exit**: no double-tracking (0 frames); truth returns to 1 image at
  η > 81.6 and the tracker follows cleanly.
- **Instrument**: scalar and grid tracers agree exactly (max |Δs| = 0.0);
  halving dφ twice moves both roots by 1.4×10⁻⁸ rad; wall time 23 s.

Reproduce: `python3 falsifier.py` in this folder (writes `falsifier-out.json`;
23 s, < 100 MB). Numbers quoted are from its final run.

## Predictions

Written before the run in [predictions.md](predictions.md). What happened:

- **P1 half-held**: birth at the limb, separation 4.7–5.1° (I said 1.5–3°);
  the caustic edge is η_crit = 81.6, not the 128 my weak-deflection formula
  predicted — the limb deflection 4M/r\* = 0.08 rad is not weak against
  θ_E = 0.04, and the geodesic truth is the authority. Structure confirmed,
  my number was 1.6× off.
- **P2 held, under-called**: predicted ≥ 2% relative brightness; measured
  41–78%.
- **P3 vacuous in this run**: the tracker never had the branch, so no stale
  branch existed to mishandle; no double-track occurred.
- **P4 (control) held** — the instrument is sound.
- **P5 held (survivor)**: max 5 iterations, no divergence on any persistent
  branch through the whole transit. Consistent with Fermat monotonicity: along
  an emitter's worldline d/dt[t_obs − t − L_opt(t)] ≤ 1 − |v| < 0 per branch,
  so each branch has exactly one root and warm-started Newton is safe *on a
  branch it already holds*. The doc's convergence story is right; its
  enumeration story is the hole.
- **P6 not run** (BH wrap family exists at all alignments in 2D; births at
  doll entry instead of a caustic line). Stated, untested.

## What would make it wrong

If the intended gather is per-pixel backward rays (§5 steals "Wolfenstein's
observer rays"; §3 caps the view at "about one sample per pixel") rather than
per-tube continuation, images are enumerated for free and §2's sentence is
dead weight rather than the mechanism — but then the doc carries two
contradictory gathers and law.md line 53 ("Positions are gathered at the
observer's past light cone. Lensing takes deflection(b) from the doll's memo")
still describes the per-tube one. Also: my scene has one lens on the sight-line;
if a designer bounded the caustic tube's angular size below the player's floor
everywhere the game can go, the miss would be beneath the floor — but near a
fold caustic magnification diverges, so some visible window always exists.

## Cost of adoption, and fit

Adopt either: (a) enumerate both ±b branches per lensing doll on each
sight-line (pruned by occlusion b > r\* and by magnification), still O(1) per
tube per lens crossed; or (b) make the gather per-pixel and pay the sample
budget. Then freeze r6 with a behaviour criterion: *image count per frame
against an exact backward ray trace over a lens transit (caustic entry and
exit), with a planted continuation-only gather that must fail*. Today r6's
sketch ("Newton iterations and samples per frame") is cost-only, B3/B16 judge
single-path deflection accuracy — nothing in lab/rungs/ or law.md's gates
would catch this. Fit: principle 30 ("what really matters is navigation,
knowledge and dynamics those need to be perfect") and principle 19 — a
threshold-triggered spawn of probe rays would be the bandaid; branch
enumeration per lensing doll is the representation that does the job.

Also recorded, no experiment needed: representation.md §6's "undisturbed
orbits ≈ 0" is stale against the board's own gold (20261006-0735 correction:
on distinct kicks the exact memo hits 0%; law.md line 35 already carries the
re-anchoring design); and §1's "N ≈ 2πm/ln 2 (m = 16, N = 128)" — 2π·16/ln 2 ≈
145, not 128. Premise checks that *survived*: the Binet band algebra
(u″ + (1−6Mu_k)u = M/L² − 3Mu_k² follows exactly from u″ + u = M/L² + 3Mu²,
sign verified; ISCO at 1 − 6Mu_k = 0; the light form consistent), and the
flat-space "one crossing" claim (strictly monotone by Fermat, single root).
Attack ranked but not falsified (no time): premise 4's event-set margin —
sparse (generator-derived positions) and dense (stepped positions) orders can
disagree on *whether* a grazing contact exists at the floor's edge, a
different-event-graph failure that r5's shared-stepping CW case cannot expose;
cheapest next probe is one margin contact through both orders on the existing
crates.

## The lens

Red-teams overweight exotics, so the falsifier is the common case (a star
crossing any sight-line — every dogfight near a planet), not the BH wrap
family. r\*/M = 50 is a compact star; normal stars give narrower caustic
tubes but the same birth with divergent magnification at the fold. What this
lens may have missed: the same gather is AI perception (§2), off-plan today;
and I did not touch costs (r6's actual question).
