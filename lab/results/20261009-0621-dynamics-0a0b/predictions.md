# Predictions (written before the decisive runs; smoke run only to t=10⁶ ticks)

Run: 20261009-0621-dynamics-0a0b. Harness: `crates/universe/examples/twin.rs` — twin
universes from the shipped plane/restricted scenes, identical seeds, one perturbed body,
`settle(t)` at geometric checkpoints, per-body `BodyRec` hash diff + fleet digest.

Cases not tuned on: everything below t=10⁶ was smoke only; all predictions concern the
held-out range 10⁶–6×10⁸ ticks and the perturbation ladder.

- **P1 (member, sub-cell perturbation).** Perturbing one fleet member's lattice position by
  1 fine unit (2⁻²⁰ of the collision cell q) changes no contact outcome: no handed-out
  body ever differs (`ndiff = 0` at every checkpoint). The integer law blocks propagation
  below its own quantum (PRINCIPLES 6: below one quantum, influences accumulate but do not act).
- **P2 (member, one cell).** Perturbation = q (one collision cell): divergence propagates
  **only along the contact graph**. Differing bodies (leaver tubes) appear only after physical
  contact with a diverged member; the count is the transitive closure of contacts, bounded
  by the number of members that ever touch the perturbed chain — not all 48 by 6×10⁸ ticks.
  The frame-origin/COM channel does **not** propagate it to non-contacting members within the
  horizon: one member's share of the origin's motion (≈1/48) is below the origin's kick quantum.
- **P3 (ship).** Perturbing one restricted-scene ship's orbit radius by 1 root unit at sep
  5.27×10⁸: either the tube/memo quantum absorbs it (twins bit-identical, `digest_eq=true`
  throughout) or, if it registers, **no other body ever differs** (`ndiff ≤ 1` at every
  checkpoint): nothing in the law reads a ship.
- **P4 (planet).** Perturbing the planet's orbit radius by 1 root unit: every ship's kicks
  read the planet's tube, so **all 8 ships diverge** (`ndiff = 8`), each within one kick step
  of its own cadence; the propagation time is the read rate, not a growth law.

What would falsify the lens's model (branching process with quanta): P2 failing via
`ndiff` reaching all bodies without contacts (a mean-field/COM instability we missed), or
P3 failing with other ships diverging (a hidden ship→ship channel, e.g. the encounter tier).
