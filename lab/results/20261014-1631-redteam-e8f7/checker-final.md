Check complCheck complete. `Grade: silver` — written to `lab/results/20261014-1631-redteam-e8f7/check.md`.

**Reproduction (exact, no number differs).** `falsifier_key_depth2.py` + `regen.sh` (frozen assertions) both pass in a clean tree; empty patch; all citations verified at source (`universe.rs:3`, `step.rs:169`, `lorentz.rs:5-13`).

**The physics is right.** I validated the oracle independently (MᵀηM = η to 1.3e-15; collinear composition = cosh(η₁+η₂)), re-derived both error laws by hand — they're algebraic identities — and confirmed them to ≤ 1e-12 at points *outside* the author's grid (β₂ 0.5–0.9, θ 45–60°, depths 5/6/8: 512/995/2,921 ticks). My own depth-1 control (β₁ = 0, β₂ = 0.9) reads ~1.8e-12. The premise reading is fair: ae29's own branch specifies "all edges accumulated … position carried up Galilean" — the sum-of-shears, exactly the V2 form.

**Why silver, not gold:**
1. Two pre-registered magnitudes missed: player row 15.2 vs predicted 25–50 (honestly reported), and the doll-tick channel — exact carries the *composed* factor γ₁γ₂(1+β₁β₂) = 1.667 collinear (66.7 % miss), not γ₁γ₂/33 %; the dossier line "exact carries γ₁γ₂ = 1.3333" contradicts its own 6,667-tick number in the same sentence, unflagged.
2. "The fix is already in the tree" overstates — `lorentz.rs:22-23` composes boosts on four-velocities only ("nothing here answers it"), and the author never ran the positive control. I ran it: integer three-shear composition (2⁻¹⁰⁰ coefficients, ae29's 2⁻⁶⁴-tick events) holds to 1.1e-11 ticks — the missing gold experiment, now specified in check.md.

**Page corrections (in place):** the 33 %/γ₁γ₂ tick-channel line, "fix is in the tree" → machinery only (with my integer probe as evidence), the matching Refuted/Open-direction lines, and the runs line graded silver. Nothing else in the run folder touched; no git commands run.
