# Predictions (written before the decisive experiment)

Held-out cases I have not tuned on, and what I expect:

1. **View-gather decomposition.** I will print, per frame, the gather's readout count
   (`ViewCache.readouts`, tube evaluations inside the light-cone Newton search) and the
   `seen` list size, on the plane bench at rtf 100. Prediction: readouts ≈ 1–3 per emitter
   (the Newton cache holds), so the cost is NOT the search but the readout itself:
   one `state_rate` (a tube read through the doll chain) costs O(10 µs), i.e. ~100× a
   raw Kepler evaluation. If readouts per emitter exceed ~10, my claim is wrong and the
   search, not the readout, is the constraint.
2. **Scaling in emitters.** With `--members M` growing (M = 100, 400, 1600), view_gather
   p50 grows linearly in (bodies + members): the gather is O(N) per frame with no
   visibility cut. Prediction: slope ≈ 40–60 µs per emitter per frame; intercept small.
   If it saturates, there is a cull I have missed and the claim dies.
3. **Engine share at fixed rtf as N grows** stays sub-linear (budgeted, capped at 5 ms):
   the engine trades rtf (overflow) for frame time, the gather cannot. So the gather's
   *share* grows with N toward 100%: at ~2,000 emitters the frame is > 90% gather and
   p99 crosses the 16.7 ms deadline on this box.
4. **Where the readout cost lives:** `state_rate` walks the doll chain and calls
   `clock_rate` (a potential evaluation) per readout. I predict ≥ 60% of gather time is
   in `observe::state_rate`/`root_state_with` (chain walk + rate), not in `blackbody`,
   JSON or allocation of `seen`.
