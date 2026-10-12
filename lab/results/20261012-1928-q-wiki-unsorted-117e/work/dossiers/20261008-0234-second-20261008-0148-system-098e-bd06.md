# Dossier — second author on 20261008-0148-system-098e

Run: 20261008-0234-second-20261008-0148-system-098e-bd06. Linux x86 cloud box;
orders of magnitude only. Scripts copied from the author's run and extended in
this folder; the tree outside `lab/results/` is untouched.

## Claim

The silver's named gaps are closed on the shipped mechanism: under a corrected
second-order light-cone reference the author's record stands bit for bit, the
design's actual structure — the static **integer** lag table read at the
**arrival-time** cell — is behaviour-neutral (1.3e-8 at c=30) and never early
on all 3,280 arrivals, which the author's float event-time-cell variant is
**not** (early by up to 5.3e-2 yr at β=0.33: the published never-early was an
artifact of the shared first-order reference); the smear invariant holds
full-doll as ≤ 3.02 **larger**-cell light-crossings at every separation
(source-cell units: max 72), and the cost ratios are now measured, not
arithmetic (82.7×/662× fewer tests per kick, 9.2×/74× less state including
the shared table).

## Bottleneck

Not a cost rung: the `b-news-gravity` build decision. The checker's named gold
experiment — implement in `crates/universe`, pass gates B13/B14/B17/G1–G6 with
per-pair cursors as the measured control — is forbidden to a lab run (never
edit the crates) and costs more than one window. This run executes its
cheapest decisive parts: fix the instrument, run the design's mechanism (not a
float sample of it), correct the falsified invariant on the full doll, and
turn the cost table into measured numbers. What it deletes stays what the
author claimed: the per-(body,source) cursor's state and per-pair tests, plus
three planned structures collapsed into one (news, multipoles, certificates).

## Evidence

All commands run in this folder. The five `toy2` configs each take ~80–105 s
(16 seeds, 5 laws, 12 yr), slightly over the 60 s budget — the scene is the
author's, unweakened; they run in parallel in ~2 min.

**1. The record regenerates from shipped code** (`regen_check.py`):
`python3 toy_news.py c30|c300|per` (~50 s each; logs `regen_c30.txt` …) and
`python3 smear.py` reproduce the committed JSONs **bit-identically** (×3 True)
and the smear headline med 2.74 / max 3.36.

**2. The instrument fix the checker named** (`toy2.py`, law `exact` = light
cone solved by fixed point on the receiver's unperturbed Kepler, 12
iterations): the record was **not** an artifact — c30: exact(2nd) vs cell =
9.425e-9 (author: 9.425e-9); c300: 5.0e-10; per: 2.8e-10; the Laplace control
still separates ~2×10⁴×.

**3. The correction the fix exposes** (not in the author's or checker's
record): with a true light cone, the author's float `cell` law (receiver cell
at **event** time) arrives **early** — `per`: max arrival delta **+2.0e-4 yr**,
`c3`: **+5.3e-2 yr** (`never_early=False` in `toy2_out_per.json`,
`toy2_out_c3.json`). The published "never early ✓ in every run" held only
because reference and law shared the same first-order bug. The design's
stated choice — receiver cell at **arrival** time, integer `ceil` — is not
"the engine's choice, smear dominates either way"; it is what makes never-early
true at all.

**4. The shipped mechanism** (`toy2.py`, law `cellint`: one static per-doll
integer table (ring, ring, Δspoke) → ceil(max-distance/W0) quanta, W0 = ring-0
width; the entry is **c-independent** — one table per doll, any c; receiver
cell at arrival; 16 entries used in the impulsive scenes, 232 in `per`):

| config | exact(2nd) vs cellint | never early |
|---|---|---|
| c30 (β_p=0.033) | max 1.26e-8 | True |
| c300 | 5.0e-10 | True |
| per (201 events) | 2.16e-10 | True (3,216 arrivals) |
| c3 (β_p=0.33) | **1.62e-6** | True |
| near (a0=1.15, ~2–3 widths) | **1.98e-6** | True |

The integer quantization costs a factor 1.3 against the float cell law at c30
and nothing measurable at c300 (both 5.0e-10). Both regime gates the design
needs now have numbers **on the shipped mechanism**: β_source between 0.033
(1.3e-8) and 0.33 (1.6e-6) — the checker's float c=10 point (7.7e-8) puts the
gate between 0.1 and 0.33; separation ≲ 4 cell widths (2.0e-6 at ~3 widths,
Laplace control exploding at 5.9 while exact and cellint still agree in order).

**5. The invariant, corrected and full-doll** (`smear_wide.py`, ~20 s, 29,977
pairs, sources rings 0–30, receivers to 98, all Δspoke — the checker's
uncommitted script rebuilt): lateness in **source**-cell crossings med 6.4,
max **72** (unbounded in distance; the dossier's "at every separation" was a
±5-ring sampling artifact); in **larger**-cell crossings med 1.46, p90 2.49,
**max 3.02, ≤ 3.02 in every separation bin** (down to 1.28 beyond 200 widths);
same-ring diametric 2.01. The bound is structural, not luck: for convex cells
dmax−dmin ≤ diam₁+diam₂ ≈ 3 larger-cell widths. Corrected invariant: **never
early; late by ≤ ~3 larger-cell light-crossings, independent of distance.**

**6. The measured control** (`bench.py`, ~5 s, real int32/int16 arrays, ops
counted, 20-sweep medians):

| N | tests/kick cursor vs cells | wall | state cursor vs cells+table |
|---|---|---|---|
| 2^20 | 82.7× (4.1 ms vs 0.10 ms) | 41× | 9.2× (10.5 M vs 1.13 M words) |
| 2^23 | 662× (31 ms vs 0.10 ms) | 314× | 74× (83.9 M vs 1.13 M words) |

The author's 83×/662× arithmetic is confirmed as measured op counts. Honest
accounting: including the shared int16 lag table (2.5 MB, one per doll) the
state ratio is 9.2×/74×, not 21×/165×; and the cell design wins only above
the crossover N ≈ 1.1×10⁵ bodies (S=10, depth 4) — below it, per-pair cursors
are smaller. Belt scale is 2^20+.

## Predictions

`predictions.md` was written before toy2/smear_wide/bench ran (the author's
record had already reproduced; that part is not a prediction). **5 of 5
sections held; one number missed.** Held: the record survives the second-order
reference (9.4e-9 ∈ [1e-10, 3e-8]); cellint passes all three behaviour
windows (1.3e-8 / 5.0e-10 / 2.2e-10) with never-early everywhere; both gates
cross as predicted (1.6e-6, 2.0e-6, Laplace 5.9); the full-doll smear
reproduces the checker's both-units structure (max 3.02 ≤ 3.6, diametric 2.01,
source-cell unbounded > 20). Missed: I predicted the state ratio including the
table as ~13×/100×; measured 9.2×/74× (I halved the int16 table's word count
wrong). **Unpredicted finding** (a failure of my tuning, not of the claim):
the float event-time-cell law is *early* under the corrected reference —
prediction 2's never-early clause was stated for cellint only, and correctly
so, but I did not foresee that `cell`'s published never-early would break.

## What would make it wrong

- Still a Newtonian toy with c exaggerated ~2000× and one changing source;
  the crates build the checker named is the only way to close that, and it is
  exactly what remains for gold: per-cell version rings + the integer lag
  table in `crates/universe`, gates B13/B14/B17/G1–G6, per-pair cursors built
  as the control. This run makes that build's design decisions safe (arrival
  cell, not event cell; larger-cell bound; β and separation gates) but does
  not replace it.
- The `exact` reference remains second-order in μ_p (receiver on star-only
  Kepler): position error ~μ_p·τ² ≈ 1e-4 AU at c=3, below the cell width —
  not the binding error anywhere measured.
- The cellint fixed point iterates the receiver cell at arrival; on a cell
  boundary it could oscillate (last iterate taken). Not observed in 3,280
  arrivals; the engine reads the cell from the body's own compiled position,
  which has no iterate at all.

## Cost of adoption

The lens `b-news-gravity` should be redirected before the build: per-cell
version rings + the static integer lag table (arrival-time cell) instead of
per-(body,source) cursors; exact per-pair light cones only inside the
encounter layer (≲ 4 cell widths) and above the β gate (between 0.1 and
0.33). Proposed lens patch (draft for the integrator; the lens is theirs):

> Build gravity-at-c on the doll's ring cells: each cell holds per-source
> version rings, read at one static per-doll integer lag table
> (ring, ring, Δspoke) → ceil(max-distance / W0) quanta of the lattice's own
> time unit (W0 = ring-0 width; the table is c-independent), with the
> receiver's cell taken at arrival time — never early by construction; late
> by ≤ ~3 larger-cell light-crossings at every separation. Exact per-pair
> light cones own separations below ~4 cell widths and sources above the β
> gate (0.1–0.33). No per-(body,source) cursors.

Live citations (the author cited archived files): the law's home is
`docs/law.md` §"Gravity travels at c" (5 October); the cell layer is
`docs/HANDOFF.md` "Gravity is a field held by cells. Multipoles are the
mechanism" — this structure is that layer and the causality certificate in
one object, as claimed (H0196).

## Fit with PRINCIPLES

- 23: "beyond c=1 means paradoxes" — never-early now verified under a true
  light cone, on the shipped mechanism, 3,280/3,280; and the record's earlier
  "never early" is honestly withdrawn where it was reference-artifact.
- 33: "a body resolves only the influences that are significant at its own
  scale" — the lateness bound is in the larger cell's light-crossing, the
  lattice's own unit, at every distance.
- 3: "Compute only surprises" — the table is static per doll; undisturbed
  sources cost nothing; 82.7×/662× fewer per-kick tests measured.
- 19: "a fix signals the wrong representation" — the float event-time cell
  was a fix; the arrival-time integer cell is the representation.

## The lens

As second author I inherit the first run's blind spots: single-source scenes
for behaviour (S=10 only in the mechanism bench), no comparable-mass binaries
(q-gravity-at-c's failure there is inherited, not retested), and I could not
run the named crates experiment — so "adoptable within one step" remains a
design statement with measured toy evidence, one build away from the gold the
checker defined. I also did not re-verify the checker's c=10 point myself; I
rely on their number for the gate's lower edge.
