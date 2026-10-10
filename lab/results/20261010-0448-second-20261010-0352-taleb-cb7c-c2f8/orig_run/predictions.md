# Predictions (written before the decisive runs, 2026-10-10)

Question: where is the plane's ruin horizon? Three probes: determinism (the unrecoverable
state), state growth per game-second (H_live, "not measured yet" per HANDOFF), and tail
convexity in load and time. All on the shipped bench (`xtask universe --bench`), external
RSS sampler at 5 Hz, no code edits.

Cases I have NOT tuned on, and what I expect there:

1. **Determinism (controls, both sides).** rtf 10, 5 s, seed 1: digest equal across
   (a) an exact repeat, (b) `--threads 8`, (c) `--unpaced`, (d) `--engine-ms 0.5`;
   digest DIFFERENT for seed 2. This is the design's claim (plane.md §Foundations 2);
   a failure here makes every other number noise.
2. **State growth (H_live).** At members 48 (39 live bodies), rtf ∈ {1,10,100,1000},
   30 s each: after a warm-up (view memo, first tubes), VmRSS is FLAT in game time —
   total ΔRSS over a run < 10 MB and the slope per game-second < ~1 KB/game-s, and
   crucially ΔRSS does NOT scale with rtf (30 → 30,000 game-seconds). Falsified if
   ΔRSS grows linearly with game-seconds (slope constant across rtf): that is a
   light-cone/history that never reabsorbs, and I would extrapolate it to the one-hour,
   4 GiB budget as the ruin horizon.
3. **Frame cost vs run length.** rtf 100, seconds ∈ {10,30,55}: p50 and p99 of frame
   CPU flat (±50%); worst hitch not increasing with T beyond noise; the tail driven by
   kick recompiles, not by accumulated history. Falsified if p99.9(55 s) > 2× p99.9(10 s).
4. **Load convexity (the one-cell fleet).** rtf 100, 30 s, members ∈ {48,192,768,3072}:
   frame_ms stays bounded (the 5 ms engine budget clips synchronous work), but the
   deferred work shows as overflow frames and rtf collapse: I expect overflow_frames
   and (1 − rtf_median/rtf_target) to grow CONVEXLY in members (contact batches in one
   Fermi frame), i.e. worse than linearly between 768 and 3072. bytes_per_body roughly
   constant (tubes are 16 B). Falsified if the worst frame grows sublinearly AND
   overflow stays ~0 at 3072 members — then the budget genuinely absorbs the cell.
5. **Seed spread (fat tails).** seeds {1..8} at rtf 100, 30 s, members 48: worst-hitch
   distribution heavy-tailed across seeds (max/median > 3), because hitch sources
   (recompiles, handoffs) are phase-locked to seed. This one I genuinely do not know;
   a ratio < 2 would say the tail is seed-homogeneous.

Kill criterion for the whole probe: if the machine's load (uptime in the embedded
machine_before/after) differs wildly between compared runs, growth ratios are noise —
report as unmeasured, not as flat.
