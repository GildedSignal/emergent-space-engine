# Predictions — run 20261012-1524-dynamics-2b28 (written before the decisive ensemble)

Model: event-driven conjunction-impulse belt (see belt.py). GM_central = 1,
planar, N bodies, encounters = conjunctions with miss distance < b, kicks =
exact hyperbolic two-body impulses. Control = same orbits, kicks zeroed (pure
Kepler schedule). Regime number = the board's meso-motion number
R = U/sqrt(mu_p/b) (U = relative speed at encounter, mu_p = pair mass).

Belt configs: N=512, W=0.08, sig_e=0.015, b=4e-3, T=1500, seeds {1,2,3},
mu in {1e-9, 3e-8, 3e-7, 2e-6}  ->  R_med roughly {50, 9, 3, 1.1}.
N-scaling: mu=1e-9, T=300, N in {512,1028,2048} with W proportional to N
(fixed linear density), seeds {1,2}.
Formation: N=32, rank spacing 3e-3 in a, sig_e=3e-3, b=1.5e-3, T=3000,
{aligned, random} phases, mu in {1e-11 (weak), 1e-8 (strong)}, seeds {1,2,3}.

Pilot-tuned on: N=512 T=300 (mu 3e-7, 2e-6), formation T=3000 mu=1e-11.
Everything below is a prediction for configs/seeds not used for tuning.

## Feedback (belt)

- P1 (mu=1e-9, R~50): amplification A = enc_rate(kicked)/enc_rate(control)
  stays in [0.8, 1.1] over the whole 1500 orbits; <e^2> grows <= 10%.
- P2 (mu=3e-8, R~9): A in [0.6, 0.95]; <e^2> grows 10-60%.
- P3 (mu=3e-7, R~3): A in [0.4, 0.85]; <e^2> grows 50-200%; the rate never
  rises more than 10% above its own early-window value (quench, no cascade).
- P4 (mu=2e-6, R~1.1): at most a <= 1.5x early transient rise, then quench;
  A_end < 0.5; <e^2> >= 3x initial; deaths <= 5% of bodies.
- P8 (kill criterion): no config shows sustained exponential growth of the
  encounter rate (>= 2 consecutive e-folds). If one does, "self-quenching,
  subcritical" is dead and the finding becomes "a gate we lack".

## Scaling (fixed linear density)

- P5: per-body conjunction rate, per-body encounter rate, and repay ops per
  encounter each change by <= 15% from N=512 to N=2048 (fitted exponent
  |alpha| <= 0.15). Total work per orbit grows as N^beta with beta in [0.9, 1.1].
- P6: repay (window-recompute) share of total ops in [0.4, 0.95], and does
  not grow with N.

## Bursts (frame load)

- P7a: belt Fano factor (variance/mean of encounters per orbit) in [0.5, 2].
- P7b: formation peak/mean encounters per 50-orbit window >= 20, for BOTH
  aligned and random initial phases (the synodic lattice is commensurate:
  rank-m pairs conjunct at T_nearest/m — structural, not an initial-condition
  artifact).
- P7c: strong formation (mu=1e-8): peak/mean decays by >= 2x from the first
  wave to the last third of the run (stirring dephases the lattice);
  weak formation keeps its wave structure (peak/mean drop < 2x).

## What I expect to be wrong / soft

- The conjunction miss distance uses a parabolic local refinement, not an
  exact minimizer: encounter rates carry O(1) calibration error, so all rate
  comparisons are ratios against the same instrument.
- Pairs with synodic period > T are excluded (dn_eps = 2pi/T): a ~7% (W=0.08)
  population of slow pairs is invisible; biases absolute rates, not ratios.
