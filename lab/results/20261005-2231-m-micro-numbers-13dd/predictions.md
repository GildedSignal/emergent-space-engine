# Predictions (written before the decisive experiments)

Run: 20261005-2231-m-micro-numbers-13dd, lens: micro numbers.
Written after reading law.md, representation.md, plane.md, crates/universe (force.rs, step.rs, lorentz.rs), crates/space (scaled.rs), and BEFORE running any probe below. The cases below were not tuned on; they are the held-out cases.

## Probe A: the changeover as a composition of integer shears (JANUS's arithmetic core)

Setting: circular restricted three-body, integer lattice, star exact + planet split by SyMBA
weights across 3 levels (mirroring crates/universe/src/force.rs). Metric: the Jacobi constant's
relative error, exact-rational observer, growth exponent alpha = slope of log(max|dJ/J|) vs
log(steps) over 50 planet orbits, median of 8 seeds; plus out-and-back bit identity; plus ns/step.

Configurations (all on the same lattice, same initial conditions):
- A1 floor-shear: every drift and kick is x <- x + exact_integer(v*h), v <- v + floor(exact rational), one rounding per component per sub-step, increment a function of positions only.
- A2 nearest-shear: same but round-half-away at the shear.
- A3 carried-shear: same but a sigma-delta carry per component (the plane's carry, lifted to sit at the shear).
- A4 trunc-chain: the plane's style — inner computation in a truncating 63-bit-significand software float (Scalar-like), one quantize+carry at the end.
- A5 rescale-round (negative control): like A2 but the velocity word's exponent adapts to |v| after each sub-step (the re-expression of bind.rs): rounding depends on v itself.
- A6 float64 velocity-Verlet with the same weights (reference anchor).

Predictions:
1. Bit identity out-and-back: A1, A2, A3 pass 100% of seeds (the shear inverse is exact subtraction); A4 passes with the carry in the state; A5 FAILS (rescale is not invertible). If A1–A3 fail, the shear-inverse claim is wrong and the probe kills JANUS's arithmetic core.
2. Exponents: A3 <= 0.1 (the carry removes the sub-quantum bias; the remainder is the split's oscillation); A2 in [0.0, 0.3] (nearest is unbiased but noisy); A1 in [0.2, 0.6] (floor is one-sided: the radial pull is systematically mis-kicked, so I expect a walk — this would say the *rounding rule at the shear*, not shear-ness alone, carries the error-type guarantee); A4 in [0.1, 0.4] (internal truncation adds bias on top of A3's carry); A5 >= 0.4 (broken bijection); A6 ~ 0.4 (r10 measured 0.43 for float SyMBA; reproducing that validates the harness).
3. |dJ/J| at 50 orbits: A3 < A2 < A4, and A3 at least 10x below A6.
4. Cost: A1–A3 within 2x of A6's ns/step in plain Rust (no SIMD); A4 the slowest (software-float normalizations).

What would make the shear story wrong: if A3's exponent exceeds 0.2 at the plane's cadence, then
bit-reversibility does not buy the B12-class guarantee at this budget, and JANUS needs a different
rounding site than the shear.

## Probe B: order-independence from rounding structure (round once, at the end)

Setting: one body kicked by 96 secondaries; compare (i) exact accumulation (i128/i256) then one
quantize vs (ii) the plane's chain — accumulate in a truncating software float, then quantize once.
20 shuffled summation orders x 100 random configurations.

Predictions:
5. (i) gives exactly 1 distinct final-velocity digest across all orders and configurations (any
   order, any thread partition, same bits). If not, exact accumulation is not order-free and the
   claim dies.
6. (ii) gives > 1 distinct digests on at least some configurations (truncating addition is not
   associative), median number of distinct digests across configurations in [2, 20].
7. Cost: (i) at most 1.5x (ii) per summed kick (i256 adds are cheap next to the products).

## Probe C: Mitchell log + 16-entry table (the view's colour path)

8. Plain Mitchell log2: max absolute error on the mantissa in [0.03, 0.09] (known ~0.086 max).
9. With a 16-entry correction table + linear interpolation: max absolute error <= 2^-11; error of a
   composed product (two log-adds then one antilog) stays <= 0.5% relative — inside the perceptual
   budget for colour, far from the 1% oracle gates.

## Cost-only claims (no probe, analysis in the dossier)

10. RNS, posits, signed-digit/online arithmetic, level-index, quarter-square: each killed by a named
    missing requirement (comparisons/division, closed addition, fixed-word hardware, bounded ranges,
    native high-half multiply). These are argument, not measurement; the dossier states the argument.
