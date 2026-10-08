# Predictions — run 20261008-1521 (second author on 20261008-1419-system-2f89)

Written BEFORE the decisive census/best runs. The instrument (census.py grid, bisection,
classification) and its controls are frozen; controls already pass on tuning data
(base k8, 40 steps: worst |K(root)| = 7.3x the float floor, 0/127 flip failures,
Kepler-only negative flat with 0 roots). The predictions below are for the scenes and
variants NOT yet measured. Anchors are the author's numbers (roots anywhere on the
alpha grid {0.25..4}: 55.7% k=6 / 42.0% k=8, one-planet belt scene) and the checker's
(one-signed on [1/8,8]: 39.8% k=6 / 58.0% k=8; on [1/64,64]: one-signed 3.2-41%,
runaway roots at alpha ~ 8-23). Those anchors measured "root anywhere on a wide grid";
nothing below has been measured.

## Frozen definitions

- usable root: alpha* in [1/2, 2] (the step stays within 2x of nominal in either direction).
- kill line (memo P8, as frozen by the author): a usable solution is missing at > 1% of
  steps, i.e. frac_usable < 0.99.
- scenes: base (belt, e 0-0.3, seed 4), seed99, ecc (e 0.5-0.85), two (2nd planet
  0.4 mu at 9.5), flyby (hyperbolic passes, seed 7). Variants P (plain states),
  Z (p_t reset so K(start)=0), best (full trajectory solved on the band each step).
- 8 ships, 200 census steps (300 for flyby), grid [1/64, 64] 3/octave, bisection 42 iters.

## Predictions

P1 (plain census, usable fraction, per scene x k):
- base k8: 0.25-0.45 (point 0.35); base k6: 0.40-0.62 (point 0.50)
- seed99 k8: within 0.10 of base k8
- ecc k8: 0.30-0.65; two k8: 0.25-0.55 (generic Omega does not rescue the solve)
- flyby: the highest of all scenes, k8 0.50-0.85, k6 0.55-0.90 (the cubic term
  competes at encounters; still < 0.99)
- every k6 point >= its k8 point minus 0.05

P2 (runaway disclosure, plain): among steps whose only roots lie outside [1/2,2],
median closest-root alpha > 3, and median |K(alpha=8)| / |K(alpha=1)| > 10 (the residual
has left the nominal scale before the crossing; these are not usable solves).

P3 (one-signed on the full grid [1/64,64], plain): between 0.05 and 0.45 in every
scene (base k8 ~ 0.35-0.45; checker's wide-bracket numbers had roots 59-96.8%).

P4 (structural collapse, Z): usable(Z) < usable(P) in every scene x k; Z base k8
<= 0.15; Z everywhere <= 0.60. (On the SEM manifold K(start)=0, so K(end(alpha)) =
alpha^2 C2 ds^2 + alpha^3 C3 ds^3: with K(start) = 0 the offset that supplied roots
on plain states is gone; only cubic competition remains.)

P5 (best trajectories): frac_usable < 0.50 in every scene; conditioned on the previous
step having found a root, the next step's usable fraction is at most half of the
fraction after a no-root step (success at step n starves step n+1); trajectories
finish 2 periods, <= 1 ship lost per scene, 0 nan.

P6 (verdict): every scene x k x variant has frac_usable <= 0.90, i.e. the kill line
(>1% steps without a usable solution) is exceeded >= 10x everywhere -> the kill is
structural and scene-independent. Refutation: any cell >= 0.99 -> the kill is
scene-dependent; I report the boundary.

P7 (encounter concentration): in base P and flyby P, median r_min(usable steps) <
median r_min(one-signed steps) (usable roots concentrate at encounters).

P8 (audits): nan fraction 0 everywhere; k6 residuals ~ 16x k8 (median |K(alpha=1)|),
confirming the ds^2 scaling on the same record.
