# Predictions (written before the decisive runs)

The change: the per-frame `rekey()` sweep over all entities is gated on the player's displacement
since the last sweep (`wander ≥ quantum`, `quantum = last_want/64`), and the frame loop serves
due-ness from a tick-keyed calendar (one peek) instead of draining every entity past the target.
The horizon and the fleet cap subtract the staleness slack (`wander`).

Cases I have not tuned on, and what I expect there:

1. **Quiet frames (zero events), the wall itself.** Legacy arm: per-frame cost grows linearly with
   n (the three Calendar touches per body; I expect ~0.3–1 µs/body at 10⁴–2×10⁵, matching the wiki's
   43–60 ns/body rekey plus the drain). Lazy arm: per-frame cost flat in n (a few µs at 2×10⁵), with
   rekeys ≪ frames (the player orbits at ~10⁻⁴ c, so wander grows ~10 root units per rtf-100 frame
   against a ~5,300-tick quantum: I predict < 5 sweeps in 200 frames).
2. **Digest identity across schedules, lazy arm.** All 15 (seed × rtf × threads × budget) configs
   print one digest, because the cut settles by tick-due-ness and resolution order is a schedule
   (H: engine core schedule-independent, taleb-40c0).
3. **Digest identity across arms.** `ES_EAGER=1` and the lazy arm print the same digest for the
   same (seed, rtf, threads, budget): the input log is absolute ticks, so canonical history is
   identical, and the cut resolves the same set of items in a different order.
4. **The universe test suite** (plane, ties, lifecycle, replay, throttle, motion, clock, origin,
   view) passes unchanged: it compares digests across budgets, thread counts, paces and step sizes,
   which is exactly what the tick-due loop permutes.
5. **Where it could fail (my own red team):** (a) same-tick ties resolved in a different relative
   order than deadline order — if ties are not fully pinned by (tick, id) the digests move and the
   construction is killed; (b) the fleet cap's slack subtraction making a fleet lag past a cut —
   impossible by settle's drain, but if `Fleet::horizon` misbehaves with a small cap the suite will
   hang or diverge; (c) the wall_ms=0.05 arm (a starved frame) leaving tick-due items unresolved at
   the frame's end — the digest must still match because the cut settles; if it does not, the
   horizon logic leaks into canon and the run reports that.
