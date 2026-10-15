# Predictions (written before the decisive sweep)

Instrument: both systems evaluated at the **same invariant pair (ĥ_real, L)** — the
design's own construction (representation.md §1: ν "enters only through the energy
map", so the doll is the Schwarzschild geodesic at ĥ_eff = 1 + (ĥ_real²−1)/(2ν), same
L). Reference: 2PN EOB (A = 1−2u+2νu³, Q₂ = 2ν(4−3ν)u²p_r²), 3PN A-potential as a
truncation bracket. No time integration: turning points and radial quadratures.

Cases below are NOT tuned on (the tuning cases are the ν→0 control, the closed-form
doll check, and the numerical stability of the quadrature, which are instrument
validation, not physics results).

- **P1 (ecfd cross-check, held out):** at ν = 0.25, p̄ ≈ 20 M, e = 0.6, the doll's
  periastron-advance relative error is between +0.2% and +0.6% (ecfd measured +0.36%).
  If it lies outside, my instrument disagrees with the earlier run and I say so.
- **P2 (scaling):** at fixed e, ν the error scales ~ (M/p̄)²: error(p̄)/error(2p̄) ≈ 4
  ± 1. At fixed p̄, e it scales ~ linearly in ν (the 2PN ν-term), ratio
  err(0.25)/err(0.01) ≈ 25 ± 5.
- **P3 (the 1% bar):** the doll's advance error crosses the rung's own period bar
  (0.1%) only inside p̄ ≲ 60–80 M and crosses 1% at p̄ ≈ 12–18 M (ν = 0.25, e = 0.6).
  Between 20 and 10 M it is a player-visible few-percent dynamics error.
- **P4 (e-dependence):** the error at e = 0.3 and e = 0.9 is within a factor ~2.5 of
  e = 0.6 at the same p̄ (mild eccentricity dependence — no strong e-amplification).
- **P5 (plunge boundary):** the doll's plunge separatrix (Schwarzschild ISCO, u = 1/6)
  sits at a *larger* radius than the true ν = 0.25 separatrix (A's +2νu³ term deepens
  the well), so the doll **fabricates premature plunge**: the misclassified band has
  ΔΩ_φ/Ω_φ of one-sided sign, magnitude ≈ 5–15% in orbital frequency at ν = 0.25,
  shrinking ~linearly in ν.
- **P6 (period):** the radial-period error is the same order as the advance error at
  the same (p̄, e, ν), not an order larger.
- **P7 (instrument floor):** 2PN vs 3PN references agree within a factor 2 of the
  reported ν-error at p̄ ≥ 10 M; below p̄ ≈ 8 M the bracket opens and I downgrade the
  numbers to indicative.
