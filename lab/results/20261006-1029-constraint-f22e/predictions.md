# Predictions (written before the decisive instrumented run)

State so far (measured, unpaced/paced benches above): the frame is view-bound at every
operating point (93% at rtf 1, ~72% at rtf 100 paced); the gather is a serial loop over
all bodies (`for i in 0..u.n_bodies()`, view.rs:294) plus all active fleet members
(view.rs:343), with a Newton crossing per body whose readout cost grows with the game
time a frame sweeps (gather p50 1.41 ms at rtf 1 → 2.63 ms at rtf 100, same scene class).

## Held-out cases (not tuned on)

1. **Readouts per body per frame** (the cache's Newton guess quality), at rtf 1 and
   rtf 100: I predict median readouts/body in [1.5, 4] — the cache lands one Newton step
   from the root most frames, but the guess degrades as rtf grows (the cone sweeps more
   game time per frame). If it is > 8, the cache's slope model is broken, not the loop.
2. **Gather cost per emitter**: I predict the per-body Newton crossing dominates the
   per-member extrapolation by >= 10x (a crossing calls `state_rate`, which evaluates a
   binding; a member is arithmetic). So gather p50 per body >> per member.
3. **Emitters seen grows with N, cost linearly**: at the members-4096 scene (192 bodies)
   `view_json` (which serialises every seen emitter) is already the largest part (46%);
   I predict json ms scales ~linearly with seen emitters, ~3-6 us/emitter.
4. **The engine stays under its 5 ms budget at rtf <= 100 on this scene** (p99 5.2 ms,
   46/1200 overflow frames already seen); the first component to break the 16.7 ms frame
   as N grows is the view, not the engine, because the engine's cost follows events
   (61/s at rtf 1, 330/s at rtf 100) while the view pays per body per frame regardless
   of change.

## What would make the constraint claim wrong

- If readouts/body is ~1 at all rtf and gather per emitter is ~1 us, then the O(N) loop
  is cheap in constant factor and the constraint is elsewhere (engine per-event cost);
  the adoptable fix would then be nothing on the view.
- If the gather's cost does not grow with rtf on a fixed scene, my "cost follows swept
  game time" mechanism is wrong.
