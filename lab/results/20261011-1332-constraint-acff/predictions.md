# Predictions (written before the decisive runs)

From the first pass on main (bench rtf 1 and rtf 100, kick-bench, all in this folder):
engine demand at rtf 100, 39 bodies, 30 s wall = 1035 ms engine time (34.5 ms per wall
second, 11.5% of the 300 ms/s frame budget), but the p99 frame sits at the 5 ms budget
cap (37/1800 overflow frames) and the achieved rtf's lowest 1% is 19.6 against a target
of 100. The mean is fine; the tail and the ceiling are the question. Per-item costs by
kind: player 1270 µs, ship 257 µs, fleet slice 57 µs. Kick resolver (pure, ships only):
median 76 µs, p99 407 µs, exact memo hit 0%.

The decisive runs add a per-frame trace (engine_ms per frame + per-kind item/cost deltas,
top worst frames printed) and scale the plane's own axes: members 48 → 400, threads 1 → 4,
rtf 100 → 1000.

## Predictions, falsifiable, on cases not tuned on

P1 (tail composition): in the worst 5% of engine frames at rtf 100, members 48, the
dominant cost is **player items** (the clock law's steps, which shrink during burns and so
cluster many per frame), not ship kicks and not fleet slices: ≥ 50% of summed engine time
in those frames is kind=player.

P2 (sustainable rtf cap): engine demand is ~0.345 ms per game-second, so the 300 ms/s
budget caps rtf near 870. At rtf target 1000 (members 48, threads 1) the median achieved
rtf falls below 1000 (I expect 800–950) with sustained overflow, while frame times stay
under 16.7 ms (the budget hides the demand; only the time factor shows it).

P3 (member scaling): at members 400, engine demand per game-second grows roughly linearly
(fleet slices and leaver makes dominate the growth), so at rtf 100 the run becomes
budget-bound: overflow frames grow by an order of magnitude (≥ 300 of 1800) and the median
achieved rtf drops below 100 (I expect 20–80).

P4 (threads): the budget is wall time and the queue is order-independent by design, so
threads 4 at members 400, rtf 100 recovers most of the loss: median achieved rtf back
above 80, overflow frames reduced ≥ 3× versus threads 1.

P5 (unit cost): the player's per-item cost stays ~1 ms regardless of step length (its
steps during a burn are shorter but each still pays a full rebind), i.e. player engine
cost per game-second is flat in the step cap — the cost is per event, not per distance.

What would make me wrong: P1 wrong if the tail is ship-kick rebind bursts or fleet handout
makes instead; P2 wrong if the budget lets the horizon run ahead of resolved work (rtf
median ≈ 1000 with hidden debt); P3 wrong if slices per game-second do not track member
count; P4 wrong if threads do not share the budget (serialized queue) — each would relocate
the constraint and I would report the measured composition instead.
