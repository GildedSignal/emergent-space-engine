# Predictions (written before the decisive runs)

Context measured so far (not tuned on): kick resolver median 35 µs (plane-made ships), 92 µs (fleet
leavers), p99 412 µs; the orbit-shape compile measured out-of-line on the same keys costs ~50 µs
mean, i.e. ~63% of a median kick; 807 of 830 kicks rebind and all 807 exact ShapeKeys are distinct
(no reuse without a law change — confirms the 5 October adjudication at the mechanism level).

The decisive runs, not yet run:
1. `compile_sweep`: `Orbit::compile` cost vs eccentricity e (weak field, the plane's regime),
   fixed periapsis; plus the plane's own distribution of e over its 807 kick shapes.
2. The scale Fermi folded with that curve.

## Predictions

- **P1 (curve shape):** compile cost grows roughly linearly in log2((1+e)/(1−e)) — the band count
  of the dyadic integration. So e = 0.9 should cost ~5–8× e = 0.1, and e = 0.99 ~15–30× e = 0.1.
- **P2 (plane's own mix):** the plane's kick shapes concentrate at low e (p50 < 0.2); the leavers'
  92 µs median is carried by an e tail above ~0.5, not by a different code path.
- **P3 (tail):** at e ≥ 0.97 a single compile exceeds 300 µs — enough by itself to explain the
  observed p99 kick of 412 µs without invoking cache or allocator effects.
- **P4 (the strategic one):** even deleting the compile entirely (impossible: the rebind needs the
  new shape) buys at most ~2.7× on per-kick cost. So reaching a billion bodies needs the cadence
  lever (kicks per orbit) or an incremental shape update, not a faster compile. If P4 holds, the
  constraint statement "compile dominates the kick" is true but NOT sufficient as a plan.

A failed P1/P3 would point at the panel CAP or the strong-field path, not the band count, and
would itself be a finding about where compile cost really lives.
