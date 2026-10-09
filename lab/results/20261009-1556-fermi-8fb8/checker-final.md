Working...
Check complete. `check.md` written to `lab/results/20261009-1556-fermi-8fb8/`; nothing else in the folder touched; no git mutations.

**Grade: silver.**

**Reproduced:** all 8 `mc_*.json` bit-identical in a clean tree (231 s total, every command ≤ 60 s); `size.py` regenerates the sizing table, the budget boundary (k ≈ 1.9×10³) and traffic numbers. Prediction discipline verified by mtimes (predictions 16:09 → script 16:11 → JSONs 16:11:53+); held-out seeds 2–3 confirm the growth laws.

**The headline survives attack:** H_A = 0.499·log₂k + 5.05 (analytic control exact), reabsorption real (gap 7.5–8.5 bits), and my extreme-tail adversarial (u_min = 10⁻⁶, ~1000σ₁ kicks) keeps slope at 0.532 — far from the 0.8 kill line.

**Why not gold — three record defects:**
1. **The 8.3-bit 2-D "correlation penalty" is an estimator artifact.** The author's H_A_2d = 16.717 for all k ≥ 2¹⁰ is literally the plug-in ceiling log₂(65536) + Miller–Madow. My independent control (ρ=0, separate counts) reproduces a spurious "penalty" of 8.40 bits; Kraskov k-NN on the author's exact processes gives true MI 0.313 bits (gauss; analytic 0.322) and 0.005 bits (rutherford). The author's P5 prediction was **right**; the "shared encounter-count latent" explanation and the "joint scar code saves ~2×" design consequence are unsupported — elements are near-independent.
2. **A control is misreported:** "no-program ≈ 11.0 flat (11.01–11.05)" — shipped JSONs say 11.04–11.83, rising ½ bit/doubling past k = 2⁹; P6 failed at large k but is reported as held.
3. **The multiset law is n-dependent** (H_M at k=2¹³: 4.55 → 4.07 → 3.16 for n = 2¹⁴/2¹⁶/2¹⁷) but stated as universal; population granularity never stated.

Minor: gap lower bound 7.5 not 7.6; multiset created:retained actually 8.8–12.0×10³; h_kick 4.84–5.05 vs predicted "2–4" (unreported miss); run.log empty; `analyze.py` referenced but absent.

**To gold:** one experiment — re-measure 2-D coupling ceiling-free, sweep n for the multiset branch, fix the no-program row. No new physics; the claim, verdict and sizing stand.
