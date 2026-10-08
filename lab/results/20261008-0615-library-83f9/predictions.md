# Predictions (written before the run; nothing below was tuned)

Decisive experiment: `exp_cadence.py` — a belt surrogate of the kick layer.
Scene: N=1000 bodies, a in [0.95, 1.05] AU, Rayleigh e (cold: sigma_e = 0.05, hot: 0.20),
mu = 1, one perturber mu_p = 3e-3 on a circular orbit at 1.6 AU (never crossed). T = 10 orbits.
Machinery for every policy: exact Kepler drift between kicks, impulse kick
dv = a_pert(r - r_p(t)) * dt. Truth = the same machinery at 512 kicks/orbit.
Policies: fixed(k), k in {8,16,32,64}; trigger(delta_v): after each kick the next kick is
SCHEDULED at dt = delta_v / |a_pert| (local, closed form, one division per kick), capped at one
orbit. No per-frame checks. Cost counted = kicks applied (+1 division each).

Held-out predictions (cases not tuned on; medians over 3 seeds):

- P1 (the gold bar): at matched median |da/a| error vs fixed16, trigger(delta_v) applies
  >= 4x fewer total kicks than fixed16. Reason: most bodies sit far from the perturber and coast.
- P2 (fat tails): under the trigger, the p99 body receives >= 8x more kicks than the median body.
- P3 (one rule, two scenes): the SAME delta_v (chosen once on the cold belt to match fixed16's
  error) keeps the hot belt's median error within 2x of that scene's own fixed16 error, with a
  kick cut >= 2x (hot belts kick more; the cut shrinks but survives).
- P4 (kill criterion, written before the run): if the trigger needs >= 1/2 of fixed16's kicks to
  match its median error, scheduling from |a_pert| alone is KILLED as the cadence rule — the
  residual would then be dominated by what local drift magnitude cannot see (resonance phase,
  e-vector orientation), and the rule must schedule from a richer local invariant.

Numbers are floats; this is a mechanism probe of a policy, not a canonical outcome (PRINCIPLES:
floats explore, integers decide). Behaviour metric: median |a_T(policy) - a_T(truth)|/a over
bodies; also p95. Deterministic seeds 1..3.

---

# Post-diagnosis addition (disclosed: written AFTER the first run killed P4)

First-run outcome (cold belt, medians): fixed16 med_err 6.0e-5 at 160k kicks; magnitude
trigger reaches that error at ~550-600k kicks (between trig3e-5: 1.1e-4 @ 466k and
trig1e-5: 1.7e-5 @ 813k) — P1 failed, P2 failed (k_p99/k_med = 1.2, not >= 8), P4 FIRED:
scheduling from |a_pert| alone is KILLED. Diagnosis: per-kick impulse error ~ jerk*dt^2/2,
so the interval must come from the LOCAL JERK (curvature of the perturbation along the
arc), not its magnitude; magnitude is nearly uniform across this belt (d = 0.55-0.65 AU).

Diagnosed variant (still local, closed form, one sqrt per kick):
  dt = sqrt(2*delta_v / jerk_est),  jerk_est = max(2*mu_p*|ddot|/d^3, a_pert*|n - n_p|)
with d, ddot from body and perturber states at the kick. New predictions:

- P5: at matched fixed16 med error, the jerk trigger applies <= 1/4 of fixed16's kicks
  (kicks concentrate near conjunctions where the field curves).
- P6: k_p99/k_med >= 4 under the jerk trigger on the hot belt (phase concentration).
- P7: the same delta_v holds the hot scene within 2x of its fixed16 error.
- P8 (kill): if the jerk trigger also cannot beat fixed16 at matched error here, then NO
  local closed-form rate rule sets this layer's cadence; the cadence must come from the
  certificate machinery (the energy register's residual), not the field's local derivatives.
