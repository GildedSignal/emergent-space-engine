# Predictions (written before the first change; held-out cases never tuned on)

Metric: `pure_kick` µs and `whole` µs/item from `crates/universe/examples/kick_probe.rs`
(scenarios A-tune, C-held, D-held in the loop; B-held and the digests only in the final run).
Machine: shared 8-vCPU runner; median of 3; run 1 of the baseline (load 7.6) was 2× slow and is excluded.

Baseline (median of the clean runs): A pure 34.0 µs / whole 51.8 µs/item; C 39.4 / 79.6; D 34.5 / 50.5.

## H1: dedupe the three decodes per kick

A level-0 kick decodes the same binding three times: `readout(t)` (kick), `orbit_state(t)`
and `orbit_state(event_time)` (both inside rebind, for the proper-time bookkeeping).
`orbit_state(event_time)` is a pure function of the binding: I will store it in the `Binding`
(one `Scalar`, the proper time at the binding event, set from `bound.orbit` which `bind_in`
already computes) and pass the orbit state from the kick's own readout into rebind.

- Same values by construction (decode is deterministic), so **every digest must be identical**.
- Predicted gain: two decodes ≈ 2 × 2.7 µs gone of 33 µs → A pure_kick ≈ 27–29 µs (−14–18%).
- Held-out C, D should move by the same absolute ~5 µs (their kicks decode the same way).
- bytes/body will rise by ≤ 16 B per binding segment (one Scalar) — predicted invisible
  next to the 134 KB/body baseline (dominated by compiled trajectories).

## H2 (if H1 lands): the scheduler's position cache

`apply` computes `root_state_raw` (6.8 µs) after every event, only to feed `pos[i]`,
which is read by `light_distance` — a scheduling heuristic. Prediction: deduping the centre
state it re-reads (already read by `tide` in the same event) is worth ~3–6 µs/item on the
whole-universe metric, without touching a single bit of state (same value, cheaper path).

## What would make H1 wrong

If `OrbitState.proper_time` at `event_time` is not what rebind subtracts today (e.g. the
binding was re-created on a path that does not go through `bind_in`), a digest will move:
that is a kill for the change, not a tune.

## Stop rule

Three rounds in a row under 10% gain on the median pure_kick → stop and write up.
