# Predictions (written before the decisive runs)

Run 20261020-1729-scout-4c79, topic fleet-doll-speed. Instrument: exact float64
Schwarzschild Riemann (analytic Christoffels, M=r-dependence only) projected on the
boosted static orthonormal frame at periapsis (eigenvalues are invariant under the
spatial rotation to the parallel/Fermi frame, so no finite-difference and no
separation parameter enter the coefficient claims), plus a parallel-transported frame
+ geodesic-deviation ODE for the integrated channels, plus true finite-separation
geodesic pairs for the nonlinearity. Held-out cases: every number below is computed
from the closed forms only; the grid's measured values are not fitted.

- **P1 (radial, the cure's license to β 0.999):** the exact periapsis radial
  eigenvalue divided by the Newtonian 2M/r_p³ equals γ_p²(2+β_p²)/2 to better than
  0.1% at β_p ∈ {0.25, 0.5, 0.7, 0.9, 0.95, 0.99, 0.999} and r_p ∈
  {6, 8, 10, 20, 50, 100, 300}M (β_p = speed measured against the local static
  observer). **Kill:** any deviation > 1% anywhere ⇒ the contraction is not the exact
  law at the game's high-c edge and the freeze criterion (od 2) cannot extend past
  β 0.9.
- **P2 (along-motion cancellation):** the along-motion eigenvalue divided by the
  Newtonian transverse M/r_p³ is exactly 1 (within 1e-12 relative, machine floor) at
  every point of the grid. **Kill:** any deviation > 1e-9.
- **P3 (out-of-plane, the page's quoted-but-unmeasured channel):** the out-of-plane
  eigenvalue ratio is γ_p²(1+2β_p²) to < 0.1%; the rival form γ_p²|1−2β_p²| (which my
  sign-algebra could not exclude by hand — the reason od 4 needs a measurement) is
  excluded by > 3× at β_p 0.9. **Either branch is a result:** if the measured form is
  the rival, the page's quoted γ²(1+2β²) is refuted at 3D scenes.
- **P4 (radius independence — the integrator's amendment, od 1):** the P1 residual
  shows no M/r_p trend (|residual| < 0.1% at every r_p from 6M to 300M at fixed β_p).
  The speed amplification is kinematic and exact, so it leaves the weak-field error
  budget entirely; what the legality rule must gate is compactness, not speed.
  **Kill:** a residual growing like M/r_p ⇒ the closed form is a weak-field statement
  only.
- **P5 (second-order-in-ξ, the unseparated half of od 3):** the true finite-separation
  stretch converges to the deviation-ODE stretch linearly in the initial offset; at
  ξ₀ = r_p/1000 the nonlinearity is < 1%; at the frame's own extent bound r_p/32 the
  deviation-ODE understates the true radial stretch by [predicted: 3–10%] (the
  quadratic term the letter's H0203 note already prices at Newtonian order).
- **P6 (the letter's error at its own cap):** at β_p = 0.25 the letter's Newtonian
  radial coefficient errs by exactly γ²(2+β²)/2 − 1 = 1.5β² + 1.875β⁴ + … = 9.99%,
  against its budget line "1PN = O((nR/c)²) = 6.25%": the budget misprices its own
  cap by the kinematic term it excludes.

Decisive commands: `python3 instrument.py grid` (the P1–P4, P6 table),
`python3 instrument.py nonlin` (P5). Each under 60 s.
