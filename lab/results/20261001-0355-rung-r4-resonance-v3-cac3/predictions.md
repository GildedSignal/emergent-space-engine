# Predictions (written before the decisive full-matrix run)

Tuned on two development cases only: 2:1 mu=3e-4 exact commensurability
("dev-21": truth libration, e max 0.0727, amplitude 1.201 rad) and the
control at period ratio 2.55 ("dev-ctl": truth circulation, e max 0.0104).
Everything below is a prediction about the other 19 cases.

## Truth-2400 (the reference)

- All six "exact" resonant cases (both resonances, all three mu) librate.
- Detuned cases (+-1/3 of the nf2 half-width, inside the island by
  construction) librate with large amplitude; at mu = 3e-5 the island edge
  is nearest, so 0-2 of those 12 detuned cases circulate in the truth.
- Truth max e1 grows with mu: mu=3e-5 -> 0.02-0.04; mu=3e-4 -> 0.06-0.11;
  mu=3e-3 -> 0.25-0.5 (2:1 pumping above 3:2, roughly).
- Controls: e1 stays within +-20% of 0.01; all circulate.

## nf1 / nf2

- Regime match 18/18 (or 17/18 if one mu=3e-5 detuned case sits on the
  separatrix in the truth).
- e_pump ratios in [0.80, 1.15] (dev: nf1 0.885, nf2 0.838; the truth's
  osculating-e wiggle rides on top of the envelope, biasing the ratio down).
- libration_amplitude_ratio >= 0.9 (dev: 0.966 / 0.982); nf2 closer to 1
  than nf1 at mu=3e-3 where e^2 terms matter.
- controls 3/3 pass.
- evaluations_per_orbit in [0.3, 3] (dev: 0.69 resonant, 2.1 control);
  the compiled cycle is traced once per case and replayed exactly.

## truth-1200 (positive, judged against 2400)

- pump ratios within [0.99, 1.01]; amplitude ratio >= 0.98; regime 18/18;
  controls 3/3. (RK4 at 1200 steps/orbit is converged far beyond these
  thresholds; the ladder 600/1200/2400 brackets it.)

## averaged (negative)

- e1 constant at 0.01 everywhere -> e_pump_ratio_min about 0.02-0.3 on
  resonant cases (fails pump), and it circulates where the truth librates
  (fails regime). Controls pass (e1 constant is the right behaviour there).

## arc-g8 (negative)

- Repeats r4 v2's kill: first-order kicks along the unperturbed arc without
  phase feedback over-pump e; e_pump_ratio_max >= 1.5 at mu=3e-3 (v2's
  refinement study said about 2x). Regime may qualitatively match (libration)
  but with the wrong amplitude; controls borderline (v1 failed controls).
- evaluations_per_orbit = 8 quadrature nodes per conjunction window:
  about 2.7 (3:2 resonant), 4 (2:1) and up to 7.3 (control 5.0) per orbit.
