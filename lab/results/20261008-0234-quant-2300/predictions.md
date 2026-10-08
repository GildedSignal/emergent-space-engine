# Predictions (written before the decisive runs)

Instrument check already seen (not a prediction): at `--rtf 1 --seed 7 --members 48` the bench
replays 23 distinct kicks in 6 s; resolver-only timing via `Instant::now` around `step::process`.

The decisive runs: `--rtf 100` at members {4, 48, 400}, seconds 6, seed 7 (capacity curve), then
`perf stat` / `perf record` on the members-48 run (stage attribution and per-kick counter rates).

Cases not tuned on; what I expect there:

- **P1 — stage attribution.** The Kepler tube fit (`bind`/rebind) plus the exact readout dominate a
  level-0 kick: > 50% of resolver samples land in bind/fit/readout, not in `force::acceleration`.
  Rationale: exact i64/i128 dyadic arithmetic with normalization on every op; forces are
  O(#secondaries) and the plane's dolls have few secondaries.
- **P2 — allocation.** The `Vec<Secondary>` allocated per kick (`Ctx::secondaries`) is measurable
  but < 10% of a kick at members 48.
- **P3 — capacity.** Median µs/kick stays flat from members 4 → 400 (within 2×): a kick reads O(1)
  other bodies (its doll's sources are structural, not per-member). The tail (p99) grows with the
  working set as histories spill past L2/L3 (256 KiB/core, 8 MiB shared here): I expect p99/median
  > 3× at members 400 but < 3× at members 4.
- **P4 — counters.** Per kick on the order of 10⁴–10⁵ instructions (exact integer arithmetic, not
  cheap ALU), IPC < 1 (dependency chain, `Res` branches), < 20 L1 misses per kick at members 48.
- **P5 — budget.** If median ≥ 10 µs/kick, one Haswell core sustains < 10⁵ kicks/s, and the goal
  (10⁹ bodies × 32 kicks/orbit ≈ 10³ kicks per game-second, RTF 100 ⇒ 10⁵ kicks per wall-second)
  already consumes a whole core. Kill line for the *measurement*, pre-registered: median µs/kick
  growing > 4× from members 4 → 400 means the resolver is not O(1) in universe size and the
  capacity cliff is inside the shipped plane, not beyond it.

Falsifiers: if forces dominate instead (P1 wrong), cadence is the only lever and per-kick cost is
already minimal; if the median is flat but the p99 is flat too (P3 half wrong), the resolver is
cache-clean and the allocator's tail problem lives elsewhere (scheduler, view).
