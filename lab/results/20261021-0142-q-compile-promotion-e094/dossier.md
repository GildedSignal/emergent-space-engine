# Dossier — 20261021-0142-q-compile-promotion-e094

## Claim

The `promotion` wiki page is compiled from 407 lines (current best 234) to 87
lines (current best 13, budget 15) with **no supported number lost**: a census
of all 546 distinctive numeric tokens in the old page finds 542 (99%) verbatim
in the new page and the remaining 4 behind a cited run — 0 lost — with all 14
distinct run ids kept (one line each) and every one of the old page's 13
refuted claims retained as one line each.

## Bottleneck

Not a physics bottleneck but the wiki's own: `lab/wiki/index.md` flags
`promotion` **over budget (407 lines, current best 234)** — the page had
become a log, and README rule (25) says an over-budget page "is compiled back
under it before it takes new runs". The gain is a page the integrator can act
on in one reading (the gold bar of the lens); what it deletes is 321 lines of
superseded narrative while keeping every standing number where the next author
will find it.

## Evidence

All numbers regenerate with `./regen.sh` (< 1 s; `python3 verify.py`), which
applies the wiki's own budget rule (`lab/wiki.py` line 88: current best > 15
non-blank lines or page > 300 lines flags over budget):

```
old page: 407 lines total, current best 234 non-blank
new page: 87 lines total, current best 13 non-blank      (budgets 13<=15, 87<=300 PASS)
structure: sections in order=True, header keys intact    PASS
runs: old 18 lines / 14 distinct ids -> new 14 lines / 15 distinct; missing=[]  PASS
numbers: 546 distinctive tokens -> 542 verbatim (99%), 4 behind a cited run, 0 LOST  PASS
section Refuted: 14 entries; Open directions: 8; Contradictions: 1 line; Runs: 14
headline numbers verbatim: 21–24×, 0.11%, 167–214 ns, 91.7–99.7%, ~3×10³×  all Y
VERDICT: PASS
```

What the compile did, section by section (`wiki/promotion.md` in this folder):

- **Current best, 234 → 13 lines.** The old page's ten blocks (4f59, 396d +
  checker, 5f36, b083, 2e42, 604c + provenance, c439, 8792/cbc5 memory and
  CPU halves) collapse to one line per standing result, newest first: the
  phase axis sound and 21–24× (4f59); its resident-vs-crosser domain (4f59);
  the seam flight and its decade-up (396d); the 1-D-index verdict; the exact
  tier and the quantization-signed residual answer (5f36); the 2D selector;
  the 10⁶ price (5f36); the shared-orbit structure (b083); the comb-owned
  frame tail (2e42); the crowd-proportional observer bill (604c); the O(1)
  read census (c439); mint+demote (8792); the coast-scoped memory half
  (cbc5/8792). Each line carries its run ids and its domain ("do not quote
  past 3×10⁴" etc.).
- **Refuted, 13 old claims → 14 lines.** Every old bullet kept as one line;
  one retirement the old page recorded only inside Current best is promoted
  to its own line: b083's "19.2 ns a member" window-lookup figure, retired by
  5f36's 3.2 µs `searchsorted` at K = 10⁶ (the compare price itself stands).
- **Open directions, 5 → 8, ranked by board row.** The old od 1's four
  bracketed addenda (396d's, 4f59's pricing of (b), the supersession of the
  local bail) are resolved into their own ranked entries, each naming the
  scoreboard row it moves (live-set/families for the seam answer channel and
  the interval-h lever; kick-cadence ~10³ for the comb's de-phased births;
  per-body-state for ES_SECULAR).
- **Contradictions: 1 line.** None standing — the section's five resolutions
  (8792, c439, 2e42, 396d, 4f59) are kept as one pointer line each inside it,
  with the P6 coast-only watch note.
- **Runs, 18 lines → 14.** The old section listed five runs twice as
  truncated duplicates (b29a, 760f, c4d3, the 1d52…0619 range line, cbc5);
  each is now one line with the fuller claim fragments merged, all 14 distinct
  ids kept, plus this run's own line. Claims ≤ 20 words.
- The 4 tokens held only behind their run: `21.5` (396d-checker's
  99,715 × 216 B ≈ 21.5 MB a held scan), `1.3e-9` (5f36's same-orbit ⊥ bound),
  `3002` (2e42's `ev=3002` worst-frame tag), and `1120` — a tokenization
  artifact (the timestamp of run id 20261016-1120-cdf0), not a finding.

## Predictions

Written before the check in `predictions.md`; outcome:

- **P1 held** (13 ≤ 15 current-best lines — under the predicted 14–15; 87
  total ≤ 300).
- **P2 held on both parts**: 100% coverage (0 lost), and the verbatim fraction
  came in at 99% against a predicted floor of 55% — the 15-line budget
  accommodated nearly every number inline, so the "honest risk" I flagged
  (digests and controls pushed behind runs) touched only 3 real tokens.
- **P3 held with one count corrected**: the old Runs hold **14** distinct ids
  (I predicted 13 — the `1d52 … 0619` line carries two ids on one line, as it
  did before); 18 lines → 14 (13 deduped + this run), none missing.
- **P4 held**: 14 refuted lines (13 kept + the 19.2 ns retirement added).
- **P5 held**: all five headline numbers verbatim (`21–24×`, `0.11%`,
  `167–214 ns`, `91.7–99.7%`, `~3×10³×`).
- **P6 (kill criterion) did not fire.**

## What would make it wrong

A number the census calls "verbatim" could be verbatim but *misattributed*
(moved to a line citing a different run than its source) — the census checks
presence, not attribution; I re-checked each compiled line against its source
block while writing, but a checker diffing attributions is the right
adversarial pass. The census's "behind a cited run" fallback is per-paragraph
in the old page, so a number accidentally dropped from a multi-run paragraph
could hide behind a neighbor's id; with 542/546 verbatim this binds at most 4
tokens, all listed above. Adoption cost: the page replaces
`lab/wiki/promotion.md` at publish (`lab/wiki.py apply`); nothing else reads
it, no code changes.

## Fit with PRINCIPLES

"Text has a cost; no busywork" (P11) and the wiki budgets (Julien, 12
October: "maybe we need a karphaty style wiki where the current best and
directions are clear and not missed to update") — the page shrank 4.7× with
nothing supported deleted; "a run that supersedes a line replaces it, and the
old line goes to `## Refuted` as one line" is now actually true of this page.
Via negativa: the deletion *is* the work; no new claims were added, per
"results are never rewritten here, only compiled".

## The lens

A compile lens risks two blind spots. (1) It trusts the old page's
attributions: where two runs disagreed, I kept the newer/adjudicated reading
(5f36 over b083's idealized "empty answer"; 2e42 over 0552's SCAN_BACKLOG
mechanism; 396d's checker over the author's P3/P4) as the old page itself
adjudicated them — a fresh look at the *runs* might adjudicate differently,
but that is a physics run's job, not a compile's. (2) Choosing which numbers
stay inline is taste: I kept every number that a reader deciding "fix the
comb first, then the seam's answer channel, and price h for crossers" needs,
and pushed instrument-integrity details (digests, control matches, decode
point lists) behind their runs; a different taste would draw the line
elsewhere, and the census bounds that choice (4 tokens).
