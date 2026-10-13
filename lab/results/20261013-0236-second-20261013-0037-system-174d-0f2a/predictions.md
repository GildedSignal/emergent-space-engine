# Predictions — 20261013-0236-second-20261013-0037-system-174d-0f2a

Written before the decisive runs. Tuned on nothing stronger than the instrument smoke test (a 2 s and
4 s paced battery at seed 1, run only to prove the probe decodes `clock` and `r` correctly — the smoke
run did show L8/L12/L15 law-cadence counts of 2/11/24, so those three numbers are instrument-familiar,
not held out; everything below at 8 s, at seed 7, in demand mode, and every per-event budget number is
unmeasured). The question is the checker's named experiment: re-price the tide's counterfactual with
the law's own regime-scaled cadence (`plan_interval`'s `want` before the thrust clamp, i.e. `step_for`,
1/2^step_log2 of the tube's radial period) instead of the coast's fixed granularity.

- **P1 (the law's own cadence is burn-bound almost everywhere).** In every flight at every level,
  ≥ 95% of thrust kicks have `clock_full > step`: the burn's chop, not the tide's cadence, sets the
  observed step. Only near the plunge (L15, deep r) can `clock_full` approach the burn step.
- **P2 (the re-priced counterfactual stays ~an order below the burst at every level, including the
  paced L15 plunge).** Law-cadence events over the same flights: ≤ ~5 at L8/brake/turn, ≤ ~15 at L12,
  ≤ ~40 at L15 even at 8 s of flight (where the fixed-granularity counterfactual mints ~2.6–3.1×10⁴).
  The deletion therefore wins ≥ ~30× in kick events at every level, and the inversion the checker
  found is an artifact of the fixed divisor, not of the lever.
- **P3 (the per-event budget is regime-scaled by the law itself).** The tide one law-cadence event
  carries, `tide_q · clock/step`, grows with depth: ~5×10⁸ quanta at coast-like radii (recovering the
  coast median by construction) and ≥ ~10¹¹ near the L15 plunge — within an order of the ~5–7×10¹¹
  the checker read off today's plunge kicks. The law's phase rule, not a new knob, does the scaling.
- **P4 (cross-seed stability).** At seed 7 the law-cadence counts and per-event budgets match seed 1
  to within ~2× (item counts exactly; wall-clock and per-kick tides vary with the shared box), and
  the composition (kick0 ≈ boundary, opens 0, decides = inputs) is unchanged.
- **P5 (demand mode agrees).** In demand mode at 4 s (so the turn flight's 2.5 s burn actually fires),
  law-cadence counts are within ~2× of paced at the same level; the turn-then-burn flight shows the
  burst arriving with the burn keys (its demand evidence now includes a burn, closing the original's
  undisclosed gap).

Kill criterion for the re-priced claim: P2 failing at L15 (law-cadence count ≥ the burst's kick count
at 8 s), or P1 failing wholesale (the law itself wants the fine cadence during ordinary burns — then
the deletion deletes nothing and the lever is dead, which would refute the run's claim outright).
