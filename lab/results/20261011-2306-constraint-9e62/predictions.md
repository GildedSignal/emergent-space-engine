# Predictions (written before the instrumented run)

Setting: the plane at the flight setting (rtf 100, 48 fleet members, 76 emitters), gather
instrumented into five buckets: `bodies` (the Newton light-cone loop over the 27 non-fleet
bodies), `eval` (the `state_rate` readouts that loop spends, counted inside), `fleet_setup`
(the fleet origin/rate reads), `fleet_motions` (`f.motions` copies), `fleet_members` (the
per-member float work incl. blackbody). Not tuned on any of these numbers; the members=4/48/400
sweep above gave only totals, and the paced/unpaced contrast gave only the cold-cache factor.

1. **Bodies dominate the warm gather.** I predict `bodies` (incl. its `eval`) is 40–60% of
   gather ns at 76 emitters warm (unpaced): each of ~27 bodies pays doll-chain readouts in
   i128 `Scalar` arithmetic with history walks, against pure-float member math. The per-body
   cost (≈15 µs warm, measured) is ≈1.7× the per-member cost (≈9 µs) with half the count.
2. **The readout, not the iteration count, is the cost.** I predict `readouts` ≈ 1.2–2.0 per
   body per frame warm (the ViewCache guess is good), so each readout costs ~5–10 µs; if
   readouts were ≥4 per body the guess machinery, not the readout, would be the target.
3. **`f.motions` is a cheap copy**: < 10% of the fleet loop at 400 members (it delegates to
   the stepper's state copy; if it instead walks lattice events it will exceed the member
   float work and prediction 3 fails).
4. **Cold-cache inflation is pointer-chasing-bound.** I predict the `bodies` bucket's share is
   *higher* paced than unpaced (integer Scalar + history walks touch scattered memory; the
   members' float loop is streaming). If the inflation were frequency-only it would hit both
   buckets equally.
5. **Scaling:** at 400 members the gather stays ≈ 0.42 ms + ~9 µs × members (warm, linear,
   no superlinearity); extrapolated to 10⁴ emitters the gather alone is ≥ 90 ms/frame warm,
   i.e. the gather, not the engine, is the frame's constraint at any real emitter count until
   per-emitter cost drops ~100×.

Kill criterion for my claim ("the gather is the constraint"): if the instrumented split shows
`bodies`+`fleet` together < 50% of the gather, or readouts ≥ 4 per body warm, the constraint
naming is wrong and the run reports that.
