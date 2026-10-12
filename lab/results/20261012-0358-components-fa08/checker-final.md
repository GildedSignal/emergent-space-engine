Working...
Check complete. `lab/results/20261012-0358-components-fa08/check.md` written; nothing else in the run folder touched.

**Grade: silver.**

**Reproduced** (clean tree, empty patch — everything regenerates from the shipped code):
- Kick-bench: identical digests and memo counters (27 rebinds, exact hit rate 0.0), median 57.97 vs 57.93 µs.
- Jet-probe: **bit-identical** on every deterministic error-law number (crossings 38/112/2, 510/1, 350/1198/4, 38/110/2, all `e*_last`), timings within noise. The D² law's internal scalings check out (1/δ: 38→350; √floor: 38→112; field-independence: 38=38).

**Why not gold:**
1. **My held-out cases break the headline constant.** The dossier ran every case at one eccentricity (actually e = 0.4375 — the dossier's "e ≈ 0.28" misreads its own k = 1/(1+e) quantum). At e = 0.75, N* = 8 in both fields — below the author's own pre-registered kill threshold (< 30), degrading the 21× cut to ~7×. Pure-tangential correlated kicks give N* = 30, so "38 = correlated worst case" is false. The D² law survives; "C ≈ 0.8" does not transfer.
2. **A failed pre-registered prediction absorbed silently**: E2 predicted N* ≈ 300–3,000 (safe interval ≥ 100); measured 38 — not listed among the dossier's misses.
3. **The author's own named gap**: N* was measured with the oracle re-time, not the derivative-corrected jet the design will run — an estimate, not a bound.
4. **Novelty is refinement, not a new lever**: the jet, C·drift², re-anchoring and 0.05 compiles/kick are already in law.md (red-team df81). The genuinely new adoption-grade fact is J1t: the memo's period derivatives are measured-mandatory (die at kick 1–4 without them), upgrading law.md line 14's spec detail; I verified the shipped tables store no derivatives.

**Gold experiment**: the same harness with ∂Δt/∂E, ∂Δt/∂L carried instead of the oracle re-time, across an e-ladder 0.28–0.9 — giving the per-body C the re-anchor certificate needs, or the jet's kill for the high-e belt population.
