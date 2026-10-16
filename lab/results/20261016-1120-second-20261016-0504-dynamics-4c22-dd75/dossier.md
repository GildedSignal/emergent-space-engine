# The corrected instrument confirms every headline of 20261016-0504 and rewrites its composition paragraph: the storm is one doll's own kicks and boundaries, the "pull lane" never existed

## Claim

Run 20261016-0504-dynamics-4c22's checker named one experiment for gold: re-fly the event attribution
with the deduplicated `ES_ATTRIB` instrument (the original patch declared the counters Vec twice and
took twice per frame, so row *i* read frame *i*/2's counters and odd rows read drained zeros) and
amend the composition/lane paragraph. Done, on this run's own record: **every headline of the
original table regenerates exactly** (baseline 334/136, stag 260/136, phase 53/25, envelopes,
events/game-s, and the digest controls — OFF bit-equal to the frozen record, so the dedup touches
instrumentation only), and the corrected composition is **stronger than the checker's 20-s
preview**: the worst-12 storm frames at 6,000 game-s are **97.2% Home-doll items (211.0 of 217.1
events/frame)**, the single worst frame (334 events) is **100% attributed (d2 k76 b255, d3 b3)**,
the player's doll d0 carries **zero** events in every worst-12 set, and over the whole flight the
attribution is exclusively d2+d3 (83.2% of all events; kicks 9,824 ≈ boundaries 9,711). The
original's "second delivery lane" / "pull lane" (145.7 of 217.1) and P4's one-population-two-lanes
revision were pure instrument artifact; the corrected N=0 floor split is (40.6: dolls 20.4 /
residue 20.2) and the phase arm's post-collapse worst frames keep the N=0 plane's shape
(32.1: dolls 13.8 / residue 18.3) — the collapse claim survives with corrected numbers.

## Bottleneck

Unchanged from 20261016-0504 (the board's first gap, bodies in the flyable engine): the storm is
~9.8 ms M1-rate of the 12-ms letter; this run does not move that bottleneck, it repairs the record
that documents it. What the correction buys is the *aim*: a de-phase or secular-kick lever must
target **one doll's planet-local population and its boundaries** (kicks ≈ boundaries in equal
number), not a putative fleet stream through the player's lane — a wrong lane reading would have
sent the next run looking at pull-lane scheduling that does not exist.

## Evidence

Budget-free coast (`budget 100000 ms`), rtf 100, seed 1, one thread, this Linux box (8 vCPU,
load ~1, quiet). Generator `scripts/run_batch.sh`, analysis `scripts/summarize.py` (lane split
re-computed as tot / d0 / d2+d3 / residue), `scripts/analyze.py` (author's, unchanged — its rows
are now frame-aligned). Raw per-frame rows + per-doll attribution: `data/*.txt`; everything
regenerates via `regen.sh` (~4 min: builds + 8 flights + 3 digest runs).

**P1 — identity control (held, exactly).** My patch = the author's patch minus the 8 duplicated
instrument lines (plus 5 comment lines); the law is untouched: digests OFF = the frozen record
bit-for-bit (N=100 `4b822570…` kicks 1530, N=1000 `6895ce06…` 3767, N=3000 `ddd5b1cc…` 3767);
stag `e5e9bea5…` 3750; phase `708f7d82…` 3932. Table: baseline 60 s max 334 / p99 136 / ev/gs 4.02 /
envelope 198·192·178·210; stag 260/136/4.02 (180·188·178·195); phase 53/25/4.78 (36·24·13·12);
N=0 max 51; N=600/10³/10⁴ 20-s flights identical (240/136/5.82, 157·159·154·152); phase 10⁴
53/26/8.18.

**P2 — the corrected composition (held, stronger than predicted: I said ≥88%, measured 97%).**
Worst-12 frames, 60 s baseline: **tot 217.1, d2+d3 211.0 (97.2%), d0 0.0, residue 6.1** (the
author's broken reading: 217.1 / 71.4 / 145.7). Worst-6, all one doll plus d3's constant 3:

| frame | events | d2 | d3 |
|---|---|---|---|
| 3173 | 334 | k76 b255 (=331) | b3 |
| 1586 | 251 | k21 b227 | b3 |
| 793 | 240 | k26 b197 | b3 |
| 2379 | 229 | k34 b192 | b3 |
| 396 | 212 | k30 b166 | b3 |
| 1189 | 207 | k32 c2 b161 | b3 |

Frame 3173's attribution sums to exactly its 334 events: the biggest beat is 100% Home-doll
kicks+boundaries. Whole flight: 23,690 events, 19,702 attributed (83.2%), **all** of them d2
(19,559: k 9,824, b 9,711, c 24) + d3 (143) — d0 never appears, at any N or arm. The stag arm's
worst-12 is the same story (202.4: 197.7 dolls, residue 4.8): the re-formed comb is also ~98% d2.

**P3 — the N=0 floor (held).** Corrected worst-12: **(40.6: d0 0.0, dolls 20.4, residue 20.2)** —
the author's "pull lane 35.8" was the same artifact. The floor is half doll traffic, half the
background the first-item attribution never sees; there is no third population at any N.

**P4 — the phase arm's shape (held in substance; letter missed low by 1.2).** Post-collapse
worst-12: **(32.1: d0 0.0, dolls 13.8, residue 18.3)** — I predicted dolls 15–30; measured 13.8.
The claim that survives: the collapsed worst frames have the N=0 plane's composition (roughly half
doll traffic, half background; 43% vs N=0's 50%), so the de-phase leaves the plane's own floor, now
with corrected numbers instead of the artifact pair (5.5/26.6).

**P6 — N-independence of the corrected split (held).** The 20-s worst-12 split is bit-identical at
N = 600, 10³, 10⁴: **(177.6: 0.0, 164.9, 12.7)** — the checker's preview number, now on three
independent flights of this record.

## Predictions

`predictions.md` was written after the instrument fix was verified (both parities attributed,
worst-6 all d2) and before the batch above. P1 held exactly; P2 held stronger (97.2% vs ≥88%
predicted); P3 held at the line (20.4 vs ≥20); P4 held in substance, letter missed by 1.2 (13.8 vs
a 15–30 band — disclosed); P5 held (d0 = 0.0 everywhere, under the <8 bound); P6 held bit-identical.

## What would make it wrong

The corrected instrument is still first-item-only (`resolve_body`'s first plan item): it
under-counts bodies that resolve several items in one frame, and the residue (6–20 events/frame)
is whatever never passes a body resolution — I do not decompose it further, and nothing in the
claim rests on it. The composition numbers are this scenario's locals (the ladder's Home doll at
coast); other scenes' doll populations could mix differently. The phase arm itself remains
unflown on legality (B13/B14-class) and its +19–41% front-loaded price is unchanged by this run;
adopting anything still needs the gates. Cloud wall-times are this box's; event counts and
digests are exact and deterministic.

**Cost of adopting:** none — this is a record repair plus a composition correction; the levers and
their prices are exactly run 20261016-0504's (the de-phase is a law change, gates unflown; the
doc's own step 5, secular kicks for stable planet-doll bodies, deletes the comb's events rather
than spreading them — and this run sharpens its target: one doll's kicks *and* boundaries, in
equal number).

**Fit with PRINCIPLES:** "Measure before claiming" and the lab's own lesson from 5 October —
"agreement between runs is not independence when they share a harness; check that the measured
events are distinct" — is the whole of this run: the original's two analysis scripts agreed because
they shared the broken rows, and the phantom lane was the narrative that artifact shaped. "No work
for no reason": knowing the storm is one doll's own boundaries kills any lane-scheduling work
before it starts.

## The lens

The second-author lens (reproduce the checker's named experiment, no more) kept this run narrow,
by design: I did not re-open the mechanism, the M1 timings, or the arms' legality, and the residue
(what the first-item attribution never sees) is characterised only far enough to show no d0 and no
second population hides in it. What the lens may have missed: whether the residue is doll-level
schedule work or multi-item resolutions — one grep-sized question for whichever run next touches
the comb.
