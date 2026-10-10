# Predictions (written before the decisive matrix)

Instrument: WH belt (exact Kepler drift + heliocentric mutual kicks + indirect term, DKD, fixed
shared step), Benettin shadow at total norm d0 = 1e-8, renorm at 1e-6. Belt: N equal masses,
uniform a ∈ [0.95,1.05], Rayleigh σ_e = 0.05, uniform angles; time in orbits at a = 1.

Cases below are NOT tuned (the matrix fixes them after this file).

- **P1 (negative control, μ = 0):** each body is integrable Kepler; shadow growth is shear only,
  so L(t) is algebraic (fits ln t better than t), λ_raw declines with horizon, ≈ 0.02–0.03 per
  orbit at T = 200. Fallback = 0, dH undefined/0.
- **P2 (positive control, N = 50, μ = 1e-2, 20 orbits):** strong scattering; growth exponential,
  λ_exp ≳ 0.1 per orbit, run stays clean (fallback = 0, dH < 1e-2). If it corrupts, the
  strong-scattering regime needs finer steps and I report that.
- **P3 (cadence, N = 200, μ = 1e-4, spon ∈ {4,8,16,32,64,256}):** λ_exp converges to the
  spon = 256 truth within ~30% at spon ≥ 32 (the plane's H0190 32 kicks/orbit region);
  at spon ≤ 8 I expect ≥ 3× inflation of λ_exp while |ΔH|/H stays below 1e-3 (the energy
  instrument is blind to chaos-type error). If λ already inflates at spon = 32, the engine's
  cadence lever has a dynamics-side floor it must not cross.
- **P4 (N-scaling at fixed belt mass μ = 1e-4, N ∈ {50,100,200,400,800}):** excess surprise rate
  (median λ_exp minus the μ = 0 baseline) declines with N, fitted exponent α between −1 and −1/3
  (2-D kinetic estimate α ≈ −1: scattering depth ∝ m at fixed Σ). Per-body non-derivable
  information SHRINKS as the belt is refined at fixed surface density.
- **P5 (growth law at μ = 1e-5):** still exponential (conjunction chaos above the shear
  baseline). If it flips algebraic (indistinguishable from the μ = 0 control), the belt at game
  μ is quasi-derivable and H_live's floor is the shear baseline only — the strongest possible
  result for the game.

Any of P3–P5 failing is itself the finding; the run reports it either way.
