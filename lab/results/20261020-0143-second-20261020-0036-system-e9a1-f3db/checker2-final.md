Working...
Check complete. Verdict written to `check2.md`: **Grade: gold**.

**What I verified independently (blind to the first checker):**

1. **The refutation is real and total.** I censused all eight of e9a1's committed `.err` files from its branch: every burn arm pulls nonzero in root (1e5: 467 calls/103,219 pulled; 2e5: 467/203,292; both 40 s arms: 606/138k) — only coasts pull 0. Its "0 ships pulled, every arm" is contradicted by its entire committed record, and I confirmed the misread mechanism on the page: its awk did `split($4,a,"=")` then `a["pulled"]` — a string index into a numerically-split array, always 0.

2. **The attribution survives attack beyond the flown domain.** 3e5 (outside the author's range): the pull carries 2454.4 of 2463.0 ms; the worst frame's event count (49,885) = max pull (49,884) + 1 at the same frame target — the freeze *is* the pull, algebraically. rtf 2000: the pull still binds the disease (866/871 ms); under the cure the scan becomes the measured successor wall (38.8 ms worst item, p99 35.6). 40 s wall: pull still dominant.

3. **The cure is what it claims.** `ES_ROOT_STREAM`/`naive` code lines byte-identical to ee4d's committed gold patch; the probe is print-only; cure collapses 3e5 to 15.8 ms with root pulls drained to 0.

4. **Honesty held.** P1/P3 failed on their letters under pre-registered failure-handling clauses and are reported as failures — the disqualifier (failure reported as held) does not apply. Exact ms drift with load (805→871) but every count and attribution ratio is stable across three independent generations.

I corrected the author's wiki page with two checker2 notes (domain extension; the cure-at-rtf-2000 scan wall), restored the tree to base, and left nothing running. One disclosure: my 40 s arm peaked at 3536 MB footprint — it completed, and nothing in the grade hangs on it.
