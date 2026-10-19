# Predictions (frozen before the decisive grid run)

Instrument smoke check (not decisive): circular-limit precession must match
6*pi/p at p=100 to <1e-3 relative; the far-field control cell must hold
(below). If either fails the instrument is broken: VOID, fix before reading.

Question: does the multiply-add cycle update (representation.md L67, under
L60's "at most one floor unit per event") survive one-quantum kicks near the
Schwarzschild separatrix p_sep(e) = 6+2e (units M=1)?

Setup frozen: e in {0.1,0.3,0.5,0.7,0.9,0.98}; kappa = p-(6+2e) in
{0.05,0.1,0.25,0.5,1,2,4,8}; kicks q in {2^-16, 2^-20, 2^-24} relative, on E
and L separately, both signs; budget = 2^-w * |Delta| with w in {16,20,24}
(primary w=20, q=2^-20). Truth = periapsis-to-periapsis integration of the
exact geodesic ODE (DOP853, rtol 1e-12). Derivatives by Richardson FD.

- P1 (divergence law): the Delta_t remainder scales as q^2/kappa^2
  (consecutive q arms differ by 4x in q -> 16x in R, to a factor ~2); the
  w=20 budget is violated for kappa < kappa*(e) with kappa* of order
  0.05-0.5 at q=2^-16.
- P2 (boundary scaling): kappa* shrinks as sqrt(q): kappa*(2^-20) ~
  kappa*(2^-16)/4, same order statement.
- P3 (phi vs t): Delta_phi also violates but in a band ~10x narrower than
  Delta_t's (weaker separatrix divergence); Delta_tau behaves like Delta_t.
- P4 (control, far field): at kappa=8, e=0.5, q=2^-20: R/budget < 1e-3 on
  all three channels (the premise HOLDS far from the separatrix; this is
  the positive control that must pass).
- P5 (crossing): at kappa=0.05 with q=2^-16, at least one kick direction
  leaves the bound region (plunge or unbound): the truth has no cycle at
  all, while the Taylor extrapolate returns finite numbers -> categorical
  failure, counted separately.
- P6 (population, honest scoping): the *static* bound population inside
  kappa*(q=2^-20, w=20) is small (order 1e-3-1e-2 of a smooth-in-p
  population); the load-bearing channel is the adiabatic one — every
  Peters inspiral (listed at L67 as a kick source) traverses kappa from
  O(1) to 0, so it crosses the unlicensed band with probability 1 and ends
  at an unrepresentable crossing. If kappa* comes out so small that even
  the last 0.05 of kappa is licensed at q=2^-20, the premise survives on
  this grid and I report it as licensed with the measured boundary.

Kill criterion (frozen): the multiply-add premise is refuted on the
separatrix family if any kappa >= 0.05 on the grid violates the w=20 budget
at q=2^-20 (P1), or if P5 holds (crossing unrepresentable). It survives
(with a measured licensed domain) only if neither happens.
