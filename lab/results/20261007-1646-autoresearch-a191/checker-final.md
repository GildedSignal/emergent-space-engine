Working...
**Grade: silver** — written to `lab/results/20261007-1646-autoresearch-a191/check.md`. Tree restored to clean baseline.

**What I did:** applied `work/patch.diff` in a clean tree, built base/patched/prof-free binaries from one target dir, interleaved A/B on 7 scenes (the dossier's 4 plus adversarial members 200, members 4, rtf 10×30 s), profiled with `EMERGENT_PROF=1`, ran both test suites, checked file-time order of `predictions.md`, and searched HISTORY/docs for novelty.

**Findings:**
- **Physics claim verified:** `proper0` is provably the same decode at the same event tick at all four `Binding` construction sites; the canonical digest hashes `r.proper` (the accumulated τ), so digest equality is a real gate. Replay + canonical digests bit-identical on all 7 scenes, `refused` 0, 18 suites / 104 tests green, `u_tau2` collapsed to 0.0%.
- **Timing reproduces — only with the diagnostic scopes stripped:** made −17…−19%, leavers −6…−10% (matches the claimed −16…−21%/−6…−11.5%).
- **The gap that caps it at silver:** the shipped `patch.diff` has always-on per-panel prof scopes (~350 guard drops/kick: `quad` 189k, `weak_quad` 173k, `node` 115k calls per 10 s). As shipped, base vs patch = made +2%, **leavers +9–12% regression** — the dossier's commands run verbatim do not regenerate its headline numbers. The A/B must have held the scope overhead common-mode, which the dossier doesn't state.
- **Below the gold bar regardless:** 1.1–1.2× per-kick, no component deleted, no premise killed; the measured 60–66% compile wall confirms the adjudicated memo story rather than overturning anything. Predictions held (one disclosed miss); novelty clean against all H entries.
