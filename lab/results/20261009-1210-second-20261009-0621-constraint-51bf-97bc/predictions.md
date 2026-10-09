# Predictions (written before the lever runs)

The reproduction is done: mode-0 (lever unset, patch applied) gives digest `6ce636fa…` on stock and
patched binaries; the unpaced view digest `cb69811f…` matches the author's bit for bit; bodies 0.947–0.950
of the gather. The finer split (new buckets) says, unpaced: partial readouts 300.8 ms of the 890.1 ms
bodies loop, of which sources' tube reads (`ctx.secondaries`) 159.4 ms, field arithmetic (`force::field`)
31.2 ms, the rest the emitter's own tube reads and bookkeeping.

The checker's gold experiment: the named lever — one shared read of a doll's field sources per frame
(`ES_SHARED_FIELD=1`) — and the bar: gather share falls materially (frame median ~3× lower, or gather
below the engine's share), universe digest unchanged, B16 intact. Cases not tuned on; what I expect:

1. **Outcomes cannot move.** The lever touches only `observe::partial` (the view's read layer; the
   engine's kicks read their own sources in `step.rs`). Digest `6ce636fa…` bit-identical in every
   lever mode. Mode 2 (canonical path drives the view, shared path only measured) gives the same view
   digest as mode 0.
2. **The dedup factor is large.** Field-source first touches drop to ≈ dolls × frames; I predict
   ≥ 80% of secondaries fetches become reuses, and `sources_tube_ns` falls by ≥ 80%.
3. **The gold bar is NOT met, and the refutation is the result.** The sources' tube reads are
   159.4 ms of an 890 ms bodies loop; deleting nearly all of them cannot bring the gather (0.67 of
   the frame) below the engine (0.21), nor cut the frame median ~3×. I predict: bodies loop falls
   ~15–20% (unpaced), frame p50 improves ≤ 1.3×, gather share stays ≥ 0.58. The constraint remains
   the gather; the residual top term is the crossing search's own tube work (binding walks and
   per-level `cartesian` reads, the ~590 ms outside `partial`), a representation question, not a
   scheduling one.
4. **The display delta is real but small.** Mode 2's max stepped-state delta: nonzero (the shared
   read tick differs from later emitters' mids by up to the scene's retarded-time spread,
   ~10⁷–10⁸ ticks), max position delta ≤ 1 root unit (≈ 1.5 km; the emitters themselves move
   ~0.1–1 root units per frame), max velocity delta ≤ 10⁻⁶ doll units. B16 passes (analytic gate,
   independent of the gather); the view tests pass.

If (3) fails the other way — the gather does fall below the engine — the checker's bar is met and
the claim is gold as stated. If (2) fails (little dedup), the lever is a no-op and the anatomy, not
the sharing, was wrong.
