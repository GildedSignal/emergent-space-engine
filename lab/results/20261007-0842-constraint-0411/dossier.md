# Dossier: 20261007-0842-constraint-0411 — the plane's constraint is the view and the burst, not the kick

## Claim

On the plane as it flies (39–428 bodies, fleet 48–400, rtf 1–1000), the smooth-frame constraint is **not** the engine's per-frame kick cost (engine p50 ≤ 0.92 ms, ≤ 23% of every frame) but (1) the O(bodies) view gather, 70–77% of every frame's p50 (~3.8 ms fixed + ~11 µs/body ⇒ a ≈1,100-body ceiling at 60 Hz from the view alone), and (2) for the p99, thread-immune engine bursts (engine p99 5.3–6.3 ms at 1 and 8 threads; 23% of frames over budget and delivered rtf stalling to 0 at 400 members × rtf 100).

## Bottleneck

Board focus item 1 ("fewer kicks per orbit … kicks dominate the engine's cost") is true *inside* the engine but the engine is not the frame: deleting the engine's p50 entirely would speed the frame at most 1.3× (Amdahl on a 23% share). The measured constraints for the goal's smooth-frame pillar are the gather (p50) and the burst tail (p99) — "the algorithm that allocates the work to prevent those heavy tails, it's the most important one" (CL 09-25 14:28), already the board's slack-skin lever. Expected gain from acting on this: the body-count ceiling at 60 Hz moves from ~10³ (view-bound) to the engine's ~10⁵+ per frame; the p99 tail (the actual deadline violations) becomes fixable. Nothing here demotes the kick ladder for the *billion-scale* engine cost (per game-second, per body-bit) — different denominator; see "the lens".

## Evidence

All commands ≤ 60 s except `behave` (99 s). Binary: `X=/home/glmlab/lab-target-3/release/xtask` after `cargo build --release -p xtask` (39 s). Machine: GitHub Actions runner, 8 vCPU, load ~1.0 before runs (uptime recorded in each JSON; `machine_state` fields for therm/batt are macOS-only and empty here). Raw JSON in this folder: `bench-rtf{1,10,100,1000}.json`, `bench-rtf100-ms15.json`, `bench-rtf100-t8.json`, `bench-m400-rtf{1,100}.json`, `bench-m400-rtf100-t8.json`, `kickbench.json`, `behave-plane.txt`, `engine-judge.txt`.

```
$X universe --bench --seed 1                          # 30 s, paced 60 Hz
$X universe --bench --seed 1 --rtf R                  # R in {10,100,1000}
$X universe --bench --seed 1 --rtf 100 --engine-ms 15 # elevate the budget
$X universe --bench --seed 1 --rtf 100 --threads 8    # thread control
$X universe --bench --seed 1 --members 400 [--rtf 100] [--threads 8]
$X universe --kick-bench --seed 1                     # < 1 s
$X behave --law plane                                 # 99 s
$X engine-judge --gates E1,E2,E3,E4,E5,E6,E7,E8       # 33 s
```

**Where the frame goes** (p50 shares; `where_the_time_goes_ms`):

| run | bodies | frame p50/p99 ms | engine % (p50 ms) | gather % (p50 ms) | overflow frames | rtf med / low 1% |
|---|---|---|---|---|---|---|
| rtf 1 | 39 | 3.30 / 4.60 | 4.9 (0.149) | 74.1 (2.37) | 2/1800 | 1.0 / 1.0 |
| rtf 10 | 71 | 4.39 / 10.56 | 7.4 (0.176) | 77.2 (3.42) | 30 | 10.0 / 9.9 |
| rtf 100 | 76 | 4.17 / 10.27 | 17.9 (0.238) | 69.1 (3.44) | 41 | 100.0 / 19.7 |
| rtf 1000 | 76 | 7.19 / 12.82 | 23.4 (0.915) | 69.8 (5.93) | 95 | 1000.0 / 10.8 |
| m400 rtf 1 | 192 | 8.23 / 12.40 | 4.8 (0.196) | 38.7 (2.68) | 38 | 1.0 / 0.0 |
| m400 rtf 100 | 428 | 8.87 / 14.62 | 21.7 (0.425) | 64.5 (6.53) | **419 (23%)** | 100.0 / **0.0** |

- View total (gather+json+wire) p50 = 3.84 ms + 11.1 µs/body (least squares over the 7 body counts; marginal 39→428 bodies = 12.2 µs/body). View alone reaches the 16.7 ms deadline at **≈1,100 bodies**. At m400 rtf 1, JSON serialisation alone is 3.83 ms p50 (192 bodies) — the wire is per-body linear too.
- **Engine per game-second falls with rtf** (3.5 ms/game-s at rtf 1 → 0.35 at rtf 100 → 0.088 at rtf 1000): fleet-battle work is per *presented frame* (slices capped by the retarded light deadline, `universe.rs` `resolve_fleet`), not per game-time; kicks do scale with game time (7 → 284 → 1,360 → 5,538) and with members (1,360 → 8,383 at m400).
- **The burst tail is the deadline risk and threads cannot buy it out:** engine p99 5.3–6.3 ms in *every* config; at 8 threads rtf 100 improves (frame p50 4.17→1.40, gather 3.44→0.98, overflow 41→3, rtf low 1% →100) but m400 rtf 100 gets *worse* overflow (419→451) with engine p99 unchanged (5.73→5.74) and rtf low 1% still 0.0. Elevating the budget (`--engine-ms 15`) clears overflow (41→4) but pushes engine max to 16.3 ms and frame p99.9 to 19.0 ms — over the deadline: the burst is indivisible, not starved.
- **Distinct kick cost is not the frame problem:** kick-bench median 60.4 µs (leavers 366.5 µs); exact memo hit 0%, quantized 3.7% — reproduces the 5 October finding on this build.
- **Schedule independence holds on the bench:** identical digest `41343a14…` at cut 609076340 across 1 thread / 8 threads / 15 ms budget.
- **Known state reproduced:** E1–E5, E7, E8 PASS (E6 fails only on missing `prepared-mutants.json` artifact state); `behave --law plane`: B13 60/64 (known marginal), B12 known-miscalibrated, **B14 times out at its 60 s limit on the plane** (not in HANDOFF's state list), G/B7-class probes unanswered by the plane wrapper (they gate `--law space`). The scripted player dies at rtf 1000 (`player_alive: false`) — the script's own warned failure mode (a burn spans 16.7 game-s), not an engine refusal.

## Predictions

`predictions.md` was written before the sweep. What happened: (1) engine-share crossover by rtf 100 — **wrong**, the engine peaks at 23%, the view stays ~70% at every rtf; (2) delivered-rtf ceiling ≈ 86× — **wrong**, rtf 1000 delivers median 1000 because engine work per game-second falls with rtf (fleet slices are per-frame, retarded-deadline-capped — found in `resolve_fleet`, not assumed); the predicted stall showed up in the *tail* instead (low 1% = 10.8, and 0.0 at m400); (3) budget elevation moves the ceiling — held for overflow (41→4) and rtf low 1% (19.7→100), missed the tail worsening (p99.9 19.0 ms); (4) members scale engine cost — held at rtf 1 (3.5→14.6 ms/game-s), sublinear at rtf 100 (leavers leave and die); the "ceiling ≈10×" number was wrong; (5) view floor — held (3.1–7.9 ms, grows with bodies, which grow as leavers become bodies); digest identity across schedules — held. The two wrong predictions share one cause: I modelled engine cost as per-game-time before reading `resolve_fleet`; the fleet is causally bounded per frame. Kill criterion (delivered rtf ≥ 500 at target 1000) fired — reported as such.

## What would make it wrong

The gather is explicitly a debug instrument ("For now this is physics, not visuals", docs/plane.md). If the production view is O(visible) by construction (zoom-as-minimap), the gather constraint is scaffolding and the durable findings reduce to: the burst tail (thread-immune, 23% overflow, rtf stalls to 0) and the engine's per-game-second cost at scale. Also: one machine, one seed per config, Linux x86 (orders of magnitude only — the integrator re-measures on the M1); the gather's µs/body on M1 efficiency cores could be ~2–3× worse. B14's timeout could be my runner's shared load rather than the plane's cost (it ran alone, load ~1; still, single observation).

## Cost of adopting, and fit

Adoption cost: zero code; a priority order. The redirect: (a) treat the view gather's LOD — "the zoom level is the minimap" (OC#30) — as a first-class bottleneck item, since "Nothing is evolved that can be derived when looked at (clocks, redshift, views)" (PRINCIPLES #3) and the gather re-derives every emitter's crossing every frame; (b) keep the slack skin (b-encounter-skin) as the p99 lever — it is the only measured fix for the thread-immune bursts; (c) the kick ladder stays the lever for engine cost *per game-second* at scale, not for frame smoothness. An hour saved at the bottleneck is the whole system's; an hour saved in the engine's p50 is, today, a 1.3× mirage.

## The lens

A frame-throughput audit cannot see the compiler's cost per body-bit at billion scale — the board's kick-first order may still be right against the 190-core number even though the engine is 5–23% of the player's frame; I measured the game the player runs, not the universe the compiler must mint. I also did not touch the GPU path (E1 reports `metal=false` here) and read the fleet's per-frame bounding from code after the prediction, not from an independent measurement of the battle's lag behind the light cone at rtf 1000 — whether the fleet's committed tick visibly trails its retarded deadline at high rtf is the natural next probe.
