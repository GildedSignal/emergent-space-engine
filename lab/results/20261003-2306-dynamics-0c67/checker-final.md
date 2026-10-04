Working...
Check complete. `lab/results/20261003-2306-dynamics-0c67/check.md` written; nothing else in the run folder touched (all my scratch work in `/tmp/check-0c67`); no git operations.

**Grade: silver.**

What I did and found:

1. **Reproduction — bit-exact.** All six dossier commands rerun in a clean tree (109 s total, 2 vCPU); all nine output JSONs byte-identical to the author's. Every quoted number checked out: wall positions 0.825/0.675/0.60/0.525/0.475, fit α = 0.244 (C ≈ 0.95), interior 0/360 at e ≤ 0.05, 7/180 at e = 0.2 in the 2:1 wing, belt fraction 0.348, floor 1.1%, step-halving control identical.

2. **Pre-registration verified by mtime.** `predictions.md` (23:09:25) predates both implementations and every result file (23:14+). Failures P1–P4 honestly reported; the disclosed method kill (variational → twin-shadow) is real.

3. **Adversarial cases.** 400-orbit horizon: interior commensurabilities still clean. Held-out μ = 0.02: wall at 0.6375–0.65 vs 0.635 predicted — the μ^{1/4} law interpolates, the strongest independent confirmation. But e = 0.3/0.4: an interior web reappears (a=0.55, e=0.4 → 90% decorrelate, 80% ejected), so the wall is an e ≲ 0.2 law. eps = 1e-12: geography robust, the 7/180 count soft (3–7/180).

4. **Why not gold.** (a) The operative claim — "the orbit-averaged kick layer is valid through the entire interior" — is unmeasured: both twins run under the truth integrator, so the metric sees chaos, not the cheap layer's systematic bias, and r4's kills (≈2× e-pumping at interior resonances, at e₀ = 0.02) live exactly in that blind spot while the author's proposed rung gates only the e = 0.2 wing. (b) P3's pre-registered held-out thresholds failed (56%/67% vs >60%/>80%) — by the integrator's own precedent that caps at silver even though the failure is the finding.

5. **Gold path named:** the integer-law rung with averaged kicks below 1−μ^{1/4}, judged by r4-style e-pump/libration gates at the interior 2:1 and 3:1 at e₀ ∈ {0.02, 0.2}, B14 precession, plus the eccentric-secondary probe. Also flagged: the "floor" control is actually real orbit-crossing chaos (a=0.85, e=0.2 crosses the secondary), the renormalization is dead code with a mismatched docstring, and the metric's sensitivity floor (λP ≳ 0.115/orbit) is implicit.
