# Predictions (written before the assists/handoff/binaries decisive runs)

Binaries (already spot-checked at 5 seeds while wiring, not tuned on the 1024-seed set):
- eob-doll period_pass_fraction = 1.0 and nu_effect_pass_fraction >= 0.99: the energy map
  is 1PN-exact, residuals are 2PN (~3e-6 at p=1000).
- test-mass nu_effect = 0.0 (no nu channel). newton period/nu = 0.0.
- precession: under the faithful truncation estimate (exact-vs-oracle gap at nu=0,
  ~7.6/p), NO seed in [20,1000] judges (min gap 0.76% > half-tolerance 0.5%).
  Under the milder oracle-internal next-PN term (~4.2/p) ~40 judge and pass.
  I record the faithful reading and expect min_judged_seeds = 0 to fail the rung's
  judged criterion - that is a rung-design finding, not a doll failure.

Assists (held-out: not simulated yet):
- patched doll within 1% of the N-body reference for most impact parameters;
  largest errors at b = 50 R_earth (third-body tide over the long shallow flyby):
  expect assist_pass_fraction in [0.9, 1.0]; median |dv| error < 0.3%.
- turn angles from ~15 deg (b=50) to ~150 deg (b=1.5).

Handoff (held-out):
- a symmetric 1-year-periodic 2:1 resonant orbit with ~SOI-scale encounters exists
  near x0 ~ 1 - 0.004, ydot0 ~ 4.1; Newton shooting should find it in < 10 iterations.
- energy-error growth exponent <= 0.05 (patched handoffs inject ~1e-4 errors that
  random-walk, not compound).
- if shooting fails: fall back to a co-orbital chain and report honestly.
