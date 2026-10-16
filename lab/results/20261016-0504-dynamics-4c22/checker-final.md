Working...
Check complete. Verdict: **silver**, written to `lab/results/20261016-0504-dynamics-4c22/check.md`.

**What reproduced (runner's regen + my own flights on the applied patch):**
- Every event number in the dossier's table (334/136 → stagger 260/136 → phase 53/25; N=0 floor 51), and the OFF-arm digests bit-equal the frozen record `artifacts/runs/nladder/ladder_digests_newpop.txt` (P5).
- Adversarial, beyond the author's domain: **N=10⁵** (a decade out) has identical stats (p99 136, max 240, ev/gs 5.82); at **12,000 game-s** the comb's max 334 recurs (standing) and the phase collapse holds (53/23), with the overhead decaying to **+10.8%** (the +19–41% is front-loaded stubs); **burn** storms too (max 328). Mechanism verified in shipped code: `aligned` anchors to the absolute grid (`t.rem_euclid(step)`) while `plan_clock` chains — beats at exactly ~330 game-s.

**What broke (why silver):** the patch's `ES_ATTRIB` instrumentation is duplicated — two `take()` pushes per frame, so row *i* reads frame *i*/2's counters or drained zeros (proof: 186/186 attributed rows are even-indexed). With a deduplicated build the worst-12 storm frames are **~93% Home-doll items** (k26–32, b135–197; unattributed ≈ 12.7, not ~146). The dossier's "pull lane / one population, two delivery lanes" reading and P4's revision are artifacts, wrong by ~10× — the corrected reading makes the comb claim cleaner, but it invalidates a load-bearing evidence sentence. I corrected the three overstatements in the author's `wiki/nladder.md` in place, marked `[checker]`.

Gold path named in check.md: re-fly attribution with the two-line instrument fix and amend the dossier paragraph; adoption still needs the B13/B14-class legality rung the author already flags. Tree restored pristine; no commits made.
