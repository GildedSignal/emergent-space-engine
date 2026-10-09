# Autoresearch log — run 20261009-2043-autoresearch-d4f1

Artifact: the plane's kick resolver (`emergent_universe::step::process`), replayed by
`xtask universe --kick-bench` on the plane's own deterministic scene.
Metric: µs per distinct pending ship kick (median / p99), plus a per-phase breakdown.
Behaviours held fixed: the bench's `replay_digest` (blake3 of every resolver record update)
and `refused` must be bit-identical to the uninstrumented baseline (`131a39825923d748…`
seed 1; verified across two independent builds and 6 repeats).

| # | Hypothesis | Change | Measurement (seed 1, 37 kicks) | Kept? |
|---|---|---|---|---|
| 0 | baseline | none | median 46–62 µs across 3 repeats (shared box, ±15% run-to-run), p99 ≈ 440 µs | — |
| 1 | the cost is spread across the resolver's phases | instrument phases 0–11 (readout, secondaries, tide, force, sigma-delta, rebind, bind's `Rebinding::from_state`, clock reads, ext time, drift plan) | front half (readout+secondaries+force+tide+sigma-delta) ≤ 6 µs of ≈ 97 µs mean; `bind_from_state` 76 µs (78%) | kept (instrumentation) |
| 2 | inside `from_state`, the exact bisection (`fit_key`, ≤128 iters + `root_witness`) is the cost | sub-instrument `from_state`: `fit_key` / `Orbit::compile` / rest | `fit_key` 4.5 µs (9% of total); **`Orbit::compile` 65 µs (67% of total, 85% of bind)**; rest 6 µs | kept |
| 3 | the compile's µs are in the quadrature knot table, so a Vec preallocation or fewer knots buys ≥10% | read `append`/`quad`/`bound`: CAP = π/4 ⇒ only O(tens) of quads per weak shape — the arithmetic cannot account for 65 µs as a *median*; the mean is carried by tail kicks (median kick 48 µs < compile mean 65 µs; all shapes are `Cycle`, no passages) | not measured — no bit-exact-safe restructure fits the 60-min window; a knots preallocation is bounded by the O(tens) count, i.e. < 10% | reverted before landing (nothing to keep) |
| 4 | the breakdown is a property of the resolver, not of seed 1 | held-out seeds 2 and 3 (predictions.md written first) | seed 2: bind/total 0.61, compile/bind 0.57, fit_key 0.12, front 0.19; seed 3: 0.83 / 0.85 / 0.04 / 0.07 | kept |

Stop rule: three consecutive < 10% rounds — reached (rounds 1–3: the remaining safe levers
are all below 10%; the two big levers, the shape memo and the compile's tail, are law changes
/ other owners' work, see dossier).
