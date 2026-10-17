Working...
**Grade: gold** — written to `check2.md`, with the author's `wiki/promotion.md` corrected in place.

**What I did**

1. **Reproduced**: the runner's regen pass (exit 0) regenerates every dossier number — 68/540 over frames at 0.6% scan / 98.6% comb (seed 1), p99 frames 98.7% comb, worst frame `ev=1002` comb 43.8 ms vs scan 0.24, digest `4916c14e…3172` identical to 0552's, census md5 identical ×3, channels close to ≤1.6% unaccounted. Applied `work/patch.diff` myself in the clean tree, rebuilt (12 s), confirmed the binary.

2. **Predictions**: `predictions.md` (18 m) predates the decisive flights (13→8 m); P1–P4 held with margin, P5's failed half is reported by the author, not hidden.

3. **Four attacks, one beyond the tested range**:
   - **K=2×10⁴** (decade past the author's 10⁴): over frames 0.7% scan / 95.1% comb, worst `ev=20,002` comb 923 ms, pin 43×20,039×216 B ≈ 186 MB (∝ K), hwm 932 MB — the trend extrapolates exactly.
   - **Seed 5**: 68 over, 97.7% comb, per-answer 4.41 ms — class holds; but placement 72% and held_max 54 broke two page universals ("88–95%", "≤ 26") → corrected the page; tail claim untouched.
   - **rtf 25**: over count 68→21 but the whole wave still lands in one frame (`ev=1002`, comb 54.1 ms) — the wave is birth-phase-locked; folded into open direction 2.
   - **200 beside a 10⁵ belt, seed 2**: 0 bails, 453.5 candidates, tier stays off — pair-dependence confirmed on the second seed.

4. **Novelty**: nothing on the published page, in HISTORY, or in nladder's per-frame attribution (different population) anticipates the split or the inversion; the scan-queue/69f3 priors are cited. This is the exact experiment 0552's checker named for gold.

5. **Fit**: answers the board's top question (which term breaks first as the plane grows) for K = 200→2×10⁴, kills 0552's SCAN_BACKLOG mechanism, and deletes a wrong next step at zero build cost — PRINCIPLES 12 and 19 both on point.

No commits, nothing else in the run folder touched; my probe outputs live in `/tmp/check2/`.
