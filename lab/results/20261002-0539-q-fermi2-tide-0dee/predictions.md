# predictions.md — run 20261002-0539-q-fermi2-tide-0dee

Written before the decisive verification suite (`verify.py`). Development and
tuning used only: circular r=10; bound rp=8, ra=24; unbound E=1.2, L=5 at
r ∈ {8, 20, 50}; scatter points in the boosted-frame consistency check.
Everything below concerns families and checks NOT exercised during tuning.

## Held-out families

whirl (e=0.95, p=7.95), circular r=6.01 (near ISCO), circular r=1000
(Newtonian), eccentric e=0.9 p=10, eccentric e=0.1 p=10, unbound E=1.05
L=4.1 (near-critical), parabolic E=1 L=4, radial L=0 E=1.2.

## Predictions

1. **mpmath direct construction (40 digits: metric -> Riemann -> numeric
   parallel transport) vs closed forms in double: every component of C^P,
   C^B, omega, dPhi/dphi agrees to <= 1e-12 relative** at every sample of
   every family above (Phi taken from the transported frame, so the check
   never uses the closed-form rotation).
2. **Eigenvalues of the closed-form C^P equal {m(1+3L^2/r^2), m,
   -(2+3L^2/r^2)m} to <= 1e-12**, at every sample including whirl and
   near-ISCO; they are independent of E: at equal (L, r), orbits with
   different E and different rdot give identical eigenvalues to 1e-14.
3. **Deviation integration** (coordinate-level, Riemann from Christoffels)
   vs the 3-space ODE x'' = -C^P(r(tau), Phi(tau)) x with closed forms:
   relative difference <= 1e-8 over ~0.2 of an orbit, every family.
4. **Finite differences of nearby geodesics** (Richardson in epsilon over
   epsilon/2): |C_FD + C_closed| <= 1e-4 relative to max|C| at every sample
   and every frame direction, all families.
5. **Whirl family**: omega, dPhi/dphi, C components all finite and smooth
   through periapsis (rp = p/(1+e) ~ 4.08); no divergence of any closed form
   (the only zero-denominator risks are r=2M and G^2=0, neither reached).
6. **Radial L=0**: omega = 0 exactly; the transported frame angle stays at
   0 to 1e-10; C^P diagonal with values (m, m, -2m) in (theta, phi, r) axis
   order, independent of infall speed.
7. **Parabolic E=1 (sharp form)**: dPhi/dphi = -1/2 exactly at every r and
   L of that family (1e-15), total Phi change over the full inbound-outbound
   sweep close to -pi (frame angle measured through periapsis passage).
8. **Circular anchors at r=6.01 and r=1000**: omega = sqrt(M/r^3) to 1e-12;
   per-orbit Phi change = -2 pi sqrt(1-3M/r); Newtonian eigenvalues at
   r=1000 within 0.5% of {m, m, -2m}.

## What would make it wrong

- Any component mismatch above 1e-12 vs mpmath: the closed form is wrong
  (transcription or simplification error), not roundoff.
- Eigenvalues with residual E-dependence: my rationality claim is wrong.
- The deviation/FD checks agreeing while mpmath disagrees (or the reverse)
  would isolate whether the error lives in the Riemann level or in the
  frame/rotation level.
- Parabolic dPhi/dphi != -1/2 exactly: the rotation formula is wrong.

Predicted outcome: all pass; the only expected residuals are integration
truncation in checks 3-4 and Gram-Schmidt drift in the long transports.
