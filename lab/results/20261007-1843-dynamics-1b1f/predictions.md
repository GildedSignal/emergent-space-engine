# Predictions — run 20261007-1843-dynamics-1b1f (written before the decisive grid)

Model: planar Kepler epicycles around one M*, elastic hyperbolic deflection at every
conjunction with miss distance b < R_kick = 10·R_cap. Encounter := b < R_cap (game-scale
capture radius). Hot belt: N=300, W=0.08 in a, Rayleigh e (σ=0.05), random phases,
T=400 orbits, 48 steps/orbit, K=8 phase neighbours. Gentle/violent split by the
focusing factor F = μ/(R_cap·v_rel²) ≈ 2m/(R_cap·σ_e²), v_rel ≈ e (shear-dominated).

Cases not tuned on: the cold starts (σ_e = 1e-4), the R_cap and N sweeps, seed 2/3.

- **P1 regime split.** m ≤ 1e-6 (F ≲ 0.3): the belt survives 400 orbits (a_std stays
  within ×2 of 0.023, e_p99 < 0.4, ejections ≈ 0). m ≥ 1e-5 (F ≳ 2.7): destroyed
  (a_std > 0.2, ejections > 10). Threshold F* ∈ [0.3, 3].
- **P2 rate attractor (gentle).** Encounters/body/orbit flat within ±20% over 400
  orbits, and equal to the kicks-off control within ±30%: stirring does not move the
  load; the geometric conjunction rate is the attractor.
- **P3 violent decay.** m ≥ 1e-5: rate spikes then decays as the belt smears;
  R(350–400)/R(peak) < 0.3.
- **P4 burstiness.** Fano factor (var/mean of per-orbit encounter counts), orbits
  200–400: gentle ∈ [0.8, 1.5] (Poisson-like, no cascade); violent > 2.
- **P5 cluster factor.** Gentle regime: encounters within ±1 orbit after a given
  encounter ≤ 2× the baseline rate (no cascade in sparse belts).
- **P6 scalings (gentle).** R ∝ R_cap^1, R ∝ N^1 at fixed W; exponents within ±0.2.
- **P7 cold starts.** m=1e-4 from σ_e=1e-4: accelerating e-growth (stirring transient),
  rate at 400 orbits still far below the hot belt's geometric rate (t_heat > 400).
  m=1e-6: rate stays ≈ the cold geometric rate (no stirring visible) — a cold belt at
  game mass ratios stays near its program for the whole session.

A result outside these bands kills the corresponding claim, not the method (P9).
