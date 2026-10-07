Working...
Check complete. `lab/results/20261007-1801-dynamics-532c/check.md` written; nothing else in the run folder touched.

**Grade: silver.**

**Reproduced:** all three parts (`conjmap.py A|B|C`, clean copy) bit-identical to the stored JSONs in 21.6/27.7/17.5 s; `hit_B.npy`/`pairs_B.npy` replay exactly; file times put `predictions.md` (18:04) before every stored result (18:18–18:21); the empty `patch.diff` matches the disclosed unapplied patch.

**Independently verified (my own code, three adversarial cases):**
- χ_t < 1 for crossing coplanar pairs is exact geometry — 0 violations in 166,638 random asymmetric-e pairs (max χ_t = 0.99999).
- The leak and jitter, with my own Kepler propagation and conjunction anchor: radial leak 0.59–0.79 across cells (author: 0.68–0.92), dL std 2.39–2.61 rad (author: 2.00–2.53). The conjunction anchor is genuinely the wrong event anchor; the Öpik-leak magnitude at the deepest cells is construction-sensitive (mine 0.13–0.62 vs author's up to 0.95) — order of magnitude robust, exact value not.
- Sticky resonance is real, not an ε artifact: ε-stratified sticky rate 0.368 vs 0.035 at fixed ε band (10×), corr(small-q, ε) = 0.03.

**What failed my attack:** the −1.44 gap "power-law tail" is pure ε-heterogeneity — an iid Bernoulli mixture with the same per-pair ε reproduces the CCDF (−1.79 vs my dense-fit −1.80). Also the dossier prose contradicts its own stored table in four places (worst-χ_t direction backwards, unsupported 0.55 median, 1.9 vs 2.00 rad, ranges silently truncated), and P1 failed on magnitude everywhere it ran (41–95% measured vs 0.5–6% predicted) — the run's own χ_t finding explains why, but it should be named a failure.

**Why not gold:** the held-out record is mixed (P1 magnitude failed, P2 tail ratio failed, P3 magnitude failed, P4's decisive part never reached), and the decisive band — grazing χ_t → 1 where r8 v2's 0.5–6% leak actually lives — was never run. The one experiment to gold: add the grazing cells, weight a realistic belt population, use the corrected W (the shipped W≡1 statistic is broken as disclosed; corrected ν = W·ε puts 61% of this crossing population in the deep tier), and test the r8 v3 design's second-order window bound rather than its point anchors.
