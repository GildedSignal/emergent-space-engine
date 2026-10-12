# 20261012-1524-constraint-2bb7 — the constraint lens on the flying plane

## Claim

At flight pace (rtf 100) the presented frame's constraint is the **view pipeline, not the engine**: gather + JSON + wire take 49–72 % of frame CPU at every measured scale, grow linearly in presented emitters with no cadence, and bust the 16.7 ms frame at ≈1.7k presented bodies (p99 already ≈10 ms at 410), while the engine — the board's #1 — only saturates its 5 ms budget at the same scale and stays at 24–32 % share; and 75–78 % of live emitter-frame pairs change by less than a display quantum, so the cheapest lever is **view cadence (compute only surprises), before cheaper readouts or fewer kicks**.

## Bottleneck

The board's live question #1 (fewer kicks per orbit) and the queued build `b-readout-cost` both attack the engine/gather's per-item constant. Measured on the whole, that is the wrong constraint today: the view recomputes and re-serialises every emitter every frame unconditionally. Cadence bounds the variable cost at ~25 % of today's (~4×) at flight pace without touching what the player differentiates; the readout constant and the kick count act only on the remainder.

## Evidence

All runs unpaced (compute time only), thread 1, seed 1 unless noted, Linux x86 8 vCPU shared (loadavg 1.6–2.4; orders of magnitude only — the M1 re-measures). Binary: `~/lab-target-2/release/xtask` (built from this tree; the tree carries this run's instrumentation, see below).

The scaling table (`where_the_time_goes_ms`, p50 ms per frame):

| config | bodies | frame p50 (p99) | gather p50 | engine p50 | json p50 |
|---|---|---|---|---|---|
| rtf 1, m 48 | 28 | 0.63 (0.73) | 0.46 (72.5 %) | 0.023 (3.9 %) | 0.10 |
| rtf 100, m 48 | 71 | 1.01 (3.3) | 0.76 (64 %) | 0.052 (24 %) | 0.10 |
| rtf 1000, m 48 | 76 | 1.68 (5.6) | 1.08 (64 %) | 0.228 (30 %) | 0.08 |
| rtf 100, m 400 | 410 | 4.76 (10.1) | 2.99 (54 %) | 0.42 (32 %) | 0.66 |
| rtf 100, m 2000 | ~1750 | 20–21 (32) | 10.5 (49 %) | 5.2 (budget-saturated) | 4.1 |
| rtf 100, m 8000 | 4253 | 50.4 (65) | 30.1 (7.1 µs/emitter) | 5.1 (saturated) | 12.2 |

- Gather is O(N) per frame, uncapped: 5.6–10.6 µs per emitter per frame from 71 to 4253 bodies. rtf median holds 100 up to m 400 and collapses at m 2000 (rtf 0.0024; overflow 275/300 frames).
- **Surprise measurement** (this run's instrumentation): the fraction of live emitter-frame pairs whose direction (<1e-4 rad ≈ ⅕ px at 60°/1080 px), shift (<1e-3) and angular radius (<1e-4 rad) **all** changed less than a display quantum since the previous frame: **75.0 % / 78.2 % / 78.3 %** (seeds 1/2/3, m 2000, rtf 100, 390k–582k comparisons). At rtf 1 the same scene is 15 % (the view really is moving at 1×; the freeze appears at flight pace).
- The crossing solve is already cheap: 0.55–0.57 tube readouts per emitter-frame at m 2000 (the Newton memo works). The 6–7 µs/emitter is the unconditional recompute + serialise, not the solve.
- Engine: `engine_cost_by_kind` at rtf 100 m 400 — ship 69 µs/item, player 368 µs/item, fleet 20 µs/item; kick-bench (`--kick-bench --seconds 5 --rtf 100`): distinct pending kicks median 35 µs (p99 86), leavers 94 µs; quantized cycle-memo hit 89 %, exact 0 % (matches the 5 October correction). The 5 ms engine budget is only reached at ≳1.7k bodies.
- Gates on main, for the record: `behave --law plane` — B13 60/64 (matches handoff), B12/B14 known-broken-or-timeout here (B14 hit the 60 s limit on this shared box), G1–B11 unanswered for the plane law; `engine-judge` — E1–E5, E7, E8 pass, E6 UNSUPPORTED (missing prep artifacts on this runner), E9 fails phase 1 as designed. Nothing new fails; this run's edits touch only xtask's bench/session.

Commands (each ≤ 60 s):

```
cargo build --release -p xtask                       # CARGO_TARGET_DIR=~/lab-target-2 on this runner
$X universe --bench --unpaced --seconds 10 --rtf 1   --seed 1
$X universe --bench --unpaced --seconds 10 --rtf 100 --seed 1
$X universe --bench --unpaced --seconds 10 --rtf 1000 --seed 1
$X universe --bench --unpaced --seconds 5  --rtf 100 --members 480   # clamped to 400
$X universe --bench --unpaced --seconds 5  --rtf 100 --members 2000 --seed {1,2,3}
$X universe --bench --unpaced --seconds 5  --rtf 100 --members 8000  # 1.98 GB RSS: the memory cap
$X universe --kick-bench --seconds 5 --rtf 100 --seed 1
$X behave --law plane ; $X engine-judge
```

`--members` > 400 needs this run's patch (xtask/src/universe/mod.rs clamp 4→20000) plus the `view_surprise`/`view_readouts` fields in xtask/src/universe/session.rs and mod.rs; the patch ships with the run.

## Predictions

`predictions.md` was written before the sweeps. D1 held in direction, missed in size: engine share rises with rtf (24 % → 30 %) but never approaches the budget at ≤76 bodies, and even at rtf 1000 the view keeps 64 %. D2 held: view pipeline crossed 16.7 ms between 410 and ~1.7k bodies (predicted 1–2k), linear per emitter. D3 held (gates as per handoff; B14's timeout is this box's). The unregistered surprise (75–78 % below quantum) exceeded what D2 implied.

## What would make it wrong, cost, fit

- **Wrong if** the game as flown spends most time at rtf ≫ 1000 (engine then dominates), or if the browser-side cost dwarfs the server frame (the bench excludes it — the view's share is then a *lower* bound, not an overestimate), or if the display quantum is judged smaller than 1e-4 rad/1e-3 (tighten it and the 75–78 % falls; the measurement, not the conclusion, is quantum-dependent). Shares, not absolute times, carry the claim across machines.
- **Cost of adopting:** per-emitter cadence in `ViewCache` (refresh when the emitter's own rate of change says its (direction, shift, radius) crossed a quantum) plus a delta wire. No law change; the digest is unaffected (observation stays pure — cadence changes when the same pure value is recomputed, i.e. instrument latency, never outcomes). Bounded staleness on fast emitters must come from their measured rate of change, not a fixed TTL.
- **PRINCIPLES:** "Compute only surprises. Cost follows change and entropy" (#3) — 3 of 4 emitter-frames compute nothing the player can differentiate; "The view is an instrument" (#28) — the instrument today has no display quantum; "a body resolves only the influences that are significant at its own scale" (#33) — the player symmetrically resolves only emitters significant at their scale. plane.md §7 already demands bounded work per presented frame; the gather/json/wire are today the frame's one unbounded synchronous claim.
- **Where the constraint moves next:** after view cadence, the engine's event rate binds (5 ms budget saturated at ≳1.7k bodies at rtf 100; kick window setup 92 % per the 6 October gold) — the board's #1 is the *second* constraint, not the first. At rtf ≤ 10 the view stays the constraint down to ~100 bodies.

## The lens

The constraint lens measures the whole as it flies today — one star system, one battle scene, no browser, no galaxy doll — so it cannot see constraints that only exist at the next scale (H_live, encounters at N, the light cone's growth). It treats the shipped bench as the game; Julien's page adds DOM/canvas cost on top. It also inherits the bench's scene: the 75–78 % below-quantum figure is a fleet-battle geometry (dense, co-moving small emitters seen from afar); a scene of many bright nearby emitters would freeze less — the measurement should be re-run on such a scene before freezing any cadence gate.
