# Predictions — 20261018-0308-redteam-30a0 (written before any measurement)

Premise under test: representation.md §2 L48 "Contacts use the **exact integer
special-relativity law** (`es-lattice-relativistic-v1`)". Exact SR means the outcome of a
contact is a function of the two worldlines only — invariant under which inertial frame the
engine's lattice sits in. The resolver builds its reflection normal from `d` = separation at
the detection chronon's **lattice-simultaneous** end (`relativity.rs` `resolve_law`,
`d = x_b − x_a` after the advance), and detection itself tests the reach ball in lattice
time (`law.rs hit`). Both inputs are frame-sliced. Fermi estimate of the swing: the normal
in the pair COM is `normalize(d_x/γ_c, d_y)` with γ_c the frame-dependent COM Lorentz
factor, and d is pinned within |w| of the lattice-frame ball entry; across a frame boost W
the sub-bin entry phase moves by O(|w|) and d_x contracts by 1/γ_c, so the outgoing
deflection should swing by O(β_rel · obliquity / ρ) rad, ρ = reach/|w|.

Instrument: the shipped stepper (`Chronon`, `Law::RelativisticV1`, Q = 2^20), driven on the
SAME two worldlines presented in frames boosted by W (exact boost construction of initial
data, rounded to lattice integers). Metric: the outgoing relative velocity's direction in
the pair COM (frame-invariant definition of the outcome), θ_out(W). Positive control: an
f64 covariant SR elastic reference (COM-simultaneous contact, |d_COM| = reach, reflect
about d̂_COM) run through the identical arms — must be invariant to rounding noise.
Negative control for the instrument: an arrival-phase scan at W = 0 must move the law's
θ_out while the reference stays fixed (the instrument separates law from reference).

Scene: equal masses (and 16:1 arms), reach = 4·|w| (ρ = 4, the resolving regime —
skip-free at every u tested), closing β_rel along x, impact parameter u = b/reach.

## Frozen predictions

- **P1 (the kill):** at β_rel = 0.6, u = 0.45, the shipped law's θ_out varies across
  W ∈ {−0.5, −0.3, −0.1, 0, +0.1, +0.3, +0.5}c by **≥ 3° (0.05 rad)**, while the covariant
  f64 reference on the identical arms varies **≤ 0.001 rad**.
- **P2 (head-on invariant, the law's one exact case):** at u = 0, the law's swing is
  ≤ 0.01 rad at every β_rel and W. (The normal is x̂ in every frame.)
- **P3 (ordering):** the swing grows with obliquity (u 0 → 0.7) and with β_rel (0.2 → 0.9)
  at fixed ρ.
- **P4 (held out, genuinely uncertain):** a transverse boost (W along y, same |W|) at
  β_rel 0.6, u 0.45 produces a swing comparable to (within 2× of) the longitudinal arm.
- **P5 (the gates' blindness, by construction):** the E and p ledgers close exactly
  (residual + carries absorb everything) on every arm, including the maximally swung ones.
- **P6 (held out):** mass ratio 16:1 at β_rel 0.6, u 0.45 swings within 2× of the 1:1 arm
  (the channel is geometric, not mass-dependent).
- **P7 (arrival phase, same frame):** shifting the initial x-offset by fractions of |w| at
  W = 0 moves the law's θ_out by O(degrees) at u = 0.45 (the sub-bin entry phase), while
  the covariant reference is fixed. This is not the ether claim (no frame change) but it
  must be present if my mechanism reading is right.

If P1 fails (law invariant like the reference): the premise survives its strongest cheap
attack and that is the reported result (a surviving premise is worth reporting).
