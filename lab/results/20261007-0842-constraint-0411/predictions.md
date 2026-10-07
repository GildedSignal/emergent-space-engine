# Predictions (written before the rtf/members sweep, 2026-10-07 08:50 UTC)

Baseline measured first (seed 1, 30 s paced, 39 bodies + fleet of 48, machine idle, load ~1.0):
frame p50 3.30 ms; engine 4.9% share, view_gather 74.1%, view_json 14.6%, wire 6.3%;
engine ms is 96% fleet (1810 slices, 55.5 µs each; 7 kicks; 60 µs per distinct kick from the kick-bench);
engine demand ≈ 3.5 ms CPU per game-second; engine budget 5 ms/frame at 60 Hz = 300 ms CPU/wall-second.

Held-out cases and predictions (not tuned on):

1. **rtf sweep (10, 100, 1000, paced, seed 1):** engine share rises ∝ rtf, view share falls.
   Crossover (engine share > view share) between rtf 10 and 100.
2. **Delivered rtf ceiling ≈ 86×** (= 300 ms/s ÷ 3.5 ms per game-second), because the 5 ms budget
   caps engine work per frame. So rtf 100 is *at* the ceiling (rtf_median ≤ 100, mostly below),
   and rtf 1000 delivers ≲ 90 with overflow on most frames and a growing tick backlog (presented
   tick falls behind the cut; overflow_frames large).
3. **Elevating the budget moves the ceiling ∝ budget:** `--engine-ms 15 --rtf 100` delivers
   rtf_median ≈ 100 (budget no longer binding; frame p99 still < 16.7 ms). If instead the ceiling
   stays ≈ 86, the constraint is a serial cost inside `frame_to` that ignores the budget — that
   would falsify the budget-cap reading.
4. **Fleet members scale the constraint linearly:** `--members 400` (8.3× members) at rtf 1 keeps
   frame p50 < 8 ms but multiplies engine ms per game-second ≈ 8× (≈ 28 ms/game-second), so the
   delivered-rtf ceiling at 5 ms budget falls to ≈ 10×; at rtf 100 it cannot hold.
5. **The view is a per-frame floor independent of rtf:** gather+json+wire ≈ 3.1 ms p50 at every rtf;
   no frame goes below it. At rtf ≥ 100 the engine p50 ms/frame stays ≤ budget (work is delayed,
   not dropped): the digest at the canonical cut stays exact (bit-identical across rtf is NOT
   predicted — different schedule, same resolved state at the cut is the design claim; I predict
   identical digests only between same-rtf runs).

Kill criteria: if delivered rtf at 1000 ≥ 500, or engine share at rtf 100 < 20%, the "budget-capped
slice cost" constraint story is wrong and I report what the numbers show instead.
