Working...
Check complete. **Grade: gold** — written to `check.md`, with two surgical corrections applied to the author's proposed `wiki/nladder.md`.

**What I did:**

1. **Reproduction** — re-ran the decomposition independently from the regen CSVs: every era count exact (kick/boundary combs 105,780/5,924 … 102,949), arrivals bit-identical to 0a46's record (crest bins 0.400/0.717/0.415/0.702… to the digit), coast payload split 45.6 µs/kick vs 8.58 µs/boundary, player class flat (387±1 items, 0.46 s/era), anchor 822–906 inside the 811–948 family. Walls/freeze sizes are disclosed shared-box draws.
2. **Code verified** — step.rs:717-718 does insert the boundary at `t+full/2` and the kick at `t+full` (the half-period payload offset is bit-structure); universe.rs:770/:802/:975-980/:1008-1010 match the dossier's accounting and the killed H-latch.
3. **Four adversarial arms, three outside the author's grid** — seed 2 burn (nested freeze 735 ms, same alternation); coast to 120k gs, double the flown duration (split holds 4.3× through all eight eras, player flat, no decay); N=2e4, below every flown grid (comb + nested crest hold, freeze scales with K); and a per-frame least-squares decomposition of coast (43.9 µs/kick vs 5.7 µs/boundary, R²=0.93 — burn's cn2 refuses the same fit, confirming the two-channel structure).
4. **Predictions** — self-refuting bars (P2 main branch dead, P3's concentration and wall-equalization failed as reported) argue genuine pre-registration; the failures carry the finding.
5. **Page corrections** — "IDENTICAL stream" → "IDENTICAL kick stream" with the disclosed −2%/−13% in-window events (deferred first boundaries), and "46% of stream events" → ~50% (regen: 49.7%/50.7%; the dossier's figure understates, decision-neutral).

The run inverts 0a46's mechanism attribution (payload, not path), flies the previous checker's named gold experiment whole, and leaves a one-step adoption: birth stagger ≥ one comb width (freeze 718–1231 → 40.6 ms, −17% wall), with payload interleave or boundary-comb deletion as the named open direction — topic stays open.
