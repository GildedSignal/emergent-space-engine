# Predictions (written before the held-out battery)

Config under test = round 1 (j-grid cache + early exit in `d_of_s`) + round 2c (merged arcs: analytic
superset window instead of the numeric crawl) + round 2b (Wide full-arc checks at k=16).

Tuned on: `scale n 10000` and `verify a` only. Held out: `verify b`, `verify c`, `verify d`,
`verify long`, `scale n {1000,3000,30000,100000}`, `scale sigma`, `steady 3000 3.3e-4 {10,100,1000}`.

1. **Zero misses everywhere.** `missed = 0` and `truth_outside_cone = 0` on every belt of every
   verify set, including the adversarial `c` (coorbital, narrow-adversarial, equal-period-keys).
   Reason: the merged window is a superset by the angular necessary condition (equation of centre
   bound + chord bound), and the cross paths are decision-identical to baseline.
2. **The risk I can name:** the k=16 scan on merged brackets (baseline 64). If a merged pair's
   distance over one period bracket has two sharp minima below ρ more than ~1/16 of a period apart,
   a bracketing can be missed. Prediction: does not happen, because |Δn|·T ≪ 1 rad makes the
   relative geometry near-stationary over one period (one slow minimum). Falsifier: `verify c`
   coorbital belt.
3. **`false` on verify c** may rise vs baseline (more conjunction proposals on merged pairs), but
   stays ≤ 3× baseline and `method_s` on every verify belt is ≤ baseline (the setup saving
   dominates the extra k=16 checks).
4. **`setup_ns_per_pair`** at n ∈ {3000, 30000, 100000} stays in 2.5–4.5 µs (baseline ≈ 9.2 µs at
   10⁴; composition is scale-free at fixed density), and `setup_evals_per_pair` < 1 (baseline 20.3).
5. **`run_ns_per_pair_1000_orbits`** ≤ baseline at every n. At horizons ≤ ~400 orbits the merged
   change is a pure win (setup −4.7 µs/pair vs run +~1–13 ns/pair/orbit).
6. **Negative control (instrument must be able to fail):** with the merged window shrunk 10×
   (`lam × 0.1`, deliberately unsound), `verify c` reports `missed > 0`. If it does not, the gate
   cannot detect unsound windows on this belt and every "missed = 0" above is void.
7. **`steady` at 3.3e-4**: `hits_per_body_orbit` unchanged (same encounters), `events_per_body_orbit`
   within 1.3× of baseline at horizon ≤ 100, and below baseline at horizon 1000.
