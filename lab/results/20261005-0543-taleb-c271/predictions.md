# Predictions (written before the decisive runs)

Calibration seen so far (not tuned on, but seen): at 2 s and 20 s game time, the plane's digest at a
fixed canonical tick differs across schedules (oneshot ≠ s60 ≠ jitter; events3 ≠ s60) with **no
player inputs at all**; threads 1/2/4 give identical digests at fixed schedule (20 s).

Held-out cases and predictions:

1. **The law without fleets** (`scenario::restricted`: star, planet, ships; no fleet, no player):
   digests at a fixed canonical tick are IDENTICAL across oneshot / s60 / jitter / events3, at 60 s
   and 120 s game, for threads 1 and 2. The lanes/pull causality is canonical; only the fleet reads
   `self.target`. If this fails, the law itself is schedule-dependent — a worse finding than predicted.
2. **The plane with an empty fleet battle** (if `plane_with` accepts an empty world): schedule
   invariance is RESTORED (identical digests across schedules). The divergence lives in the fleet's
   frame-paced battle (`self.target.min(cap)` at universe.rs:495), not in body records.
3. **Mechanism counters**: across schedules at the same canonical tick, the fleet's committed
   internals differ — slices, kicks, epochs/anchors, or leaver count differ (stats and fleet state
   at the cut), while the set of resolved body events is the same. The digest divergence is carried
   by the battle's chunking (epoch boundaries and leaver hand-offs at frame boundaries), not by
   floating-point noise.
4. **Longer horizon does not heal it**: at 120 s game the schedule-dependence persists (digests
   still differ; the gap is structural, not a warm-up transient).
5. **Threads invariance holds everywhere**: t1 == t2 == t4 at fixed schedule, also in restricted and
   at 120 s (the resolve_wave purity claim holds).
6. **E2 (fixed absolute input log, flush-free)**: the input log stays identical (exactly 2 entries)
   across schedules, but digests still differ (the fleet coupling is independent of the player).
7. **E3 (the bench's held-key script)**: any change of frame pattern changes the digest — the input
   log itself moves (decisions land at schedule-dependent presented ticks). Two identical s60 runs
   in one process give identical logs; two jitter patterns give different logs and digests.
8. **Cross-process**: every per-mode digest is identical across two separate process invocations
   (no hidden per-process randomization, e.g. HashMap iteration order, in the physics).

What would make the fragility claim wrong: if restricted digests differ across schedules with no
fleet present, or if the divergence turns out to be my harness comparing different canonical ticks
(now must be exactly T in all runs before the digest — the harness loops until `now >= T` then
settles at T; I will assert the cut tick is T in every run).
