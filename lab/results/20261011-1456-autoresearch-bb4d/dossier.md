# Dossier — run 20261011-1456-autoresearch-bb4d (lens: autoresearch)

**Claim.** The plane's kick cost is 84% `Orbit`/`Passage` compile, and that cost is panel count (~140 quadrature panels per kick; ~450 for a fleet member's passage) times a flat ~200 ns/node with no arithmetic hotspot — so the next 10× must come from the representation (fewer certified cut points per compile), not from micro-optimization; the one micro-change tried (exact word division for `fast_quad`) is bit-identical and free but buys 0% on x86.

**Bottleneck.** Board #1: "kicks dominate the engine's cost … cheaper events" (ns per event). Measured on the plane: ship 70 µs/kick, player 344, fleet member 364-472 µs/kick. Expected gain from the attribution: it redirects the lever from arithmetic to panel count.

**Evidence** (all commands ≤ 60 s; Linux x86 shared runner, orders of magnitude only):
- Baseline: `KICK_REPS=9 xtask universe --kick-bench --seconds 20` → made median 42-64 µs, leavers 362-382 µs, 32 kicks; plane digest `46d63fe0cb18daee…`, replay digest `f3e04738b88805ce…`.
- Phase attribution (`KICK_PHASES=1`, same command): rebind 92.9 µs/kick (87% of tracked), compile 90.2 µs/kick (84% of a kick), quad 129.4 µs/kick over ~140 quad calls/kick, cut 9.2, fit_key 4.6, decode 5.5, readout 4.4, ctx 8.4, forces 1.3.
- Round 1 (guarded exact `div_word` for the four u128 divisions in `fast_quad`): digests unchanged, 0% speedup on x86 → the divisions are not the cost (LLVM lowers them well); kept as an exact cleanup, likely a real gain on aarch64 where 128/128 division is fully software (unmeasured here).
- Round 2 (timed `cos` inside quad): ≤ 10 ns of ~200 ns per node → not the cost.
- Exactness on the whole plane: `xtask universe --bench --rtf 100 --seconds 20 --unpaced` → digest `6ce636fa13458efb…` **identical** to the pre-change baseline.
- `cargo test --release -p emergent-space` → 40 tests green.
- Full log: `log.md`; instrument: `emergent_space::lab` phase timers + `KICK_REPS`/`KICK_PHASES` in the kick bench (all in this run's patch).

**Predictions** (`predictions.md`): the speedup prediction (1.3-1.8×) **failed** on x86 — honest miss, the division hypothesis was wrong on this CPU. The exactness predictions all held: identical digests on every held-out case (seeds 7 and 13: made 67.8/44.9 µs, leavers 471.7/386.8 µs, `refused: 0`; whole-plane digest identical; tests green).

**What would make it wrong.** A node-level hotspot that only shows on the M1 (different division/isqrt costs) — the x86 attribution could mislead there. The panel-count reading assumes the band walk is intrinsic to the crossing-table certificate; if a consumer of `crossings` tolerates a coarser band grid, the compile could shrink 10× without touching nodes, which would falsify "the lever is not arithmetic".

**Cost of adoption.** Small: the guarded `div_u128_word` is exact (digest-proven), a few lines in `crates/space/src/num.rs` + `orbit.rs`; the phase harness is env-gated and zero-cost when off (keep for the next runs, or drop before merge). Fit with PRINCIPLES: "the cheapest compute is compute not done" (P1) — the finding says the compute not done is panels, and "A fix signals the wrong representation" (P19) — micro-fixes inside the node are the wrong layer.

**The lens's blind spot.** A local search finds local optima: I confirmed no in-node 10× exists on x86, but the structural change that beats this result is at the representation level — (a) compile passages with a coarser certified band grid where no certificate reads those crossings, or (b) amortize the shape's band table across kicks by caching `OrbitShape` per `ShapeKey` **with the tail keyed by the passage edge** (the memo's 0% hit rate measured shape reuse, and this bench's 26 rebinds were 26 distinct shapes, so reuse must be argued from a richer workload — e.g. fleets that hand out members on similar outbound tracks — before it is worth building).

**Grade asked for:** silver — real, reproduced, digest-verified attribution that redirects the board's #1 lever (cheaper events → fewer panels per compile), one exact change adopted, and the next run's experiment named; not gold because nothing moved 10×.
