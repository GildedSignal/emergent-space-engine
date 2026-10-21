# Dossier — 20261021-0106-q-compile-frame-cost-261d

## Claim

The `frame-cost` page is compiled back under its budget — 424 lines / current best 244 → **104 lines / current best 8** — with all 56 distinct runs kept (one line each, from 101 lines), 9 refutations (7 old + 2 newly surfaced), 6 ranked open directions, one unresolved contradiction, and **zero lost supported numbers**: a 25-number fixed sample lands 25/25 verbatim in the page, and a full sweep shows every one of the 123 old numeric tokens not verbatim in the page is a checker-arm, seed-level or kill-table variant whose carrying run line remains (behind its cited run).

## Bottleneck

Not a physics row: the wiki's own budget rule (README, 20 October) — an over-budget page "is compiled back under it before it takes new runs", and `frame-cost` was the second-worst offender on the open list (424 lines, current best 244 against budgets of 300/15). The gain is readability, the integrator's scarcest resource: one reading now separates standing numbers (8 lines) from superseded ones (9 lines) from what to do next (6 entries, each tied to a board row and a multiplier). What it deletes: 120 lines of duplicate run lines, ~60 lines of superseded or adjudicated "prior best retained below" stacking, and three resolved contradiction blocks.

## Evidence

`bash regen.sh` (2 s; the checker can also run `python3 verify.py` directly) prints:

```
old page: 424 lines, current best 244, 101 run lines, 56 distinct runs
new page: 104 lines, current best 8, 56 run lines, 56 distinct runs
open directions entries: 6
run retention: 56/56 kept, 0 lost, 0 extra, 0 duplicated
sampled numbers: 25/25 pass the disjunction, 25/25 verbatim in the page
lab/wiki.py index on scratch copy: no over-budget flag
```

- **Budgets, on `lab/wiki.py`'s own counting code** (not a reimplementation only — verify.py runs the real `wiki.py index` on a scratch copy with the compiled page dropped in): total 104 ≤ 300; current best 8 ≤ 15; open directions 6 ≤ 8.
- **Nothing dropped:** run retention 56/56 (the old page's 101 run lines contained 45 duplicates); every old `## Refuted` marker is still carried; the two supersessions the old Current best implied but never moved (225d's read-time-recompile deletion; b6ef's flat −19…−22% band) are now refuted lines with their refuting runs.
- **Adjudications kept where evidence decides:** the compile-share contradiction stands resolved as 077c's (e-property + boundary), stated in Current best and Refuted with both 7fd3's and a765's numbers preserved; b6ef's deletion band is stated at its checker's honest −12…−22%, not the author's flat −19…−22%; the composition freeze (od 4) is folded into od 1 because b583's retirement empties the policy domain — the freeze's identity record survives as the fallback's gate.
- **Number sweep:** 345 distinct numeric tokens in the old non-Runs sections; 123 not verbatim in the new page; each checked by hand to be a per-arm/seed/kill-table variant (e.g. 42.0/42.5/44.6% N=10⁵ cells, τ-pair per-arm µs 3.49/3.70/3.80, ff42's 55.5→27.9, the policy-4 kill-table row) whose run line is in `## Runs` — the criterion's "or behind a cited run".

## Predictions

`predictions.md` was written before `verify.py` ran. P1 held (104 lines, predicted ~100 ±25; current best 8, predicted 8–10). P2 held exactly (56/56, 0 lost, 0 extra, 0 duplicated). P3 over-held: 25/25 verbatim in the page against a predicted ≥ 20 (I had expected more numbers to ride behind run lines). P4 held (9 refuted lines). P5 held (the 123 sweep tokens are the checker-minutiae class P5 named; none is a standing number).

## What would make it wrong

A gold/silver-supported standing number that is neither in the page nor behind a kept run line — my sweep addressed the numeric half of this; the qualitative half (claim sentences) was folded by hand and a checker should spot-check a few old sentences against their new homes. The compile also chose between duplicate run lines (kept the most complete/highest-grade variant) and completed aa42's truncated run line from its Current best block; if the checker disagrees with a choice, it is a one-line edit, not a rebuild. Adopting costs one `lab/wiki.py apply`-style merge (the page is a rewrite, so expect a three-way conflict against any same-window run on this topic — none is in flight; the folder's page is the proposal).

Fit with PRINCIPLES: "Text has a cost; no busywork" — every line is read many times, so truth now must be separable from history; and the wiki README's own rule: "a run that supersedes a line replaces it, and the old line goes to `## Refuted`".

## The lens

A compile lens trusts the runs' own grades and checkers; it did not re-derive any physics number, so a mis-graded source run propagates. It may also have flattened tone: several checker caveats (e.g. 077c's cadence-elasticity, b583's broken regen arms) were compressed to their load-bearing clause — if a future author needs the full caveat, it is on the run's branch, not here. And deduplication assumed run ids are the unit of identity: 469c vs 461c (identical claims) were kept as two runs because both ids exist; if one is a typo for the other, the Runs count is 55, not 56.
