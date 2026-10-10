Working...
Check written. Verdict: **silver**.

**Reproduction (complete, bit-for-bit).** Clean tree, empty patch: all nine JSONs regenerate identically (`cmp`), `check.py` prints 23/24 with the same single FAIL (P2's constant, 5 vs 10–25); `causal.py` is byte-identical to the original run's and `run_a.json` matches the original branch's published record. Peak RSS 314 MB. Provenance holds: predictions.md (09:41) predates the decisive outputs (10:00–10:02), and reverting the one marked line regenerates exactly the disclosed first-pass exponents (−0.698/−1.003) — the instrument-fix history is truthful.

**Five attacks.**
1. **Seeds (17–20):** d1b flatline 99.7–100.0% of λ_agg·R_sub, zero rule misses, λ_agg/λ_tot = 0.68–0.71 — the headline law is robust; the twice-missed constant is honestly reported (5–10 across seeds).
2. **Coherent fleet on the real scene:** the fleet *does* surface (24 crossings at rq=sep vs 0 signed — P2 is signed-specific), but the bound holds exactly (127 vs 127, zero misses).
3. **Counter completeness:** analytic piecewise-linear crossing count equals the toy's publishes in all four cells — no undercount.
4. **Adoption rule vs its own ghost result:** aggregate ghosts at the shipped window `min(r_q_agg,R)` leave **568,310 unserved reads** on run E's own scene; window R serves all. The deliverable's rule contradicts its own experiment.
5. **Component count:** λ_agg(K) = K·λ_agg(1) (2.03×/3.01×/3.92×) — the author's named-but-skipped risk is real, linear, benign.

Plus an analytic confirmation: λ_agg/λ_tot = 1 − dx/(σ·R_sub) = 0.699 exactly — condition 2's floor is derived, not fitted.

**Why silver, not gold.** The boundedness thesis survived every attack, but the headline level (λ_agg·min(r_q_agg,R_p), "zero unserved reads") is measured with all sub-quantum readers excluded, while the run's own run E proves those readers load-bearing and needing window R — the honest parent chain is λ_agg·R_p (the 144× the dossier itself computes, mislabeled "over-retention for zero served reads"). One named experiment closes it: rerun d1b's parent chain under E's reader model and fix adoption rule 3's window.
