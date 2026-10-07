# The allocator is one mechanism, and the plane already has it; the paper one is unused, and the one missing rung is per-region staleness

## Claim

The plane's frame loop (one causal-deadline heap, a wall budget, a global horizon) already **is** the engine's whole allocator: outcomes are bit-identical across budget, thread count and pace under overload (12 runs, one digest per scene), and overload degrades without a single hitch — but only for *bursts*. Under **sustained** overload the global horizon collapses the player's presented time ~600× (a cliff, not the budget-proportional dip), because any region that cannot catch up freezes the *whole* presented time. The allocator work worth doing is that one rung (engine.md rule 8 rung 2: a lagging region's sky goes stale; the player never waits), not a scheduler: `crates/allocator` + `xtask/src/regions.rs` — the paper machine (certificates/slack/forecasts/QoS) — is used by nothing in the plane and is a retirement candidate.

## Bottleneck

Board bottleneck 4 (smoothness and the allocator; Julien: "the algorithm that allocates the work… it's the most important one", register: *adopted, not built* — and it is in none of the 14 queued builds). This run replaces the open design question with a measurement and a deletion: the queue exists, works, and needs one rung, not a cathedral.

## Evidence

All numbers from shipped code, Linux runner (8 vCPU shared, orders of magnitude only), `cargo build --release -p xtask` once; each command ≤ 40 s. JSON reports in `out/`, per-frame traces as described below.

1. **The digest never moves** (the "budget changes *when*, never *what*" premise, plane.md foundation 7, tested at three knobs under load):
   - members 48, rtf 100, 12 s: identical digest `a0096d59e1…` for engine-ms {5,1} × threads {4,1} × paced/unpaced (4 runs).
   - members 400, rtf 1000, 12 s: identical digest `bfacdfc5bb…` for engine-ms {5,2,1,0.5} × threads {4,1} (6 runs) — i.e. through **100 % overflow frames** with the budget cut 10×.
   - members 48, rtf 1000: digest `ddaeac1cdd…` (1 run; the scene differs, so its digest differs by design).
   ```
   cargo run --release -p xtask -- universe --bench --seconds 12 --rtf 1000 --members 400 --threads 4 --engine-ms 2
   ```
2. **No hitches anywhere**: worst frame 16.64 ms across every overload run (h16 = 0 in all 12; one 8-second rerun caught a single 17.3 ms frame). Overload never produces a tail; it produces time dilation. `worst_hitch_ms`, `hitch_counts` in every report.
3. **The cliff (sustained overload)**, members 400, rtf 1000, threads 4: engine-ms 5 → 2 keeps events/s budget-proportional (2963 → 934; threads 1: 3528 → 1490) but the achieved RTF collapses 309 → 0.03 (threads 1: 1000 → 0.12). Per-frame instrumentation (this run's patch, env `UNIVERSE_TRACE=1`, prints `target horizon events overflow` per `frame_to`; tree restored by `run.sh` after the run): advance of presented time per frame falls 523 305 → 845 ticks (~600×), while frame wall stays ~9–12 ms. Mechanism, from the code: the horizon is the **global** minimum of unresolved light-delayed deadlines (`crates/universe/src/universe.rs` `advance`, 789–833, and `frame_to`, 862–874); one group that cannot clear (the fleet) clamps the player's presented time to its own chain. Bistable, not proportional: either the mandatory window clears (full rtf) or presented collapses to the binding region's rate.
4. **Transient overload is exactly as designed** (foundation 7: "a brief, smooth dip… never a hitch"): members 48, rtf 1000, default budget: median 1000×, lowest 1 % 619×, 30 overflow frames, h16 = 0.
5. **The wave pessimizes as wired**: `resolve_wave` fires for every ship whenever threads > 1 (one budget unit per wave, kind-triggered, not density-triggered). members 48: engine p99 5.53 ms (4 threads) vs 2.04 ms (1 thread); members 400: events/s 2963 vs 3528, stall 0.03 vs 0.12. Shared-runner caveat: orders of magnitude; the M1 (4P+4E) must re-measure before anyone deletes the wave.
6. **The paper allocator is unused by the plane**: `grep -rln "emergent_allocator"` → only `crates/allocator/{examples,tests}` and `xtask/src/regions.rs` (the old regions judge). `crates/universe` implements its own queue.

## Predictions

Written before the decisive runs (`predictions.md`). P1 digest invariance: **held** (all runs). P2 smooth degradation: **half-held** — no tail explosion (h16 = 0 everywhere), but the RTF dip is a cliff under sustained load, not smooth in the proportional sense; my "no cliff / rtf stays > 25 % of the previous rung" criterion failed at engine-ms 2. P3 (wave ≥ 1.5× *better*): **inverted** — the wave is 1.5–2.7× worse on every metric measured. P4 (members 48 never overflows at rtf 1000): **wrong** — 30 overflow frames at the default budget, 19 even at rtf 100.

## What would make it wrong; cost of adoption; fit

- Wrong if: the M1 flips the wave result (5); per-region presentation ever changes a digest (it must not: present stale is a view choice over committed state, and the digest is taken at the cut after `settle` — but this is asserted from the design, not yet measured); or region scale (10⁵+ live entities, many dolls) needs cross-region priority the single heap cannot give — the crate's QoS ideas would then return.
- Cost: near zero for the finding (measurements on main); the fix is one rung in `frame_to`/`advance` (horizon from the player's own chain plus per-region staleness marks), red-teamed by B8-style digest checks; the wave needs a density trigger (or an off switch) after an M1 re-measure.
- PRINCIPLES: 1 ("the best part is no part" — delete the second allocator), 12 (p95/99 and the allocator — here measured, not designed), 22 ("the simulation decides" — the horizon already reads the queue, not a forecast), 5 (slack not proximity — the deadline order already is light-cone slack). Engine.md rule 8 rung 2 and plane.md foundation 7 are the owned sentences this measures.

## The lens (what it may have made me miss)

The system lens unifies; the hard special case is the co-orbital formation itself: a tight fleet's members share nearly one deadline, which is exactly where the global horizon is weakest — my overload scene *is* the adversarial case for my own "one queue is enough" claim, so the unification is proven only at the plane's scale, not at region scale where memory pressure joins time as the scarce thing. Also: 8 vCPU shared timing, single scene family (one system, one player), and the trace's `events` column is contaminated by the post-loop `settle` calls (the horizon column, read over the first 480 lines, is clean).
