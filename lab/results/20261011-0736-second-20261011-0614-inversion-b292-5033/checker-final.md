Working...
Check complete. **Grade: gold** — written to `lab/results/20261011-0736-second-20261011-0614-inversion-b292-5033/check.md`.

**What I verified:**

1. **Reproduction (clean tree + `work/patch.diff`)** — all 13 scene lines regenerate byte-identically (only wall-clock fields differ); `taleb adj` gives the gold's exact numbers (disputed 197, missed 4, extra_true 193, extra_false 0, rank_max 4; its λ̄-binned brute found 40 of 234); the previously missing b292 c0 line regenerates byte-identically from the **original** instrument (`orig-patch.diff` applied in a clean tree); the 8 stored b292 lines match their branch; `taleb.rs` is the gold's verbatim; the raw `ranks.lbar` column, watch and window fields match between fixed and original records on all 8 overlapping scenes.

2. **The fix is right** — `mean_anomaly` wraps to [0,TAU) (kepler.rs:73–76), so raw `m+ϖ` was circular-order noise that cut both ways (w1 99→59, s5 99→39, d30 94→98); `rem_euclid(TAU)` restores the ±k-watch invariant, and k̂/soundness were wrap-immune all along (code-read + raw-vs-fixed identity).

3. **Predictions** — mtime 07:42:50 precedes every fixed-instrument run (07:46:23+); all nine held, with the blind subset (w1b/w1c) holding on its ranges.

4. **My four attacks, all confirming:** seed 42 on both geometries (35/64.5% control, 71/94.2% w1 — third-seed robustness); ϖ span 2π (52/91.0%, the corrected ϖ sub-claim survives the extreme); a **fourth order metric** neither run measured — mean-anomaly rank, 97–99 max, 93.7–96.6% > 4 everywhere, closing the "no phase-order family escapes it" assertion with measurement; and the fleet arithmetic (11.6 TB = 29% of quadratic, 64 GB = 200× the gold's 300 MB).

**Missed (recorded in check.md):** predictions.md overstates which predictions were blind (the first checker had published c0b/aspread/n1k/e5 — the dossier labels them correctly); "90–100% > 4" vs its own aspread 88.7%; the mean-anomaly metric absent from the record; e > 0.5 untested. None change a conclusion.

Tree left clean; nothing else in the run folder touched.
