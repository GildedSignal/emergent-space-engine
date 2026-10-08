# Predictions (held out before the decisive measurement)

Artifact: the plane's kick resolve path (`xtask kick_bench`, `cost_split`, and the stage bench
`a48d_bench` built this run). Metric: **µs per pure kick resolve** (median of the bench loop),
Linux x86, orders of magnitude only.

Behaviour constraints (what "fixed" means):
- the whole `emergent-universe` test suite green (motion, replay, ties, lifecycle, throttle, plane);
- `xtask universe` replay digests unchanged (bit-identical readouts);
- `emergent-space` and `emergent-engine` suites green (the changed constructor is shared).

## Change under test (round 1)

`Rebinding::from_state` computes `Residual::between(state, decoded_event())` — a full
`trajectory.state` + `cartesian` evaluation — whose result the kick path's `bind_in` never reads
(it rebuilds the residual against the tube's tick-quantized decode). Split a `fit_only`
constructor (residual zero) and call it from `bind_in`.

## Predictions, on cases I did not tune on

1. **P1 (the claim):** pure kick resolve drops by the cost of one `state`+`cartesian`
   evaluation. Measured attribution says state ≈ 2.3 µs, cartesian ≈ 0.3 µs, so I predict
   32.6 → 29.5–30.5 µs (−7% to −10%). If the drop is < 3%, the attribution is wrong somewhere
   and the round is reverted.
2. **P2 (no behaviour change):** all suites above stay green and replay digests are identical,
   because `bind_in` provably never reads `fit.residual` (checked: it uses trajectory,
   periapsis_time, periapsis_angle, clockwise only). Any digest change = revert, no arguing.
3. **P3 (held-out workload):** on `kick_bench` (the xtask deterministic replay over the plane's
   own scene, a different workload than my stage bench: fleets, member handouts), the median
   kick falls by the same absolute amount (2–3 µs), i.e. −6% to −9%, and the p99 falls by no
   LESS than the median in relative terms (the deleted work is per-kick constant).
4. **P4 (regression guard):** `emergent-space`'s events tests (handoff path) unchanged, since
   `from_state` keeps its residual; only the universe's bind path switches.

## Stop rule

One round here (time-boxed window). If P1 holds and suites are green: kept. If not: reverted
and the dossier says why.
