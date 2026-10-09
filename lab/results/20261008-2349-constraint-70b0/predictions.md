# Predictions (written before the decisive run)

Instrumented finer: `ramped_in` splits into `binding_at` (history search + `Binding` clone),
`cartesian` (the integer tube decode) and `partial` (force field + second readout).

Cases not tuned on (held out):

1. **Inside one ramp** (the rtf=100 plane, ~99k ramps over 900 frames): the integer tube
   decode `cartesian`/`readout` takes the majority of ramp time (> 50%), the `Binding`
   clone in `binding_at` is second (10–40%), and `partial`'s force evaluation is minor
   (< 10% of ramp time; `fields` is only ~11% of ramps).
2. **Growth in game time at fixed bodies**: the per-frame gather cost at tick T does not
   grow with the number of retired history segments (prune keeps ~2; `binding_at` is a
   partition point, not a scan). A second run at rtf=1000 with ~same body count has
   per-emitter crossing cost within 2× of rtf=100 (it may rise from longer Newton walks
   when arrival rates deviate, not from history length).
3. **Frame share at the service level**: view_gather stays ≥ 60% of the frame at every
   rtf in {1, 100, 1000}; the engine never exceeds ~25% at its 5 ms budget. The one
   constraint on smoothness at plane scale is the gather's O(bodies) synchronous claim
   per presented frame (~42 µs per emitter), not the engine.

If (1) fails the other way (clone dominates), the cheapest exploitation changes (store
layout, not law). If (2) fails (cost grows with history), that is a bug-class finding:
an unbounded read cost, worse than a slow constant one.
