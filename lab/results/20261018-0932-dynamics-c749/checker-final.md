Working...
Check complete. `check.md` written with **Grade: silver**, and the author's proposed wiki page corrected in place.

**What I did:**

1. **Reproduced independently** — my own parser (`/tmp/check_law.py`), not the author's `analyze.py`, on both raw executions: execution 1 (3 fires) and the runner's regen (5 fires) — all 8 with `D == fin_hi − s0` exactly, s0 exact, `out=` shut; exec 1's m<0 stats match the dossier to the chronon (min −432, max −48, median −224). Every fire is the shipped assert itself (`alloc.rs:1499`, exit 101) — the patch is print-only as claimed.

2. **Attacked outside the author's range** — three arms: galaxy 12288/36 fleets (**0/4 fires** — incidence is *not* monotone in scale), margin 0.25 (2 fires, law exact, including a **total-invisibility publish-blind fire**: fatal pair in no armed line at all, 13 fully green publishes before it), min_region 8 (containment holds, 161 RBs `out=` shut). Also: the dossier's ranges broke on regen — violations to 192 (12 windows), bboxes to 3,384.

3. **Why silver, not gold**: three pre-registered prediction letters failed (P3/P5/P6 — each honestly disclosed, and P3's failure is the run's second finding), which caps at silver by this lab's own precedent; and the pooled headline numbers (0/267, 94/261, 3,148) include an execution whose raw draws the run's own `regen.sh` deletes, so they cannot regenerate — the law itself regenerates robustly (16 fires since the author's 6, zero counterexamples). The gold-making experiment is named: re-pre-register the corrected law and fly it held-out on the fresh rungs my arms already pass.

Tree restored to clean (only `lab/results/` untracked, as found).
