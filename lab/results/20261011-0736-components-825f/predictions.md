# Predictions — 20261011-0736-components-825f (allocator component)

Written before the decisive traced runs. Exploration so far (no per-item data seen yet):
baseline `--rtf 100 --seconds 30 --unpaced` (76 bodies): engine p50 0.045 / p99 1.28 / max
5.66 ms, 3 overflow frames; `--members 400` (428 bodies): engine p50 0.13 / p99 5.29 / max
6.48 ms, **111 overflow frames, rtf lowest-1% = 0** (presented time stalls), no hitch above
16.7 ms; `--rtf 1000`: engine p99 3.83, 4 overflows. Player items cost 337 µs (48 members)
vs 1560 µs (400 members). Budget = 5 ms wall.

The traced runs will split every frame's engine work into **mandatory** (deadline ≤ frame
target: its light already reaches the player) and **deferrable** (deadline > target).

- **P1 (who stalls the frames).** In the members-400 run, the frames that overflow (mandatory
  work left undone) are dominated by the **player's own items**: entity = player, cost
  ~1.5 ms each, several landing in one frame during burns, light distance 0 (zero slack, not
  deferrable by any policy). The fleet slices and ship kicks, having the planet's light
  distance as slack, are not what breaks the budget.
- **P2 (the compute-ahead share).** Across all frames of the same run, ≥ 70% of resolved
  engine time is deferrable (deadline > target). The 5 ms budget is mostly spent on
  compute-ahead, which is the design's intent (PRINCIPLES 17), not waste.
- **P3 (slack depth).** The median deferrable item has slack ≥ 10 frames (deadline − target
  ≥ 10 frame advances). Falsified if the battle's ships sit near the player (small light
  distance) and the median slack is ~1 frame.
- **P4 (the allocator's own bookkeeping).** `rekey` (deadline recompute, O(entities) per
  frame) costs < 100 µs per frame at 428 entities; per item resolved it is noise today. The
  number matters only as a scaling flag (O(entities)/frame), not as a current cost.
- **P5 (the overshoot mechanism).** The worst frame's engine wall ≤ budget + the single most
  expensive item, and that item is a player item (motion-law v2 step): the tail above the
  budget is item granularity, bounded by the most expensive item kind.
- **P6 (inertness, schedule independence).** The traced run's digest at the canonical cut
  equals the untraced run's digest (same seed, members, cut), and a run with `--engine-ms 10`
  gives the same digest again: instrumentation and budget move *when* work happens, never
  *what*.

What would make the component interesting instead: if P1 fails and the mandatory demand of
*fleet/ship* work itself bursts above 5 ms (a capacity floor already at 428 bodies), or if
P2 fails and most of the 5 ms is mandatory (then eager compute-ahead buys nothing and the
budget is pure truncation). Either way the idiot index (actual p99 spend vs mandatory p99
demand) is the deliverable.
