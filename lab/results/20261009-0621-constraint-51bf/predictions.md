# Predictions (written before the instrumented run)

The dashboard (bench-paced-r100.json, bench-unpaced-r100.json) already shows the view gather at
67% of every frame (p50 3.6 ms paced / 0.72 ms unpaced) against the engine's 21%, at the player's
setting (rtf 100, 60 Hz, 71 bodies + 48 fleet members). The instrumented run splits the gather.
Cases not tuned on; what I expect there:

1. **The bodies' crossing loop is the bulk of the gather**: I predict the per-body loop (Newton
   crossings with tube readouts through the doll chain) holds ≥ 50% of gather time, against the
   fleet-members loop and the observer setup. Rationale: ~70 bodies × 1–3 readouts × (2 tube reads
   + 1 field evaluation each) per frame, while the fleet loop is one `motions()` read plus
   arithmetic per member.
2. **Inside a readout, the field evaluation dominates**: in `observe::partial` (the readout the
   view uses for a body inside a kick window), I predict `force::field` + the secondaries' tube
   reads hold ≥ 40% of readout time, against the body's own `cartesian` tube reads. Rationale:
   `field` walks the doll's secondaries and reads each one's tube at the midpoint tick.
3. **The fleet loop is secondary**: ≤ 25% of the gather.
4. **The paced–unpaced gap is cache, not work**: the same split holds in both (shares within
   ±15 percentage points), so the unpaced run's split is honest evidence for the paced player's.

If (1) fails and the fleet loop dominates, the constraint is the battle's readout, not the
crossings, and the exploit changes with it.
