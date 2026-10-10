Working...
Check written. Summary of the verification:

**Grade: silver**

**Reproduced (clean tree, /tmp):** all three simulation commands (`cadence.py A`, `cadence.py B`, `exp2.py`) rerun **bit-identically** to the stored npz files. `analysis.py`, `exp2_analyze.py`, `conv.py` print the dossier's numbers. Numbers no shipped script prints (B histogram `8:1235…256:162`, 6.81x; C `8:1526/16:10`; zeta-strata 2.27→1.01) recompute exactly under independent re-derivation.

**Discrepancies found:**
- exp2 "honest pooled savings 4.4x" → actually **2.7x** (8000/2960); the error overstated the scheduling lever — the correction strengthens the author's own kill branch
- Belt A is **2048** bodies, not 1024
- FTLE "shear" formula is **44× off** (predicts 0.30/yr, measures 0.0069; lambda nearly flat in a). The payload survives though: medians identical at μ and 3μ (ratio 1.00), so the instrument genuinely doesn't read chaos
- C's FTLE number was absent from the stored analysis.json (file landed after analysis ran) but regenerates — timing gap, not fabrication
- Base-prediction pre-registration unverifiable (mtime 18:28 > ladder outputs 18:23–18:26); the exp2 addendum's pre-registration **is** timestamp-verified, and P8's failure fired the pre-registered kill branch as written

**Adversarial probes:** apsidal-precession tracking quantifies the e-metric's blind spot (p90 error 0.052 rad over 120 orbits at K=4, 0.017 at K=8 — a boundary on B14-class gates, not a kill); FTLE structure; bit-determinism.

**Novelty:** no HISTORY entry measures per-body cadence demand, scheduling ceilings, or a resonance-scalar ranker; H0190 measured kick counts, not sufficiency. Directly feeds queued q-cadence.

**Gold experiment:** re-derive K* under the plane's own frozen gates (B14 precession, B17) and the real orbit-averaged kick layer, on belt B and the NEAR set. Only check.md was modified in the run folder.
