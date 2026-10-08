# Autoresearch log (run 20261008-1521-autoresearch-a48d)

Artifact: the plane's kick resolve path. Metric: µs per pure kick resolve (stage bench
`a48d_bench`, cross-checked by `cost_split` and `xtask universe kick_bench`), Linux x86,
orders of magnitude only. Behaviours held fixed: universe/space/engine suites green,
replay digests bit-identical.

## Attribution (before any change; a48d_bench, n=3000, plane scene, ship 14)

| stage | µs | of kick |
|---|---|---|
| process (full kick) | 32.6–35.1 | 100% |
| bind (the rebind) | 14.9–16.0 | ~46% |
| — from_state inside it | 11.1–12.1 | ~35% |
| — Orbit::compile | 3.3 | 10% |
| — fit_key + at_radius + angles + residual-between | ~5.2 | 16% |
| — decoded_event (state 2.3 + cartesian 0.3) | ~2.6 | 8% |
| readout (own state) | 3.3 | 10% |
| secondaries (moon state) | 3.3 | 10% |
| tide (centre state) | 3.3 | 10% |
| force::acceleration | 0.8 | 2% |
| at_phase solve+read / read only | 3.09 / 0.32 | solve ≈ 2.7 |

Known-dead levers not touched: exact-memo of compile (distinct kicks hit 0%, board 5–6 Oct);
cadence/averaging (six runs, board); quantized memo (law change, 94.5% hit but changes orbits).

## Round 1

- **Hypothesis:** `Rebinding::from_state` computes `Residual::between(state, decoded_event())`
  (one full trajectory decode) whose result the kick path's `bind_in` discards (it rebuilds the
  residual against the tube's tick-quantized decode). Deleting that decode cuts the kick by
  ~one state+cartesian ≈ 2.6 µs.
- **Change:** split `fit_only` (residual zero) out of `from_state` in `crates/space/src/binding.rs`;
  `bind_in` (`crates/universe/src/bind.rs`) calls `fit_only`. `from_state` unchanged for the
  handoff and engine callers.
- **Metric:** kick 32.64 → 29.48 µs (**−9.6%**; bind 14.88 → 11.71). Predicted 29.5–30.5 (P1 hit).
- **Kept**, pending suites: results below.

## Round 2 — not run (time-boxed window). The next candidate, for the record

`fit_key`'s exact bisection (up to 128 midpoint iterations with a 6-op Q62 polynomial each)
inside the ~5.2 µs fit segment: seed the bracket from a float estimate of the outer turning
root, then land on the same adjacent Q62 pair verified by exact `poly` evaluations (fall back
to the full bisection on any doubt). Expected −2 to −3 µs/kick (−7–10%); needs a differential
corpus test (same `OrbitKey` out on thousands of states) before it can be kept.
