# Predictions (written before the decisive runs)

The construction: a **due lane** (an indexed min-heap on each entity's next item tick) so a frame
with nothing due exits after one peek, plus a **lazy rekey** (the full deadline pass runs only
after the player's record changed or its evaluation time moved), plus **no deferral** (every
entity keeps its calendar slot; nothing is popped and put back). Resolution order among due items
becomes the lane's (tick, id) — the canonical key order — instead of deadline order.

## Tuned on
Nothing yet: the patch was written from the code's own invariants (each deadline input changes
only where `requeue` already runs), not from any measurement.

## Held-out expectations

1. **Zero-event frame cost.** Shipped, at N = 1e4–2e5 root-doll ships: ~0.2–1 µs per body per
   frame (the wiki's 43–60 ns rekey + the drain/requeue passes; streaming pushes it up with N).
   Lazy: **flat, O(1)** — I predict p50 < 3 µs per frame at every N, and the p50-vs-N slope
   exponent below 0.1 (shipped: ~1).
2. **Digest identity.** Plane scenario (fleet, player, 8 scripted decisions) at 5 schedules
   (threads 1/2/4/8/3 × budgets unlimited/200/7/64/MAX × steps): one digest per seed in shipped;
   the lazy run gives **the same digests bit for bit**, because resolution order among due items
   is a schedule and the cut is protected by the pull-driven reads.
   *Where it can break:* the fleet's cap reads the calendar's second-min deadline; with deferred
   entities no longer set aside the cap can be smaller, changing the battle's slice boundaries. If
   a partial slice is not exactly resumable the plane digest moves — that kills this construction
   (not the direction), and lazy-rekey alone would be retried.
3. **Busy cost.** Settling N = 5e4 ships to a fixed horizon: within ±10 % of shipped (the lane adds
   one heap set per requeue, ~100–300 ns against a ~75 µs event).
4. **Test suite.** `cargo test --release -p emergent-universe` all green on the lazy path (it is
   the default after the patch). A red digest test falsifies prediction 2 directly.
5. **Presented time under overflow.** The horizon is now the calendar min over *all* unresolved
   entities (shipped recomputed the deferred set's deadlines — same values, since nothing else
   changed them), so `Frame.presented` and `overflow` should match shipped behaviour; I expect no
   observable difference beyond timing.

## What would make me abandon the construction

Any digest difference at a canonical cut in mode 1 vs mode 0, in any scenario, on any schedule.
