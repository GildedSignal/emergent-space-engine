# Predictions (written before the decisive verification)

The work is a compile, not a physics run: the decisive experiment is the
faithfulness verifier (`check_compile.py`) run on the finished page. These are
the cases I have not tuned on — the full number-token sweep over the old
page's `## Current best` and `## Refuted`, not my hand-picked favourites.

1. **Dedup.** The old `## Runs` holds 81 raw lines but only **57 distinct run
   ids**; 24 exact-id duplicates get deleted (7922 appears 5×, 009b and cd6e
   3×, thirteen more ids 2×). Where duplicates carry evolving grades
   (awaiting → pending → silver), the latest line (silver) is kept.
2. **Budget.** The compiled page lands at **9** non-blank `## Current best`
   lines (limit 15) and **~125 total lines** (limit 300), by `lab/wiki.py`'s
   own counting rule (which I replicate in the verifier).
3. **No run lost, none invented.** The set of run ids in the new page equals
   the old page's set (57 = 57); no id appears twice in the new `## Runs`.
4. **Number faithfulness.** Sweeping *every* number token from the old
   `## Current best` + `## Refuted`: **0 lost**. I expect roughly 55–70% to
   appear verbatim in the new page, the rest (fine census detail: 719,845;
   100,091; 165.9–36,054.9; 21.7 µs; anchor hexes; per-arm wobble) to sit
   behind a run id cited in the new page.
5. **Short-id carry-over.** Every short id the old page cites in prose
   (b063, 1e74, a669, b30b, b9ae, 0e37, 12db, 6701, b172, efd4, fe85, …)
   appears somewhere in the new page, so "behind a cited run" stays true for
   every number that cites them.
6. **Kill risk (what would make this fail).** A supported number that is
   neither in the new page nor on a cited run's line — i.e. a fact I dropped
   while compressing. If the verifier finds any, the compile is not done.
