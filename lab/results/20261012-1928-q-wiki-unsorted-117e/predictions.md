# Predictions — 20261012-1928-q-wiki-unsorted-117e (lens: sort the unsorted runs)

Written before the verification pass (`verify.py`, `grades.py`), which
re-derives every check below from the `origin/claude/lab-<id>` branches. The
classification itself was derived from the 81 dossiers and the twelve wiki
pages. One correction made before any verification ran, disclosed: P4 below
first said "nine" runs; counting the list I had written gives thirteen — the
number thirteen is the prediction of record.

## P1 — Grades match the assignment sheet.

For every non-missing run, the sheet's grade equals the two-checker rule read
off the branch (`gold` iff both checkers say gold; `lead` if either says lead
and neither says gold; `silver` otherwise). I expect zero disagreements; any
disagreement would be a publisher-grep defect (the missing-`Grade:`-line
family of fa4b/6586), not a mis-graded run.

## P2 — Second-author runs land on their parent's page.

All 29 `second-*` runs' parent branches exist, and every parent that a wiki
page already cites sits on the page my placement names. I expect exactly two
deviations, both argued in the dossier: `aa29-0ee9` (parent `aa29` is on
encounters for the CF-pass overlap; the second run's substance is the
resonance lock judge) and `a1a4-a194` (parent `a1a4` is on high-gamma-clock
for the γ-wall; the second run's substance is the plunge-tube record itself).
No other mismatch.

## P3 — Five new topics, no more.

Exactly five clusters of ≥ 3 runs share a topic no existing page holds:
`smoothness` (16), `binet-cells` (5), `resonance-gate` (4), `contacts` (4),
`plunge-tubes` (4). Every other run lands on an existing slug — `kick-jet`
20, `memory-h-live` 6, `handoff` 5, `encounters` 4, `gravity-news` 3,
`kick-cadence` 3, `frame-cost` 2, `view` 2, `b12-statistic` 1,
`coorbital-cert` 1 — or a proposed single-run slug `changeover` (1). The
verify pass must count exactly these totals (sum 81).

## P4 — Overlap with today's sibling q-wiki runs is exactly thirteen runs.

The wiki pages updated today (kick-jet, memory-h-live, handoff, and the rest
of the twelve) already list thirteen of my 81: c3a5, ec9d, 0083, 620e, a48d
(kick-jet); ba64, a9c4, d205, 6a0e, c304 (memory-h-live); 6586, 0d8c, 2da8
(handoff). The check must match run ids only as Runs-list entries or
parenthesised citations — a second author's id embeds its parent's id, so a
naive substring grep false-positives (it did, on first pass: f045, cc88,
762d). Extra genuine overlaps mean my "unsorted" premise is partly stale; I
would report them rather than re-place runs differently.

## P5 — Every run has a dossier with a claim.

81/81 dossiers fetched from the branches; none empty beyond a title; each
yields a ≤ 20-word claim for the table without guessing (no `[NO-CLAIM]`
rows in the final table).

## What would falsify the sorting itself

A cluster I split across two pages that one dossier names as one question,
or a run whose dossier names an existing topic I missed. The verify pass
greps each dossier for the twelve existing slugs and reports every hit
against my placement (all hits found were context words — `view`, `belt` as
English — none a topic claim).
