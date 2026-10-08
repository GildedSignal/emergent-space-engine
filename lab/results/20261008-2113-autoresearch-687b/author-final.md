Working...
Deliverables complete: `dossier.md`, `predictions.md` (written pre-measurement, outcome appended), `log.md`, `patch.diff` (163 lines), all in `lab/results/20261008-2113-autoresearch-687b/`; gates 11/11 on the delivered sources; no commits made.

**Claim:** the galaxy readout's per-sample cost (splat = 94% of the frame) is not scalar-arithmetic-bound — an exact reciprocal division in `locate` plus an f32 projection hold every frozen gate and buy a paired median of 0.93× (range 0.87–1.01 over seven held-out cases incl. single-thread), so the real levers for the billion-ship readout are sample batching per compiled orbit, image tiling, or a GPU splat, not scalar micro-optimization.
