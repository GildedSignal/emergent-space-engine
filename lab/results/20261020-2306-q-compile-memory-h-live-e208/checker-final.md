Working...
Check complete. `check.md` written at `lab/results/20261020-2306-q-compile-memory-h-live-e208/check.md` — **Grade: gold**.

**What I did:**

1. **Reproduced** — `./regen.sh` exit 0; every dossier number matches (587→178 lines, Current best 333→15, 110 dated ids, 26 Refuted, 7 open directions, 0 of 559 tokens lost).
2. **Re-verified with independent instruments** (not the author's): a stricter no-canon tokenizer (all 4 number-run deltas are punctuation variants of surviving numbers in context), Refuted preservation 25/25, the 3 dropped Runs lines audited as genuine dangling duplicates, the completed second-checker line traced to the old page's own record, the +1 Refuted entry (CLI clamp) verified in shipped code at `xtask/src/universe/mod.rs:40` exactly, and `wiki.py index` dry-run: no over-budget flag.
3. **Adversarial** — mutation test found the instrument's real blind spot (page-global token matching: a number deleted from Current best survives unnoticed via a Runs line; quantified — 47/559 tokens Runs-only, 5 non-citation, none material); whole-line deletion *is* caught, so it's an instrument, not a control. Full `wiki.py apply` simulation with the run's `base` commit: **clean merge, 182 lines, index clean** — the dossier's "large diff or conflict" worry was wrong in the run's favour, though the Runs union does resurrect the 3 dropped dangling lines (cosmetic).
4. **Predictions** — 4/5 held; the one miss (178 vs 195–215) is honest and on the safe side. Mtime proof was destroyed by the runner's restore, noted in check.md.
5. **Novelty/fit** — directed queue compile of the index's worst page; unblocks all future runs on the live-set rows; "Text has a cost … rewritten in place."

No overstatement found in the author's proposed page; no in-place correction needed. Live `lab/wiki/` untouched; no git operations; sandboxes removed.
