# Predictions (written before the decisive run)

The falsifier is a faithful Python port of `crates/universe/src/view.rs::crossing`
(integer-tick Newton with the `(1 - speed - 1e-4)` acceptance window, bracket
fallback, 64-readout cap, warm/cold/foreign guesses) on uniform-motion emitters
in the root frame (c = 1, 1 tick = 1 light-tick). Cases I have NOT tuned on:

- **P1 (cost, relativistic content).** Warm-cache readouts per emitter are ~1
  only for slow emitters. At |beta| = 0.9 transverse or receding, >= 2 readouts
  for >= 90% of emitters, because the acceptance window is `1 - speed` wide
  while g falls by `1 + n.beta` per tick. The H0211 claim "about one readout
  per emitter" holds only for non-relativistic content; the 0.9c stream (B15)
  costs 2-3x.
- **P2 (empty window, cost only).** At combined closing speed >= 1 - 1e-4
  (e.g. 0.9c player vs a 0.999c stream head-on), `1 - speed - 1e-4 < 0` makes
  the first-readout acceptance window empty, so every emitter needs >= 2
  readouts even warm. I predict NO correctness loss: the bracket path returns
  the same tick as an exhaustive last-tick-with-g<=0 scan for every emitter.
- **P3 (tick quantization of the emission event, near range).** The rendered
  emission event is the integer tick, not the real root, so the apparent
  angular error is ~ v_perp * dtick / D. At 1080p with a 90 deg FOV
  (1.5e-3 rad/px) I predict the error crosses one pixel at D* ~ v_perp * 1
  light-tick / 1.5e-3, i.e. ~ 600 light-ticks (~3000 km) for v_perp = 0.9:
  invisible at interstellar range, ~1 px per tick of quantization in a
  relativistic dogfight at thousands of km.
- **P4 (held-out, correctness of "any cache gives the same view").** A foreign
  cache (guess wrong by 1e5 ticks, clamped to [0, t_now]) and a cold start
  return the identical tick for every emitter in the sweep, within <= 6
  readouts even at combined closing 0.9999. If this fails anywhere, the
  doc claim in view.rs ("any cache, however stale or foreign, gives the same
  view") is false and the attack lands as correctness, not cost.
- **P5 (one crossing, no lensing).** Arrival time is strictly monotonic in
  emission time (d t_arr/d t_e = 1 + n.beta > 0 for |beta| < 1), so each tube
  crosses the cone exactly once: I predict zero double roots over a 10^5-case
  sweep of beta in [0, 0.9999] x impact parameter x observer velocity. This is
  the premise surviving, reported as such.
