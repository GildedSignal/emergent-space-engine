Working...
Check complete. `lab/results/20260930-1241-library-d690/check.md` written — **Grade: lead**.

**What I did and found:**

- **Reproduction (exact):** copied `experiment.py` out of the run folder (its files untouched), ran `FAST=1` (47 s) and the full mode (499 s ≈ 8.3 min as claimed). Both reproduce the author's metrics **byte-identically** (deterministic seeds). patch.diff is empty. All four quotes are verbatim in the Readwise cache; 758 books / 4,484 highlights exact. Dossier ratios (17×/6.1×/6.0×) check out.
- **Predictions:** pre-written by mtime order (13 min before metrics.json); run.log is 0 bytes, so the audit trail is mtimes only. Held as reported, misses disclosed honestly.
- **Adversarial cases (4):**
  1. **Anchored control — kills the headline.** Adding one line (`dx += 0.02·(0.30−x)`) to the graded law and re-matching activity (0.3559): the graded law then **beats** binary — crossPopSD 2.8e-4 vs 7.9e-4 (N=10⁴), 1.3e-4 vs 4.9e-4 (10⁵), timeSD 3–4× lower. The author's graded control is a martingale (neighbour pulls sum to zero), so the 6–17× measures *anchored vs unanchored*, not *binary vs graded*. The author had named this risk in "what would make it wrong" but left the claim and the "delete the graded evaluation layer" proposal standing on it.
  2. **"Absorbing" is a mislabel:** the binary toy churns at 0.35 flips/agent/step — the Taleb commitment mechanism is never implemented, so the toy can't support it.
  3. **Criticality sweep (supports author):** no bimodality, tails ≤ 1.05 across δ = 0.30–0.90; minority just goes extinct above δ≈0.7. No avalanche inversion.
  4. **5% forced flips (supports author):** no amplification in either law.
- **Experiment B** is a Monte Carlo check of a CLT identity (analytic SD·√n ≈ 0.189; measured 0.175/0.192/0.190) — the n* = ε⁻² rule is sound, adoptable arithmetic for B5, but not an empirical result.
- **Novelty:** first lab run; prior Readwise passes (H0055–H0066) were cadence-OS; the decision-layer comparison is new to the docs — and now disconfirmed as evidenced. The surviving, narrower lesson: a linear local decision law leaves the collective mode free to diffuse; the layer must anchor that mode by local nonlinearity — binary vs graded is unsettled by this run.

Nothing else in the run folder was modified; no git commit or push.
