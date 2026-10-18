# Predictions (written before the decisive run)

The attack: representation.md thesis 3 ("every quantity is kept in the form in which its
change is an addition") + L50 ("thrust grows the rapidity linearly in proper time") applied
to the ship's attitude. Boosts do not commute ([K_x, K_y] = −J); a heading accumulator and
a velocity can carry only the abelian part. The exact law is Ḃ = B·(αK_x̂ + ωJ) on the
frame B; the missed term is the Wigner/Thomas rotation θ_W, extracted from B = R(θ_W)·B_pure(β).

Instrument: exact SO(2,1) integration (composition of exact matrix exponentials, 10⁵ steps;
self-checked by step-halving), vs the shipped letter (heading h ← h + ωΔτ; velocity by exact
relativistic addition along h at fine flushes — the shipped `burn` is exact composition, so
any divergence is the accumulator's, not the composition's).

Cases below were NOT tuned on; the run sweeps them once.

- P1 (control, positive): collinear flight (nose along velocity, any α, any γ): θ_W = 0
  to integrator precision (< 1e-9 rad), shipped velocity matches exact to < 1e-9.
- P2 (control, positive): pure turn at any speed, zero thrust: θ_W = 0 (< 1e-9) — rotation
  commutes with itself; the accumulator is exact when no boost is composed.
- P3 (control, negative): two perpendicular boosts of rapidity φ = ψ = artanh(0.9)
  (γ ≈ 2.29 each): the composed order matters by a Wigner angle I predict in (20°, 60°).
- P4: a 180° velocity reversal at γ = 2 (constant speed, off-axis burn): |θ_W| > 90°
  accumulated by the end of the reversal.
- P5: a full 360° loop at β = 0.6: |θ_W| ∈ [50°, 130°] (the two candidate closed forms
  2π(γ−1) = 90° and 2π(1−1/γ) = 72° both lie inside; I do not pre-commit to either).
- P6: the record's own off45 brake (nose 45° off velocity, held, from γ = 2, no turn keys):
  |θ_W| passes 30° before the velocity direction has turned 90°.
- P7 (physics feedback, not just the view): the shipped law's thrust rides its accumulator
  heading, so after P4's reversal the position error exceeds 5% of the path length.
- P8 (monotonicity): at fixed manoeuvre, θ_W grows from 0 with β (0.1 → 0.5 → 0.9);
  the failure is exactly the relativistic sector, absent in the Newtonian limit.
