Grade: goldCheck complete. **Grade: gold** — written to `check2.md` (and `checker2-final.md`) in the run folder.

**Reproduction** (patch applied to a clean tree, all dossier commands re-run):
- Every counter bit-for-bit: reference 406,220 events / 203,017 kicks / 1.0000 rekeys-per-kick; anchored 3,204 compiles = 0.01598/kick, 197,340 re-anchors, wall 9.29→5.18 s = 1.795×; 2⁴ row 0.1093; Jupiter seeds 2–6 |Δa|/a med 1.51–1.65×10⁻³ (max to 4.6×10⁻²), seed 6 alive-diff 1 + one readout off the integer word; Saturn 0.0000 compiles/kick with med 5.8×10⁻⁵; determinism bit-identical; tightening row 0.520 / 2.1×10⁻⁵; headroom 5.99×10¹⁴ vs 3.09×10¹⁴.
- The gate claim verified by temporary edit: the existing lifecycle pin fails at `reanchor_num: 48`, passes at default — the refutation is seen by an existing gate.

**Predictions**: pre-registered (mtime 18 min before the outputs); the kill line tripped on every Jupiter seed exactly as written, and it is falsifiable (num 1 would pass it). Failures honestly disclosed.

**My three adversarial cases**: (A) at 4× the tide (2⁻⁸) compiles/kick rises to 0.066 — the 0.05 compute target is field-strength dependent, undisclosed, direction strengthens the kill; (B) at 48 game-years the median |Δa|/a grows 1.4× but the max 12× (superlinear tail); (C) error ∝ threshold / compiles ∝ 1/threshold confirmed on fresh seed 13 — no threshold reaches the 10⁻⁶ floor below always-compile. Mechanism confirmed in code: the residual's velocity offset is never integrated into position (bind.rs `readout`), so the error is first-order.

**Novelty/fit**: no prior measurement of this in HISTORY or the docs (law.md:35 specifies the re-anchor for the jet *with* stored derivatives; the 5 October kill was the re-rounding memo; H0207's re-anchoring is the battle frame). It corrects a design premise on the engine's own path, adoptable in one step (keep the lever off, redirect to the jet's derivatives and H0190 averaging) — the components-4643 gold precedent.
