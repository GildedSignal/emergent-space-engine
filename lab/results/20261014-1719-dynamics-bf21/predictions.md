# Predictions (written before the decisive runs)

Scene: the ladder belt (seed 1), 2×10⁵ ladder bodies, L8 prograde burn from frame 60, rtf 100,
12 ms budget, 160 s flights (the wave's first kicks land at 13.0–14.5 k game-s ≈ 130–145 wall s).
The fix under test is env-gated (`ES_PULL_CAP`), so baseline and fix are the same binary.

## The wave's anatomy (wave_train, settled past the first wave)

1. The belt's steps collapse to one or two powers of two (the pow2 rounding of `step_for`): the
   step census has ≥ 90% of bodies on a single power of two.
2. The items after the first wave sit one step later (second ≈ first + step), so the wave is a
   **train**, not a one-shot: the arrival pattern recurs at the step, and within each wave the
   arrivals span only ~1.1 k game-s (the p01–p99 of the first wave), i.e. ~24× narrower than the
   step. Phase mixing does NOT disperse the cohort (the kick grid is anchored at birth, not at the
   orbital phase).
3. The gap census after the settle shows the same collapse (one dominant gap).

## The fix (wave_flight, ES_PULL_CAP=64 on vs off)

4. Baseline reproduces taleb-6138: monster frames of order 10²–10³ ms in the wave window
   (13.0–14.5 k game-s), carrying ~10⁴ events each, spaced ~50 frames (the player's item cadence).
5. With the cap: the worst frame in the wave falls to ≤ ~20 ms (the capped pull, ~64 events ≈ 3 ms,
   plus the budgeted frame) — no frame above ~3× budget; the wave's cost becomes lag (presented
   time falls behind, then recovers), as on the coast.
6. `digest` is **bit-identical** with the cap on and off (the canonical cut answers every held
   scan; resolution order among ships changes no bit), and `stats.encounters` is equal.
7. Held scans at the end of the flight are nonzero with the cap (the deferred wave scans answered
   at the settle), and the settle itself stays cheap (< ~10 s).

## What would make this wrong

- The deferred scans answer against pruned or stale bindings (the gate on `ship_ticks`' minimum
  fails): digest differs, or encounters differ → the fix is not free and must be re-derived.
- The monsters persist with the cap (the batch is not the look-ahead pull): then taleb's reading of
  `universe.rs:769` is wrong and the cost lives elsewhere (the drain itself or the rekey).
- The second wave measured flatter than the first (phase mixing real): prediction 2 fails, the
  train is a transient, and the stagger is unnecessary (the wiki's one-shock reading stands).
