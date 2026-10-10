Working...
Check complete. `lab/results/20261010-0920-quant-30e1/check.md` written; tree restored (only untracked `lab/results/` remains, as found).

**Grade: silver.**

What I did, in evidence:

- **Reproduced from the patch** on a clean tree: seeds 1 and 23 give bit-identical op counts (add 992 / mul 1011 / div 254 / sqrt 46 per leaver kick), panel counts (~182), memo counts (0 of 5,438 exact reuses, 246 quantized shapes = 22:1), and both digests; medians within noise (87.7 vs 87.8 µs).
- **Held the author's control to the fire:** reverted the patch, rebuilt the unmodified binary — digests identical, so the counters provably watched identical work; instrumentation overhead ≈8% (80.8→87.7 µs), under the pre-registered 1.5× kill line.
- **Whole-plane cross-check on unmodified code:** engine 31.8%, view_gather 53.6%, player 2075 µs/item (31.5× a ship), 2067 events/s — all match.
- **Three adversarial cases** (4× density, sparse, near-idle): compile-per-kick, 0% exact reuse, and op scale all hold; leaver median is workload-dependent (113.6 µs sparse) — orders of magnitude only, as scoped.
- **Predictions:** written 9.5 min before the decisive runs; P5 verified on the held-out JSONs myself.

Why silver, not gold: the headline mechanism ("~80% is memory churn") is inferred, not measured — i128 panel arithmetic is compute wearing churn's clothes, and the stage timing covers only 8.8% of made samples and 0% of the dominant leaver path. Also "bound = 1.00/kick" is actually 0.963–0.983 on leavers. The decision input (counted arithmetic <20% of the event; the jet is the per-event lever) survives all of this. The gold experiment: instrument the leaver path's stages plus allocation/key-search-vs-i128 counters inside `bound` — one build, one 15 s run. Novelty is partial by the author's own framing: exact-memo-0% was known (H0213); the event-interior pricing and the player-event price are new.
