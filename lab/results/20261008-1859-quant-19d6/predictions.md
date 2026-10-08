# Predictions (written before the decisive runs)

Question: where is the plane's event-throughput knee (the rtf at which the 5 ms/frame engine
budget stops holding the 60 Hz pace), and what is the market impact of the player's burn — its
cost in events, frame-CPU tail, and wake breadth (which other bodies' event streams change)?

Harness: `cargo run --release -p xtask -- universe --bench` (deterministic script: short burns
every 4 s of game time, level `--level`, canonical-tick log, digest at a canonical cut, machine
state recorded). Cases below are not tuned on; the level flag and the rtf sweep have never been
run on the record (HISTORY shows only rtf 100, level 0, p99 2.45–2.72 ms on the M1).

- **P1 (baseline, x86 reproduction).** rtf 100, level 0, 30 s: frame-CPU p99 ≤ 4 ms (M1 record
  2.45–2.72 ms; x86 shared box, orders of magnitude only), overflow 0, rtf median = 100.
- **P2 (knee).** Events per game-second are set by the scenario (fixed kick cadence, ~33 bodies
  + 48 fleet members), so events/frame grows ∝ rtf until the 5 ms budget binds. Per-event cost
  is µs-scale, so the knee — first rtf with overflow frames > 0 or lowest-1% rtf below 90% of
  target — lands **between rtf 10³ and rtf 10⁴**. Below the knee, engine p99 CPU grows ∝ rtf;
  above it, RTF collapses toward a fixed events/s ceiling and overflow frames accumulate.
- **P3 (wake breadth).** Level 15 vs level 0 (same seed, script, cut): item counts for planet
  and moon kinds **exactly equal** (nothing reads the player); ship and fleet counts within
  ~10% (ships never read the player; fleet members only via contacts, if at all). The player's
  own items may grow (handoffs, rebinds at high β) but stay < 5% of all events.
- **P4 (tail containment).** Level 15's p99.9 frame CPU within 2× of level 0's, and hitch
  counts above 16.7 ms ≈ 0 in both: the budget moves work, never changes it (plane foundation
  7). The worst single frame may rise (a handoff burst), the p99 barely moves.
- **P5 (controls).** Digest(level 0) ≠ digest(level 15) — the burn flew; if equal, the flag is
  broken and the run is VOID. rtf 10 is the negative control (no overflow, rtf on target); some
  rtf in the sweep must overflow (the positive control that the budget can bind at all). If
  nothing overflows up to rtf 25,600, the knee is above the range and I report that.

Kill criteria: knee below rtf 300 means the plane at Julien's 100× runs within 3× of capacity
(capacity, not smoothness, is the bottleneck); non-player item counts or the p99.9 moving > 2×
under a burn falsifies bounded-work-per-frame in practice, not just in design.
