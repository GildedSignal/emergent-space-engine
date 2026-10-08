# Predictions (written before the decisive experiment)

Held-out cases: none of the numbers below were tuned on the simulation; they are
derived analytically from Kepler scalings before running. The simulation is
Kepler (the belt's weak-field limit of the two-body doll), first-order jet
(cycle from initial (E, L) + stored ∂/∂E; offset accumulated exactly), kicks
applied per orbit.

Notation: n*(e) = kicks survived until the periapsis-epoch error crosses the
10⁻⁶ relative floor (law.md's floor). Belt arithmetic uses B18b's own scene:
Rayleigh e with σ = 0.3, banded p; kicks/orbit 0.3 (H0190 with averaging);
crossings per cycle creation 2m·log₂((1+e)/(1−e)) + 8 at m = 16 (B9).

## A1 — the cycle-derivative jet at the separatrix (the decisive run)

- **P1.** At fixed periapsis p and fixed *absolute* kick size δE, the horizon
  scales as n*(e) ∝ (1−e)^(2/3) (from relative kick δE/|E| ∝ 1/(1−e) and epoch
  error ≈ (5/4)(δE/|E|)² n³). Point prediction: n*(0.99)/n*(0.5) ≈ 0.074;
  accepted band [0.03, 0.15].
- **P2.** The failure is confined to the time channel. The angle channel
  (apsidal advance) stays below the 10⁻⁶ relative floor at every e for the same
  kicks (Kepler Δφ = 2π exactly; GR's 6π/(p(1+e)) varies only 2× over all e).
- **P3.** Belt arithmetic: with σ_e = 0.3, the top 1% of the e distribution
  consumes ≥ 30× the median body's per-orbit compile crossings, and the p99
  per-body compile cost exceeds 100× the median.
- **P5 (control).** Random-sign kicks of the same |δE| survive ≥ 3× longer
  than correlated (secular, same-sign) kicks.

## A2 — strong deflection / photon ring (secondary, analytic + numeric)

- **P4.** The first relativistic image of an aligned source sits within ~1
  pixel (1080p, 60° FOV → ~10⁻³ rad) of the shadow edge for observers outside
  r ≈ 6M (predicted offset at r_o = 10M: ~5×10⁻⁴ rad), so the one-sample-per-
  pixel cap hides it visually — but placing it at all needs (b − b_c)/b_c
  resolution finer than ~10⁻³, which a uniform-b, single-valued deflection
  memo cannot give. Deflection α(b) diverges logarithmically (Darwin):
  α ≈ −ln(b/b_c − 1) − 0.40.

## A survivor (analytic, no run needed)

- The flat-space gather premise "each visible tube crosses the observer's past
  light cone exactly once" is *true*: F(τ) = τ + d(τ) has F′ = 1 − β·n̂ ≥ 1 − β
  > 0 for any subluminal emitter, bound or not. Multi-crossing is a curved-
  spacetime (lensing) phenomenon only.
