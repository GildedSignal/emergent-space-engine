Working...
Check complete. **Grade: gold** — written to `check.md`, with a confirming bracket added to the run's wiki page.

**Verdict basis:**

1. **Reproduction (exact, clean build).** Crates byte-identical between the two bases; rebuilt `breathe` from 84b2's committed patch — every regenerated arm is byte-identical to 84b2's committed data, and the seed-1 12800 series is line-identical to the first checker's own arm through tick 9216. Every cell of all three dossier tables reproduced by my own script, including the 84b2-sourced F64_late ladder cells.
2. **Held-out.** predictions.md (01:49) predates all decisive data (≥01:53). The decisive P1 held with kill lines unfired; P4's number missed (2.0–2.1% vs ≤1.6%) and is honestly reported as the instrument lesson.
3. **Adversarial, all confirming** (evidence in `chk2/`): fresh seed 4 extinguishes at t 10240 (F64_late 1.88); 6400 flown to H 16384 falls F64_late 4.96 → 2.87, so the "6400 row smuggles ringdown" reading is flown, not inferred; **n = 25600 (outside the author's range, partial 10 blocks)** extinguishes at t 18432 — inside the pre-stated 18–30k band — with m@8192 now 3.86% (the fixed-window artifact grows on) and onset ≈ ∝ side (the super-linear hint was seed scatter).
4. **One record defect:** this run's `work/patch.diff` is empty — the harness source is 84b2's committed patch, not this folder's; reproduction unaffected but flagged in check.md and on the page.

Tree restored to base, no processes left, no git commands run.
 (my applied patch removed); no git commands run; no processes left.
