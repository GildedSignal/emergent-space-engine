# Dossier — 20261019-0141-redteam-c78d (premise red-team)

## Claim

The design's aggregate-readout letter — "Aggregates are one sample each, and the screen
caps the work at about one sample per pixel" (docs/representation.md L59; the same
 "~1 sample/pixel" row at L116) — is refuted on the **occlusion** channel: one sample is
one occlusion predicate, so any fleet-scale eclipse is all-or-nothing; a fleet larger
than the planet it passes behind is shown **totally gone** for the sample's eclipse
window while ≥ 89% of its flux remains visible (measured 89.1% mid-transit error at
R_f = 3·R_p, 99.0% at 10·R_p), the failure survives exact retarded-time geometry and
k⁴ beaming at β 0.5 (total blink while 53.5%/81.5% of the seen flux is visible, transit-
plane/sky-plane fleets), and it occurs exactly where 1885's dispersion refutation reads
zero (β = 0, uniform fleet) — the two channels are orthogonal and both must be paid.

## Bottleneck

Not a board bottleneck: a premise hole in the view (the doc's own cost table, "The view
≤ 1 sample per pixel per frame"), opened by e59e (opacity absent) and 22d1 (the per-row
occlusion law measured) — this run closes the aggregate half that wiki direction 5
explicitly named unmeasured. Gain: it deletes the one-sample-per-aggregate rule before
any occlusion is wired (the rule is the natural first implementation of L59 and would
ship the artifact), and replaces it with a closed form (the occluded fraction of a
uniform-disc aggregate is the circle–circle overlap area — derivable, "compute only
surprises") or the pixel cap the same line already licenses.

## Evidence (exact float instrument, `occlusion.py`, 16 s, deterministic seed 20261019)

Uniform-disc fleets (N = 10⁵ static / 2×10⁴ at β), exact behind-disc predicate;
one-sample = the representative point's own predicate (centre, and median of 20 random
members); circle–circle overlap closed form as cross-check (P9: max deviation 0.0030,
i.e. MC noise); β arm: exact per-ship retarded time (quadratic, past root) + 3D
segment-vs-disc predicate (22d1's law) + exact SR k⁴ weights. Occluded flux fraction
f = flux remaining/total.

| config | peak err | err @ mid | f₁ @ mid | f_true @ mid | f_true min | time>5% | total-blink time |
|---|---|---|---|---|---|---|---|
| R_f/R_p = 0.01, impact 0 | 0.289 | 0 | 0 | 0 | 0 | 0.01 | 0 |
| R_f/R_p = 1, impact 0 | 0.605 | 0 | 0 | 0 | 0 | 0.67 | 0.07 |
| **R_f/R_p = 3, impact 0** | **0.891** | **0.891** | **0** | **0.891** | **0.889** | 0.67 | 0.22 |
| R_f/R_p = 10, impact 0 | 0.991 | 0.990 | 0 | 0.990 | 0.989 | 0.09 | 0.09 |
| R_f/R_p = 3, grazing impact 2.8 | 0.067 | 0.067 | 1 | 0.933 | 0.933 | 0.25 | 0 |
| β 0.5, R_f = 3, transit-plane | 0.592 | 0.535 | 0 | 0.535 | 0.535 | 0.18 | 0.06 |
| β 0.5, R_f = 3, sky-plane | 0.835 | 0.185 | 1 | 0.815 | 0.815 | 0.15 | 0.06 |
| control N = 1 | 0.000 | — | — | — | — | — | — |

Mechanism, closed forms (all verified by the instrument): mid-transit error =
1 − (R_p/R_f)² for R_f > R_p (0.889 at 3, 0.989 at 10 — measured 0.891/0.990); the
error > 80% window is exactly the **sample's** eclipse width 2·R_p (measured 2.00 R_p)
inside a fleet transit of 2(R_p+R_f) = 8 R_p; the R_f = R_p peak 0.605 sits at the
limb-crossing step where the centre flips behind while 40% of the fleet is still outside
(lens area A(0.99,1,1)/π = 0.397 → f_true 0.603, f₁ = 0); the blink is sample-choice-
invariant (random-member: path peak 0.305, blinks the whole fleet's flux on one member's
predicate at a random phase). The pixel cap of the same line is the cure at
O(pixels): h = R_p/2 → **145 samples, peak error 3.0%**; h = R_p/8 → 1957 samples, 0.46%
(both time>5% = 0) — 690× compression against per-ship at 3% error. The closed-form
overlap itself is the cheapest cure (0 extra samples, cf_dev 0.003 vs 10⁵ ships).

Frozen kill criterion (predictions.md, written before the run): one-sample FAILS if any
R_f ≥ R_p config shows peak error > 5% with partial dimming (f_true > 0 where f₁ = 0).
Verdict: **REFUTED** (0.605–0.991 ≫ 0.05, every R_f ≥ R_p config, both orientations at
β 0.5). Licensed safe domain: R_f ≲ 0.1·R_p *in duration* (time>5% = 0.01 of transit) —
but even there a limb-crossing flash of O(0.5)·fleet-flux exists for ~2R_f/v (one frame
or less; sub-frame at belt speeds).

## Predictions

`predictions.md`, 10 pre-registered. Held: P1 (N=1 exact, 0.000), P3 (89.1% ≈ 1−(1/3)²,
blink width 2.00 R_p, f_true_min 0.889), P4 (99.0%), P5's duration half (0.67 > half),
P7 (145 samples → 3.0% < 15%; 1957 → 0.46% < 5%), P9 (cf_dev ≤ 0.0030 < 1%). Missed,
each sharpening the law's domain: **P2** (safe-regime peak: 28.9%, not <5% — the crossing
flash is O(0.5) for any size; safe in *duration* only), **P5's peak** (60.5% vs the
30–50% band — the just-inside window is worse than my hand lens areas), **P6** (random-
member mid error 0.109 vs centre 0.891, far outside ±10pp — the random member is usually
visible at mid; its artifact is the random-phase whole-fleet blink, path peak 0.305),
**P10** (grazing impact 2.8: 6.7%, no blink — the centre never passes behind; grazing
failure is a *missed eclipse*, not a blink). **P8 held in form, split in magnitude**:
total blink persists under the exact retarded predicate (f₁ = 0 while 53.5% transit-plane
/ 81.5% sky-plane of seen flux visible); the ">80%" number holds for the sky-plane
orientation (peak 0.835), not the transit-plane one (deeper ships sit deeper in the
shadow cone, so 46% of the fleet is truly occluded there — correct physics, orientation-
dependent). Instrument fix, disclosed: the β arm's first window missed the seen transit
(light-time shift β·d ≈ 12.5 R_p); widened and mid redefined to the seen eclipse centre
(argmin f_true); static-arm numbers unchanged.

## What would make it wrong

- Fleets in this game always subtend less than ~0.1× the occluders they pass behind
  (then P2's regime is the game's and the letter is duration-safe; the census entry would
  record the licensed domain, not a refutation). Counter-evidence on the record: a
  "fleet on one orbit" (taleb-09b5's 400-ship formation) spans an orbital-radius-class
  arc against planet-radius occluders — R_f/R_p ~ 1–3 is the formation case, and any
  player LOS passage with impact < R_p blinks it.
- The eventual occlusion wiring samples per pixel (not per aggregate) from day one — then
  the letter's first clause is dead but its second clause was the cure all along (P7);
  adoption cost is then ~nothing (the pixel cap is already the screen's budget).
- The k⁴-weighting or retardation could conspire to make the blink invisible — measured
  the opposite (the beamed approaching flank is the *unoccluded* part, softening the
  number but never the blink: f₁ reaches 0 in every relativistic arm).

Cost of adoption: the closed-form overlap (or per-pixel samples) replaces the one-sample
predicate — O(1) per aggregate per frame either way, no per-ship loop; fits principle 3
(derivable ⇒ never evolved). Fit with PRINCIPLES: the refutation *defends* principle 28
("the view is an instrument… it's a space clock literally" — an instrument that blinks
out whole fleets carries no information) and principle 20 (tail events: the blink is the
worst case, not the average); the cure is principle 35's simplest form.

## Rung criterion (none exists today; verified: no file in lab/rungs/ mentions occlusion
or eclipse; r6 gates per-emitter cost/presence only)

**eclipse-parity, aggregate half** (freeze-ready): configs — candidate: closed-form
overlap (or per-pixel) aggregate occlusion; negative: the one-sample aggregate (L59).
Criteria: (a) behaviour — an N ≥ 100 fleet at R_f ≥ 3·R_p transiting at impact 0 behind
a planet must match the exact Σk⁴-occluded fraction within 5% at p99 over the transit
and reproduce f_true_min ≥ 0.88 at R_f = 3·R_p; (b) type — the negative must show f = 0
for a ≥ 2·R_p path window (error > 80%); (c) cost — ≤ 150 samples per aggregate.
Judged in the observer's frame at player β, both fleet orientations (transit-plane and
sky-plane); the β arms' exact predicate (retarded time + 3D segment-vs-disc) is the
oracle. This folds into representation-premises direction 2's eclipse-parity rung as its
aggregate arm, and direction 5's unmeasured tail is hereby measured.

## The lens

Premise red-team ranks by player visibility; this attack is maximally player-visible
(fleets are the game's noun) but it inherits the lens's blind spot in the other
direction: exotic-regime costs (strong-field occlusion near the photon sphere, occluder-
observer comoving frames, aggregate emitters partially dimming *other* aggregates) were
not swept — direction 5's remaining tail (extended occluders, fleet-doll occluders) stays
open. The six premise-census entries (two-body doll, Binet, kicks, dense≡sparse, view,
undisturbed≈0) were re-checked against the page and left as standing: no cheap un-tried
falsifier remains for them at this lab's reach (the EOB strong-field flank needs an
NR-calibrated oracle; the rest is guarded or measured).
