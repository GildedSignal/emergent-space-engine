# Rung (draft, second author): the plane's smoothness SERVICE gate — zero-tick stalls, not wall hitches

Proposed freeze from lab run 20261008-1337-second-20261008-1252-taleb-2570-9420 (the checker's
named experiment on 20261008-1252-taleb-2570). The integrator freezes; nothing here touches the
crates, gates or `main`.

**Question.** At 100× RTF the plane's wall cost saturates under load (the engine clamps), so a
wall-hitch gate certifies a service that freezes: the failure moves into frames that present
zero new game time. Is the shipped plane's service level — judged on the instrument it already
ships, `rtf.lowest_1pct` (the 1st percentile of per-frame `game_ticks·TICK_SECONDS/wall_dt`) —
holding at 4× design load, and does the canonical digest stay invariant to the engine budget
there (the budget moves work, never decisions)?

**The service criterion (frozen):** no frame presents zero ticks at 4× design load, judged as
`rtf_low1_median >= 1.0` — the worst 1% of frames must still make at least 1× real-time
progress (a zero-tick frame scores exactly 0; a one-tick-in-16.7 ms frame scores 0.0003, so
both fail). Median over ≥ 3 seeds (no worst-seed gates on a noisy estimator). `digest_invariant`
= 1 iff the run's digest equals its engine-ms-50 twin's at the same canonical cut.

**Configurations.** All on the shipped bench, `xtask universe --bench --rtf 100 --seconds 30`
(defaults: paced, threads 1, engine-ms 5), seeds {1, 7, 13}; `members` clamps at 400
(`xtask/src/universe/mod.rs:32`) so the ladder never leaves the real range.
- `plane-1x` (positive): members 48, the design load. Must pass.
- `plane-4x` (candidate): members 192. The service level under test.
- `plane-8x` (negative): members 384, the top of the unclamped range. Must fail `stall`.
- Reported, not gated: members 96 (the bracket point), wall p99/worst, overflow frames,
  gather share and max, ev/s, bodies.

**Metrics** (per configuration, from the bench's own JSON):
- `rtf_low1_median`: median over the 3 seeds of `rtf.lowest_1pct`.
- `digest_invariant`: 1 iff the digest at engine-ms 5 equals the digest at engine-ms 50 (and
  0.5) at the same cut, same seed, unpaced 15 s twins.

```configs
plane-1x positive
plane-4x candidate
plane-8x negative
```

```criteria
stall behaviour rtf_low1_median >= 1.0
exact type digest_invariant >= 1
```

**Expected verdict as frozen (this box, Linux x86):** KILL — `plane-4x` fails `stall`
(`rtf_low1_median` ≈ 0 at 192 members on every seed; the collapse starts between 1× and 2×),
`plane-1x` passes both, `plane-8x` fails `stall`. The KILL kills the configuration (the
shipped service level at 4× load), never the method; it is the gate the allocator work must
pass. Locations are this machine's (the M1 is ≈ 4× faster per H0211); the shape is what
transfers.
