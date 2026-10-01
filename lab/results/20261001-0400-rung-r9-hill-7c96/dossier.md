# Dossier: rung r9 (Hill regime), run 20261001-0400-rung-r9-hill-7c96

**Claim:** Orbit-averaged tidal kicks keep a moon's *class* right everywhere
they are asked (a/R_H <= 0.3), but its *precession* only to tau ~ 0.004
(a/R_H ~ 0.17) - 20x lower in tau than the class edge at 0.49 R_H - and a
compiled two-frequency torus follows the class of every seed it declares yet
the precession of only 13% of them, because the evection forcing drives the
eccentricity through near-zero where a fixed-frequency apsidal phase cannot
follow. tau0 = 0.0036 (precession-gated), compiled_fraction = 0.046.

**Bottleneck:** B14 and the regime selector in `docs/law.md` (tides and the
tau regime): where orbit-averaged kicks stop, and how much of the Hill
problem compiles into two-frequency tori.

## Metrics (metrics.json)

| config | class_match | prec_match | dense_steps | extra |
|---|---|---|---|---|
| truth (positive) | 1.000 | 1.000 | 0 | - |
| kick-avg | 1.000 | **0.554** | 0 | tau0 = 0.0036 |
| hill-torus | 1.000 (45 declared, non-chaotic) | **0.133** | 0 | compiled_fraction 0.046 |
| no-tide (negative) | 1.000 | **0.000** | 0 | - |

The positive passes, the negative fails exactly one way (frozen periapsis),
so the rung is decidable: **KILL of kick-avg and hill-torus on the
precession criterion**; both pass class and cheap. Under verdict.py this is a
KILL of configurations, not of the method.

Truth: 256 seeds, 101 escaped (76 prograde from 0.43 R_H, 25 retrograde from
0.73 R_H), only 4 class-flips under da/a = 1e-6 (escapes are robust, not
chaotic-flagged); bound retrograde moons survive to 0.89 R_H. Convergence:
24 seeds re-run at rtol 1e-13 - zero class changes, worst precession-rate
change 0.00% (check_truth.py). Total DOP853 work ~3.7 M steps (nfev 44.4 M);
dense_steps is 0 for every configuration because none of them is the engine's
dense order (the truth is the external reference; criterion kind is `type`).

## Evidence

Sampler: `random.Random(20261010)`; per seed drawn a/R_H ~ U[0.1,0.9], mean
anomaly, periapsis angle, in that order; seeds 0-127 prograde, 128-255
retrograde; e0 = 0.05 (the rung fixes a/R_H, senses and phases, not e0).
tau = (2/3)(r_apo/R_H)^3, r_apo = a(1+e0). Truth: CR3BP in the rotating
frame, DOP853 rtol = atol = 1e-12, 50 planet orbits; class from the final
state (osculating a < 0 or r > 2 R_H); chaotic = class flips under da/a =
1e-6. Precession rate = robust |z|^2-weighted, Cauchy-reweighted slope of the
unwrapped argument of the secular eccentricity vector (double Hann over 2
planet orbits), one identical pipeline for every configuration
(`common.prec_rate` after `common.secular_z`).

Commands (this folder, cloud x86 4 vCPU):

```
python3 verify_secular.py   # closed forms vs 64-pt Gauss-Legendre quadrature: max rel err 3.9e-15
python3 truth.py            # 290 s wall, 4 procs; prints counts and nfev
python3 cands.py            # ~3 s; kick-avg (RK2 kicks, one per moon orbit), no-tide, hill-torus
python3 metrics.py          # writes metrics.json, table.json
python3 check_truth.py      # rtol 1e-13 ladder, 24 seeds: 0 mismatches, 0.00%
python3 picture.py          # picture.png
```

kick-avg's model: the single (moon-orbit) average of the rotating-frame
quadrupole tide (the evection Hamiltonian) with alpha = 1 + (3/2)e^2, beta =
(5/2)e^2; its mean circulating precession is (3/4)(n_p^2/n_m), the classic
evection rate, and it matched the truth's deep seeds to 1.5-3% (a/R_H ~ 0.12).
The 25 precession failures in its domain sit at a/R_H in [0.17, 0.30]: the
octupole and the (n_p/n_m)^2 terms break the 10% window there, and the
retrograde stationary-precession point (rate through zero) sits near 0.3 R_H
where the *relative* error explodes. hill-torus: a single-frequency
rotating-frame Fourier fit covers nothing (coverage ~ 1e-4; the regular Hill
moon is quasi-periodic with two frequencies, not periodic), so the compiled
generator is the two-frequency fit of the secular eccentricity vector;
declaration = coverage >= 0.90 + frequency-diffusion between window halves
(Laskar LDV), frozen before scoring. 81/256 declared; all 45 judged declare
'bound' and all 45 are bound; but the compiled phase winds spuriously when
|c0| ~ |c1| (forced ~ free eccentricity, e grazes zero): only 6/45 keep the
10% precession window over the held-out 30 orbits.

## Predictions

`predictions.md` was written before the 256-seed run. Hit: prograde escape
band from ~0.43-0.5 R_H, retrograde bound to ~0.85-0.9, no-tide failing
precession exactly, hill-torus class 1.0, chaotic fraction low, kick-avg
precession failing its domain gate, tau0 near a/R_H ~ 0.2 (measured 0.17).
Miss: I predicted 55-75% declared tori and 0.35-0.6 compiled_fraction;
measured 32% declared and 0.046, because a 20-orbit window pins a ~0.02/orbit
frequency only through the phase slope and the near-zero-e grazing defeats
the fixed-frequency compile far more often than expected. Also missed: the
single-frequency rotating-frame fit's total failure (found and fixed during
the run, disclosed above).

## What would make it wrong

The 10% precession window is an *error size* on a quantity that passes
through zero (retrograde stationary point, evection-modulated rates); the
rung's own r2 lessons warn against exactly this. tau0 = 0.0036 is therefore
metric-driven: gated on class alone, the edge sits at tau ~ 0.07-0.09
(a/R_H ~ 0.45-0.5), matching law.md's tau0 = 0.08. e0 = 0.05 and the draw
order are this run's choices. The precession estimator (secular smoothing +
weighted robust phase slope) is shared by every configuration, so candidate
ordering is fair, but a different estimator shifts the fractions.

Cost of adopting: nothing to adopt as-is - this rung says where each regime
*starts*, not that either candidate is the law. Fit with PRINCIPLES: "under
the right representation many symmetries can appear" (32) - the two-frequency
torus is the right representation for class (45/45) but not for the apsidal
phase through e ~ 0, where the rung's own fallback (the dense order) is the
honest answer; "we know we have a fish, we need to find its water".

## The lens

The regime-selector lens wanted one sharp tau0; the honest answer is two
numbers: class breaks at tau ~ 0.08, precession at tau ~ 0.004, and the
compiled torus's phase breaks where forced ~ free eccentricity. A gate that
mixes them (the 10% relative window near a zero crossing) will misgrade -
the integrator's criterion-writing rules (r2) predicted this shape of failure.
