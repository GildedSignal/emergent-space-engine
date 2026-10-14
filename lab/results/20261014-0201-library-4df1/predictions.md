# Predictions (written before any measurement)

Bottleneck: nladder open direction 3 — compaction as the scheduled spike. The shipped
`Shelf::compact` (crates/shipmem/src/shelf.rs:822) drains the whole hot tier in one call,
per-group steps tracked as `max_step_ns`; the frame pays whatever the burst piled up.

Probe: a budgeted `compact_budgeted(max_groups)` that seals at most k groups per call and
keeps the rest hot (oracle-verified, same slot semantics), driven through
`SHIPMEM_SLICE=<k>` in `examples/measure.rs`. Control arm `SHIPMEM_SLICE=0` = one-shot
shipped behavior. Pops: battle (adversarial, ae3d's 12.1 ms worst step), convoy (calm
control). n = 4e5, updates = 1e5.

Cases not tuned on, and what I expect there:

1. **Max slice ≈ worst single-group step, not the burst.** With k = 1 group/call the
   worst *slice* (one call, incl. re-sort overhead of the remainder) drops far below the
   one-shot call time on battle — prediction: max_slice(1) ≤ max single-group
   `max_step_ns` × ~1.5. If it does not drop (slices as heavy as one-shot), the spike is
   inside one group and group-granularity amortization is dead on arrival.
2. **Amortization is near-free.** Total compaction work (sum of slices) within ~1.3× of
   the one-shot total on both pops; per-slice p99 ≪ max. If total blows up > 2×, the
   re-sort per slice dominates and the budget must live inside the event stream, not
   around it.
3. **The floor is the group, and it is above the frame slice.** On battle I expect the
   worst single-group step to stay ≥ ~0.5 ms regardless of slicing — i.e. scheduling
   cannot buy a 60 fps frame budget at group granularity; the budget knob must go
   intra-group (scar row-blocks). Convoy's floor I expect ~10–100 µs (slicing suffices
   there).
4. **Burst structure survives amortization.** Per-slice times on battle stay bursty
   (max/p50 ≫ 3, close to the one-shot ratio) because arrival, not service, carries the
   variance — matching ea91's avalanche finding; a fixed per-frame service budget, not
   drain-on-idle, is the compatible policy.
5. Held-out pops (stream, formation), same expectations as 1–3 with milder magnitudes.
