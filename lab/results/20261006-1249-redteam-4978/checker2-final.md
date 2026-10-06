Working...
Check complete. **Grade: gold** — written to `lab/results/20261006-1249-redteam-4978/check2.md`; nothing else in the run folder touched, no commits made.

**Reproduction:** bit-identical (3 s, < 50 MB; `work/patch.diff` empty). Predictions (13:02) precede the decisive output (13:08); `run.log` is empty, so mtimes are the only order evidence. Instrument independently validated: the Darwin quadrature algebra re-derived, RK cross-check to 7 digits, and the C2 gap vs 1PN is genuinely 2PN (my p = 225 probe sits 2.08 % off, the expected order).

**Adversarial cases (mine):**
- ε-scan at δ = 10⁻³: error ∝ ε²; even a 10⁻⁵-of-L kick leaves Δφ 14× and Δt 132× floor — ε = 10⁻³ not cherry-picked.
- Two new L families (3.9, 3.55): same blow-up (10⁵× floor at δ = 10⁻³) — generic, not an L = 3.7 artifact.
- P4 plunge re-verified three ways (root count, RK from the true turning point, corrected quadrature), plus the **reverse flip** (plunge→bound kick), which the dossier didn't test — the type error is bidirectional.

**Defect found:** `plunge_phi` has a √2 algebra slip — the true horizon sweep is **12.51 rad, not 8.85** (ratio exactly 1.414214 across three independent methods). It sits in one supporting sentence; P4's verdict (plunge, no pericenter ever, phantom bound cycle) is insensitive, so it corrects the record rather than demoting the grade. Also flagged: the unquantified width of the recompile band and the loosely framed P4 clocks.

**Novelty/goal fit:** complements df81 (which *calibrated* a global C; this shows C diverges by ≥ 6 orders near the separatrix and the flip is unrepresentable); no gate covers kicked strong-field orbits (B12 Jupiter-like, B19 unperturbed-only — verified against law.md's table); HANDOFF's `NoBoundOrbit` freeze and both representation.md quotes are real. Kills law.md line 35's premise in its own designated strong-field domain; adoption is one local step.
