Working...
Check complete. **Grade: silver** — written to `lab/results/20261010-1407-constraint-775f/check.md`; tree restored (patch reversed, only untracked `lab/results/` remains; no commits).

**What I did:**
- **Reproduced** from a clean tree: applied `work/patch.diff`, rebuilt release, reran the dossier's commands. Readouts identical (69.24 and 288.9 vs 289.3/frame), gather share 63%/55%, engine p99 pinned at its 5 ms budget, rtf lowest-1% = 0 at 415 bodies, galaxy render 30–43 ms median with 60/60 frames over 16.7 ms in all three views. Slope 8.9 µs/body/frame (author 7.4) — same order on a shared box.
- **Verified the structure in code**: `view.rs` walks `0..n_bodies()` uncalled-for-cull, no budget; the HTTP server runs the same `Session::step` loop.
- **Adversarial cases**: `--members 1600` (the prediction's own unreported largest case) and a 40 s run — body count saturates at 415–428 under every knob, so the "ceiling ≈ 2,200 bodies" is an extrapolation the shipped bench cannot reach, and prediction #3 is untestable on it. Galaxy bench reproduced.
- **Novelty checked**: H0210 already recorded "the view gather is 83% of a light frame", and the lens brief knew the cost grows with N. New here: search-vs-readout decomposition, the budget asymmetry, the galaxy quantification.

**Why silver, not gold:** reproduced and real, but the directed lens (`b-readout-cost`) asked for a build with gates improving; this run delivers a measurement that redirects it. No 10× delivered, nothing deleted. The gold experiment: the budgeted/amortized gather itself, on a bench that can grow bodies past ~430.

**Named misses:** the body-count saturation undisclosed; engine unit costs quoted from ambient-loaded runs beside clean gather numbers; "B15" mislabeled (it's the frozen galaxy gate, not the readout queue item).
