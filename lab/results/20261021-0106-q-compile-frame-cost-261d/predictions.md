# Predictions (written before the decisive verification)

The decisive experiment: `verify.py` audits the compiled page against the old
`lab/wiki/frame-cost.md`. Cases below are not tuned on; the compile exists, the
checks have not run yet.

- **P1 (budgets):** the compiled page passes `lab/wiki.py`'s rules — ≤ 300
  total lines (predict ~100, ±25), `## Current best` ≤ 15 non-blank lines
  (predict 8–10), and `wiki.py`'s own counting code run on a copy flags nothing.
- **P2 (run retention):** all 56 distinct run ids of the old page's 101 run
  lines appear exactly once each in the new `## Runs` (the 45 duplicate lines
  collapse; no run id is lost or doubled). Predict 56/56.
- **P3 (sampled numbers):** for the 25-number sample listed in `verify.py`
  (fixed before running), each is found verbatim in the new page or its
  carrying run id is cited in the new page. Predict ≥ 20 of 25 appear verbatim
  in the page itself (the rest ride behind their run lines); 25/25 pass the
  disjunction.
- **P4 (refutations kept):** every claim the old `## Refuted` carries (7
  entries) is still carried as refuted, plus the two supersessions the old
  Current best implied (225d's read-time-recompile deletion; b6ef's flat
  −19…−22% band). Predict 9 refuted lines, none dropped.
- **P5 (standing numbers):** every number the old Current best states as
  standing (not struck as an artifact) is either in the new page or behind a
  cited run line. I expect to lose verbatim page placement for at most the
  checker-extension minutiae (grid radii 5/12/23/40 arm detail, seed-level
  counter lists) — those stay behind their run ids.

## Kill criteria

- Any budget breach, any lost run id, any duplicate run line → the compile is
  not gold-grade; fix before the checker sees it.
- A gold/silver-supported standing number that is neither in the page nor
  behind a cited run → the compile dropped supported content; not acceptable.
