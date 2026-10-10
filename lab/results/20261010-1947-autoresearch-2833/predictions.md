# Predictions (held out before the optimization loop's decisive runs)

Metric: `universe --kick-bench --seconds 2` `kick_us` median (pure resolver, ns per kick),
digest `971e97d7247c01bab309f3154003fb0091feabc662c2fa42f990fc5ab68c33c4` must stay
bit-identical for every kept change. Baseline (seed 1, this Linux box): 46.857 µs.

Phase profile (instrumented run, clean spans): rebind ≈ 2/3 of the kick —
tau readout 9.6 µs, fit_key 6.4 µs, cycle compile 7.5 µs, at_radius 1.6 µs,
residual decode 5.2 µs; outside rebind: readout 5.3, secondaries 3.7, force 6.5 µs.

## Held-out cases (not tuned on)

1. Seeds 2 and 3 of the same bench (never run during the loop).
2. The universe behaviour suite (`cargo test -p emergent-universe -p emergent-space`):
   every kept change must leave it green.
3. The `--describe` scene digest must be unchanged.
4. A longer bench (seconds 6) must show the same relative speedup as seconds 2.

## Predictions

- P1 (cache the event-time proper time on the binding): saves one of the two
  orbit_state readouts in the tau readout → 8–12% off the median (≈ 4–5 µs).
- P2 (allocation/normalization fast paths in the cycle-compile's shape build):
  compile is 7.5 µs; knots are built per compile, so removing reallocation and
  redundant normalization saves 1–2 µs (2–4%).
- P3 (equal-exponent fast path in Scalar::add): Scalar ops are ~10 ns each and
  adds are maybe 30% of them; I predict < 3% — likely reverted.
- P4: The floor for bit-identical work in this resolver is ~30 µs/kick on this
  box (the fit + compile + decode are already lean integer paths); a structural
  change (reuse across kicks) is needed beyond that, and it is NOT the quantized
  memo (killed: random walk) but exact-offset re-anchoring (law.md line 35).
- P5: force+secondaries+readout (≈ 15.5 µs) cannot shrink bit-identically except
  by caching secondaries per (doll, tick) across bodies in one frame — outside
  the single-kick resolver the bench measures, so I predict no gain in this
  metric and leave it alone.

If the digest ever changes, the change is reverted whatever the speed.
