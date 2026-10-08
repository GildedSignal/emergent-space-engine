# Predictions (written before the decisive experiment)

Tuned on (already measured, rtf 1 and rtf 100 default scene, 28 bodies + 1 fleet of 48 ≈ 77 emitters):
frame p50 3.3 ms, view_gather share 75% (rtf 1) / 70% (rtf 100), i.e. ~31–45 µs per emitter per frame;
engine share 5–17%, no hitch above 16.7 ms.

The decisive experiment varies only the fleet's member count M ∈ {48, 448, 948} at rtf 1, unpaced,
10 s (600 frames), and fits `gather_p50 = a + b_body·28 + b_member·M`. The members enter the gather
as pure extrapolation (no Newton, no doll-chain walk); the 28 bodies each pay a doll-chain walk with
fixed-point tube readouts per Newton step.

Held-out predictions:

- **P1 (split):** the per-member marginal cost is ≤ 5 µs and the per-body cost is ≥ 60 µs, so at the
  default scene the bodies loop is ≥ 80% of the gather even though members are 62% of the emitters.
- **P2 (first wall):** at M = 948 (≈ 976 emitters) the gather alone is ≥ 20 ms p50, i.e. the view —
  not the engine — is the first frame-budget wall as the scene grows; frame p99 > 16.7 ms with
  engine still inside its budget.
- **P3 (serialization):** view_json + wire grow linearly in emitters too and together stay ≤ 40% of
  the gather's cost at every M.
- **P4 (engine holds):** at M = 948 the engine's total share of the frame stays below the gather's
  share (fleet members advance in lattice batches, cheap per member; no overflow explosion).

What would falsify the constraint claim: if the gather instead grows sub-linearly in M (selection
somewhere), or the engine share overtakes the view's before ~10³ emitters.
