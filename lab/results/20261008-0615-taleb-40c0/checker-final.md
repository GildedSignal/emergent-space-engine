Working...
Check complete. `lab/results/20261008-0615-taleb-40c0/check.md` written, tree restored, nothing else touched.

**Grade: gold.**

**Reproduced bit-for-bit from the dossier's commands** (patch applied to clean tree, fresh build): 16/16 matrix lines, 12/12 play lines, and all three control digests. The core claim holds exactly as reported — one digest per seed across every schedule path, only presentation counters move. The leak reproduces exactly too: four distinct digests per seed, encounters 68–102, contacts 0–14, and the ruin form (`play60-starve`: same machine, same fps, different load → encounters 100→68, contacts 4→14).

**My three adversarial cases strengthened it:**
1. **rtf 1** (the author's admitted unmeasured gap): the leak persists at the page's default pace — digests split across fps for both seeds tested, and the load-only form splits for seed 22. The player's canonical position moves even where encounter counters chanced to be stable.
2. **512 members**: still splits (contacts 4 vs 12).
3. **Threads on the play path** (untested by the matrix): `play60-starve` thr8 ≠ thr1, while `frame-starve` thr8 = thr1 = direct — so the core stays thread-clean and the difference flows through the same decision-tick seam. Thread count is a leak axis the author missed.

**Predictions**: file timestamps confirm `predictions.md` (06:23) preceded `matrix.txt` (06:24) and `play.txt` (06:28); all five pre-registered predictions held; the play seam was honestly declared post-hoc and isolated by a control I reproduced.

**Recorded against it**: the dossier misquotes HANDOFF (the risks list names no silent nondeterminism), and section 1's core negative is confirmatory — adba97a/H0213 (5 October) already measured "one digest over five schedules and budgets", uncited. Section 2 is the novel part: law.md's frozen Ties rule says decisions are "never at a wall-derived one", yet the shipped live loop writes wall-derived ticks into the log the rule depends on, and `kick_bench.rs:68` shares the seam — so bench digests are wall-derived too. Adoption is one step: two lines quantizing the decision tick to scheduled game time, plus a play60/play30 equal-digest regression test (which should also pin the load-only pair, per my rtf-1 run).
