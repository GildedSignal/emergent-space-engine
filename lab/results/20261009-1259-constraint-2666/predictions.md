# Predictions (written before the decisive experiment)

Question: inside the view gather (61–69% of every flown frame, measured 2026-10-09), where does the time go, and what is the cheapest change that removes it?

Cases I have NOT tuned on (the profile will decide):

1. **Attribution.** I predict the Newton light-cone crossing readouts (`state_rate` through the doll chain, exact arithmetic) dominate the per-tube cost, and the fleet-member extrapolation loop dominates the per-member cost. I predict a nontrivial fixed part (player `root_state` + `clocks_with`) under 20% of the gather.
2. **Per-emitter floor.** I predict the marginal gather cost is 5–10 µs per fleet member and 50–150 µs per tube body, i.e. the gather is O(catalogue) with no visibility bound — at 10⁶ emitters it would be 5–10 s per frame, so the gather, not the kick resolver, is the first wall on the way to scale.
3. **Cheapest exploit.** I predict the crossing's Newton readout for a *distant, slow* emitter can be skipped entirely on most frames (its arrival tick and colour change by less than the player's differentiation floor), cutting the gather by more than half on this scene, without changing any emitter the player can differentiate. If the profile instead shows the cost in fixed player work or in `rest`/colour math, this prediction fails and I report that.

Kill criterion: if the gather's cost is NOT dominated by per-emitter work that temporal coherence can skip (i.e. fixed player work > 50% of the gather), the "view is the constraint" claim downgrades to "the view is expensive but flat", and the constraint moves back to the engine's budget overflow.
