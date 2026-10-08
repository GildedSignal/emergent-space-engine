# Predictions — 20261007-2344-quant-4211 (quant lens: the deadline queue's capacity)

Written before the decisive benchmark. Scene: N bodies uniform on a 30 AU disc
(R = 3e9 ticks, TICK_SECONDS = 4.925e-6 s), player crossing at beta x rtf, 60 FPS
(frame = 3383 x rtf ticks of game time), belt-like power-of-two steps, budget cap
50k resolved events/frame. The queue mechanics are copied faithfully from
`crates/space/src/events/calendar.rs` (4-ary indexed heap, (Scalar,slot) keys,
tie by slot) and `Universe::advance`/`rekey` (rekey-all, peek-drain by event time,
defer-then-requeue).

Variants:
- V0 ship: rekey all (sqrt + set), drain, defer + requeue (sqrt + set).
- V2 skin: triangle-inequality skin of width s on the deadline; recompute sqrt +
  heap set only when the interval [lo,hi] outgrows s; heap key = lo (a lower
  bound on the true deadline). Drain kept for comparability.
- V3 keyed window: heap key = max(t_e, dl); entities with key > target + W parked
  in 64 dyadic buckets, promoted as the target reaches them; sqrt only on touch.
  No drain (the loop breaks at min key > target: mandatory work is deadline-bound).

## Tuned-on cases (the sweep itself)
N in {1e4, 1e5, 1e6, 3e6, 1e7}, beta = 0.1, rtf = 100, s = 2^24, W = 2^24.

## Predictions, not tuned on
1. V0's per-frame queue cost (rekey + drain, resolve a no-op) exceeds the whole
   16.67 ms frame budget by N = 1e6, and exceeds a 1.67 ms (10%) scheduling share
   between N = 1e4 and 1e5. Capacity N*(ship) ~ 1e5 bodies.
2. The heap mutation, not the sqrt, dominates rekey: set/pop ~30-80 ns/entity at
   1e6 slots vs sqrt ~5-10 ns. (Von Neumann, not arithmetic.)
3. V2 at s = 2^24, beta <= 0.1: < 5% of entities per frame need sqrt + set (the
   interval widens by 2 x beta x 338k x rtf/100 ticks/frame); frame queue cost at
   1e6 drops >= 2x vs V0 but stays O(N) through the drain and the per-entity
   widening stream. Resolved-set equality with V0 under unlimited budget: 100%
   of frames; horizon (presented time) never optimistic beyond s.
4. V3: amortized queue cost < 3 ns/entity/frame at 1e6 (>= 10x under V0), and the
   resolved sets stay deadline-faithful: with unlimited budget, every frame
   resolves the same multiset of events as V0; the horizon differs by at most W
   plus the skin (never optimistic beyond that).
5. Held-out boundary (not tuned): beta = 1, rtf = 1000 (frame advances 3.4e6
   ticks): V2's recompute fraction rises above 30% (the skin stops paying);
   V3 degrades gracefully (promotion traffic follows the frame's game-time
   advance, not N).
6. Held-out scene: 1e6-body fleet concentrated on one ring at 1/30 AU (the
   co-orbital gold's concentration), player crossing it: V0's drain cost is
   unchanged (O(N) regardless), so concentration changes event volume, not the
   queue's floor — the floor is the rekey + drain, both blind to where bodies are.

Kill criteria: if V0 at 1e6 costs < 1.67 ms/frame (queue comfortably inside
budget at 100x the plane's current body count), the flat heap is not a
bottleneck at any planned scale and the right dossier is "nothing to build".
If V3 cannot match V0's resolved sets under unlimited budget, V3 is wrong as
built (order semantics broken), regardless of speed.
