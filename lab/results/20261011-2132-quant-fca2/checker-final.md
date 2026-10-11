Working...
Check complete: `lab/results/20261011-2132-quant-fca2/check.md` written, grade **silver**, tree restored to clean (patch reversed, nothing else in the run folder touched).

**What I did:**
- **Reproduced** from a clean tree: applied `work/patch.diff`, rebuilt (35 s), reran A/B/C/D. All headline numbers regenerate within shared-machine noise; digests bit-identical at M=48/500/2000 (`09e40859`, `fde83535`, `b0fe6088`); leak quarters, gather share ~0.60, contact batch 49.4 ms at frame 1, 0 hitches to rtf 10⁴, digest invariance across pacing/budgets, paced 3.5× unpaced — all confirmed.
- **Four adversarial cases:** M=1000 brackets the crossing (p99 18.8, 41 hitches); the **paced** crossing the author never measured (M=500 paced 14.0 / 0 hitches, M=1000 paced 25.9 / 428 hitches — M* ≈ 750 holds as flown); a determinism probe (identical digest, but `bodies`-at-end is wall-time dependent — the "96% handed out" figure is approximate); a burst re-measurement (the +6% burn figure is inside noise; only "no hitch" survives).
- **Novelty:** capacity M*, readout dominance, the leak, and the batch claim are new against H0200–H0215/board/lenses (the 6.7 µs per-readout cost and H0210's p99 were known).

**Why silver, not gold:** P1 — the central held-out prediction — failed (~10× off on the crossing, wrong breaker stage), and P4's number doesn't survive re-measurement; by the grade's letter and the 1 October precedent that caps below gold. Everything claimed reproduces, the foundation-7 violation is measured and quotable, and the one experiment to gold is a pre-registered second round: paced M* and stage shares across seeds plus the memory attribution the run leaves `[INFERENCE]`.
