# Autoresearch log — run 20261011-1456-autoresearch-bb4d

Artifact: the plane's kick resolver (`crates/universe` step/bind → `crates/space` orbit compile).
Metric: median µs per distinct kick (`xtask universe --kick-bench --seconds 20`, `KICK_REPS=9`, median of 9 replays per kick; resolver is pure).
Behaviour constraint: bit-identical digests (plane canonical-cut digest + kick replay digest + crate tests).

## Instrument built first
- `emergent_space::lab`: 12-slot atomic phase accumulator, zero-cost when off (`crates/space/src/lib.rs`).
- Phase timers: readout / ctx / forces+quantize / rebind {from_state {fit_key, compile}, decode} in `crates/universe/src/{step,bind}.rs`; quad / cut / tail_quad / cos / quad-call-count in `crates/space/src/orbit.rs`.
- kick-bench: `KICK_REPS` (median of K replays per kick), `KICK_PHASES` (phase report).

## Baseline (seed 1, 32 kicks: 23 made, 9 leavers)
made median 42.4-64.2 µs, leaver median 361.6-382.4 µs, all 44.4 µs (spread = shared-box noise).
Attribution: **rebind 87% of tracked time; compile 84% of a kick (90.2 µs/kick); quad 129.4 µs/kick over ~140 quad calls/kick (~60 for a cycle kick, ~450 for a passage kick); cut 9.2 µs; fit_key 4.6 µs; decode 5.5 µs; readout 4.4 µs; ctx 8.4 µs; forces 1.3 µs.** Per node ~170-240 ns.
Digests: plane 46d63fe0cb18daee…, replay f3e04738b88805ce… (instrumentation is behaviour-neutral: both unchanged).

## Round 1
- Hypothesis: fast_quad's four native u128/u128 divisions (`__udivti3` software division) dominate the node.
- Change: guarded exact word division `div_u128_word` (div_word when `n>>64 < d ≤ 2^64-1`, native division otherwise) for g, g1, ratio, rt in `fast_quad` (`crates/space/src/num.rs`, `orbit.rs`).
- Measure: made 39.1-57.9, leavers 364.2-382.4 µs — **0% on x86 (kept: bit-identical, digests equal; on aarch64/M1 `__udivti3` is fully software, so the gain there is unmeasured but strictly non-negative)**.
- Verdict: hypothesis WRONG on this CPU (LLVM already lowers these 128/128 divisions well). Reverted? No — kept as a free exactness-preserving cleanup; it is not the lever.

## Round 2
- Hypothesis: `cos` (13 nested factors per node) dominates the node.
- Measure: cos total 28.85 µs/kick of which ~25 µs is the instrumentation's own two `Instant::now()` per call (560 cos calls/kick × ~45 ns) → **cos itself ≤ 10 ns/node ≈ 4% of node cost**. Hypothesis WRONG.

## Round 3 (analysis, not a code change)
Per-node cost is distributed (isqrt, 4 word divisions, i128 products, shifts; per-panel Knot push + 5-integral Scalar add). No single component exceeds ~15% of the node. Three rounds in a row under 10% → STOP per the lens rule.

## Structural read (what the attribution implies)
The kick's cost is not an arithmetic hotspot; it is **panel count × ~200 ns**: a weak-field passage walks ~320 dyadic band appends + ~107 tail panels from band 1 out to the passage edge; a cycle ~50-60 panels. The band walk is intrinsic to the certified crossing table (every band in the radial window is a real crossing), so the 10× lever is representation-level: fewer certified cut points per compile (coarser band grid where no certificate consumes the crossings), or not recompiling (the shape memo measured 0% hit rate on this workload — 26 distinct shapes from 26 rebinds — so reuse as designed does not help the plane).

## Held-out set (run once, final configuration)
- seed 7: made 67.8, leavers 471.7, all 75.0 µs, refused 0.
- seed 13: made 44.9, leavers 386.8, all 45.5 µs, refused 0.
- Whole plane `--bench --rtf 100 --seconds 20 --unpaced`: digest **6ce636fa13458efb… IDENTICAL to baseline**; engine share 0.207 vs 0.202; ship 80.7 vs 70.0 µs/item (shared-box noise, same order).
- `cargo test --release -p emergent-space`: 40 tests, all green.
- Prediction "1.3-1.8× faster" FAILED on x86 (the divisions were not the cost); the exactness prediction held everywhere (all digests identical, zero refusals).
