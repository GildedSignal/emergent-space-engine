Working...
Check complete. **Grade: gold** — written to `lab/results/20261011-0006-second-20261010-2314-taleb-6baf-2b8e/check.md`, nothing else touched.

**What I verified (all bit-exact):**
- **Record regeneration**: fresh `hlive.py belt_s1` identical to the author's; `metrics-regen.json` vs the original run's stored `metrics.json` differs only in `wall_s_max` — and the comparison is non-circular (runs5.sh's cp/mv preserved the original metrics before re-analysis).
- **The 10⁶-ship run, re-run in full (19 min)**: `live_frac_final` and every plug-in value bit-identical; the corrected `knn_final_full.k8` = −7.46257974627337 equals `_fix(stored)` to all printed digits — the headline 20.66 bits/ship stands. The disclosed ψ(N)−ψ(k) unit-bug correction is exact (recomputed from stored samples first, matched to 1e-4).
- **All 4000-ship k-NN values** recomputed exactly from the stored dumps; `hlive2w2048.py` is the documented sed; bandwidth arithmetic recomputed exactly (861 / 3.6×10⁴ / 1.8×10⁵ events/wall-s; the original's ÷RTF-instead-of-÷seconds error confirmed).
- **Adversarial**: held-out seed 7 reproduces every invariant (sweep ratios 15.2/16.0/16.0, secular 0.552, p99/med 4.04, tail 100% inner-band); the 2:1 resonance ring — the author's own unmeasured caveat — generalizes the secular floor (0.498/P_p) with a flatter tail, confirming the caveat's direction without breaking the claim.

**One real find the author missed**: `plugin()` (inherited from the shipped `hlive.py`) computes H_plugin + log₂(K/N) + Miller, not the plug-in — the quoted 18.99/18.22 should be 19.15/18.79 and "−1.7 bits undersampled" is −1.5. Conclusions survive; recorded in check.md along with smaller overstatements (k-stability 0.05 not 0.02, P8's range missed, a window mislabel).

Gold rationale: the first checker pre-named this experiment as the gold condition; it was done and exceeded (the checker's own stride-2 prescription was itself shown instrument-bound), the bandwidth premise is corrected by 3–5 orders, and adoption is design-inputs only.
