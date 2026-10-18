# Predictions (written before the decisive run)

The two-word (a, ȧ) store — ȧ by backward difference against the previous kick's own field
evaluation, zero extra source evaluations — replacing `observe::partial`'s per-read mid-field
evaluation. The one-word (a constant per window) failed the frozen gates at ratio 356× against
the 3× bar (f2b7); the two-word is second order at the handover by construction (the slope is
continuous across boundaries where a constant jumps).

Cases not tuned on (the gates' own ensemble, 12 ships of the restricted problem, 100 planet
periods, plus the 4×-finer-step arm):

1. **Gate `the_readout_between_kicks_reads_the_boundarys_error`** (worst readout/map ratio
   ≤ 3×, per ship): PASSES, point estimate worst ratio 1.0–2.0 (the shipped per-read arm reads
   1.11×). The one-word's failure mode (first-order jump at every boundary) is absent by
   construction; what remains is a quadrature of the same order as the midpoint rule with a
   constant ~10× larger at worst.
2. **Gate `the_readout_error_falls_as_the_step_squared`**: PASSES — the arm is second order
   (velocity error ~ ä·step³), so it falls ≥ 8× wherever the map output falls ≥ 8×.
3. **Gate `the_readout_between_kicks_is_bounded`** (worst absolute ≤ 2e-3): PASSES, point
   ≤ 5e-4.
4. **Where I expect the weakest margin:** the close-pass ships (0 and 2, steps shrinking as
   they near the planet): the backward difference is stale by one step, and ä is largest
   exactly there. If any gate fails, it fails on those ships first, with the ratio (not the
   order) blowing up.
5. **Digests:** the word rides kick records, which digests never hash (549f's one-word
   measured bit-identity) — I predict every digest/outcome test passes unchanged with
   `A_WORD=2` on, and the whole suite bit-identical with it off.
6. **Fallback windows** (no prediction, disclosure): the first window after every clock
   (re)plan, after a handoff or a burn's flush, and across silent (sub-quantum) kicks carries
   no fresh word — those reads fall back to the shipped per-read evaluation.
