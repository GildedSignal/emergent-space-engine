Grade: silver

Abstract: Claim: on the flying plane the frame's constraint is the unbudgeted view gather, not the engine; ~90% of its output is unchanged per frame, so the first 10× is surprise-gated reuse. Reproduced bit-close: gather share 0.669 vs 0.694 paced (canonical digest identical), engine p50 0.047 ms and gather 0.721 ms unpaced (author 0.047/0.724); decomposition at 64/329/3778 entries gives 0.75/2.97/27.45 ms, 7.19 µs/entry, readouts ≈ entries, surprise 4.7/8.2/7.4%. Expected gain ~10× on the median frame, projected not measured. Cost: one seam (per-entry gate + gather budget). H0210 already had the gather at 83% of a frame; new are the post-cache decomposition, the surprise rate and the unimplemented foundation-7 budget.

## Reasons

**Reproduction (clean tree, patch.diff empty, verified).**
- Paced bench: shares gather/engine/json/wire 0.669/0.203/0.091/0.037 vs author 0.694/0.175/0.092/0.038; p99 frame 10.70 = 10.70 ms; engine p99 5.15 vs 5.24 (budget bites); 49 vs 45 overflow frames; **canonical digest identical** (`41343a14…`) — schedule-independent outcomes, evidence regenerable. Absolute paced medians differ ~4× (frame p50 1.07 vs 4.37 ms) under 7× lower load (0.16 vs 1.14); the author disclosed load and claimed orders of magnitude only. Shares and tails — the actual claim — reproduce.
- Unbudgeted bench: engine p50 0.0471/p99 1.30 ms, gather p50 0.721 ms (author 0.047/1.30/0.724). Exact.
- gatherbench 48/400/4000: p50 0.747/2.97/27.45 ms (author 0.744/3.00/27.75); entries 64.2/329.4/3777.7; readouts 70/290/2573; surprise 4.72/8.23/7.43%; slope 7.19 µs/entry; 11.5 µs/readout. Within ~1%.
- Kickbench: 35.1 µs median, exact memo 0.0, quantized 0.9449, replay digest equal.
- Code and doc claims verified: `session.rs:83-85` budgets the engine (`Budget::wall(engine_ms)`) then calls `gather_cached` with no budget; plane.md foundations 5 and 7 and the `view.rs` cache comment are quoted verbatim.

**Predictions.** mtime order: predictions.md 05:34:32 precedes the decisive gatherbench (05:35–05:40). All four held: readouts >60% → ~100%; slope 7.2 µs/entry; surprise <5% → 4.7% at members 48 (barely, 8.2% at scale); engine median 5–15× below gather. One discipline note: bench-unbudgeted.json landed 05:34:37, 5 s after predictions.md — a 20 s run, so it overlapped the final write; prediction 4 alone is exposed, and it is the least load-bearing.

**Adversarial cases (mine).**
1. Untuned scale members 1200: 1043 entries, p50 9.17 ms → 8.6 µs/entry; linear, no blowup. Surprise 10.1% — above the author's 4.7–8.2% band; >89% still unchanged.
2. rtf 400 (4× play speed): surprise **23.3%**. The deletable fraction is strongly rtf-dependent; the ~10× claim is scoped to rtf 100. "What would make it wrong" names quanta and the near field but not this.
3. Fresh seed 7: surprise 9.1% — same range.
4. Cold gather (no memo): 112 readouts vs 70 warm, 1.09 vs 0.73 ms — the H0211/H0213 cache is already spent; readouts dominate either way, confirming the decomposition and that deletion, not a better memo, is the remaining lever.

**Novelty.** H0210 (1 October) already records "the view gather is 83% of a light frame" and H0211/H0213 built the gather cache; the dossier's headline is qualitatively known and cites none of it. What is genuinely new: the post-cache decomposition (readouts ≈ 1 per entry, ~100% of gather), the 7.2 µs/entry linear scaling and the 16.7 ms breakpoint, the **measured view surprise rate** (no prior measurement found in HISTORY.md or docs), and the verified fact that foundation 7's gather budget is unimplemented.

**Goal fit.** Principle 3 verbatim: "Nothing is evolved that can be derived when looked at (clocks, redshift, views)"; principle 1, "the cheapest compute is compute not done"; smoothness is a board concern. It corrects the frame-level reading of the board's engine-side focus list. PRINCIPLES respected: pure read, no law or gate touched, honest cloud caveats.

## The one experiment that would make it gold

Wire the per-entry surprise gate (recompute when the crossing's Newton slope says the entry could cross a quantum, else re-emit) plus the gather budget foundation 7 mandates; show the observable view is identical (or lag bounded below a perceptible quantum) and measure the frame at members 4000 — the measured 10×, not the projected one. The author names this experiment and did not run it.

## What the author missed

- H0210/H0211 uncited: the constraint's dominance was known; only the post-cache state and the surprise rate are new. The dossier reads as a discovery.
- rtf dependence: surprise triples to 23.3% at rtf 400; the gate's deletion budget must be a function of the time factor. Not run, not named.
- "Breaks the 16.7 ms frame at 3,770 visible entries" is the tested point, not the breakpoint: by the author's own slope the median gather crosses 16.7 ms near ≈2,300 entries — less headroom than stated.
- The gatherbench player is passive (no scripted burns, unlike the xtask bench), so the surprise rate omits thrust-induced colour/shift changes; the rtf 100 shares matching suggests this is minor, but it is unmeasured.
- Predictions were written while the unbudgeted run (prediction 4's subject) was finishing — seconds of overlap; keep runs and writes strictly ordered.
