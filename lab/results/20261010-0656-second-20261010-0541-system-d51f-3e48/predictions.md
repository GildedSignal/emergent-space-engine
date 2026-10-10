# Predictions (written before the decisive run)

Question (the first checker's named experiment, verbatim): build the incremental deadline — the
deadline carried by the arrival rate the view already computes, here in position form (the last
readout walked forward by its velocity, `d(t) = |x(t) − X|` moving at `n·β`, so `deadline' =
deadline + Δt·(1 + n·β)` to first order) — and show the engine frame drops, with digests equal at
a **settle cut**, across seeds and rtf, including a β→1 flight.

Cases I have NOT tuned on: plane seeds 3 and 99 (rtf 100), seed 7 at rtf 10 and 1000, stream at
β = 0.99 toward / away / toward with the observer at 0.9c. Tuned on: plane seed 7 rtf 100 (the
run's own scene) and this machine's baseline of it (engine median ≈ 100 µs, 1123 sched walks at
≈ 9.5 µs each, 2827 events over 300 frames).

1. **Walk amortization.** The re-anchor policy (a real walk only when the carried displacement
   `|v|·Δt` could pass 1/8 of the light distance) pays ≤ 150 walks on the seed-7 flight against
   1123 (≥ 7× fewer; I expect ≤ 60). If walks stay ≥ 500, the policy is wrong at the plane's
   scale and the saving is not there.
2. **Engine median drop.** Seed 7 rtf 100: the median engine frame drops by ≥ 20 µs (the walked
   flight's median is inflated by the same instrumentation the carried flight pays, so the drop is
   the walk's cost, slightly understated). If the drop is < 10 µs, the tax was not the walk.
3. **Digests at settle cuts.** Equal in all 8 configurations (5 plane, 3 stream). This holds the
   design's own claim (the digest is "independent of schedule") under a real scheduling
   perturbation. If any differs, the control is REL → 0 (re-anchor ≈ per event): digest equal
   there means the carry broke something canonical (my bug, likely prune); digest still different
   means the schedule-independence claim itself fails — either kills the incremental deadline as
   built.
4. **Views at the cut.** The gathered view hashes equal in all 8 configurations.
5. **Deadline error.** On the plane: median relative error < 2% of the light distance, max < 15%
   (the 12.5% re-anchor bound plus one event's drift). On the stream (inertial 0.99c worldlines,
   where the rate form degrades to 0.01/1.99 but the straight carry is exact): < 1e-6. If the
   plane's max exceeds 30%, the bound is not what the code does.
6. **Presented time.** The carried flight presents ≥ 90% of the walked flight's ticks before the
   settle (a deadline that lags defers work but must not collapse the rtf).
7. **rtf 10 / rtf 1000.** The walk amortization and the digest equality hold; the drop's *share of
   the mean* engine frame is smaller than at rtf 100 (more events per frame dilute a per-event
   tax) — reported, not asserted.

Stated limit (not run): no shipped scene has relativistic *events*; the β→1 flight tests
deadlines, view and digest under inertial 0.99c worldlines and a 0.9c observer, not kicks at β→1.
