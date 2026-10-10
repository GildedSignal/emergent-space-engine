Grade: gold

**Abstract.** Second-author completion of silver e9a5: all four named defects closed on a record that regenerates. Reproduced bit-for-bit (`python3 probe.py`, 16 s, 618 MB; rerun byte-identical, env diff only). Cold belt at belt density: 40.29 raw / 41.74 corrected bits → 5.2/7.8 GB at 2/3 dof — does not break 8 GB; the 47.9 figure indeed belongs to Σ×2500 ∧ cold (confirmed in the parent's stored metrics). Estimator bias measured +1.453 ± 0.015 bits, all absolutes corrected. Time fixed (16 384 orbits = 534.5 real-years at 100×). Churn 375.4/orbit = 6 076 events/frame. My attacks: correction robust to non-Gaussian tails (≤ 0.4 bits against a 1.4-bit margin); kernel stable ±0.4 % to grid/cutoff; 100× colder σ₀ leaves H unchanged. Adoptable now: the q_v octave rule and churn budget quote corrected digits.

**Reasons.**

*Reproduction.* Clean tree, empty `work/patch.diff` (no repo edits). `python3 probe.py` in a scratch copy: every headline digit regenerates exactly (belt 35.7138 corrected; cold_belt 40.286/41.739 → 5.217/7.826 GB; cold_dense 47.906/49.359 → 9.255 GB; bias 1.4533 with all 24 trials in [1.4239, 1.5015]; floor triple ±1.1 %/±0.8 %; churn 375.364 → 3.645×10⁻⁶/game-s → 6 075.76/frame; 53 454 game-yr / 534.5 real-yr; reabsorption 99.99997 %; last-octave slopes 0.995/1.007/0.735/0.651). Second rerun byte-identical (same md5); peak RSS 617 932 KB, wall 16.2 s — inside every budget. Controls still pass and the impulse-only negative control still fails at 14.56×, so the kernel check can fail. Cold Σ-linearity is exact (443 357.73/2500 = 177.3431). GB arithmetic exact (8 GB = 64 bits at 10⁹).

*Predictions.* `predictions.md` (−3 m) precedes probe.py's last edit (−2 m) and metrics.json (−1 m); run.log empty, mtimes are the order evidence. All six held numerically, including the kill directions ("if above 42 bits the claim needs weakening" — it came in at 40.3).

*My attacks (all inside stated margins).*
1. **Bias robustness on non-Gaussian marginals** (the correction was calibrated on Gaussians): through the exact pipeline, a t³ product errs −0.13 bits and a 98/2 ×8-sd mixture — far heavier-tailed than any epoch here — errs −0.37 bits. The tightest call in the table, cold_belt at 3 dof, has a 1.4-bit margin: holds.
2. **Grid and cutoff sensitivity**: λ⁺ and D_weak move ≤ 0.4 % across 2 000–16 000 bins and BMAX ×0.5–×2; σ-growth is above-floor-variance dominated (sub-floor share ≤ 0.1 %), so the physical cutoff is not load-bearing.
3. **Colder extreme** (σ₀ = 10⁻⁴, 100× colder): σ@16 384 = 0.4682 vs 0.4674, H = 41.77 vs 41.76 — the cold-belt result is σ₀-independent in the self-limiting regime; the claim strengthens with cold.
4. **Finer floor q = 10⁻⁷**: belt churn 52 942 events/frame — "churn binds, not memory" confirmed in the direction that hurts.
5. **Cross-check against the parent (git e1675df)**: the parent's coldswarm raw H = 47.890 = Σ×2500 ∧ σ₀ = 0.01, confirming the misattribution story; the refactored `shape_entropy_H` is bit-equal to the parent's inline arithmetic on identical inputs (verified directly), as claimed.

*Novelty.* The parent silver was the first H_live measurement (HANDOFF:70 "not measured yet"; plane.md:36). This run adds no new physics and says so; it converts that silver's record into an adoptable one and closes the one open scene (cold at belt density). Distinct from components-98bc's 0.126 bits/body static program and r2's carry widths.

*Goal fit.* Board focus "fitting 10⁹ in 8 GB … decided by distinctions created per game-second". The completed record says the store never binds for smooth scenes (memory ≤ 7.8 GB at 3 dof, worst cold case) and churn does (6.1 k events/frame at q_v = 10⁻⁶, ∝ 1/q_v) — which constraint binds is itself the finding. PRINCIPLES 24 ("the memory floor is information-theoretic") now with a declared estimator; PRINCIPLES 10 ("Measure before claiming"); "A test that cannot fail is a control" honoured by the still-failing negative control.

**The one experiment (if silver were in play): not needed.** What remains open is stated by the author and inherited, not introduced: the resonance/Lyapunov channel is argued, not bounded — B18b's rung should pin the resonance fraction.

**What the author missed.**
- P1's mechanistic sub-number (σ_resid ≈ 1.5–2.5 m/s) missed by 4× (0.466); "all six held" is true of the falsifiable headlines, and the regime conclusion survives (σ_resid = 47× σ₀), but the dossier does not report the sub-miss.
- The decisive predictions were anchored on the parent checker's published numbers (40.3 bits, 1.46 bits) — disclosed in predictions.md, inherent to the second-author role, but P1/P2 therefore test reproduction more than foresight; the 4× σ miss is the honest blind part.
- Growth tables are not RNG-stream-identical to the parent's (the new bias calibration consumes draws first): σ differs by ≤ 1.4 %, pure MC noise, harmless and unstated.
- The dossier's PRINCIPLES-6 framing (sub-floor accumulation) is where churn's small term lives (≈ 20 of 375 mutations/orbit), but σ and H growth are above-floor-variance dominated (≤ 0.1 % sub-floor); the mechanism paragraph could say so.
