# Predictions (written before the clamp-raised sweep)

Context: the checker killed the "scene saturates at 428 bodies" finding (a CLI clamp,
`clamp(4, 400)` in xtask/src/universe/mod.rs:32) and named the gold experiment: the sweep at
true members, the corrected finding, and the readout floor re-derived against H0213's 1.2.
Known to me before these runs (the checker's own 10 s probe at true 4800): 3744 bodies and
climbing, gather 60.7% of a collapsed ~51 ms frame, player item 24.5 ms. Everything below
predicts beyond that probe; the 30 s runs, the true 480 case, the plane's own readout count
and the fixed/marginal decomposition are held out.

Inputs to the fit, from the author's record (already measured, not held out): gather p50
3.46 ms at 76 bodies (baseline), 6.6 ms at 428 bodies (the clamped run). Those two points fit
an affine law: fixed ≈ 2.8 ms, marginal ≈ 8.9 µs per body — NOT the stream probe's 15.4 µs
per emitter. H0213's 1.2 readouts/emitter against the stream's 1.98 explains the ratio:
15.4/1.98 = 7.8 µs per readout ≈ 8.9/1.2 = 7.4 µs per readout. The invariant is the cost per
readout (exact integer doll-chain math); per-emitter cost is geometry-dependent.

## Predictions

1. **The plane's gather is affine in bodies: fixed 2.5–3.5 ms + 8–10 µs per body per frame**
   (≈ 1.2 readouts × ~7.5 µs per readout). The stream's 15.4 µs/emitter is its geometry's
   readout count (1.98), not a universal per-emitter floor. The plane_readouts probe's bins
   will show µs_per_body flat near 8–10 µs across the ramp and readouts_per_body ≈ 1.1–1.4
   (H0213's regime), not 1.98.
2. **view_rel (shipped) reproduces H0213's ~1.2 reads/emitter on its 0.9c cases** while the
   author's stream geometry (dist 5e7) gives 1.98: the readout count depends on how stale the
   memo's linear guess is, i.e. on geometry, so "1.98 is the floor" is dead as stated; the
   floor for a cached crossing is 1 readout when the guess lands inside the acceptance window.
3. **True 480 members (30 s):** ~508 bodies at end; gather p50 7–9 ms (affine law), gather
   share 60–75%; frame p50 9–13 ms; first hitches above 16.7 ms in the hundreds per hour;
   player µs/item 4–7 ms (the O(N) scan); ship µs/item within 2× of the 97–106 µs the author
   measured (no O(N) term).
4. **True 4800 members:** bodies climb past 3744 toward ~4800 (or a battle-loss plateau);
   gather p50 40–75 ms; the frame collapses (p50 45–80 ms) with the gather still ≥ 55% of it;
   the engine keeps deferring (overflow frames ≈ all frames, rtf lowest 1% = 0.0); the
   player's item alone (25–40 ms) exceeds the engine's whole 5 ms budget — the author's
   prediction 2, which the clamp cost them, holds at true N; the frame's worst hitch tracks
   the gather's max, not the engine's.
5. **The claim survives with amended numbers:** the constraint stays the view gather at every
   true N measured; the 650-emitter ceiling is re-derived from the affine law (fixed ~2.8 ms
   and json+wire's own linear term both subtract) — I expect it to move by less than a factor
   of 2 (order unchanged), and the ≤ 5× micro-optimisation bound survives per readout.

## Kill criteria

- Gather share < 50% at true 480 or 4800 while the frame's worst tracks the engine or json →
  the constraint is not the gather at scale; the claim is dead and I report that.
- The plane's fitted marginal per body comes out ≥ 15 µs (the stream's number) → the
  fixed-cost reading is wrong; per-emitter cost is the invariant and the author's ceiling
  stands as written.
- plane_readouts shows ~1.98 readouts per body in the plane as flown → H0213's 1.2 does not
  describe the plane; the author's floor claim stands and my prediction 1 is wrong.
- Readouts per body in the plane fall below ~1.05 (below the one-readout floor plus rounding)
  → the accounting is wrong somewhere; investigate before claiming anything.
