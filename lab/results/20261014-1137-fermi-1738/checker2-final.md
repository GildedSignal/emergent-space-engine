Working...
**Grade: gold** — written to `lab/results/20261014-1137-fermi-1738/check2.md`.

**What I verified (all independent of the author's scripts):**

1. **The audit's core claim reproduces from primary sources.** I read 90fb's `budget.py`/`budget-table.md`/`cascade.jsonl` and effb's `ledger.py` off their origin branches myself: 90fb's `kicks_s = N·K_AVG/P·RTF` = 222/s is the whole billion's kick stream, so the "0.966/0.077 cores **per cell**" row is the partitioned total — a literal per-cell rate would be 9.66e-6. 90fb's own cross-checks (max-rtf 5,216, k=32 re-derivation 110 ≈ the historic 190) force the total reading. effb's `enc_skin = 0.077·(N/1e4)` regenerates 7.7e3/1,925×/7,051×/5.2e5 exactly as the double count plus a 100× rtf frame mix. Every cube cell regenerates to 3 digits in my own recomputation.

2. **Anchor, third independent run:** 812.8 pairs/kick, changed 0.0024, slack 0.9458 — exact.

3. **Adversarial, outside the author's range:** I built 90fb's bench against the *current* shipped crate and ran the never-measured points: n=10⁷ X=150 → 165,435 pairs/kick vs law 175,322 (−5.6%, inside the ≤7% band; the ∝n law the whole 10⁹ cube rides on holds a decade beyond its anchor), and n=4×10⁶ verify with 10⁴-body cells → global == cells = 66,555.1, 0 mismatches. Also resolved 90fb's c6W anomaly (15,412.6 vs 18,703.5) as a kick-sample artifact, not a cells pair-cut.

4. **Novelty:** effb's own checker repeated the erroneous composition in its novelty note; the wiki carries the mislabel; HISTORY/git are silent — the error was live and adopted (effb silver merged).

**Missed by the author** (in check2.md): the contiguous-**narrow** shipped-cadence wall is 5.19×10⁵ — exactly effb's held-out number (effb's wall regenerates as one cube cell, stronger than the dossier's "all walls above it"); the board line predates effb and matches the surviving single-belt+skin range; the "~10² islands" ratio bracket is actually 10⁻³–10¹; 90fb's queue rows carry no second double count. None touches the central claim. The proposed wiki page is faithful — no corrections needed.
