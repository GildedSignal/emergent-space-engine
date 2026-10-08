# Predictions (written before the sweep)

The sweep: `universe --bench --seconds 15` at members ∈ {48, 400} × rtf ∈ {1, 100}, plus
readouts-per-frame instrumentation. Held-out axes I did not tune on: seed (fixed 1), threads 1.

1. **view_gather scales linearly in members** (fleet members are gathered one Seen each, every
   frame). Slope prediction: 25–60 µs per member per frame (from 2.35 ms p50 at ~39 gathered
   bodies at rtf 1). At 400 members I expect view_gather p50 ≈ 10–25 ms — alone over the 16.7 ms
   frame budget at 60 Hz.
2. **rtf raises view_gather modestly** (crossings move faster, more Newton readouts per body per
   frame): ≤ 1.6× from rtf 1 to rtf 100 at fixed members.
3. **The readout stays the constraint on every probed point**: view_gather share > engine share
   at all four corners, and view_gather p50 > engine p50 at all four corners.
4. **Readouts per frame ≈ 2× gathered bodies** (one Newton evaluate + one verify per crossing),
   i.e. the crossing readout, not the Seen/push arithmetic, dominates the gather.
5. **Extrapolation to the goal**: at the measured slope, the gather alone caps the plane at
   ~300–700 bodies at 60 Hz — while the engine's measured average per-body cost would allow
   ≥ 10× more bodies in the same budget. The constraint for "billions" is the readout's
   per-body-per-frame coefficient, not the kicks (which the board ranks first).

Kill criterion for my own claim: if the engine share exceeds the view share at any corner, or
view_gather grows sublinearly in members (culling already present), the "readout is the
constraint" claim is wrong and I report the engine as the constraint instead.
