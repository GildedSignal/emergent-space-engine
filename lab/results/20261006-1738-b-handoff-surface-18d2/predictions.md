# Predictions (written before the decisive experiment)

Run 20261006-1738-b-handoff-surface-18d2: the single-surface handoff on extended coordinates
(the Opus motion memo §2.4, §5 step 3). Everything below is predicted from the memo and the
code as read, before any measurement of the change.

## The design being tested

- One predicate, a function of the state, checked at s-boundaries, the same in both directions:
  planetocentric `E_p < 0` and `r < r_c = R_H/2` (where the tide/pull ratio (r/R_H)³ = 1/8).
- The handoff map: the event offset boosted by Λ (nine shears on the position, R3's machinery),
  the velocity by R3's shears (unchanged), the child's clock offset as one deterministic shear of
  the child's own position words (Δt′ = −w·Δx′∥ exactly on the parent's simultaneity slice), so
  out-and-back is the identity on the integer words and the tick.
- The clock law (motion v2) extended to ships and players of planet dolls; planets keep the old
  split. For a child doll the perturbing field gains the parent (the star) as a source — the
  existing `field`'s pull-minus-origin-fall is exactly the tide — and the clock's constants gain
  the centre's own orbit as the source that sets Δs.

## Predictions, each falsifiable

1. **P5 (held out: the maps' exactness).** For 1,000 states at each of β = 0.01, 0.3, 0.9, capture
   then release returns the identical (position words as values, velocity words as values, tick).
   Prediction: 1000/1000 at every speed, provided the child's length grid is finer than the
   parent's by at least the boost's Jacobian γ (the test's dolls differ by 2^10; γ(0.9) = 2.29).
   The register `p_t`, re-projected on both sides of a handoff, returns identical words whenever
   it was the projection of the state before (a pure function of words that round-trip).
2. **Where the satellites live (held out).** At r_c = R_H/2 exactly, the 0.5 R_H and 0.9 R_H
   satellites of P4 are **not** in the planet's doll (the predicate `r < R_H/2` fails at birth);
   only the 0.3 R_H ones are captured. I predict the gate's outcomes are still correct: the memo's
   float replica held bounded Jacobi error for satellites run entirely in the parent doll.
3. **P4 (the decisive probe).** Regular satellites at 0.3, 0.5, 0.9 R_H, prograde and retrograde,
   2,000 planet periods: the decade ratio of the median Jacobi error ≤ 1.3 on all six. Predicted
   levels (not gated): 1e-6 to 1e-4, the 0.3 R_H prograde ones the largest (strongest tide, and
   they are the closest to the surface's chatter region), the retrograde 0.9 R_H the smallest.
4. **A moon born in the planet's doll never leaves.** A circular moon born at 0.3 R_H (prograde
   and retrograde) is never released over 100 planet periods: `stats.handoffs` stays 0 for a birth
   in the doll, and the body's doll never changes. (Births at 0.5 and 0.9 R_H are released at
   their first s-boundary — that is the surface working, not a failure.)
5. **B13 unchanged or better.** Flybys have E_p = v∞²/2 > 0 always, so no ship of the gate is
   captured ("passing ships need no handoff"); the time transformation resolves the flyby in the
   root doll as in steps 1–2. The only new work is the predicate read per boundary. Predicted:
   the same 60/64-or-better detail line at step 7, ±1 ship.
6. **B12 similar or better.** Fewer handoffs (only real captures, deep, at a synchronised
   boundary, and symmetric in both directions): the memo §1.3's mechanism predicts smaller
   per-crossing Jacobi jumps. Predicted: the worst error within 2× of the current value, the
   median exponent not worse.
7. **B14: the risk gate.** Moons below 0.5 R_H now run in the planet's doll at about 2^7 steps
   per planet period ≈ 12–14 kicks per moon orbit (about 5× fewer than today's 64). Predicted:
   classes agree at least as well as today (the tide is exact per kick; the split is symplectic),
   apsides within the gate's 10%. Moons at 0.5–0.9 R_H run in the root doll at 280–350 kicks per
   moon orbit. If B14's class agreement drops below 95%, that is a kill signal for the child-doll
   constants (Δs from the planet's period), not for the surface.
8. **B17 unchanged.** The resonant ships never satisfy the predicate (E_p > 0 at r >> R_H/2); the
   root-doll code path for d = 0 keeps its bits. Predicted: the same detail line as on main.
9. **G1–G6 unchanged.** They judge `crates/space` through the default law; nothing in the
   compilation path is touched. Run as a control only.
10. **Cost.** One extra centre-state read per boundary for root-doll ships: predicted ≤ 1.3× the
    per-event cost of steps 1–2, and fewer total events for B14 (the 100× cheaper moons).

## Kill criteria (frozen before the run)

- P5 fails at any speed → the event/tick map is not exactly invertible; kill the tick-shear form.
- P4's decade ratio > 1.3 on any satellite → the surface's switch compounds; kill this
  configuration (the surface at R_H/2 with re-projection), not the method.
- B14's judged-class agreement drops more than 2 seeds below its value on main → the child-doll
  clock is mis-derived; report as a measured failure with the diagnosis.
- Any of B13/B17 regresses beyond ±1 seed / a threshold → stop and diagnose before adopting.
