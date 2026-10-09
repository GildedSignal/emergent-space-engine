# Predictions (written before the held-out runs)

Tuned on: `xtask universe --kick-bench --seconds 55`, default seed 1, this Linux box,
5 repeats (baseline) + the instrumented run. Held out: seeds 2 and 3, same command,
run once each, after this file is written.

The measurement (seed 1, 37 samples, mean over fired and carried kicks):
total resolver ≈ 97 µs/kick; `bind_from_state` 76 µs (78%); inside it `Orbit::compile`
65 µs (85% of bind), `fit_key` 4.5 µs, rest 6 µs; `clock_reads` 8.9 µs;
`secondaries` 3.7 µs; readout+force+sigma-delta+drift_plan < 2.5 µs combined.

## Held-out predictions

1. **The shape compile dominates on every seed.** For seeds 2 and 3:
   `compile / bind_from_state ≥ 0.75` and `bind_from_state / (sum of all phases) ≥ 0.65`.
   The plane's scene is the same kind of system; I expect the ratios, not the absolute µs, to hold.
2. **The fit's bisection is never the cost:** `fit_key / total ≤ 0.15` on both seeds.
3. **The front half is noise:** readout + secondaries + force + tide + sigma-delta together
   ≤ 15% of the total on both seeds — so micro-optimizing them caps any gain at ≈ 1.2×.
4. **Absolute scale:** medians within a factor 2 of seed 1's (shared box, timing noise ±30%);
   replay digests differ per seed but are identical across repeats of the same seed
   (checked for seed 1 across two separate builds: `131a39825923d748`).
5. **Refusals stay 0** on both seeds (the instrumentation cannot change behaviour; if a
   refusal appears, the probe corrupted the law and the run is void).

## What would make the claim wrong

A seed where the compile share drops below ~50% of bind: then the cost follows the scene's
orbit mixture (many near-circles hitting the symbolic-circle fast path), and "the compile
is the lever" is scene-dependent, not a property of the resolver.
