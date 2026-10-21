# Predictions (written before the decisive runs)

Decisive runs: `ktail 20 100 <seed> 48 <N>` for N = 1e5 (seeds 1, 2) and 3e5 (seed 1),
coast, on this Linux box (shared, 8 vCPU). Not tuned on: these seeds/N are the first
flights past the 4-s/10k smoke, whose numbers I used only to debug the instrument.

Instrument convention (stated, so the checker can price it): every item is resolved by
its own `advance(Budget::events(1))` call, so each item also pays the per-call fixed
cost (rekey etc., measured ~6.7 µs at 10k in the same run). Absolute µs are therefore
upper bounds; ratios within a kind, tail shape, and worst-frame composition are the
measurements. The frame drains fully (no 12-ms cut): "served ms/frame" is what the
frame wants, not what the budget allowed.

- **P1 (ship tail ratio, N-flat):** the ship item's max/mean stays in 2.5-4.5× and moves
  < ±30% from 1e5 to 3e5.
- **P2 (the player item dominates service):** the player item's mean ≥ 10× the ship
  item's mean at every rung.
- **P3 (worst frame is service-driven, p99 frames arrival-driven):** at the max-served
  frame the correction (served / (events × mean)) ≥ 1.5 in at least one rung; at the p99
  frame it is < 1.
- **P4 (the >p99.9 tail is a different population):** plain kicks carry < 50% of the
  >p99.9 tail's sub-counters at every rung (boundaries/handoffs/opens dominate) — so a
  mean-kick cost cut moves the tail budget little.
- **P5 (the drain-revealed freeze):** max served/frame ≥ 50 ms at 3e5 within 20 s (the
  comb class visible with the budget removed).

What would make the run a kill of my own premise: if the ship item's distribution is
tight everywhere (max/mean < 2) AND the worst frames are pure arrival piles
(correction < 1 everywhere), then the service tail is not a lever and the mean-cost
program (GPT kickcost) is the whole story — I would report that as the result.
