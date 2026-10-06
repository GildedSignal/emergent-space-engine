# Predictions (written before the instrumented run)

Baseline (uninstrumented, this Linux box, seed 1, 20 s): made-body kicks median 43.4 µs (23 samples),
leaver kicks median 404 µs (9 samples), p99 474 µs. Exact and quantized memo hit rates both 0.0.
HANDOFF's M1 numbers: 29 µs per kick, 15 in "rebinding fit and compile".

The instrumented run decomposes `step::process` for replayed kicks into stages:
readout / forces (secondaries+tide+acceleration) / quantize / fit_key / compile (Cycle or Passage) /
at_radius+residual, plus knot and passage-tail panel counts. Predictions from code reading, not tuning:

## Made-body kicks (cycle rebinds), of ~43 µs
1. compile (OrbitShape::bound quadrature) ≈ 45–60%, dominated by the generic-path
   `node()` (about 10 heavyweight i128 Scalar ops incl. sqrt/div per node, 4 nodes per panel).
2. fit_key ≈ 10–20% (a ≤128-step bisection of the cubic, partly accelerated by root_witness).
3. readout ≈ 10–20%; forces ≈ 5–15%; at_radius+residual ≈ 5–15%.
4. Knots per compiled cycle shape: 10–60.

## Leaver kicks (passage rebinds), of ~404 µs
5. compile (Passage::compile) ≈ 80–95% of the kick.
6. The passage tail ladder (panels shrinking x by 15/16 each, from x=2^-10 down to the
   endpoint near periapsis/outer_radius) is the bulk: I predict 100–300 tail panels,
   each a `tail_quad` plus Integral adds. The band loop and shape build are minor.

## Floors (the idiot index)
7. A generic `node()` costs ~200–500 ns; the same math in the style of `fast_quad`
   (u64 products + one isqrt + shifts, already in the file for the strong branch) is
   ~30–60 ns: a ~6–10× ratio, if the plane's shapes really take the generic path.
8. The tail ladder at ratio 15/16 needs ~4.27 panels per octave of x; a certified
   log-spaced ladder (ratio 1/2) would need ~1 panel per octave: ~4× fewer panels
   at the same per-panel work.

## Held-out cases (not tuned on)
- `--seed 7` and `--seconds 55`: the stage percentages above stay within ±10 points
  of the seed-1 values; medians move < 30% (cloud box, shared).
- The replay digest is unchanged by the instrumentation (timers write nothing):
  same digest as the baseline run at the same seed and seconds.

## What would make the premise wrong
- If compile is NOT the dominant stage for made-body kicks, the HANDOFF attribution
  ("15 of 29 µs in rebinding fit and compile") mislocates the cost on the M1 too, and
  the lever is elsewhere (readout or forces).
- If leaver passages don't dominate their own 404 µs (e.g. it is fit_key refusing and
  retrying), the tail-ladder theory dies.
