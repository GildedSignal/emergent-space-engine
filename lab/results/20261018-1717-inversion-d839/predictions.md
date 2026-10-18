# Predictions (written before the decisive flights)

Scene: the ladder's own (`nladder` example, patched print-only: /proc footprint, `LADDER_CAP_S`, a
probe line every 300 frames). Calibration: `belt_first 30000` puts the belt's first items at
13,051–14,542 game-s (p50 14,071), the locals' at 21–5,289; the ladder flights of record end at
20,000 game-s, so no second cadence wave has ever been observed. The decisive flights go to
36,000 game-s (N=30,000 and N=100,000, coast, rtf 100; control N=0).

- **P1 (the wave repeats, and where).** Every belt body is born at tick 0 with one Δs shared per
  doll, so kicks come as waves at integer multiples of each body's first item: a second kick
  concentration at ~26,100–29,100 game-s, mirroring the first (same p50 spread ≈ 1,500 game-s),
  visible as the second step in the probe's cumulative `kicks`. KILL of the frame question if no
  second concentration appears (then the belt's cadence is not wave-like past the first item and
  everything below is about the locals only).

- **P2 (memory: saturation, not ratchet — the decisive one).** `bpb` (dashboard bytes/body) and
  RSS step up at wave 1 and stay FLAT through wave 2 and beyond (within ±10% of the post-wave-1
  level). Derivation: `Universe::prune`'s horizon is `(now − keep).min(oldest − 2²⁶)` with
  `keep = 2·light_distance + 2²⁶` and `oldest` the nearest pending item (≈ now), so a binding
  retired at wave N is droppable well before wave N+1; `BodyStore::prune` keeps at least one
  retired segment, so the steady state is 1 retired + 1 current per belt body — the scoreboard's
  "~5,100 B after the first kick" is a constant, not a function of play time. FALSIFIED if `bpb`
  grows monotonically across wave 2 by more than +10% (history accumulates per wave): then the
  10⁶/10⁷ memory walls are at wave count, not body count, and ladder.txt's "4 GiB at ~1.7×10⁶"
  under-states the wall by the number of waves flown.

- **P3 (the catalogue does not leak).** `cat` (compiled-orbit cache entries) returns to ≈ bodies
  after each wave (retire releases the old key, the kick compiles a fresh one). FALSIFIED if `cat`
  grows by ≈ a body-fraction per wave (the cache leaks per kick — a memory ∝ waves channel that
  is not the history).

- **P4 (wave 2's frame cost ≈ wave 1's).** Max engine ms in wave 2 within ~30% of wave 1's, and
  over-budget frames ≤ a handful at N=3×10⁴ (ladder.txt's after-fix wave 1 at 10⁵: max 11.95 ms,
  0–1 over). FALSIFIED if wave 2 breaks frames wave 1 did not — the suspects the flight should
  separate: the `prunable` calendar's backlog walk, and the second full prune pass.

- **P5 (coast holds nothing at this K, for this long).** `held` stays ≤ O(10) over 36,000 game-s
  at N=3×10⁴ (the coast drain answers in-frame at this scale; acf2's K=10³ finding extended two
  decades in time and one in K). If held grows linearly instead, that is the known mint law
  (memory-h-live), reported as background, not as this run's claim.

- **Held-out arms for the checker** (not flown by me): N=10,000 and N=100,000 at horizon
  300–400 s; the burn flight to 36,000 game-s; and the wave-2/wave-1 comparison at a horizon cut
  between the waves (24,000 game-s: wave 2 must be absent, `bpb` flat — the negative control).
