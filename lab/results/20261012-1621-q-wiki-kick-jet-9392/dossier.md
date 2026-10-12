# Dossier — 20261012-1621-q-wiki-kick-jet-9392 (compiler run: wiki page `kick-jet`)

## Claim

The `kick-jet` page is compiled: the jet (a kick updating a compiled cycle from stored
derivatives, law.md:35) is retired by six standing golds, a kick recompiles its cycle
exactly, and the page gives the integrator the replacement's measured price, the refuted
claims, the ranked open directions and the two unresolved contradictions without opening
a dossier.

## Bottleneck

The board's `kick-jet` bullet ("six golds refute the multiply-add update; what is the
cheapest exact kick on the shipped representation"). The wiki is the lab's memory
(Julien, 12 October): this run deletes the rediscovery cost — 30 runs on one topic, read
once, weighed by grade, with the unconfirmed and the ungraded kept visibly separate.
No new physics; the gain is that the next author and the integrator start from the page,
not from 36 branches.

## Evidence

- The page: `wiki/kick-jet.md` in this folder (30 run lines: 29 kick-jet runs + b242,
  missing). Every claim cites run ids; grades are the integrator's clustering (a check.md
  "gold" without a confirming second check stands silver — df81, 8306, 7922, e86c, 96b4,
  6164, 67f2 all have single-checker gold grades and are recorded at their standing
  grade, with df81 and 8306 flagged for their single checks).
- Adopted state on `main`: law.md line 35 retires the jet (12 October) citing 4978, b33f,
  d617 and noting "the adopting run of 6 October had one checker"; HANDOFF line 44:
  "six golds refute it; it is not wired into the plane". The six standing gold
  refutations are 4978, 9a04, a059, b33f, ee08, d617.
- No experiment was run (the compiler's mandate); no contradiction between runs demanded
  a probe — the one live disagreement (b33f vs 2c68) is settled in structure by the
  ungraded b242 and differs in observable (gates vs drift floor), so it is recorded as a
  contradiction with its deciding experiment named, not probed.
- Regenerate everything: `bash lab/results/20261012-1621-q-wiki-kick-jet-9392/regen.sh`
  (~5 s; extracts the grade lines, the retirement text and the load-bearing numbers from
  the run branches and `main`, and re-counts the page's run lines).

## Predictions

`predictions.md` was written before the page. Held: P1 (law/HANDOFF retirement text),
P2 (the six golds; the single-checker golds standing silver), P3 (representation.md:67
still carries the multiply-add — recorded as the design-doc-lags contradiction), P5
(every sampled number appears verbatim in its run's dossier or checker abstract), P6
(the b33f/2c68 contradiction, different observables, no run measured both). Missed, and
corrected in the page: P4 said b242's branch was missing entirely — the branch exists
with a dossier but no `check.md`; its dossier refutes 2c68's "bounded by construction"
(shadow-reset artifact, error compounds across rebinds) and supplies the offset × age
trigger correction, so the page cites it as ungraded, and the miss changed the
Contradictions entry for the better.

## What would make it wrong

- A sampled claim not traceable to its run's dossier/check.md, or a grade misread
  (the checker samples five claims).
- A run misfiled: the 29/6/1 split (below) is judgement, not measurement; a compiler of
  another topic may claim one back (the cross-topic list is the handoff).
- The retirement being newer than a cited run's evidence: the page's current best
  mirrors law.md:35 as of `main` 54fcac1e; a law change after that date reopens it.

Cost of adoption: none (a wiki page; publishing merges it into `lab/wiki/` three-way).
Fit with PRINCIPLES: "Text has a cost" (11) — one page against 36 branches; "Survive
compaction… anything that isn't written durably is lost"; the page keeps contradictions
rather than resolving them by fiat (31: "keep contradictions").

## Runs that belong to another topic (for that topic's compiler)

- **memory-h-live**: `20261007-2057-second-20261007-2002-spacex-3b99-be63` (gold) —
  belt mutual walk needs 4.3×10¹² orbits at 10⁹; an embedded 10⁻⁷ M* body gives 90% of
  the 51.2-bit ceiling in 32 orbits; σ(1/b) is an n-growing order statistic, Hill-floored
  restores n-stability. `20261011-1332-fermi-e3bc` (silver) and
  `20261011-1456-second-20261011-1332-fermi-e3bc-c4ce` (silver) — the 10⁹ budget:
  per-event compute and per-active-body cycle memory (0.75–3.4 KB) bind; c4ce measures
  crossing_state 0.34–0.42 µs and re-anchor ρ 0.001–0.002/rebind closing rtf 100 at 10⁹
  (cited from the kick-jet page for the exact path's affordability).
- **frame-cost**: `20261010-0656-second-20261010-0541-system-d51f-3e48` (gold) — the
  incremental deadline (arrival rate in position form, re-anchored past ⅛ of the light
  distance) deletes the scheduler's per-event walk (1123→42) at bit-identical digests;
  −26.6 µs on the mean frame, flat on the rtf-100 median.
- **kick-cadence**: `20261010-1816-system-67f2` (silver) — deferring a kick's application
  walks energy linearly (exponent 1.01 at 36 renewals/orbit vs 0.07 immediate); the
  renewal quantum has one home and it is not the impulse side.
- **gravity-news**: `20261011-1102-scout-4c5b` (silver) — Peters' flux balance drifting
  the exact tube's (E, L) is adoptable (handoff = separatrix, re-key wall, 1PN flux
  contract); the checker corrected its circ_L √a artifact (the P9 "spurious e = 0.81"
  was born on a plunging orbit). Cited from the kick-jet page for "inspiral is not a jet".
- **missing, not graded**: `20261011-1814-second-20261011-1729-system-2c68-b242` —
  branch exists, no check.md; its dossier (carry compounds across rebinds; offset × age
  trigger; B12/B13 fail on the baseline tree today) is cited as ungraded wherever used.

## The lens

The compiler lens reads checkers' abstracts first and dossiers only where they disagree,
so a number an abstract garbles but a dossier states correctly could pass through; the
five-claim sample is the guard. It also inherits the integrator's clustering as the grade
of record — if that clustering is stale (a second check landed after 12 October 12:21),
the page's grades are stale with it. What it may have missed by topic: runs whose primary
claim is cost but whose secondary claim is memory or the scheduler (eea5, 0ccd, 8c81)
were kept in kick-jet on their dominant claim; a frame-cost or memory compiler may
reweigh them.
