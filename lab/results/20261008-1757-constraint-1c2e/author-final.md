# Run 20261Run complete. Artifacts in `lab/results/20261008-1757-constraint-1c2e/` (dossier, predictions, both benches, sweep, gate log); patch touches only the bench's instrumentation (replay digest unchanged: `10597678d37370c8`).

**The claim, in one sentence:** on the plane as shipped, the engine's per-event constraint is the orbit-shape compile that almost every kick pays — a measured 0.73 µs per knot with knots ≈ 6 + 15.4·log₂(r_apo/r_peri), the same dyadic law as B9's readout bound — and the plane's own workload makes it expensive because 76% of its kicks are fleet leavers at median e = 0.94 (p99 = 0.9995), putting the compile at 54% of the mean kick and under the 415 µs p99 tail, with no bit-identical reuse possible (807/807 distinct ShapeKeys, confirming the exact memo's 0% at the mechanism level), so the only levers are cadence, the law-level quantized grid (~18×, Julien's call), and the new lead this run prices: compile only the arc the next event will read, blocked on getting the period without the full integral.
rgo run --release -p xtask -- universe --bench --seconds 20 --rtf 100`
- `cargo run --release -p xtask -- universe --kick-bench --seconds 15 --rtf 100` (with this
  run's patch applied: adds `compile_share` and the kick e-mix to the output)
- `cargo run --release -p emergent-space --example compile_sweep` (with this run's patch)
- `cargo run --release -p xtask -- behave --law plane` (99 s)
