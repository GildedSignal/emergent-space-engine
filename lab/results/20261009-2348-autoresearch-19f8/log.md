# log.md — autoresearch loop on `Rebinding::from_state` (crates/space)

Artifact: the plane's per-kick compile (`fit_key` cubic inverse + `Orbit::compile` quadrature + binding trig + residual decode). The board's #1 question is kicks ("kicks dominate the engine's cost") and the taste log says the plane recompiles an orbit on ~99% of kicks — so ns per rebind is the engine's per-kick cost.
Metric: ns per `Rebinding::from_state` call on a fixed deterministic corpus (tune p50/p99); behaviour held by a 64-bit digest of every output (bit-identity) + the crate suites.
Machine: shared Linux x86, 8 vCPU, load 1.4–2.1 during the run; interleaved A/B used for the final call; orders of magnitude only (cloud rule).

Attribution (feature-gated phase timers, `work/instrumented-attribution.diff`): compile ≈ 47%, fit ≈ 25%, orient ≈ 9%, residual ≈ 19%. Op counts per call: ~54 `Scalar::div`, ~31 `isqrt` (~94 wide divisions), ~317 `mul`, ~404 `add`; bisection ≈ 76 iterations with ~27 sign evals skipped by the witness.

| # | hypothesis | change | metric (tune p50) | verdict |
|---|---|---|---|---|
| 0 | baseline | — | 12914 ns, digest fd33f759b10e569f | — |
| E1 | isqrt's Newton `u128/u128` (`__udivti3`) is the division floor; `div_word` (2 digit divs) is faster | swap division inside isqrt | exact (0 mismatches / 800k values) but **1.00×** on this machine | reverted |
| E2 | `Scalar::add` pays `raw()`'s checked chains; a no-renorm fast path helps | guarded fast path (normal-magnitude check after the denormal bug) | digest ✓, +2% (noise) | reverted |
| E3 | `poly` computes `z·z` twice per eval (68 evals/call) | hoist `z2` | digest ✓, ~1% | **kept** |
| E4 | witness bracket has the only sign flip → start bisection tight (84→~20 iters) | `lo,hi = a,b` on witness success | **digest changed, `witnessed_fit_keeps_the_full_search_key…` failed**: the rounded poly is not monotone at fine scales, so the full midpoint sequence defines the answer | killed (control worked) |
| E5 | `node()` computes `cos ψ` and `x(ψ)` twice | reuse `xi` | digest ✓, ~1% | **kept** |

Stop rule hit: E3/E4/E5 three consecutive rounds under 10%. Final interleaved A/B (same load): BASE p50 ≈ 13071 ns vs KEPT ≈ 12982 ns → **~0.7%, noise-level**; digests identical on tune and held-out; 50/50 space tests green.

One idea that carried the (small) gain: deleting a duplicated exact expression (compute once, use twice) — the only change class that is bit-identical by construction.

What would beat this local optimum (blind spot): per-event cost at this representation is floored by the exact division chain (~half the call) and by a bisection whose iteration count is semantic, not waste. The 10× levers are structural: (a) fewer rebinds per orbit (cadence — the board's standing conclusion), (b) warm-starting the quadrature from the previous kick's knot table (changes bits unless a refinement-invariance proof exists), (c) re-measuring the division floor on the M1 (ARM64 has no 128/64 divide; `div_word` vs `__udivti3` may differ there).
