# Autoresearch log — 20261006-1135 (artifact: the plane's kick resolver; metric: kick µs, digest-gated)

Baseline (instrumented build, `xtask universe --kick-bench --rtf 100 --seconds 30`, seed 1):
made median 36.6 µs, p99 51.4 (noise band 51–58 across identical builds), leavers 103.9, n=1158.
Linux x86 cloud box — orders of magnitude only; the integrator re-measures on the M1.

Anatomy (per sampled kick, means, from phase timers): rebind 82 µs = compile 60 (85% in
`OrbitShape::append`/`quad`) + fit 4.2 + remainder 5.3 + decode 4.0; secondaries+tide 7.2;
own readout 3.9; acceleration 1.1. Per compile: ~55 EDGE bands (16/octave ladder), ~63 knots,
~130 quad panels ≈ 520 `num::cos` (47.7 ns measured) + ~520 `div_word` (18.0 ns). 1125/1158
full-bound compiles, 33 passages, 0 circle fast paths. Exact memo hit rate 0% (re-confirms the
5 October correction), quantized cell 95.5% (the known law-change, not taken).

| # | Hypothesis | Change | Metric (made med / leaver med) | Kept? |
|---|---|---|---|---|
| 1 | The universe's `bind_in` throws away `from_state`'s `Residual::between(decoded_event())` (one full decode+cartesian per rebind) | `from_state_lean` skips it; events layer keeps the full path | 36.6→32.1 / 103.9→97.3 (−12% / −6%), digests identical | **KEPT** |
| 2 | Allocation + hoisted constants in the compile path are worth a few % | pre-sized knot/crossing vecs via ladder simulation; hoisted `ONE−k`, `3k` in `weak_quad` | 32.1→32.3 / 97.3→96.3 (noise), digests identical | REVERTED (weightless) |
| 3 | `num::cos` (55% of a quad) can be rewritten cheaper bit-identically | not attempted: measured 47.7 ns ≈ 26 bounded u64 multiplies — ~1.5× the multiply hardware floor; no bit-identical slack found | — | STOP (predicted <2%) |

Stop rule: round 2 gained <1% and round 3's primitive measurements bound it under 2% —
three sub-10% rounds. Final clean-build verification (no instrumentation), seeds 1/2/3:
digests all bit-identical to baseline; made median 36.6/36.5/36.7 → 31.5/31.5/31.5 (−14%),
leavers 103.9/84.8/100.5 → 88.5/71.3/85.5 (−15%), p99 within noise.
