Working...
Check complete. Verdict written to `lab/results/20261014-1631-library-7f99/check.md`, one correction added to the author's `wiki/nladder.md`.

**Grade: silver.**

**What held under reproduction:**
- `audit.py` re-runs exactly: 26/26 kills, 5/5 revival anchors, 877/427 recompiles/frame, 9,158× headroom; all arithmetic re-derived (33333/78=427, 33333/38=877, 12821/1.4=9158).
- All six automation-debt sites are real shipped code at the cited lines (`radial.rs:50-51,193,226,247-248,254`; `encounter.rs:175`).
- Every third-party number (b29a's 38–78 µs / 9–26% refusal / 8,257 B; 0e37's 1,806 B / 520 B / 0 belt reads / 1.4 game-s cast; a2c1's 84× / keep 17 / 1,017 of 1,028 / 905→2,885) traces to the wiki.
- Corpus is genuine: cross-validated against library-9192's independent Readwise fetch (same first book; the Musk anchor sits in its `page_8.json`); 9192 died gradeless, so "mined verbatim for the first time" holds against all seven prior library runs.
- `predictions.md` (16:35:50) precedes `audit.py` (16:38:53) — held out honestly.

**What broke under attack:**
- My wider add-back sweep found a missed sixth revival: r9 killed kick-avg, yet `docs/law.md:30` keeps kicks orbit-averaged on stable orbits (PRINCIPLES: "restored"). Law level is 3/26 ≈ 12% landed, not "2 = 8%" — prediction 1's "≤ 2" is not robust, and by the author's own decision rule the law level sits *at* quota rather than bracketing it. The actionable claim (frame path 0 add-backs) survives.
- The 26-kill census is a sample (encounters/b12/kick-cadence/kick-jet Refuted sections hold more), and the kill unit is inconsistent (14 B12 candidates = one event).

**Why silver, not gold:** `work/patch.diff` is 0 bytes — nothing was deleted and no behaviour measured on shipped code; the ≥10³ headroom is safety arithmetic on other runs' numbers, and prediction 3 is a control that cannot fail. The gold experiment is exactly the held-out prediction 4: delete the two sensors + sticky promotion, rerun the 10³ arm and the retrograde-0.49-R_H chatter case — a measured ~60× deletion if it holds.
