Working...
**Grade: silver** — written to `lab/results/20261007-2057-spacex-de6a/check.md`.

**Reproduction (exact):** applied `work/patch.diff` on a838a28, reran all four bench commands — digests, cut ticks, event counts and every entropy digit match (s7's "1,464" in the dossier is 1,465, a transcription slip). Clean-build digest `29f440d6…` independently verified identical to the instrumented runs; 10/10 lib tests green; tree reverted after.

**Adversarial finding (the one that matters):** a horizon sweep at 200/400/1600 game-s shows carry0 bits/event = log₂(kick_events/K) with K ≈ 24 constant across all seven runs — the carry histograms are saturated (every delta distinct). So the 77%-of-bits carry number is a horizon-dependent lower bound growing toward the register width (~32 bits/kick), not a stable rate; the author's "~2⁴·⁶ distinct values" reads saturation as bounded support, and "57 GB/hour is an upper bound" has the bias direction wrong. The memory verdict (quiet 10⁹ breaks 8 GB ~7×; active fraction and reabsorption decide) survives both estimator biases.

**Also found:** the pre-registered kill criterion (funnel counts vs dashboard within 1%) fired at 0.34% — the author disclosed the numbers and honestly rescoped to the sparse order but never invoked it; code confirms `resolved` counts fleet steps that bypass the `apply` funnel. And "boundary crossings store nothing" is a word-list artifact: the instrumented five words omit `b.doll`, the one field a boundary changes.

**Gold path:** instrument the dense order's contact carries plus a horizon-invariant rate definition — that yields the scene's actual H_live, which `docs/plane.md` requires and still lacks.
