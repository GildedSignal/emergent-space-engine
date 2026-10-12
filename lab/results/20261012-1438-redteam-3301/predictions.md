# Predictions (written before the decisive run)

Target premise: `docs/representation.md` §2, Observables — "Each visible tube crosses the
observer's past light cone once; Newton's method finds the crossing, starting from the
previous frame's" — plus §6's cost row "The view: ≤ 1 sample per pixel per frame", and §3's
"the view has the hardest deadline". No rung guards this: `lab/rungs/` has no r6 (view),
and the only measurement (H0213) counted cache readouts at a steady 0.9c, never worst-case
iterations.

Falsifier: float64, flat 2D spacetime (c = 1), observer at 60 Hz proper frames, Newton on
g(t) = t + |X_obs(T) − x_em(t)| − T seeded with the previous frame's root, iteration cap 8.
Ground truth: bisection over a provably enclosing bracket. Scenes: constant-β head-on
approach; relativistic circular orbit; close straight flyby at impact parameter b; a burning
chase (thrust, "decisions are the only kinks").

## Held-out predictions

- **P1 (uniqueness, expect HOLDS):** a dense sign scan of g over the bracket finds exactly
  one root at every sampled frame of every scene. Mathematically g′ = 1 − n̂·v ≥ 1 − β > 0,
  so this should hold; a violation would kill the "crosses once" letter outright.
- **P2 (positive control, expect HOLDS):** all scenes at β ≤ 0.1: Newton converges in ≤ 2
  iterations, zero cap-hits. If this fails, my solver is broken, not the premise.
- **P3 (pure compression, expect HOLDS):** constant-velocity head-on at β up to 0.999
  converges in ≤ 2 iterations. The arrival-time compression (dt_e/dT = 1/(1−β), up to 1000×)
  is harmless by itself because the retarded map is affine; the failure needs curvature
  (orbital motion, flybys, burns) times compression. If P3 fails, my mechanism story is wrong.
- **P4 (close flyby, expect BREAKS):** straight flyby at β = 0.99 with impact parameter
  b ≤ 0.2 lt-s: p99 Newton iterations ≥ 4, at least one frame hits the 8-iteration cap, and
  the capped frame's rendered sky position is off by ≥ 0.1° (a moon-width error; very
  visible). At β = 0.9 I expect ≤ 3 iterations, no cap-hits.
- **P5 (relativistic orbit, expect BREAKS):** circular orbit at β_orb = 0.99, observer at
  3 orbit-radii: max iterations ≥ 5 with cap-hits ≥ 1 per orbit; at β_orb ≤ 0.6, max ≤ 3.
- **P6 (burning chase, expect BREAKS):** an emitter thrusting from β = 0.9 toward the
  observer: iteration p99 rises monotonically with β and reaches ≥ 4 before closest
  approach; each burn-kink crossed by the seed costs extra iterations (Newton loses its
  quadratic convergence across a kink).

If P2/P3 fail while P4–P6 hold, the finding is: the previous-frame Newton premise is sound
exactly where nothing relativistically interesting happens, and breaks precisely on the
scenes the game sells (pursuit at high c, relativistic flybys, watching a compact binary) —
at the view's hard deadline. If P4–P6 hold but P2/P3 fail too, the run is VOID (broken
instrument). If P4–P6 fail, the premise survives and I report it as such with the numbers.
