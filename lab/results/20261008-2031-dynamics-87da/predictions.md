# Predictions — 20261008-2031-dynamics-87da

Written after the stage-A control only (grid f vs direct Kepler: median rel
diff 1.8e-8). Nothing below has been tuned on. Model: decoupled Kepler pairs
(r8 v2's encounter-search model), conjunctions exact, so the miss sequence is
`f(theta_0 + k·2πα)` by construction — the tests below are about what that
buys and where it breaks, not whether the identity holds symbolically.

- **P1 (three-gap, integer decision).** For threshold m*=1e-4, among pairs
  with ≥ 8 window hits in 65 536 conjunctions, ≥ 95 % have at most 3 distinct
  inter-hit gap values (exact integer gaps). Falsified if many pairs show ≥ 4
  distinct gaps (would mean my window extraction is dirty, or the rotation
  picture fails operationally).
- **P2 (waiting-time law).** Median first-hit conjunction count k* scales as
  m*^(-1/2) (crossing arcs shrink like the square root of the threshold):
  fitted slope of log-median-k* vs log-m* in [-0.60, -0.40] over
  m* ∈ [1e-5, 1e-3].
- **P3 (per-pair equidistribution predictor).** Using only grid data (total
  window measure w from f), k*_pred = 1/w: ≥ 80 % of uncensored pairs within
  factor 2 at every threshold; median ratio in [0.5, 2].
- **P4 (arithmetic phase transition).** With beta = min_{q≤64} ||qα||:
  censoring fraction (no hit in 32 768 conjunctions at m*=1e-4) decreases
  monotonically with beta; the beta < 1e-4 bucket is ≥ 50 % censored, the
  beta > 1e-2 bucket ~ 0 % censored with median k* ≈ 1/w (equidistribution).
  Near-rational synodic ratios are the resonant populations: either quick or
  effectively-never.
- **P5 (conjunction-less leak).** Fraction of close approaches (local minima
  below m*=1e-3, dense sampling) farther than 0.2 rad in mean longitude from
  conjunction: < 2 % at e ≤ 0.2, but > 20 % at e ≥ 0.7 (consistent with
  r8 v2's 0.5–6 % belt leak and 78 % adversarial).

## Revision after a caught bug (before any decisive stage ran)


The v1 script sampled the wrong configuration slice (equal-time instead of
conjunction, i.e. M2 = M02 + (n2/n1)(theta - M01) instead of
M2 = theta + varpi1 - varpi2). The shared-harness control did NOT catch it;
an independent dense time sweep did (it found close approaches of 5.9e-4
where the wrong slice claimed a minimum of 1.69). v2 samples the conjunction
slice and its control compares against time-propagated distances at exact
conjunction times. Consequences for the predictions:

- P1, P3, P5, P6 unchanged (they never depended on the slice).
- P2/P4 as written assumed windows exist at m*=1e-4 for crossing pairs; the
  conjunction-slice minimum g_min is generically positive and of order
  e*e'*a-ish, so the threshold sweep now starts at 3e-3 and the headline
  quantity is the **window fraction vs threshold** (candidate-set shrinkage:
  the fraction of orbit-overlapping pairs that are certified never to
  encounter on fixed elements). P2's slope and P4's beta-monotonicity are
  evaluated on whichever thresholds produce windows; if no threshold in
  [1e-4, 3e-3] gives >= 30 % windows, that is itself the result and P2/P4
  are reported as not-evaluable, not as passed.
- **P6 (drift horizon).** With the window center drifting at η per
  conjunction, first-hit statistics stay within ~2× of the η=0 case while
  η·k* ≪ w, and for η ≳ w·(1/k*) the sweep dominates and every pair hits
  within ~1/η. The certificate's validity horizon is set by drift, not by
  the rotation arithmetic.

What would kill the whole picture: three-gap failing broadly (P1), or the
per-pair predictor being wildly off (P3), or the leak at belt e already
> 10 % (then conjunction sampling was the wrong skin from the start).
