# Predictions (written before the decisive runs)

Question: what does the plane's frame budget buy today — the stage split at the
tail, the capacity in fleet members and time factor, and the marginal price of
the player's burn? All on the shipped `xtask universe --bench`, Linux/x86
(orders of magnitude only; the integrator re-measures on the M1).

The runs (each ≤ 35 s): members ∈ {48, 480, 4800} at rtf 1 level 0; members 480
at rtf 10 level 0 (throughput stress); members 480 at rtf 1 level 12 (the order
price); one repeat and one unpaced run of the members-480 baseline as
determinism controls. I have not run any of these configurations before writing
this file. Tuned on nothing.

1. **The readout, not the physics, owns the frame at today's scene size.**
   At members 480 / rtf 1 / level 0, the engine's share of frame CPU at p50 is
   below 40%; view_gather + view_json + wire together take the majority. The
   engine's p99 CPU stays inside its 5 ms budget. (If the engine dominates,
   this is wrong and the bottleneck is elsewhere than the queued b-readout-cost
   build suggests.)

2. **Capacity degrades by throughput, not by hitches.** From members 48 to
   4800 at rtf 1, frame_ms p99 stays within 2× of the members-48 value (the
   per-frame budget bounds the frame); what grows is deferred work —
   overflow_frames > 0 at 4800 and/or the rtf's lowest 1% falling — and at
   rtf 10 the same happens earlier in N. If instead p99 or the worst hitch
   grows > 2× with N, the bounded-work premise (plane.md foundation 7) fails
   on the shipped code, which would be a stronger finding.

3. **The player's order is cheap at the tail but visible at the worst frame.**
   At level 12 vs level 0 (same seed, members 480, rtf 1): frame_cpu p99.9
   grows by less than 2×, and the worst hitch lands inside or within 10 frames
   after a burn window (the script burns frames 240k..240k+20) in the level-12
   run. If burns are invisible even at the worst frame, the order is free
   inside the budget — also a result.

4. **Determinism controls (must hold, else VOID):** the members-480 baseline
   repeated gives the identical digest, and paced vs unpaced gives the
   identical digest at the same cut.

5. **Held-out extrapolation (not tuned, checked after):** events per second at
   members 4800 stays above 10⁵/s on this box (the plane's event path is
   table/native-arithmetic work, not integration); if it falls below, the
   per-event cost is over ~10 µs and the "cost at a billion" gap is worse than
   the board's 190-core figure implies for the new engine.
