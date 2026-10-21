# Predictions — compile `encounters` under its budget

Written before `check_compile.py` has run once. The compiled page is
`wiki/encounters.md` in this folder; the old page is the tree's `lab/wiki/encounters.md`
(503 lines, current best 224, 138 run lines). The kill criterion for this run: a
load-bearing number from a gold/silver paragraph that is neither in the new page nor
behind a run the page cites, or a budget violation the counters confirm.

- **P1 (budgets).** The new page holds ≤ 300 lines total and ≤ 15 non-blank lines under
  `## Current best` by `lab/wiki.py`'s own counters (`best_lines`, `len(text.splitlines())`);
  a scratch `lab/wiki.py index` over a wiki copy with the compiled page swapped in reports
  `encounters` open, not over budget, no conflict flag. Expect ~136 lines, current best 15.
- **P2 (run conservation).** All **71** distinct run ids of the old page's `## Runs` section
  appear exactly once each in the new `## Runs`, in chronological order; the 138 physical
  lines collapse to 71. Two known artifacts fold: `20261017-1018-second-` (a line truncated
  mid-id by an old merge, completed to the b509 id) and `20261007-1234-quant-7578` (a
  typo'd duplicate of `20261007-1032-quant-7578`; only 1032 has a branch — grade silver).
  I expect no other id loss.
- **P3 (grades).** For every run with a branch, the grade in the new page equals
  `git log -1 --format=%s origin/claude/lab-<id>`'s `Grade:` field. Five page grades are
  stale and I correct them to the branch: 4ea2, 71a5, 73f0, 5d90 were demoted to
  "silver (second checker disagreed)" after the page's gold lines were written; 34be's
  page line still said "awaiting grade"/"silver" where the branch says gold; e828, f2f1,
  1738, f0a2, 2b89, c9c7, cd3b, 5567, 1a29 have branch grades newer than the page's
  "awaiting"/bare labels. Two runs have no branch (8cee, 2222) and keep their page grades.
  Expect 0 mismatches in the audit.
- **P4 (number conservation, curated).** A curated sample of ~120 distinctive numbers from
  every section of the old page (fixed in `check_compile.py` before its first run; not
  edited afterwards to pass): every entry is found verbatim in the new page **or** its
  carrying run id is present in the new page (behind a cited run). Expect 0 lost. The
  inline share I expect at 70–90 %: the old page's current-best blocks repeat their runs'
  numbers almost fully, but checker-provenance arithmetic (e.g. 2.8e-7, 1.2e-6 at
  belt-real hazard) stays behind its run line.
- **P5 (number conservation, held-out).** A seeded random draw of 40 number tokens from
  the old page (seed fixed in the script before its first run; I have not seen the draw):
  expect ≥ 32/40 (80 %) found inline. The misses should be dates in run ids, section
  counts, or checker-provenance arithmetic whose run line the page keeps. If a miss is a
  load-bearing constant from a gold/silver claim, that is a failure and I fix the page
  (never the sample) and disclose the fix.
- **P6 (reader actions).** Every `## Current best` line cites run ids; every `## Refuted`
  entry names its killing run; `## Open directions` ≤ 8 and each names the board row it
  moves. Expect 0 violations.

Adversarial case I set for myself (what a checker will try): sample ten numbers at random
from the old page's current-best blocks — the seven big paragraphs (f2f1, 73b5, e828,
1176, 9fd1, e87d, 08d0) hold ~200 numbers between them; my page was written to carry
their standing constants inline, so I predict 10/10 resolve.
