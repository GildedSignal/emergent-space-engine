# log.md — autoresearch on the plane's kick resolver

Artifact: `xtask universe --kick-bench` (the plane's own deterministic kick replay).
Metric: µs per kick (median over distinct pending ship kicks), and the isolated
weak-hyperbolic ladder bench (`cargo test --release -p emergent-space quad_bench`).
Constraint held fixed: **bit-identical digests** (`digest`, `replay_digest`) and the
full `emergent-space` + `emergent-universe` test suites.

Machine: shared 8-vCPU i7-4790, load ~3.5, 15 GiB (machine-state.txt). All keep/revert
decisions on medians of ≥3 runs; single runs swing ±15%.

## Where the time is (measured, not guessed)

- `Rebinding::from_state` (fit + compile) = 95% of `bind` (evidence-bind-split.txt).
- `Orbit::compile`/`Passage::compile` = 88% of `from_state`.
- Passages: the **band ladder** = 88% of compile (154 bands, 1 panel each,
  2.1 µs/panel; the x-tail is ~2 µs median). Cycles: 5.7 µs (`weak_quad`, integer).
- The panels are **weak + hyperbolic (k < 1/2, q = 0)**: the one regime where
  `quad` falls through to the generic `node()` — full `Scalar` math per node,
  including `sqrt(ONE)` (a 124-bit `isqrt` Newton), `1/1`, `/2` and `/1`,
  each through the general exact-arithmetic path.

## Rounds

| # | Hypothesis | Change | Metric (isolated ladder, median) | Verdict |
|---|---|---|---|---|
| 1 | The q=0 shortcuts are free bits | `node()`: `sqrt(1)=1`, `1/1=1`, `/2 = scale(-1)`, `/1 = identity` | 368.9 → 222.4 µs (−40%), knot digest c0192de9093e3d5b unchanged | **KEPT** |
| 2 | One shared `product(ONE−k, cos)` per node | CSE of x and a's common term | 233.5 µs (noise vs 222.4) | REVERTED (no measurable gain, larger diff) |
| 3 | More bit-exact micro-ops ≥10% | surveyed: the two genuine divisions (1/x², 3/x) and `cos` are required bits | — | STOP (documented) |

Stop rule hit: two consecutive rounds < 10%.

## End-to-end (clean build, final patch)

| Case | Baseline | Final | Digest |
|---|---|---|---|
| seed 1 55 s, leaver kicks | 365.6–376.0 µs | 229.1–248.4 µs (**−33%**) | identical |
| seed 1 55 s, made kicks | 41.1–43.8 µs | 37.1–41.5 µs (noise) | identical |
| seed 7 55 s, all kicks | 74.0–74.5 µs | 76.4–77.0 µs (noise) | identical |

## The one idea that carried the gain

The weak Taylor shape (compactness zeroed by `ShapeKey::for_orbit`) pays the strong-field
price at every quadrature node: a 128-bit square root of one, a reciprocal of one, a
division by two and a division by one, all through the general `Scalar` path. The regime
is chosen by the shape's own dimensionless numbers (q, k) — the dispatch that already
exists for `weak_quad` (k ≥ 1/2) and `fast_quad` (strong) simply has no arm for
weak + hyperbolic, so it falls to the most expensive implementation of the same values.

## What I did not do (and why)

- A `weak_quad`-style integer panel for k < 1/2: accumulates exactly where the generic
  path truncates per component → different bits → a law-version change, not a speedup.
- Lazy ladder extension (compile bands on first read): moves cost into reads/frames,
  breaks the read-only `Arc<OrbitShape>` tube; a design change for the motion-law owner.
- Memoization: exact keys are all distinct on distinct kicks (22/22 passages, 27/27
  cycles — matches the 5 October taste-log correction), so no cache can help here.
