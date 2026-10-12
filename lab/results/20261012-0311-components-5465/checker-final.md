Working...
Check complete. **Grade: silver** — written to `lab/results/20261012-0311-components-5465/check.md`; tree restored to clean, no commits.

**Reproduced exactly** (both dossier paths, 10.5 s / 0.08 s): 5,186 B/body, 54/54 distinct entries, 663/663 distinct exact keys, 45 quantized cells (0.932), and `--example plane -- 100` → 2,349 B at 29 kicks. Pre-registration holds on mtimes (predictions 03:22:48, output 03:26:41), misses disclosed.

**Four adversarial cases ran:**
- **A1 (decomposition):** the dossier's 58%/12%/29% table mixes denominators (catalogue-per-alive ÷ plane-per-71). Consistent split under the plane's own accounting: compiled trajectories **79.6%**, history segments **10.7%**, fat+plan 9.0%.
- **A2 (cache claim):** extended to **all 50 Cycle entries including dead** — bit-identical recompiles, ~32 µs each (the deferred eviction trade was one line to bound).
- **A3 (growth):** steady state confirmed — bpb *falls* 5,697→4,786 over 300→1,800 frames, slots recycle.
- **A4 (scale/regime):** 200 members → 208/208 distinct entries, bpb 6,192; Dense order → 5,204. No scale rescue, no sharing.

**Biggest author miss:** dead bodies are charged "17 × 448 B" but actually retain their last compiled entries — **9,018 B each, 41.6% of the whole store**; the census instrument never walked them. The deletion opportunity is understated ~20×, so the errors weaken precision, not direction.

**Why silver:** headline, regenerability, zero-sharing, steady state and the 240-B floor arithmetic (Residual 64 = `[i128;2]×2`, carry 16, ShapeKey 24 — verified in code) all reproduce and strengthen; but the 26× cut is asserted not flown, and the central table needed checker correction. One experiment to gold: fly the eviction + dead-freeing + SoA repack behind the `BodyStore` seam and measure the flown bytes/body.
