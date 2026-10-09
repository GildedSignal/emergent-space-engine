Working...
Check complete. `lab/results/20261009-0709-scout-5b6a/check.md` written: **Grade: lead**.

**Verdict basis:**

1. **Reproduction** — both scripts rerun in a scratch copy; `cone_results.json` and `news_results.json` regenerate bit-identically. Pre-registration timing holds (predictions.md −15 min precedes all code and results). Novelty confirmed: no HISTORY entry measures news cost against causal radius; the HANDOFF line-74 risk is real and on `b-news-gravity`'s path.

2. **The decisive metric is void.** `cone_news.py:35` subtracts `F.mean(axis=1)` per source, then line 37 sums over sources: Σ(Fᵢ−F̄) ≡ 0 algebraically. Measured residual 4.3×10⁻¹⁷ (machine epsilon × force scale 1.16). The reported "0–2 events/orbit" is roundoff zero-crossings: identical event counts at ε 10⁻⁴ and 10⁻⁶, event count grows linearly with sampling (14/48/190 at n_t 480/1200/4800), and events spread over the whole run — the dossier's "t = 0 transient" explanation is also wrong. The intended tide needs per-source `F_i(origin)`, not the mean at the probe.

3. **Honest replacements invert the headline.** Dipole-included (author's own control): 3.1×10⁴ events/orbit at ε 10⁻⁴; tide relative to the doll origin: same order. Driven by tangential shot noise (RMS 0.067–0.14 vs mean field 1.16) entirely from d<20 — the 4×10⁴-source toy disk is too coarsely sampled for a sub-quantum far field. The R-invariance of a zero signal carries no information; news was never swept against N.

4. **Salvage (real, reproduced):** naive cone ∝R² (20→40 140), significant-set saturation flat in R and N-invariant under pareto refinement (8425→8064), clump billed as 17 vs 11 aggregate levels, exp generator R-invariant — plus an undisclosed scaling issue: pareto kept-lines grow 177 870→1 269 463 under 10× refinement.

Nothing else in the run folder touched; no git operations; all scratch in `/tmp/check5b6a`, every process well under 2 GB.
