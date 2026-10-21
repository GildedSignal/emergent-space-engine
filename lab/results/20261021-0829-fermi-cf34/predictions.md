# predictions.md (written before the decisive run)

Question: budget-1e9 line 1 leaves "the belt's boundary items unpriced" while the code plans one
Boundary item per clock kick (step.rs `kick_clock`, one at `t + full/2`, one Kick at `t + full`).
What is that row worth at 10⁹, rtf 100?

- **P1 (rate):** steady boundaries/kicks ≈ 1.00 (band 0.9–1.1) for the belt population, flat across
  the hot window; per-body rates N-flat (3e4 vs 1e5 within 20%) and seed-flat (seed 2 within 10%).
  Belt bodies carry ≥ 95% of all boundary items at extra = 1e5 (the 24-member fleet and 3 planets
  are noise). Control both ways: the same ratio > 0 on non-clock bodies too (plan_interval also
  inserts a Boundary), so the row is not a belt-only artifact of my reading.
- **P2 (cost):** blended hot-window cost 20–90 µs/item on this x86 box (3aec: fired kick item stage
  82.5 µs x86, checker 83–86.5); pure Boundary resolve 3–30 µs and BELOW the pure Kick resolve
  (no force eval, no rebind); the belt readout is ≥ 50% of the pure Boundary resolve.
- **P3 (composition):** with r ≈ 1 the priced item stream at 10⁹ doubles: today's stream row gains a
  boundary term ≈ r × 4×10⁶ items/wall-s × B. At 3aec's boundary item (18.4 µs x86 / ≈10.8 µs M1)
  that is ≈ 66 cores x86 / ≈ 39 M1 — larger than the page's whole composed total (22.5–43.4 cores),
  taking "today-cost" from 5.6–10.9× the 4-core budget to ≈ 2–4× that; the closure bar
  "≤ 4.9 µs/event" halves to ≈ 2.45 µs/item once boundaries are counted at parität.
- **P4 (held out):** seed 2 and extra 3e4 reproduce P1's ratio and P2's costs within the bands
  above; the belt body's plan shows exactly alternating Boundary/Kick items with one spacing
  (the clock period, ~27.9k game-s per nladder), boundary at the half-period offset.
- **P5 (the lever):** the clock body's boundary is a readout plus two threshold comparisons and an
  anchor set — ~0 surprise of its own (the bracketing kicks share the state). Measured as: pure
  Boundary resolve − readout < 50% of readout. If so the lever is deleting the scheduled check
  (folding the thresholds into the bracketing kick's readout), not a faster item.

Kill criteria (written before the run): if steady b/k < 0.1 the row is < 10% of the kick stream —
under the board's 2× bar, the claim dies. If the blended cost < 5 µs/item or the composed boundary
row < 8 cores x86 today and < 0.5 cores after the mandatory cadence cut + split8, the row cannot
move the budget page's headline — the claim dies as immaterial. If boundaries do not appear in
`stats.boundaries` at all (items resolved lazily only on read), my premise about scheduled work is
wrong and the run reports that as the result.
