# Predictions (written before the decisive experiment)

Setup: Schwarzschild, M = 1 (geometric). Companion (emitter) on circular orbit r_s = 12M,
observer static at r_o = 50M. Truth = float64 geodesic integration (photon Binet
u'' = 3u^2 - u, travel time from dt/dphi along the null geodesic). Design letter =
flat past light cone (retarded time from coordinate distance) + memo deflection(b) ~ 4M/b
(direction only). Sweep over orbital phase Phi (angular separation emitter-observer-horizon).

- P1 (time/phase): the flat cone mis-times light by dt >= 3M for at least half of the
  orbital phases, and >= 6M near superior conjunction (emitter behind the hole).
  As orbital phase error Omega*dt: >= 4 deg over half the orbit, >= 8 deg near
  conjunction. (Basis: Shapiro ~ 2M ln(4 r_s r_o / b^2), b in [5.5, 12].)
- P2 (direction): after applying the 4M/b memo bend, the incoming-direction residual
  against the true geodesic stays >= 0.2 deg everywhere in the sweep and >= 1 deg for
  phases with b < 10M (finite-distance and (M/b)^2 terms missing from the memo).
- P3 (controls): (a) the integrator reproduces the weak-field total deflection
  4M/b + 15pi/4 (M/b)^2 at b = 100M to < 0.5%; (b) in a far-field scene
  (r_s = 1000M, r_o = 2000M) the same flat-cone error is < 0.05 deg of orbital phase
  (the attack is geometry-driven, not an integrator artifact).
- P4 (premise 1 proxy): exact Schwarzschild apsidal advance vs the 1PN formula 6pi/p:
  circular-orbit gap ~40% at p = 12M, ~10-15% at p = 25M, ~4% at p = 100M; B11's
  allowance (1% + 2*8/p) reaches ~80% at p = 20M, i.e. the gate is padded to admit
  exactly this truncation error (a shepherd, not a guard).

Not tuned before the run: the sweep phases, the far-field scene, the deflection control,
and the p-grid in P4.
