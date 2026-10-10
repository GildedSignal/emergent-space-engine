# Dossier — 20261010-2141-constraint-ae40 (lens: the constraint)

## Claim

On the plane as it flies on main, the frame's constraint is not the kick cadence the board attacks: the median frame is view-bound (the gather is 65–70% of frame CPU, ~13 µs per emitter per frame at 60 Hz, independent of rtf) and the tail frame (p99) is engine-bound by *single player events* that overrun the 5 ms budget (1.3–3.4 ms per event, growing with the doll's population through an O(doll-bodies) encounter scan), while the engine's median is 0.25–0.4 ms — i.e. the board's "fewer kicks per orbit" work optimizes the cheapest 17% of the frame.

## Bottleneck

Board focus #1 ("kicks dominate the engine's cost") is measured at the wrong level: on the plane as-flown, kicks are a minority of the *frame*. The gain from redirecting attention: the frame p99 at 400 fleet members is already 14.5 ms of 16.7 ms (87% of budget) with zero hitches left to give; the two levers that relieve it (the view readout's cost = the queue's b-readout build; the encounter scan = the Binet cone seam) are both already queued — this measurement ranks them first and second. Expected gain at the frame level: view change-gating or per-pixel sampling deletes most of 70% (>3× median frame); capping the single-event spike moves p99 by 2–3×.

## Evidence

Machine: shared Linux x86, i7-4790, 8 vCPU, load 0.5–1.0 during runs, recorded in each JSON (`machine_before/after`, `uptime_before/after`). Orders of magnitude only (Linux/x86; the integrator re-measures on the M1). All commands ≤ 60 s, binary `/home/glmlab/lab-target-1/release/xtask` (repo `target/` is redirected there by `CARGO_TARGET_DIR`), JSONs in this folder.

```
cargo build --release -p xtask
xtask universe --bench --rtf 100  --seconds 30                 # bench-rtf100.json
xtask universe --bench --rtf 1000 --seconds 30                 # bench-rtf1000seconds30.json
xtask universe --bench --rtf 10000 --seconds 20                # bench-rtf10000seconds20.json
xtask universe --bench --rtf 10000 --seconds 20 --threads 4    # bench-rtf10000-t4.json
xtask universe --bench --rtf 100 --seconds 30 --members 200    # bench-m200-rtf100.json
xtask universe --bench --rtf 100 --seconds 30 --members 400    # bench-m400-rtf100.json
```

Scene (fixed, `--describe`): 4 dolls, 28 bodies + one fleet of `--members` (76 bodies total at default 48). Frame = engine advance (budget 5 ms, causal-deadline order) + view gather + JSON + wire, paced 60 Hz, scripted burns every 4 game-s.

**The median frame is view-bound** (share of frame CPU):

| run | frame p50/p99 ms | engine p50/p99 ms | gather share | engine share |
|---|---|---|---|---|
| rtf 100, m48 | 4.42 / 10.53 | 0.25 / 5.17 | **0.697** | 0.172 |
| rtf 1000, m48 | 2.06 / 5.91 | 0.28 / 4.24 | **0.654** | 0.266 |
| rtf 10000, m48 | 9.24 / 11.83 | 4.66 / 6.22 | 0.444 | **0.520** |
| rtf 100, m400 | 8.71 / 14.50 | 0.41 / 6.05 | **0.640** | 0.221 |

The gather is ~per-emitter per-frame: m400 has 428 bodies, gather p50 6.23 ms ≈ 13 µs per body (a Newton crossing of the past light cone per body, plus a per-member extrapolation pass for in-frame fleet members). It does not fall with rtf (rtf 1000 ≈ rtf 100) because it is paid per *presented frame*, not per event.

**The engine's tail is single-event-shaped, not load-shaped.** Engine p50 0.25 ms but p99 5.17 ms and max 11.95 ms at rtf 100 with a 5 ms budget: the budget is checked between items only (`Budget::spent` in `advance`), so one item can spend 7–12 ms alone. Per-item costs by kind (rtf 100):

| members | player µs/item | ship µs/item | fleet µs/item | overflow frames / 1800 |
|---|---|---|---|---|
| 48 | **1315** | 268 | 60 | 42 |
| 200 | **1570** | 101 | 24 | 146 |
| 400 | **3432** | 106 | 42 | 413 |

The player is the most expensive body in the universe, 5–12× a ship, and its cost *grows with fleet size*: `PlayerNeighbourhood::find` (crates/universe/src/encounter.rs) tests every body in the player's doll per player event, and fleet members handed out of the frame become bodies in that doll (ship items 1542 → 15749 from m48 to m400 are leaver kicks). This is the board's top scaling risk (q-candidate-degree) already measurable at N=428: frame p99 14.5 ms, overflow in 23% of frames, rtf lowest-1% at 0.0.

**The throughput ceiling behaves as designed.** At rtf 10^4 the engine budget binds at the median (p50 4.66/5.0 ms, 34% overflow) and the cost appears as a real-time-factor dip (lowest 1% = 8.4), *not* as a hitch (worst frame 12.6 ms, zero hitches above 16.7 ms anywhere in this run set) — plane.md foundation 7 holds on this machine. Threads (4) nearly halve the ships' wave cost (engine p50 4.66 → 2.46 ms at rtf 10^4, overflow 415 → 226) but do not touch the player, fleet or gather (single-threaded paths).

Anomaly kept honest: m200's gather p50 (1.90 ms) sits below both m48 (3.46) and m400 (6.23); the gather tracks *live bodies in view* (leavers handed out, deaths), not the member knob alone. One reading, not a trend.

## Predictions

`predictions.md` was written before the sweeps, after the rtf-100 baseline. Scored there: engine p50 grows ~10× by rtf 1000 (wrong: it stays 0.28 ms — events cluster and per-item cost *falls* 268→83 µs from cache warmth; the work is event-cadence-bound, not game-time-bound); budget binds at rtf 10^4 (right); no hitches above 16.7 ms (right, and the overflow is absorbed as rtf dip exactly as designed); members 400 keeps the frame view-bound with the player ≥4× the max per-item cost (right: 3432 vs 106); threads help modestly (partly right: 1.9× on the ships' wave, nothing elsewhere); the engine spike is cadence-shaped not load-shaped (right in kind, wrong in mechanism: it is *player-event*-shaped — the O(doll) scan — not kick-boundary alignment).

## What would make it wrong

- The gather's 70% share is a property of the debug view's one-Numeric-crossing-per-body design; if the integrator's intended player view was always per-pixel sampled (galaxy style), the "view-bound" finding names a component scheduled for replacement, not the engine. The M1 could also shift shares (different memory latency); ratios, not absolutes, carry the claim.
- Per-item µs at rtf 100 mix cold/warm caches and shared-machine noise (±30% by the handoff's own note); the player-vs-ship ratio (5–12×) and its monotone growth with members are the robust part, seen on all three member points.
- The O(doll)-scan attribution for the player's cost is read from the code path (`encounter.rs` header, `find` iterating the doll) plus the growth curve; I did not instrument the scan itself (a profiler pass on one player event would pin it exactly).

Cost of adopting: zero code — a priority order for queued builds (b-readout first, the Binet-cone seam second, kick-cadence work third) and one new fact for the encounters design (the player's own events are where candidate work lands first). No gate is touched; no crate is changed.

Fit with PRINCIPLES: "Compute only surprises" (#3) — the gather pays per emitter per frame for crossings that mostly moved sub-quantum, and the budget pays per item but not per candidate; "the algorithm that allocates the work to prevent those heavy tails, it's the most important one" (#12) — the p99 is exactly where one un-preemptible item breaches the budget; "the simulation tells us what's next not us" (#22) — the O(doll) sweep is a heuristic where the law's own cone would decide. It also obeys the frame-budget contract: the budget changed *when*, never *what* (digests canonical at the cut, all runs).

## The lens

Goldratt's discipline forced the whole-frame measurement, and the whole is what moved the answer off the board's list; what the lens may have missed: I did not run the behaviour gates (`behave --law plane`) — the lens's "which gate fails" is taken from HANDOFF (B13 60/64, B12 miscalibrated, E9 fails phase 1 by design) rather than re-measured, and I did not profile a single player event to decomposition; the O(doll) attribution is code-read + curve, not instrumented.
