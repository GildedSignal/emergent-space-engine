# predictions.md (written before the decisive 256-seed run)

Tuned on: 8 seeds of the sampler (a/R_H ~ 0.12, 0.2, 0.3 pro/retro) used to
debug the pipeline (a vis-viva bug in osc(), the averaging constant, the
precession estimator), plus 6 more (0.45, 0.6) for estimator range. Held out:
the other ~242 seeds, especially retrograde 0.6-0.9 R_H and prograde near the
0.5 R_H stability edge.

1. truth: prograde moons escape for a/R_H ≳ 0.5 (nearly all, mostly
   non-chaotic); retrograde stay bound to ~0.85 R_H with escapes above that;
   the chaotic fraction (class flips under da/a = 1e-6) is 20-40%, peaking in
   the prograde 0.45-0.65 band and the retrograde 0.8-0.95 band. Bound
   retrograde precession stays |nu| < 0.05, prograde bound precession grows
   to ~0.3.
2. kick-avg: passes class on the domain (a/R_H <= 0.3: no truth escapes
   there) with 1.0, but precession_match on the domain lands between 0.90 and
   0.99: the single-averaged quadrupole is 2-6% off at a/R_H ~ 0.12-0.2 and
   18-108% off at 0.25-0.3 (the retro evection stationary point sits near
   0.3 R_H). So I predict the rung's prec criterion (>= 0.99) FAILS for
   kick-avg on its domain, and tau0 lands at a/R_H ~ 0.2 (tau ~ 0.005),
   well below the 0.49 R_H (tau0 = 0.08) that law.md's class-only argument
   gives. If instead it passes, the octupole correction was smaller than the
   0.3 R_H seeds suggest.
3. no-tide: class ~1.0 on the domain (no escapes there either), precession
   ~0 (frozen periapsis) => fails prec. This is the designed negative.
4. hill-torus: declares tori on 55-75% of the a/R_H > 0.3 seeds (most
   retrograde up to ~0.85, prograde up to ~0.45); class_match ~1.0 on its
   declared domain (the compiled torus cannot escape and declared seeds are
   bound); precession_match 0.9-0.99 (frequency drift on 30 more orbits
   breaks the 10% window for a few); compiled_fraction (tau >= tau0) between
   0.35 and 0.6 (the denominator includes the prograde chaotic sea).
5. Poincare section: nested tori around a retrograde-stable core, a chaotic
   sea for prograde x > ~0, escapes at large |x|.
