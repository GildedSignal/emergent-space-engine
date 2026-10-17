Working...
Check complete. **Grade: gold** — written to `lab/results/20261017-0428-quant-c439/check.md`, with one correction applied to the author's `wiki/promotion.md`.

**What I did:**
- Applied `work/patch.diff` at base `df0386d` in a clean tree, built plain and prof binaries, re-ran the arms. Every load-bearing number regenerates: scan candidates **148,996 identical to the digit** at N=1e4=1e5, totals 188,249/188,245 (author 188,181/188,227, wall jitter), plain=prof digest `d1822b88…` (and the digest hashes full orbital state, so inertness is proven, not assumed). The untagged "other" bucket printed zero — the reader attribution is exhaustive.
- Three adversarial cases, all confirming: **N=1e6** (a decade past the author's domain) holds O(1) — 148,492 candidates, 70.2/scan (side note: 2.31 GB RSS); **seed 2** identical at both N (188,142; 88.4/scan — near-set size is realisation-dependent); **the wave at N=1e5** (author flew it only at 1e4) — reads/event holds at 4.69, and the window yields **10.1 reads/body/20k gs, independently landing on 8792's 11.48**, closing the reconciliation with direct measurement rather than the author's composition.
- Novelty verified: no prior engine-store read census (8792's counter rode their retention patch; 3294 counted kick sites; view's 649c is the view gather). The run refutes promotion open direction 1 as stated and corrects the 10⁹ memory re-ranking — a premise shown wrong, at zero adoption cost.
- Predictions discipline held: the decisive P2 was refuted by its own pre-registered kill criterion and reported as the result.

**Page correction:** the "dwell cliff's hot set is the scan's near set … deletes at any scale" claim was an inference (census and cliff never flown together), now marked as such with the seed-2 caveat. **Noted misses:** the imported 1.7e-5 kicks/body/gs rate conflicts with kick-cadence's two-combs finding (~4× understated, same conclusion), the wave window's budget truncation, the unflown pin↔cliff link, and a 0.06%-vs-0.10% arithmetic nit.

Tree restored to base; nothing else in the run folder touched.
