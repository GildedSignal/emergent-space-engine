Working...
**Grade: gold** — written to `lab/results/20261006-1249-taleb-e013/check2.md`.

**What I did (30 min, run folder untouched, scratch cleaned):**

1. **Reproduction, exact.** Copied `probe.py` to /tmp; all 13 cases + nest check regenerate `all.log` bit-identically (X1: 2,109,763 encounters, μ̂ 1.83, miss(k=4) 17.68%, dist_max 11). `work/patch.diff` is empty — no tree edits to apply. predictions.md (13:08) predates the final run (13:20); the mid-run amendment's C-numbers match the deterministic regeneration.

2. **Five adversarial cases, all supporting the claim:**
   - **Fresh seed at new n=64k**: μ̂/n = 7.42×10⁻⁶ — dead on the author's 7.0–7.5×10⁻⁶ line; miss 0.4% between its 51k/128k neighbours. The scaling law holds out-of-sample.
   - **D3 fresh seeds ×2**: 21.4%/22.5% λ-rank misses, dist_max 20/16 — the formation kill at the gold's own n=800 is seed-robust.
   - **Full-ranking run** (all 6,351 vs capped 2,500 encounters): 23.3% vs 22.6% — no rank-cap bias.
   - **C3c + X1 fresh seeds**: 3.52% and 18.2% vs author's 3.4% and 17.7%.
   - **Tail arithmetic**: the "≈94% missed at 10⁶" is a point on a band — compounded-Poisson gives 65% (and underpredicts every measured point), plain Poisson 84%; every model says "most". Honest k(p99.9) ≈ 20–26, so the ≥1.1 GB store claim is conservative in the attack's favour.

3. **Why gold, not silver:** the premise kill is direct, not extrapolated — the gold 09b5's measured basis ("every real encounter within partner rank 4 along the orbit", with store arithmetic baking k=4 into the 10⁶ scale) is falsified at its own n=800, in the train's own trigger regime and rate gate, for **both** rank readings, so the absent binary/semantics ambiguity doesn't rescue it. Novel (no HISTORY entry). Adoptable in one design line before the encounters design freezes.

4. **Named in the report:** two undisclosed prediction misses (C0/C1 encounter counts; "distance-rank ≤ 6" broken at 23), the missing nest check at S=128 where it matters (grazing encounters likely under-sampled — misses plausibly *under*estimated), the unexamined resort cost from epicycle wobble (~40 slots wide at 128k — a second way O(n·k) fails), and the untested radial-stratification repair, which is the natural next run.
