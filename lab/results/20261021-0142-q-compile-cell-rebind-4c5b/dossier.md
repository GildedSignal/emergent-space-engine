# Dossier — 20261021-0142-q-compile-cell-rebind-4c5b (lens: compile the wiki page `cell-rebind` back under its budget)

## Claim

The `cell-rebind` page is compiled back under budget with no supported number lost: current
best 47 → **13 non-blank lines** (limit 15), page 117 → **50 lines** (limit 300), every one of
the **120** distinct numeric tokens of the old page found in the new page (108) or behind its
cited run's branch artifacts (12), **0 lost**, all 4 run ids kept one-line-each with branch-head
grades (silver, silver, silver, gold) and their truncated claims completed from the dossiers.

## Bottleneck

Not a scoreboard row but the wiki's own budget rule (lab/wiki/README.md, 20 October): the index
flagged the page `over budget (117 lines, current best 47)`, and an over-budget page "is
compiled back under it before it takes new runs" — every future run on the micro kick-cost row
(the board's `cell-rebind` lever, ~10–10²) would have had to wade through a log first. The gain
is the reader's one reading, priced at the integrator's attention on every later run.

## Evidence

All numbers regenerate with `bash lab/results/20261021-0142-q-compile-cell-rebind-4c5b/regen.sh`
(runner applies `work/patch.diff` first; it holds only the `lab/wiki/cell-rebind.md` replacement):

- **Budgets (wiki.py's own rule, `best_lines > 15 or lines > 300`):** old page reads current
  best 47 non-blank lines, 117 lines — over budget, as the index flagged; the compiled page
  reads 13 and 49 — the flag clears (`python3 lab/wiki.py index`; row: `open | 4 | **Standing
  shapes are O(1) in N …**`, no over-budget tag).
- **Number conservation (`compile_check.py`, stronger than the gold bar's ten-number sample):**
  every numeric token of the old page — census counts, B13 counts, µs constants, the 10⁹ cores
  row, seed pairs, kick counts — is either in the new page or behind a cited run; the 12
  behind-run tokens are seed-2/3 recurrence and cell pairs (0.9512, 0.9516, 1420, 1419),
  10⁵-stream deltas (0.9913, 0.9917, 0.3), the wall-budget kick counts (166985, 167262,
  167352), and the f7c3 checker's β = 0.083 and cells +1.2% — each printed with the run and
  artifact that holds it.
- **Runs:** the old section had 7 lines for 4 run ids — three runs appeared twice, once
  `(awaiting grade)` and once graded, and every claim was truncated mid-word at ≈74 characters
  (verified on the runs' own branches: their proposals carry the same cut). The compiled page
  keeps one line per id, grades matching the branch heads, each claim's first words verbatim
  and its completion taken from that run's dossier (≤ 20 words per the README schema).
- **Supersessions moved, not deleted:** f7c3's "3.7–4.5 compiled cores at 10⁹" (the 104 µs
  composition) becomes a `## Refuted` line superseded by 6e91's 4.95 µs / 0.15–0.17 cores, with
  f7c3's served estimate (~0.02–0.04 cores) noted as confirmed — the two runs' disagreement is
  adjudicated in the page, evidence on the belt's own keys deciding for 6e91. Checker 2's
  correction of "29,097 identical rebinds" (structural, 9,699 × 3 fires) becomes a Refuted line.
- **Open directions** re-ranked to 5 by the board rows they move: belt-scoped serving (live-set
  row ~400× at 10⁶ + kick row 7.8×) first, width ladder vs B13 second, turnover, resonance
  guard, Carlson last (≤1.1×).

## Predictions

`predictions.md` was held out before `compile_check.py` ran. Held: P1 (13 current-best lines,
≤300 total, index flag clears, runs 7 → 4), P2 (100% of tokens conserved; every load-bearing
constant in-page; nothing needed to be rescued back into the page), P3 (both disagreements
adjudicated with the standing side named), P4 (superscript/comma normalization sufficed — no
manual token counts), P5 (claims completed from dossiers, faithful). One deviation, in the
safe direction: I had predicted leaving 4.84 µs, 0.728 µs, 382/844 kicks, 2.03 MB and 0.20
B/body behind their runs; the final page carries them in-page instead, so only 12 tokens
(not ~20) sit behind citations.

## What would make it wrong

The compile drops a number the checker samples that is neither in the page nor in a cited
run's artifacts (the check covers all 120 tokens, so this would have to be a format the
tokenizer misses — e.g. a number spelled out in prose); or a completed run-line claim
misreads its dossier; or the three folded `(awaiting grade)` lines are ruled lost record —
they are duplicates of graded lines for the same ids, and the runs' branches keep the
originals. Cost of adoption: none beyond merging the page (the patch is one file; the index
regenerates). Fit with PRINCIPLES: "Text has a cost; no busywork" (11) and the wiki's own
budget rule — truth stays, history goes to the runs; "Pointers, not copies".

## The lens

A compile lens reads, it does not measure: I trusted the old page's numbers as the record and
checked only their conservation, not their physics — a number that was wrong in the old page
is still wrong in the new one (the checker's own sampling shares this blind spot). The lens
also biases toward deduplication; a reader who wanted the awaiting-grade snapshots inline
would object to the fold.
