# Predictions (written before the decisive runs; not tuned on)

Runs decided: `tail_view 30 100 1 5` (live loop, gather timed with readouts),
members sweep `universe --bench --rtf 100 --seconds 20 --members {48,200,400}`.

1. **The live gather is genuinely ~3–6 ms, not an artifact of pacing.** The
   static-plane example (`view_cost`) reports 0.6 ms/frame at 48 emitters; the
   live bench reports 3.5 ms p50 at 76 bodies. Prediction: `tail_view`'s gather
   *CPU* (not wall) p50 is ≥ 2.5 ms, so the gap is compute, not descheduling.
2. **The gap is readout count, not per-readout cost.** The live plane kicks
   (1,363 in 30 s at rtf 100); a kicked body's cached crossing guess goes stale
   and Newton needs more probes. Prediction: tail_view's worst gathers show
   readouts ≥ 3× the bodies, and readouts correlate with the slow frames.
3. **The view's cost is linear in bodies and kills the frame first.** At 46
   µs/body, 16.7 ms buys ~360 bodies. Prediction: at `--members 400`
   (~428 bodies) view_gather p50 alone is ≥ 12 ms and the frame p99 exceeds
   16.7 ms, while the engine (budgeted 5 ms) still fits; i.e. the view, not
   the engine, is the plane's scaling constraint.
4. **Engine budget bites only at the tail.** Prediction: overflow frames stay
   a small % at 48 members, but grow several-fold at 400 members (fleet items
   55.9 µs each), still below the view's share.

If (1) fails (gather CPU ≈ 0.6 ms), the bench's view_gather timing is inflated
by something outside `gather_cached` and the constraint claim is wrong.
