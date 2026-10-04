# Predictions (written before the decisive run)

Calibration seen (not held out): f=0.3, nk ∈ {32,16,8}, plain DKD + corr3/corr5 + avg.
Held-out cases: nk ≤ 6 at all f; all of f=0.2 and f=0.4; fr4; e_end/class behaviour.

- P1 (plain frontier): plain DKD's precession error crosses B14's 10% near
  nk ≈ 2 at f=0.2 and f=0.3, and between nk = 3 and 8 at f=0.4 (evection
  amplifies sampling error).
- P2 (correctors): corr3/corr5 do NOT extend the ≤10% frontier by more than
  1.5× in force evals per orbit. They beat plain only at fine steps
  (nk ≥ 16); at nk ≤ 6 they are worse than plain (their Z sub-kicks sample
  the moving sun at displaced phases, adding aliasing). Crossover moves to
  higher nk as f grows.
- P3 (compositions): fr4 at equal force-evals per orbit is never better than
  plain by more than 2× (4 evals/step buys nothing at these ε).
- P4 (averaging control): avg fails 10% at f=0.3 (seen: 20.7%) and f=0.4,
  passes at f=0.2 (r9's threshold ~0.17–0.2 R_H reproduced in this setup).
- P5 (failure mode at the frontier): the binding failure at minimal nk is
  e-pumping / class change (spurious escape), not precession-rate error,
  first at f=0.4.
- P6 (slope control): plain relerr ∝ nk^-2 (fitted exponent ≈ −2) at
  f = 0.2 and 0.3 over nk ∈ [4,32].
