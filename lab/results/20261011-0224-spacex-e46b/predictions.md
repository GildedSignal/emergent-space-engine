# Predictions (written before the decisive runs)

Scene: belt a ∈ [2.3, 3.4] AU, e Rayleigh(0.05) capped 0.2, Jupiter-like perturber
(a = 5.2 AU, e_J = 0, μ as run), heliocentric split truth (direct + indirect),
350 steps per inner orbit. Program: Laplace–Lagrange free precession from birth
mean elements, per-body windows of exactly 8 synodic periods. Two program
variants: (a) textbook rate A(a), no refit; (b) rate refit on the first half of
the arc (reabsorption), residual measured out-of-sample on the second half.
Quantum q = 1e-6 in e-units. Distance to nearest strong resonance (2:1, 3:1,
5:2, 7:3) in units of W = 2.5·μ^(2/3) (the repo's convention, B17).

Not yet run at the decisive scale (only smoke tests at ≤ 20 PJ, N ≤ 512,
which showed the instrument problems I fixed, and nothing at 300 PJ):

- **P1 (programs hold the bulk).** With rate refit, bodies farther than 3W
  from every strong resonance keep the out-of-sample scar below 1e-4 in e and
  NOT systematically growing: frac(>1e-4 | x>3W) < 1%.
- **P2 (resonance is where bits are made).** Within 1W: frac(>1e-4) > 50%,
  scar_e reaches > 1e-3 by 300 PJ orbits, and its entropy at q = 1e-6 is
  10–16 bits per body.
- **P3 (scarred fraction).** The fraction of this belt within 1W of a strong
  resonance is 25–50% at μ = 9.54e-4.
- **P4 (μ-scaling).** At μ = 1e-4 the same x-binned scarred fraction drops by
  about (1e-4/9.54e-4)^(2/3) ≈ ÷4, i.e. to ~7–12% (resonance widths ∝ μ^(2/3);
  the allocator's law).
- **P5 (a is the cheap field).** |Δa/a| stays < 1e-5 for x > 3W and pumps
  above 1e-4 for x < 1W.
- **P6 (instrument control).** Doubling the step resolution changes binned σ
  by < 25% (integrator noise below the signal).
- **P7 (why reabsorption must exist).** The unrefit textbook-rate program
  leaves a growing residual for x > 3W: σ > 1e-3 by 300 PJ (first-order rate
  error × e), while the refit program stays below 1e-4 there.

Kill criterion for the whole configuration (not the method): if the refit
program's out-of-sample scar for x > 3W grows through 1e-3 with a clear upward
trend (chaos everywhere, programs useless), H_live cannot be concentrated by
resonance and the shipmem program design needs a different partition than
resonance distance.
