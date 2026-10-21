# Predictions (written before the decisive check)

The decisive experiment is `verify.py`: it checks the compiled page
(`wiki/promotion.md` in this folder) against the old page (`lab/wiki/promotion.md`,
407 lines, current best 234) with the wiki's own budget rule (`lab/wiki.py` line 88:
> 15 non-blank current-best lines, or > 300 total lines, flags over budget).

- **P1 (budgets).** The compiled page passes both budgets: `## Current best` at
  most 15 non-blank lines (expect 14–15; the old page's ten blocks fold into one
  line per standing result), and at most 300 total lines (expect ~100). The five
  sections appear in the README's order; the header keeps `topic`/`status` and
  sets `updated:` to this run.
- **P2 (no supported number lost).** Census, not sample: every distinctive numeric
  token in the old page's `## Current best` + `## Refuted` (a token with ≥ 3
  characters or a non-digit — e.g. `21–24×`, `167–214`, `0.11%`, `148,996`,
  `3.6e-15`, `2¹⁰`) is either (a) verbatim in the new page, or (b) in a block whose
  run id (its 4-hex) the new page cites. Expect 100% coverage, with ≥ 55% verbatim;
  the verbatim misses concentrate where the new page points instead to the run:
  8792/cbc5's memory half, b083's instrument details, and 5f36's decode-point
  lists. Trivial tokens (bare `0`–`99`, section numbers) are excluded from the
  claim — they carry no finding.
- **P3 (runs kept).** All 13 distinct run ids of the old `## Runs` (the section
  lists 18 lines but 5 are truncated duplicates of b29a, 760f, c4d3, the
  1d52…0619 range line and cbc5) appear in the new `## Runs`, one line each,
  claims ≤ 20 words, plus this run's own line (14 lines total).
- **P4 (refuted).** The new `## Refuted` keeps every one of the old section's 13
  claims as one line each, and adds the one retirement the old Current best
  records but Refuted lacks: b083's "19.2 ns a member" window-lookup figure
  (retired by 5f36's 3.2 µs `searchsorted` at K = 10⁶) → 14 lines.
- **P5 (held-out, the checker's own ten-number sample).** Any ten numbers the
  checker samples from the old page land verbatim in the new page or behind a
  cited run. Specifically these five headline numbers are verbatim in the new
  page: `21–24×`, `0.11%` (the cold-belt F), `167–214 ns`, `91.7–99.7%`
  (comb-owned), `~3×10³×` (the 10⁶ closure).
- **P6 (kill criterion).** If P2 reports any distinctive token neither verbatim
  nor behind a cited 4-hex, the compile is wrong and this run's claim fails: the
  page must be recompiled before it can be graded. A budget breach (P1) is the
  same failure.

What I expect to be the honest risk: P2's verbatim fraction. The old page carries
instrument-integrity numbers (digests, controls, control matches like
`d1822b88…`, `2.2e-16`, `47.7%`, `42.36`/`42.5`, `5,651/5,651`) that a 15-line
current best cannot carry inline; the prediction is that each of them sits in a
block whose run the new page cites, so nothing is lost, only moved behind its run.
