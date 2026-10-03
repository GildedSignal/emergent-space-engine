# Predictions (written before the decisive run)

Baseline (config A, unmodified tree) runs first; the decisive experiment is config B:
the same deterministic kick stream with (1) per-stage timers inside
`Rebinding::from_state` and (2) an exact-`ShapeKey` intern table in front of
`OrbitShape::bound` in `Orbit::compile`. Held-out cases = the plane's own kick
stream (seed 1, 30 s at 60 Hz, scripted player), which I have not tuned on; plus
seed 7 as a fresh stream.

## Kill rules, frozen now

- **KILL the intern config** if the warm hit rate (hits / compile calls, after
  the first 100 calls) is < 5%: exact keys then never recur and a lookup table
  buys nothing (the lens's "precompute" edge is over a continuum).
- **KILL the "compile dominates the fit" premise** if the shape build
  (`OrbitShape::bound` + `from_shape`) is < 30% of `from_state`'s time.
- **VOID** if config B's replay digest differs from config A's on the same seed
  (the instrumentation or the cache broke exactness), or if refused != 0.

## Predictions

1. **Stage split of `from_state`** (fit_key : shape build : orientation/decode/residual):
   I predict the shape build is the largest stage, ≥ 50% of `from_state`.
   Rationale: `append` runs Gauss quadrature with `cos`/`sqrt` on software
   Q62.126 scalars per knot, while `fit_key` is one guarded bisection.
2. **Hit rate of the exact-key intern: < 5% (near zero after warmup).**
   Rationale: a firing kick changes the integer velocity by ≥ 1 quantum, so the
   fitted (k, q) of the *same* body drifts; distinct ships are seeded on
   distinct radii (scenario literals), so keys do not collide across bodies
   either. `Scalar` equality is exact bit equality — near-misses are misses.
3. **Consequence if 2 holds:** the compile cannot be paid once by exact
   interning; the honest floor measurement is what a kick costs with the shape
   build removed (miss-path time minus a synthetic all-hits run), which bounds
   what any compile-avoidance (incremental rebind, q-correctors) can win.
4. **Capacity (cloud x86, orders of magnitude only):** at ~29 µs/kick and
   H0190's 32 kicks/orbit (90-min orbit), one core sustains ~10^4 ships; the
   compile-free floor should push that by roughly the shape build's share.
5. **Seed 7 (held out):** same qualitative split (shape build largest, hit rate
   < 5%), because the argument is structural, not numeric.

What would make me wrong: fleet members sharing exact integer states (then the
intern hits and prediction 2 dies — measured, not assumed); the guarded
bisection in `fit_key` dominating (then prediction 1 dies).
