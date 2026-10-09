# log — autoresearch on `Orbit::compile` (crates/space)

Artifact: the scaled Darwin compiler (`crates/space/src/orbit.rs`, `num.rs`) — the
compile the plane pays on ~99% of its kicks. Metric: ns per `Orbit::compile`
(single-thread, release, this Linux box; orders of magnitude only).
Behaviours frozen: 64-bit output fingerprint over periods/advance/16 readouts per key
+ the crate's 50 tests (release and debug).

Population: tune = p_exp {2,4,7,11,15,19,24} × e {0, 0.001, 0.02, 0.1, 0.5, 0.9, 0.97};
held-out = p_exp {3,5,9,13,17,21} × e {0, 0.003, 0.05, 0.2, 0.35, 0.65, 0.8, 0.95, 0.99}.
Fingerprint before any change: tune `f4bd77fc76c8b072`, held-out `9356db3f24802745`.

Instrumentation (removed before the final patch; feature `profile`, per-compile):
p=2^4, e=0.9 → 67 cuts (13.4 µs), 71 panels (57.2 µs ≈ 800 ns/panel, all `fast_quad`);
e=0.97 → 96 cuts, 100 panels. Quad ≈ 93% of instrumented time; cuts ≈ 7%.

| # | Hypothesis | Change | Metric (tune total_ns) | Verdict |
|---|---|---|---|---|
| 0 | baseline | — | 1301204 / 1310790 | — |
| 1 | the four u128/u128 software divisions per `fast_quad` node dominate | `div_w64` (exact 128/64 word division, guarded fallback) for g, g1, ratio, rt | 1248162 / 1225729 (−5…−6%; fp unchanged) | **kept** |
| 2 | the same divisions inside `isqrt` Newton, `ratio_sqrt`, `OrbitShape::new` gmax, plus the `a = 4k+2x` identity | batch: word division in isqrt/ratio_sqrt/gmax + identity | 1221205 (≈ round 1 ± noise) | **reverted** (H5–H7: complexity, no gain); identity kept (deletes a multiply, zero branches) |
| 3 | (from #2) the per-node cost is not division-count-bound on this box | — | — | stop: two consecutive rounds < 10% |

Interleaved A/B (git stash ↔ patch, 2 pairs each, 0.2 s/key):

- tune: A 1329094/1328795 → B 1262064/1269547 = **−4.7% total, −9% median (7340→6660), −11% p90**; fp identical.
- held-out: A 2433419/2379709 → B 2260467/2296539 = **−5.3% total, −8% median**; fp identical.

Mid-run incident (honesty): reverting round 2 silently dropped `y <<= shift / 2;`
from `isqrt`; the broken build measured −30% and a changed fingerprint (649ba453…).
Caught by the fingerprint, fixed, re-verified. This is exactly what the fingerprint is for.

Final kept diff (see `work/patch.diff` when saved): `div_w64` in `num.rs`; four
divisions in `fast_quad` via `div_w64`; `a = 4k + 2x` identity. 50/50 crate tests
pass in release and debug.

Stop reason: rounds 1–2 gained < 10% each. The per-node floor under bit-identity is
~4 exact divisions + cos + isqrt; the remaining cost is structural.
