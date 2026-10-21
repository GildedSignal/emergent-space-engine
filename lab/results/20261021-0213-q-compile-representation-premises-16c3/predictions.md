# Predictions (written before the compile's verification runs)

Held-out cases: I have read the old page, its git history (to recover text the merges
truncated) and the run branches' grade subjects, but none of the checks below has run.
The decisive experiment is `check_compile.py` on the written page plus a scratch
`wiki.py index`. Kill criterion for this compile: any number the old page supports that
is neither in the new page nor behind a kept run line, or any budget broken.

1. **Number survival.** A normalizing tokenizer over the old page yields 300–400
   distinct numeric tokens; ≥ 99% survive verbatim in the new page, and survival is
   100% once the kept `## Runs` lines are included. The only tokens allowed to leave
   the prose are superseded duplicates that remain inside their kept run line
   (1645's pre-checker edge numbers 2.7°–28.3° / 33°, corrected by f2e3).
2. **Budgets.** The new page lands at ≤ 175 total lines (budget 300) with
   `## Current best` at ≤ 15 non-empty lines (budget 15; predict 12–15). The old page
   passes wiki.py's letter (196 lines, CB 10) while breaking the README's "one line per
   run" and "never their history" rules — the new page passes all of them.
3. **Duplication.** The old `## Runs` holds ~47 bullet lines for exactly 17 distinct
   run ids (measured while scoping: 47/17); the new page holds exactly 17, each once,
   and `wiki.py index`'s run count drops from 46 to 17.
4. **Grades.** The run branches record 7 gold and 10 silver; the old page marks at
   least 6 of these wrongly ("awaiting grade" or missing). The new page carries the
   branch grade for every run. (506c, e59e, 9ffc, 1885, 915d, 7bcf, f2e3 are the golds
   I read off the branch subjects before writing this file — prediction is that no
   eighteenth run and no regrade appears when regen.sh re-reads them.)
5. **Open directions.** All 7 old items survive inside ≤ 8 new items, each new item
   naming the board row it moves or "off-board (view correctness)"; 0 dropped.
6. **Contradictions.** The old section's four resolved pseudo-conflicts compress to
   ≤ 3 lines with their resolutions and run pairs; no new contradiction appears.

What would make this wrong: a supported number that only lived in the old Current
best's narrative (not in any run line or dossier) and that I fail to carry — the
tokenizer is built to catch exactly that, and any miss blocks gold, not the method.
