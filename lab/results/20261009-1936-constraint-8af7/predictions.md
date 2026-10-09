# Predictions — run 20261009-1936-constraint-8af7 (constraint lens)

Written before the attribution experiment. Baselines already measured (not tuned on):
frame CPU at 410 bodies, rtf 100, unpaced, 10 s: p50 4.76 ms; view_gather p50 3.00 ms
(54% share), engine 0.40 ms (32%), view_json 0.66 ms; overflow on 17% of frames.
At 71 bodies: view_gather 0.75 ms (64%), engine 0.05 ms (24%).

## The decisive experiment

Instrument `gather_with` (crates/universe/src/view.rs) with three atomic counters:
(0) the per-body crossing loop (Newton + `state_rate` + `push`), (1) the fleet-motions
loop, (2) time inside `state_rate` itself (the tube readout through the doll chain).
Run `universe --bench --members 480 --rtf 100 --unpaced --seconds 10`.

## Held-out predictions

- **P1 (where in the gather):** the per-body crossing loop is ≥ 55% of gather time at
  410 bodies. The fleet loop is < 15%.
- **P2 (readout cost):** with the warm ViewCache, Newton needs ≈ 1.2–2.5 `state_rate`
  evaluations per emitter per frame at rtf 100 (the crossing root advances ~
  100/60 s / 4.9 µs ≈ 3.4×10⁵ ticks per frame, locally linear, so few steps), and one
  `state_rate` costs ≥ 1.5 µs; tube readouts alone are ≥ 40% of gather.
- **P3 (scaling):** gather p50 grows ~linearly in bodies (71 → 410: ≥ 4×), i.e. the
  cost is per body per frame, not per event — the view is the one part of the frame
  that must touch every body every frame.
- **P4 (allocation is not the constraint):** `Seen` building / `name.to_string()` /
  Vec rebuild is < 20% of the bodies loop (i.e. ≥ 80% of it is crossing physics).
  Not directly measured this run unless time allows; stated as inference otherwise.

## What would make the claim wrong

- If the engine (not the view) owns the frame at the player's rtf and scale, the
  constraint claim inverts and the board's kick focus stands as the frame constraint.
- If gather cost per body falls with N (sub-linear), P3 fails and the readout is not
  per-body-per-frame; the constraint naming changes.
- If readouts per emitter per frame are ≥ 4 warm, the cache is not working as
  designed and the constraint is the solver, not the readout cost.

## Controls

The same run prints the digest; the instrumentation is counters only and must not
change it (identical digest with and without counters on the same seed and cut).

## Outcome (written after the decisive run, 19:52 UTC)

- P1 held: bodies loop 99.4% of gather; fleet loop 0.9%.
- P2 held: 0.72 (410 bodies) and 1.0 (71 bodies) Newton evals per emitter per frame;
  one state_rate ≈ 10 µs; tube readouts 97% of the bodies loop.
- P3 held: gather 0.75 → 3.0 ms for 71 → 410 bodies (3.9× for 5.8×; roughly linear).
- P4 inference only: 3% of the bodies loop is outside state_rate, which bounds
  allocation by that (not separately measured).
- Control held: digest aadaa1c8… identical before and after instrumentation, and across
  a third instrumented rerun.
- Beyond predictions: cartesian (tube decode) is 4.59 µs/call at ~2.5 calls per Newton
  eval — the decode, not the crossing solver, not the secondaries fan-out (6%), not
  allocation. `behave --law plane` with the default gate set: by-construction FAILs for
  the compiler's gates, B13 60/64 as the handoff says, B14 eats its 60 s timeout and
  B17 never runs.
