# Causal-block interval compile (2026-09-14)

Isolated `es-linearized-retarded-gem-response-v0` on
`/private/tmp/emergent-coupled-response`. Not `production_law`. Not
`Engine::advance`. No new kernel id: finite semantics stay f64 GEM-v0 on
piecewise-inertial segments.

## What compile is now

`compile_source_response` does **not** call `evolve()`. The independent
`Reference::from_genesis` still does: that is the slow Euler-`dt` tick
loop. Compile marches **interval functions** that are constant-acceleration
on causal blocks and piecewise-inertial between knots.

On a block of length `h ≤ τ/2` with `τ = r_min/c`, retarded samples of
other bodies fall in the past. Same-block cross response is spacelike, so
the discrete retarded GEM map is block-lower-triangular. Forward
substitution (Jacobi collocation of GEM-a at the block midpoint, then a
velocity update at the knot) is the Schur elimination of

`a = f_A + K_AB b`, `b = f_B + K_BA a`

for those interval functions. Charge `coefficient_construction` for the
tidal Jacobian samples that bound `K`, and `factorization` for each block
elimination step. `interval_q = max_k (h_k L_k)` is computed, not assigned
0.

Per-body knots: shared light-crossing cadence from genesis `τ`, local
kicks, and frozen-observer light arrivals of other kicks. B is not split
at A's kick, only after the cone. Horizon is not a collocation knot.
Repair catch-up collocates only the kicked body to `t_cut`, then continues
on the same cadence so direct and subdivided execution share the grid.

Worldtubes are the piecewise-inertial **decode** of those interval
functions, not `evolve()` copied into `SourceResponse.worldtubes`. Compact
Chebyshev remains a sidecar that must meet the admitted band; it is not
the compile.

## What this is not

Not a tick loop renamed: collocation is causal-block midpoint, not Euler
`dt`. Not a precomputed trajectory table of `evolve()`. Not
evolve-plus-Chebyshev. Not a \(10^{-8}\) polyline. Not KA. Not
gravitational qualification.

CausalBlocks enclosure `q` is now `τ L` (delay-grouped Lipschitz),
computed from the independent tidal bound. Extra-ray `C/(S+C)` on one
compile is **consumer-share**, a named different quantity. Equivalent
completed source histories are N measured independent
`compile_source_response` runs through H; see
`artifacts/runs/equivalent-histories-20260914/`.

## Remainder that is still named

Piecewise-inertial storage cannot carry interior `½ a h²` of a
constant-a block without a position jump, so the stored path on a block
is the inertial chord. GEM lookback uses that chord. Compact is still a
sidecar. Library host is still not native GUI. `production_law` stays
null.
