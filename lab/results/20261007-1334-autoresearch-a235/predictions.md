# Predictions (written before the decisive experiments)

Baseline (tuning corpus, 72 states, 54 bound): from_state median 47.1 µs, mean 42.7 µs;
`Orbit::compile` alone 47.2 µs mean ⇒ compile ≈ 99% of the per-kick rebind.
Held-out corpus (`heldout`, 64 states, different radii/e grid) is run only at the end.

Attribution measured (temporary counters, since reverted): ~85% of compile is the panel
quadrature (`quad`: ~47 panels average, ~4 nodes each), ~17% the band-cut loop (`cut`:
one 128-bit `isqrt` + `atan` per 1/16-octave band), rest small. Panel count is set by
eccentricity (16·log₂(1/x_a)) — that is the law's accuracy contract and must not change.

## Hypotheses and held-out expectations

- H1 (node dedup): `node()` calls `cos(psi)` twice (once as `cs`, once inside `self.x(psi)`
  which recomputes the same value). Reusing the local is trivially bit-identical.
  Predict: strong-field compiles (r ≤ 2^14, where `node` runs) drop 8–15%;
  weak-field compiles (the belt, `weak_quad`) unchanged.
- H2 (panel-loop churn): per panel the code copies the last knot's `[Scalar; 5]`, does 5
  `Scalar::add` (branch + exponent align + renormalise each) and 5 checked `Scalar::raw`.
  A running local accumulator and an unchecked raw constructor (bounds proven) keep the
  same rounding sequence. Predict: 10–20% off every bound compile.
- H3 (isqrt seed): `cut`'s `ratio_sqrt` does a u128 Newton with u128 divisions.
  A tighter seed trims iterations. Predict: ≤ 8% total; may fail to clear 10%.
- Cumulative: 1.25–1.5× on ns per compile. NOT 10×: panel count and the per-panel
  rounding sequence are the law's bits; the structural escape (shared shapes across
  bodies) is the plane's memo/jet question, already adjudicated (H0200-era, 5 Oct taste log).
- Held-out: gains within ±30% of the tuning gains (same regime mix, different grid),
  digest for both corpora unchanged after every kept change, `cargo test -p emergent-space` green.
- Kill criterion for the whole run: if three consecutive rounds each gain < 10%, stop
  and report the best configuration with the structural alternative.
