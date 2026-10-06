Working...
Check complete. **Grade: gold** — written to `lab/results/20261006-1249-taleb-e013/check.md`, nothing else in the run folder touched.

**What I did:**
- **Reproduced** the full ladder from `probe.py` in a clean /tmp copy (patch.diff is empty): every statistic in all 13 cases plus the nest check identical to `all.log` and the dossier table, field by field. Only wall times differ (shared machine).
- **Verified the extrapolation arithmetic**: μ̂(10⁶) = 7.2 from the measured μ̂/n = 7.0–7.5×10⁻⁶; raw Poisson tail 84% at k=4 (the 94% headline is calibration-dependent, but "misses most" is robust); p99.9 → k ≈ 17; store 1.15 GB vs the gold's 0.29 GB.
- **Four adversarial cases of my own**, all confirming: fresh seeds (X1 at 256k: 17.0–18.9% missed; C3c: 3.3%); random-vs-first rank subsampling (the author's 2500-cap is unbiased — 17.0% vs 18.9% — but he never flagged or tested it); S=256 resolution check (3.8% vs 3.4%); a 3D inclination variant (his declared blind spot: contacts thin 33× exactly as he asserted, yet the λ-rank hazard persists at 2% while dist-rank collapses to 2 — confirming the interloper mechanism).
- **Novelty**: no HISTORY entry covers the train's k-scaling; the target gold was adopted this morning (board taste log); nearest records are H0212 and the board's top scaling risk, which this answers for the train.
- **Predictions**: the anchor reproduced the gold's own result first (no strawman); load-bearing predictions held (linear μ̂, miss emergence, X1 at 17.7% just above its registered band); the failed bunching mechanism and the over-predicted D magnitudes were disclosed honestly.

**The one gap**, named in check.md: the radial-phase strata repair is stated, not tested — that is the next run, converting this premise kill into the replacement certificate.
