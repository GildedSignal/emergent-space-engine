Grade: goldCheck complete. **Grade: gold** — written to `check2.md`, with `checker2-final.md` filled and my blind verifier's note appended to the proposed `wiki/nladder.md` page (after checker 1's; the rest of the page needed no correction).

**What I did independently:**

1. **Reproduction.** The runner's regen re-flew all 21 flights from the frozen binary (sha `4f42b28b…` matches, carries the patch). I recomputed every derived integer by hand from the regenerated rows: `WS = demotions` at all 7 saturating arms, `N + 30,187` at four N, price law 7/7 exact, read-stream invariance at four scenes, zombies +27,911 constant, glob live = N+2,276, hit cliff 43.3/45.4/92.1%, identity 21/21. The 0757 anchors (40,187/584,807; 130,187 at cap 262,144) reproduce exactly.

2. **Found a record defect:** `knee_table.py` crashes (line 41, TypeError on a `"10^4"` string tuple) so `regen-table.txt` silently loses five sections, and `regen.sh` exits 0 regardless (no `set -e`; `tee` masks python's status). The numbers themselves regenerate — I re-derived the lost sections by hand, all exact. One-line fix owed.

3. **Three adversarial axes outside the author's domain, all confirming exactly:**
   - **Cut 96,000** (2× the deepest): `WS = demotions = 447,747`, 0 evicts, digest = ctl's, price law exact (12,928,978), and the fixed cap 16,384 degrades **7.2× → 29.9×** with play depth at fixed N — a "concurrent working set" cannot grow 3.4× at fixed N; the archive reading survives.
   - **Seed 3:** `WS = demotions = 135,019`, identity, price law exact (777,060); offset band now 28,593–35,019 across seeds, so +30,187 is seed-1's — as the page scopes it.
   - **2×10⁵ cap 262,144** (the matrix's missing above-knee arm): 0 evicts, `promos = dem = 230,187`, hits = global's exactly, rss = sat's — the knee there is exactly 262,144.

4. **Gold bar:** held-out predictions held (seed 7, cut 48k); P1's sub-linear law was honestly self-refuted and the truth (linear with constant offset) is stronger — it kills the 400√N cap rule that would have under-sized 10⁹ by ~80×. Novel against the conflicted page and HISTORY: identifies the knee as the cumulative demotion count, refuting 0757's working-set mechanism and b0ed's S=16,384 default. The 1450 dispute is closed; adoption is a rule, zero code.

Missed by the author (recorded in check2.md): the depth-degradation curve, an unwritten cap(cut) law, the zombie constant being seed-1-only, the summarizer defect, and the promote_us tails.
