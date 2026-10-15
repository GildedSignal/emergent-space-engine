# Predictions (written before the deletion's A/B)

Tuned on: the belt ensemble only (400 states, 0.5–8 AU about the star doll, e ≤ 0.25 biased small,
seed 0x9E37…, t = 4×10⁷ s, Unit::ONE). The deletion: `from_state`/`ending_at`/`outbound_arc` gain
fit-only variants that skip the residual's `decoded_event()` readout; the universe's `bind_in`
switches to them (its Bound never read the Rebinding's residual — it recomputes its own from the
turn). Held-out cases below were not run before this file was written.

1. **Belt A/B:** bind() falls by the dead decode's measured share: 18.7 → ~15.2–15.6 µs (−17±2%).
   All 400 Bound outputs (tube, residual, turn, orbit, units) bit-identical to the shipped build.
2. **Held-out, strong-field tail** (e ∈ [0.5, 0.95], a ∈ [0.5, 2] AU — the planet-flyby mix, never
   tuned on): bind() grows compile-dominated (~30–90 µs); the dead readout stays ~3–8 µs (readouts
   grow with panel count), so the relative saving shrinks to ~5–10% but the absolute grows.
   Identity still 100%.
3. **Held-out, second seed** (0xC0FFEE): same class, identity 100%.
4. **A real flight** (plane_extra settle at a canonical cut): digest and every counter identical
   to the shipped build — the deleted readout's result was never read on this path (by code
   reading; the flight is the check).
5. **Floor cross-check:** with the dead read deleted, the bind's remaining readouts (one for the
   turn) plus compile plus fit machinery sit ~15–20× above the ~0.5–1 µs primitive floor; the
   identity result (400/400) says the remaining decode is information the fit already computed
   once inside `at_radius` — the follow-up deletion is a refactor, not new physics.

Kill criterion: if the belt saving is < 5%, or any Bound bit moves, or the flight digest moves,
the deletion is dead and the identity finding stands alone as the run's result.
