# Predictions — run 20261007-1646-scout-0713 (scout lens, cadence)

Written BEFORE the held-out runs, after instrumentation and calibration only.

**Tuned on:** the `cal` scene alone (e0=0.3, mu_r=0.05, D=12, 48 orbits): the
budget line was checked there, and eps_v = 3.561e-5 calibrated as the largest
threshold where both rules hold (ruleA 5.35, ruleB 6.15 kicks/orbit).

**Held out (no tuning touches them):** h1 (e0=0), h2 (e0=0.7, D=30), h3
(e0=0.5, mu_r=0.01), mixed (192 bodies, e from Rayleigh(0.1)+U[0.15,0.7],
mu_r=0.05, D=25, 32 orbits).

**Budget (behaviour, not trajectory):** varpi-slope relative error <= 0.10;
|dq|/q <= 0.02; |de| <= 0.01 (e0=0 scenes: dq, de only). Truth = RK4 at
2048 steps/orbit, convergence 1.1e-5 relative; the kick model is KDK (second
order, verified 88x error drop from 8 to 64 kicks/orbit).

## Predictions

- **P1 (control, h1, e=0):** both rules hold the budget; kicks/orbit within
  0.7-1.5x of the minimal holding fixed cadence. No phase structure exists at
  e=0, so the rule must degenerate to uniform.
- **P2 (h2, e=0.7):** ruleB holds the budget with 1.0-2.5x fewer kicks than
  the minimal holding fixed N. The external tide is smooth and apocenter-
  weighted, so within-orbit adaptivity buys little.
- **P3 (h3, 5x weaker tide):** ruleB holds; the cut vs fixed stays within the
  same range as cal (the rule is set by eps_v against |a_pert|, so cadence
  scales as |a|^-1/2 for every body; the cut factor should be near
  scale-free).
- **P4 (mixed scene, the lens's headline):** the single global fixed cadence
  that holds every body is dictated by the worst body (predicted 8-16/orbit);
  ruleB's mean cadence is <= 4/orbit; **total kick cut 2-4x**.
- **P5 (within-orbit adaptivity):** ruleA/ruleB <= 1.3x on every scene. If
  ruleA beats ruleB by > 2x anywhere, my smoothness argument is wrong and I
  must say so.
- **P6 (failure honesty):** ruleA may fail the budget on h2 (its sup-window
  spans the long apocenter dwell). If it fails, ruleB carries any claim and
  ruleA's failure mode is named, not hidden.

## Kill criteria (decided now)

- Mixed-scene total cut < 2x at equal behaviour: per-body local cadence is
  killed as the lever for this scene family; the answer to q-cadence would be
  that gains must come from something other than local numbers.
- ruleB failing the budget on any held-out scene at eps*: the rule does not
  transfer; at best a silver with the failure named.
- A rule needing MORE kicks than minimal fixed on the e=0 control: the rule
  itself is broken, not the idea.

---

## Addendum (post-hoc configuration, written BEFORE its decisive runs)

The pre-registered rules A/B are KILLED by their own criterion: they hold on
cal but fail h2 (33% slope error at 1.6 kicks/orbit) and h3 (44% at 2.9).
Diagnosis: eps_v is an absolute velocity threshold while the budget is
relative, so a threshold set by |a| cannot transfer across mu_r and e. The
over-spend direction on h1 (5.5/orbit when 1 holds) says the same: the
trigger keys on the wrong quantity.

**ruleR (post-hoc, new configuration):** threshold the per-interval error
against the body's own per-orbit impulse |I_orbit| (both closed-form from the
osculating orbit): kicks until sup|Delta a| * dt^2/2 <= eps_rel * |I_orbit|.
Calibrated on cal ONLY (bisection on eps_rel); everything else held out.
The h1/h2/h3 fixed ladders are already known to me — ruleR's transfer is the
genuine unknown here.

- **P7 (transfer):** ruleRB holds the budget on h1, h2, h3 AND cal at the
  single cal-calibrated eps_rel. If it fails any scene, self-triggered rules
  from orbit profiles are dead at a single global constant and the dossier
  says so.
- **P8 (h1 over-spend):** ruleRB uses <= 3 kicks/orbit on the e=0 scene
  (still some over-spend vs the 1/orbit minimum: a sufficient condition, not
  a necessary one).
- **P9 (mixed headline):** ruleRB total kick cut vs the single global fixed
  cadence >= 2.5x, with >= 95% of bodies holding the budget.
- **P10 (within-orbit):** ruleRA/ruleRB <= 1.5x on every scene.

---

## Addendum 2 (second post-hoc configuration, written BEFORE its runs)

ruleR result: ruleRB transfers (holds cal, h1, h2, h3) but cannot cut — it
over-spends where the per-orbit signal nearly cancels (h1: 29.7/orbit vs 1
needed; |I_orbit| is the wrong normaliser at e ~ 0). ruleRA fails h3.
Diagnosis: normalise by the NON-CANCELLING path impulse int|a| dt instead.

**ruleP:** sup|Delta a| dt^2/2 <= eps_rel * int|a| dt over the orbit.
Calibrated on cal only (eps*=0.0422; PA 7.75, PB 12.40 kicks/orbit).

- **P11 (transfer):** rulePB holds all four singles. rulePA holds cal, h1,
  h2 but I expect it marginal on h3 (its budget sits at 9.7% on cal).
- **P12 (the honest expectation now):** even if it transfers, rulePB does
  NOT cut vs the per-scene robust fixed minimum (cal already shows 12.4 vs
  8). If the mixed-scene cut comes out < 2x, the whole single-constant
  self-triggered family is killed, and the dossier's claim becomes the
  measured reason: sufficient error bounds from orbit-local profiles are
  1.5-30x more conservative than the behaviour budget needs, because the
  budget is dominated by phase cancellations the bound cannot see.
