# log.md — 20261012-0358-autoresearch-ff43 (autoresearch lens)

Artifact: the plane's kick resolver (`step::process`, judged by `xtask universe
--kick-bench`, a deterministic replay of every distinct pending ship kick on the
plane's own scene). Metric: `kick_us_all` median (ns per kick event — board
bottleneck #1: "kicks dominate the engine's cost"). Certificate: the bench's
`replay_digest` and the universe `digest` must stay bit-identical.

Machine: GitHub Actions Linux runner, 8 vCPU i7-4790-class x86-64, shared, no perf
(perf_event_paranoid=4). Orders of magnitude only.

| # | Hypothesis | Change | Measurement (seed 1, rtf 100, 30 s) | Kept? |
|---|---|---|---|---|
| 0 | baseline | — | med 77–84 µs, p99 ≈ 380–440, n=1158; stable digests across 3 runs and 2 builds | — |
| 1 | find the kick's phases | thread-local phase timers + op counters (patch `instrumentation.patch`) | fit (`Rebinding::from_state`) = 63.9 µs/kick = **82%**; inside it `Orbit::compile` 48.8 µs (≈66 quadrature panels × 4 nodes), `OrbitShape::new` 0.5 µs, passages 3% of kicks × 332 µs; ops per kick: 595 `div_word`, 437 `cos`, 113 `isqrt` | instrumentation |
| 2 | shape memo would hit | count distinct `ShapeKey`s during builds | **1125 builds, 1125 distinct keys** — an exact shape cache can never hit (confirms the 5 Oct memo artifact at the shape tier) | knowledge |
| 3 | H1: cheaper exact `div_word` (single `divq` asm; `u128/u128` fast path) | microbench `bench_div.rs`, 200k random operands, all bit-equal to the shipped implementation | ref 26.0 ns, asm 21.9 ns, u128/u64 22.6 ns → ≤ 3% of a kick | **reverted** (<10%) |
| 4 | H2: `isqrt` Newton via word division instead of `__udivti3` | same harness, 100k operands, bit-equal | ref 89.2 ns vs 90.4 ns → 0% | **reverted** (0%) |
| 5 | H3: cheaper `cos` (13 nested factors) | derivation only | the loop is a serial dependency of floored products; any different evaluation order changes the integer result. No bit-exact win exists short of evaluating the same 26 multiplies | **not attempted** |
| 6 | lazy shape table (compile panels near the body, extend on demand) | code reading | blocked: `Orbit::state()` computes `cycles = normalized.div(period)`; the period's exact bits require the full adaptive quadrature, so laziness changes bits. Escaping it (incremental cycle count in the binding) changes the body record → digest | **dead (bit-exactness)** |
| 7 | `from_state`'s `fit.residual` is dead work in the kick path | grep consumers | true (only space's `events/handoff.rs` reads it; universe's `bind_in` builds its own residual). A lazy residual saves 3.65 µs/kick = 4.8% | **reverted** (<10%, touches a frozen crate) |

Stop rule hit: three consecutive measured candidates (3, 4, 7) each < 10%.
Tree restored to pristine (only this run folder remains).
