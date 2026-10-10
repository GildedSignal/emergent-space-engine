# Predictions — second-author run on 20261010-1152-fermi-e9a5

Written before the decisive run of the extended `probe.py`. The checker's named
experiments: cold scene at belt density, floor-invariance triple and mutation /
live-growth digits in `metrics.json`, game-second conversion fixed, estimator
bias measured. Held-out cases I have not tuned on (I know only the checker's
summary numbers, not their scripts):

- **P1 (cold belt at belt density, decisive).** `cold_belt` (Σ = Σ₀, σ₀ = 0.01)
  after 16 384 orbits stores **38–42 bits** (checker's summary: 40.3). Physics:
  λ above-floor = λ(cold_dense)/2500 = 177/orbit exactly (Σ-linear kernel), but
  the weaker diffusion keeps σ_resid ≈ 1.5–2.5 m/s ≫ σ₀, so the late epochs are
  in the self-limiting σ ∝ t^⅓ regime → end slope ≈ 0.67 bit/octave like the
  dense-cold case. **It does not break 8 GB at 2 dof (4.8–5.3 GB); at 3 dof it
  is marginal (7.2–8.0 GB).** If it comes out above 42 bits, the original claim
  "smooth scenes fit, only concentrated regions break" needs weakening.
- **P2 (estimator bias).** Plug-in histogram entropy at nb = 10⁴ over 256² bins
  with bin width sd/32 under-reports the true Gaussian entropy by **1.2–2.0
  bits**, constant in σ (the estimator is scale-free in σ/q, so the bias cannot
  depend on the epoch). If the bias varies by > 0.3 bits across σ = 0.001…3 m/s,
  per-epoch correction is needed rather than one constant.
- **P3 (floor invariance).** Belt σ_resid at orbit 1024 and 16 384 for
  q = 10⁻⁶/10⁻⁵/10⁻⁴ agree within **±4 %** MC noise (the diffusion is exact and
  floor-independent by construction: sub-floor kicks enter as exact D_weak,
  above-floor as exact-variance jumps).
- **P4 (time bookkeeping, derived not measured).** Porb = 1.030×10⁸ game-s
  (3.26 game-yr); 16 384 orbits = 1.687×10¹² game-s = 5.35×10⁴ game-yr, i.e.
  **534.5 real years of play at 100× warp** (the original dossier's
  "2.7×10⁸ game-s ≈ 8.5 years" is wrong on both numbers; conservative direction).
- **P5 (digits that will now regenerate).** Mutation rate 375.4/orbit (not 384);
  live growth 8.7×10⁻⁴ bits/orbit (not 9.3×10⁻⁴); churn 3.65×10⁻⁶ per body per
  game-s = **~6 100 events per 60 fps frame** at 10⁹ bodies and 100× warp
  (not 5 700; and the original's "3.4×10⁻⁴ per game-second" was per *real*
  second at warp — same mislabel family as the year slip).
- **P6 (bias-corrected stores).** With +1.4–1.5 bits: belt 35.7 bits
  (4.5 / 6.7 GB at 2 / 3 dof) at 16 384 orbits — **still inside 8 GB**; after
  1 orbit ≈ 21.5 bits (2.7 / 4.0 GB). The headroom claim shrinks by ~0.7
  time-octave but survives; dense ×2500 still breaks 8 GB at 3 dof only.
