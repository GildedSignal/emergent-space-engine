# Predictions (written before the decisive gather-decomposition runs)

Context: whole-plane bench at rtf 100 (paced, 60 Hz) shows the frame is gather-dominated:
`view_gather` share 0.674 (p50 3.59 ms), engine share 0.199 (p50 0.26 ms, p99 5.17 ms — the
5 ms budget bites), view_json 0.090, wire 0.037. The gather decomposes into three phases
(observer state+clocks, per-body light-cone crossings, fleet extrapolations). These predictions
are for cases I have NOT tuned on: I have only read the code, not measured the phases.

1. **Bodies phase dominates the gather.** I predict ≥ 60% of gather ns in the per-body
   light-cone crossings (71 bodies), ≤ 25% in the observer phase, ≤ 15% in fleets (48 members).
2. **Readouts per gather** (crossing evals, cache warm) ≈ 1.2–2.0 per body, i.e. ~85–140;
   cost per readout 2–8 µs (the readout-cost lens measured 6.7 µs for the motion law v2
   partial-step readout, 2.6 µs for the raw tube). If bodies share ≥ 60% at ~100 readouts,
   that closes the arithmetic: 100 × ~20-30 µs ≈ 2-3 ms... my honest expectation: the numbers
   will NOT close arithmetically, i.e. per-readout cost implied by (bodies_ns / readouts)
   will exceed 8 µs, pointing at per-body fixed overhead beyond the readout itself
   (doll lookups, rest(), radius walks).
3. **Scaling with fleet members** (`--members 400` vs default 48): fleets phase grows
   ~linearly (×8), and at 400 members the gather exceeds 6 ms p50 — fleets becomes the
   gather's largest phase at 400 members. (This is the cheapest scaling axis the CLI exposes.)
4. **The engine is NOT the frame's constraint at rtf 100 today**: engine p50 stays under
   0.5 ms and the 16.7 ms deadline is never threatened (0 hitches) at both member counts;
   the constraint on the *frame* is the gather, and the constraint *inside* the engine
   (kicks, board's #1) only binds the budget tail (p99 5.17 ms) — two different constraints
   for two different budgets (frame smoothness vs sim-days-per-wall-second at higher rtf).

Kill criterion for my claim "the gather is the frame's constraint": if bodies+fleets+observer
do not account for ≥ 90% of the measured gather p50 (3.59 ms), my decomposition instrument is
broken (the timers miss a phase) and the run is VOID on this point.
