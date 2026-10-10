# Predictions (written before the decisive runs)

Tuned on: the two runs already done (seed 1, members 48: `--bench --seconds 30` at rtf 1 paced and rtf 100 unpaced). Everything below is predicted for cases not yet run.

1. **The rtf ladder (engine vs view).** The engine's per-frame cost grows with rtf (more sim time per frame), the view's does not (it is per-frame, per-emitter). Predicted: view_gather stays the largest share of the frame from rtf 1 up to rtf ~1000; at rtf 10^4 the engine's p99 per frame exceeds ~2 ms (approaching the 5 ms budget) and `overflow_frames` becomes nonzero on some frames (the budget bites and defers work). At rtf 10^4 the engine share exceeds the view share.

2. **N scaling (no culling).** The gather loops over all alive bodies with a Newton crossing each, so its cost is linear in alive emitters with no differentiation floor. Predicted: `--members 400` (≈8× the default bodies) gives ≈8× the gather p50 per frame (µs per emitter roughly constant, within 2×), while the engine's per-frame cost grows much less than 8× (fleet members are handed out as frames; per-body event rates stay near constant at fixed distribution).

3. **The differentiation floor (the exploit headroom).** At the default scene most emitters are unresolved dots: predicted ≥50% of emitters seen per frame have angular radius below one 1080p pixel at 90° FOV (≈8.2e-4 rad) on the majority of frames, and nearly all fleet members are (they cluster within a planet's moon system seen from AU away). Predicted the readouts (tube readouts spent on crossings) per emitter are 1–3, so the readout count per frame tracks the emitter count; i.e. the sub-floor emitters' share of gather time ≈ their share of the emitter count. Seeds 2 and 3 behave like seed 1 (fractions within 1.5×).

4. **Per-emitter cost.** Predicted gather cost per emitter per frame is of the same order as one engine kick per *orbit-scale* event: ~30–150 µs/emitter/frame on this machine — i.e. at 60 Hz, gathering one emitter for one second costs about as much as 2–9 of its kicks (kick median ≈76 µs). The view, not the kicks, is the frame's constraint at player rtf.

5. **Engine burstiness at fixed rtf.** The engine's per-frame cost is bursty (p50 ≈ 0, spikes on kick/boundary frames). Predicted at rtf 100: p50 < 0.2 ms while p99 > 5× p50; the 5 ms budget is not exceeded on p99.9 at rtf ≤ 1000.

Kill criteria for my claim (the constraint is the view gather's O(N) with no differentiation floor): if gather share < 30% at rtf ≤ 1000, or gather cost per emitter falls with members=400 (culling exists), or sub-floor emitters are < 20% at members 400 — then the constraint story is wrong or the exploit headroom is marginal.
