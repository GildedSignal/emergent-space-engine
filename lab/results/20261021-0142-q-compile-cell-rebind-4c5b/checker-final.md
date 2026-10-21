Working...
Check complete. `check.md` written, worktree restored to HEAD.

**Grade: silver**

**What held (reproduced, independently):**
- `regen.sh` byte-identical on a clean tree with `work/patch.diff` applied (base = HEAD = `5c06c9cc`, matching the run's `base` file): 47/117 → 13/50, index flag clears, only the cell-rebind row changes, grades silver×3/gold from branch heads.
- My own tokenizer (different implementation, 124 tokens vs the author's 120): **0 lost**, same 12 behind-run tokens, each verified in the cited runs' branch artifacts.
- Predictions genuinely pre-registered (01:48 vs 01:52 for the check script); the post-check page edit is the disclosed safe-direction deviation; P1–P5 all held.
- Semantic audit: every load-bearing compression traces verbatim to a cited dossier (f7c3's 4,096-cell ceiling, ef8c's 394×→"~400×", checker 2's seed-3 "unmoved"); run-line completions faithful; truncation verified on the runs' branches. No page correction needed.

**What caps it at silver** — the same gap that capped all four sibling q-compile runs, which the author never tested: the shipped `wiki.py apply` merges `## Runs` as a literal union. My exact simulation of the publish: body merges clean, but all 7 folded lines come back — **58 lines, 11 run lines, every id 2–3×, the `(awaiting grade)` and mid-word-truncated claims restored**. The budget survives (58 ≤ 300, flag stays clear), so the landing is softer than nladder's (322 > 300), but the dossier's "cost of adoption: none beyond merging the page" holds only for the budgets, not for the one-line-per-run tidy. One experiment to gold: land `fold_runs` (id-keyed fold, flight-proven in the wiki-memory run) and re-simulate.

Minor finds, recorded in check.md: dossier evidence says "13 and 49" where claim/regen say 50 (stale draft number — in the dossier, which I don't edit); the 6e91 run line is 21 whitespace tokens against the ≤20-word schema; current-best line 21 stacks 6e91's facts under a "(9eeb; …)" attribution.
