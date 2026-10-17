# Predictions — run 20261017-1240-scout-f666

Written before the decisive experiment (`handoff_rule.py`). Held-out axes (not tuned on):
μ ∈ {1e-4, 1e-2}, kick sizes other than 3%, sampling dt halved, longer windows.

The replica: planar CR3BP (μ = 1e-3 primary set; planet orbital period 2π), DOP853
rtol/atol 1e-12, a body born planetocentric-circular at r0 ∈ {0.3, 0.49, 0.5, 0.7, 0.9}·R_H,
both senses, 20 planet periods. All rules replay the SAME stored true trajectory
(handoffs do not feed back — the rebind's physics error is priced separately via the
pages' scar law; disclosed limitation).

Rules:
- R0 shipped replica: per-tick owner = planet iff (r < R_H/2 ∧ E_p < 0), both directions.
- R0f: R0 at half the sampling dt (Zeno signature control).
- R1 hysteresis: leave planet iff (r > 0.65 R_H ∨ E_p > 0); enter iff (r < 0.5 R_H ∧ E_p < 0).
- R2 time-regularization: R0 + dwell ≥ 1 planet period between handoffs.
- R3 per-cycle extent (the candidate): decide only at apoapsis passages, on the cycle's
  own radial extent r_apo against the empirical stability radius f(Λ)·R_H with margin
  0.05·R_H, f continuous in the synodic sense Λ = h_z/r_apo² (0.5 prograde → 0.7
  retrograde, linear in between; no categories). Release iff r_apo > (f+0.05)R_H;
  capture iff r_apo < (f−0.05)R_H ∧ E_p < 0.

## Pre-registered expectations

- P1 (negative control — the replica must reproduce the failure class): R0 chatters on
  the marginals: ≥ 10 handoffs on (0.5,−), (0.49,−), (0.9,+), (0.9,−); class ≥ 10²
  on at least one; R0 = 0 on (0.3,±) and (0.7,−).
- P2 (Zeno signature): R0f ≈ 2× R0's count (per-tick scaling); R3's count invariant in dt.
- P3 (the candidate): R3 handoffs = 0 on every case the truth retains (including the
  0.49/0.5 R_H chatter probes); 1–5 total on cases the truth ejects (0.9 R_H class);
  never above 1 per moon-orbit on any case; classification = truth on all 8 cases.
- P4 (hysteresis and dwell, the field cures, alone): R1 leaves ≥ 1 per orbit chatter on
  at least one marginal case (the E_p flip channel is not r-hysteresis-fixable); R2
  bounds the count at ≤ 1 per planet period but delays releases — measured, not predicted.
- P5 (held-out, kick robustness): a 3% velocity kick at t = 10P on (0.5,+): R3 re-decides
  in ≤ 2 handoffs; R0 re-chatters (≥ 10 in the post-kick window).

## Kill criteria

- K1: if no R0 case reaches ≥ 10 handoffs, the replica failed to reproduce the refuted
  predicate's failure class — rule comparison VOID (instrument cannot fail).
- K2 (moon test): if R3 releases a case the truth retains deep inside (0.3,±), R3 dies.
- K3 (Zeno-free): if R3 exceeds 1 handoff per moon-orbit on any case, R3 dies.
- K4 (release test): if R3 retains forever a case the truth ejects (0.9 class), R3 dies.
- K5: if |ΔC_J| of the truth integration exceeds 1e-6 on any case, the trajectory is
  not trustworthy and everything above is VOID.

Grading bar: R3 must pass K2–K4 and beat R0 by ≥ 10² on the chatter cases to be worth
a page update.
