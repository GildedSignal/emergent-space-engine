Working...
Check complete. `check.md` written; tree restored (patch and my probe binary removed; only untracked `lab/results/` remains, as found).

**Verdict: silver.**

**Reproduced:** all 8 stored scenes byte-identical (timings masked); the missing control `c0` re-run matches its dossier row exactly (enc 234, λ̄-rank 28/p90 16, 61.1% >4, k̂ 50.6, missed 5/234); `taleb.rs` verified byte-identical to the gold's original patch, and `taleb adj` reproduces the gold's numbers exactly (197 disputed / 4 missed-true / 193 extra-true / 0 false / rank_max 4; brute found 40 of 233). `predictions.md` (06:24) predates all outputs (06:34+).

**My decisive attack:** `circ_rank` sorts raw `mean_anomaly(t)+ϖ`, but `mean_anomaly` wraps to [0,τ) — with ϖ spread the values split into two blocks at the M-wrap and cross-block ranks inflate by up to the block size (proof: a pair with true modular separation 3.3e-5 — sub-spacing — measured at rank 73). Corrected modular ranks: **the control scene is unaffected (28/16/61.1%, identical)**, so the headline refutation of the gold's rank-4 premise is exact; but w1's true max is **59, not 99** (p90 32, not 92), s5's is 39, not 99, and the "circular maximum at apsidal spread" sentence and the rank-99 worst-pair narrative are artifacts. All fractions >4 (90–100%) and the entire k̂ cost analysis (wrap-based, clean) survive.

**Further adversarial results (all strengthen the claim):** seed-40 control 76% >4; a-spread 100× makes the watch *costlier* (k̂/n_c 0.383 vs 0.254 — the author's guessed rescue direction is the opposite); nc=1000 confirms k̂/n_c scale-free (0.286 → the 3.6 GB correction stands) **and breaks the gold's own metric** (distance-rank max 10, true-longitude max 11); windows stay sound to e≈0.5.

Silver rather than gold because the evidence table's ϖ-spread maxima and one headline sentence ship inflated numbers from an uncaught instrument bug — in a run whose thesis is exactly that artifact class. The one experiment to gold: the one-line modular-ranking fix and a restated table (my corrected values already confirm every conclusion).
