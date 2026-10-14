Working...
Check complete. **Grade: gold** — written to `lab/results/20261014-2012-dynamics-71b4/check.md`.

**What I did:**

1. **Reproduced bit-exact.** Cold rerun of the decisive rows (A_K16, A_K32, Q_q0.0005, C_th0.5) with the shipped `harness2.py` in a clean tree: `dser` arrays identical to the stored npz (max diff 0.0) — this also resolves my one timeline concern (harness2.py was edited at 20:28:07 *after* the clock controls ran; the edit provably didn't touch those paths). `held_A8` slope 0.818 replicates: machine 1's clock compounds, which is the crux of the "524e artifact" claim. The convergence-ratio claim regenerates fresh (3.13/3.61/7.34).
2. **Predictions.** `predictions.md` (20:26:58) precedes the decisive batch (20:27:11–20:36:52); P1–P5, P7 held, P6 honestly reported as not fired.
3. **Four adversarial probes, all confirming the kill:** seed 777 (trigger walks 0.511, clock 0.000), horizon 800 (trigger 0.668, clock 0.024), the author's own named escape — sigma-delta remainder variant — still walks at both sensor rates (0.935 / 0.308), and the convergence-convention probe.
4. **Novelty.** The live wiki page names this exact experiment as the one that decides contradiction #3; open direction 4 priced the trigger as the standing exception. Premise shown wrong, adoptable in one step, zero cost.
5. **Page corrections** (author's `wiki/kick-cadence.md`): restored the dropped "regime-aware and coarse" summary paragraph (it held the branch-sweep note and three off-page runs) and restored 524e's Runs line to its original append-only text — the refutation already lives in Refuted/Contradictions. The new result paragraph matches the evidence number for number.

Nothing else in the run folder was touched; no git commands run.
