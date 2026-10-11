Working...
All done. The record regenerates from this folder; every claim in the dossier is grounded in the outputs beside it.

**Summary of what was done** (checker's gold path, item by item):
1. **`circ_L` fixed** (one line, `a/√(a−3)`), proven by the author's own control `EL_from_ae(a, e→0)` (1e-15 agreement; R double-root residual 1.1e-16).
2. **P9 rerun**: spurious e = **0.0** (was 0.81), final L +0.79% at ISCO — the author's pre-registered prediction had held; the "projection rule" is withdrawn as an artifact. The fixed code changes **exactly one field** of `inspiral-out.json`; all else bit-identical.
3. **Kill criterion applied** to a p=20M grid: no kill inside B11's *frozen* domain (p 20–1000, **e ≤ 0.6**, ν ≤ 0.25 — the e-cap the dossier had dropped), worst corner 4.8 with zero margin; kill fires at e₀ ≈ 0.65 (ν=0.25), ≈ 0.85 (ν=0.01); checker's case (0.25, 0.9, 110M) = 14.7.
4. **Re-keys measured, not telescoped**: 759 (circular) / 642 (eccentric) from 1000M at the 1% bar, 1.2–1.3×10⁻³/orbit — replaces the non-regenerable 690 and the 4×-high "0.005/orbit"; 642/478,997 orbits reproduces the checker exactly.
5. **Soft edges characterized**: a* moves ≤ 0.5M under 4× step tightening (e* flips 0↔0.09 — a band [6,12]M, not a 0.1M constant); W2 scaling is 4.3× per 4× (O(h) endpoint), not "2×".

Predictions were pre-registered (10 of 12 held; the two marginal misses disclosed in the dossier).

**Claim, in one sentence:** Peters' flux balance drifting the exact Schwarzschild tube's (E, L) is adoptable as the inspiral generator inside B11's frozen domain (p 20–1000M, e ≤ 0.6, ν ≤ 0.25) at the 1% bar — the pre-registered kill line is crossed nowhere inside it (worst corner 4.8, no margin) and first crossed at e₀ ≈ 0.65 (ν = 0.25), exactly the corner the frozen gate already excludes — with the handoff at the exact separatrix (a* ∈ [6, 9]M, soft e* ≤ 0.2), the generator a measured calendar event (642–759 re-keys from 1000M, 1.2–1.3×10⁻³/orbit), and no projection rule (spurious e = 0.0: the "two-flux inconsistency" was the `circ_L` artifact).
