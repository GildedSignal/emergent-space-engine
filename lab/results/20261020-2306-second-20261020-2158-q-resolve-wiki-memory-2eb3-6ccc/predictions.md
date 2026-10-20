# Predictions (written before the decisive experiment)

The checker's named gold experiment: land the fix end-to-end — hand-merge 87d0's
+92/−9 patch at HEAD, key the Runs union on run id, publish this page through the
real publisher, and measure. Facts already established (git, read-only): 87d0's raw
patch fails `git apply --check` at HEAD exactly at `lab/wiki.py:83` (its index hunk
meets the 20 Oct budgets change); the page at HEAD carries 6 Runs lines
(de18×3, 87d0×2, 2eb3×1) because the shipped union keys on exact text; the
pre-publish page (at 2eb3's base 9bf31c70) carried 3 Runs lines (de18×2, 87d0×1).

- **P1 (the merge):** 87d0's raw patch fails at HEAD in its index() hunk only;
  after hand-merging that one hunk (flag at line start via `has_markers`, keeping
  the budgets lines) and adding the id-keyed Runs union, the merged patch applies
  cleanly to pristine `HEAD:lab/wiki.py` and `python3 lab/wiki.py index` still runs.
- **P2 (the named flight):** through the patched publisher, replaying 2eb3's actual
  silver publish (ours = the page at its base commit, theirs = its graded proposal,
  base = the same commit) lands the resolved page: the body above `## Runs`
  byte-identical to what the shipped publish landed, exactly 3 Runs lines — one per
  id, with the graded wordings (de18 silver, 87d0 gold) — zero marker lines of all
  three kinds, no UNMERGED banner, and the wiki-memory index row `| open | 3 |`
  with neither flag.
- **P3 (idempotent on re-publish):** applying the same run's pages again is a no-op
  (the skip): the page is byte-identical after the second apply, index row unchanged.
- **P4 (the next publish carries a correction):** a following run's page for this
  topic (this run's, with 2eb3's line reworded from "awaiting grade" to "silver")
  lands as 4 Runs lines — one per id, 6ccc appended — and the reworded line
  *replaces* the stale variant instead of being re-added beside it.
- **P5 (negative control, shipped):** the same replay through pristine
  `HEAD:lab/wiki.py` re-adds the stale lines: 6 Runs lines (de18×3, 87d0×2, 2eb3×1)
  — the checker's measurement, reproduced as the control that must fail.
- **P6 (corpus ceiling):** at least 25 of the 41 pages carry the same-id duplicate
  artifact in `## Runs` today; folding each page's own Runs list on run id leaves 0
  pages with duplicate ids and loses no id on any page.

Kill criteria: the landing is wrong if P2's body differs from the shipped body
(content loss), any marker or UNMERGED banner survives, P3 is not byte-identical,
or the union drops a run id that either side carried.
