# Predictions (written before the decisive run)

Model: planar restricted 3-body (primary GM=1, parent mu=1e-3 on a circular orbit R=1),
Wisdom-Holoman split — exact Kepler drift + tidal kicks (with indirect term) applied at the
interval midpoint. N=32 massless bodies, a in [0.25,0.55], e in [0,0.4], fixed seed.
Horizon 100 parent orbits. Reference: fixed cadence, 512 kicks per parent orbit,
convergence checked against 256.

Scheme A (fixed): every body kicked every dt.
Scheme B (gated): per body, next interval tau = theta * |a_k| * tau_k / |a_k - a_{k-1}|
(relative field-change rule from the last TWO evaluations only; no extra field evals
spent on the decision), clamped to [dt_min, dt_max]. theta is the quantum knob.

Cases below were NOT tuned on (they are the held-out part of the sweep).

- P1 (the claim): at equal Jacobi drift D = max_t |J-J0|/|J0| over the horizon,
  B uses at least 2x fewer evaluations per body-orbit than A. If B ~= A (gain < 1.5x),
  the significance gate is dead weight, like the correctors (H0212).
- P2 (bounded, not compounding): for both A and B at reasonable coarseness, the
  log-log slope of |J-J0| vs t stays < 0.5 over the horizon (error bounded, no walk).
  A slope near 1 at some theta = the gate oversleeps and compounds -> that theta is
  past the edge.
- P3 (adversarial, large theta): theta = 0.5 must degrade worse than linearly in
  evaluations saved (the test can fail; a scheme that cannot fail is a control).
- P4 (held-out regime): gain shrinks for the most eccentric bodies (e >= 0.3):
  their field varies over their own orbit regardless, so gating buys less there.
  Predicted gain(e>=0.3) < gain(e<=0.15) by at least 2x.
- P5 (allocator consequence): B's per-body evaluation rate concentrates: the p99/mean
  ratio of per-body rate maxima exceeds A's uniform 1.0 by >= 3x — the allocator must
  budget the average maximum (Taleb), not the mean.
