# Predictions — run 20261011-0736-dynamics-ec74 (dynamics lens)

Written before the decisive Ψ-sweep. Tuned on: code unit controls only
(round-trip identity; one smoke run at Ψ=3e-3, N=400/w=0.02/σ_e=0.02, which
exploded into bound Hill pairs — that blow-up set the *dilute* parameters
below but no sweep point has been run). The RK4 single-encounter control was
also run (it fixed the encounter definition: b < 3·r_H), before these
predictions.

Setup: N=300, ring width w=0.04 (a ∈ [0.98, 1.02]), Rayleigh σ_e0 = 0.04,
equal masses, T = 200 orbits, 128 samples/orbit, K = 6 angle neighbours.
Sweep: Ψ = μ_g/(aσ_e)³ ∈ {3e-6, 3e-5, 3e-4, 3e-3}. Filling guard
n·π(3r_H)²: 0.0004, 0.004, 0.04, 0.86 (the last is deliberately beyond
validity, as the boundary marker).

Definitions: a **strong encounter** is a closest-approach passage with
b < 3r_H and χ ≥ 0.3 (χ = Rutherford angle); λ = strong encounters per body
per orbit. Twin divergence D(t) = RMS angular separation of two runs whose
M₀ differ by 10⁻⁹.

- **P1 (cadence lock).** In every run with λ ≥ 5×10⁻³/orbit/body, D(t) grows
  **exponentially** (not linearly), with e-folding time T_L satisfying
  T_L·λ ∈ [0.3, 3] orbits: one e-folding per 1–3 encounter times per body.
  ("Chaos is normal it's just the necessary interactions happening within a
  short time" — if linear instead, caches live longer and this fails.)
- **P2 (fate).** Negative self-regulation: as stirring raises σ_e, encounter
  cross-sections shrink, so λ(t) falls; by orbit 200 at Ψ=3e-4, λ ≤ 0.5×λ(0).
  In the three valid runs (Ψ ≤ 3e-4) σ_e stays < 2×σ_e0 and the ring does not
  run away. At Ψ=3e-3 (filling 0.86, beyond validity) the swarm breaks: bound
  pairs form, λ rises ≥ 10×, σ_e exceeds 3×σ_e0 — the clump boundary.
- **P3 (clustering).** Per-orbit strong-encounter counts have Fano factor
  ≤ 5, and it does **not grow** with window size 1→64 orbits in valid runs
  (subcritical: no avalanche scaling; slack spreading stays viable).
- **P4 (validity window).** In valid runs the χ distribution of strong
  encounters has median ≤ 0.5 and ≤ 20% of events at χ > 1 (where the
  one-impulse model is qualitative). The earlier RK4 control already showed
  toy/RK4 element-change ratios 1.08–1.42 for χ ≤ 0.31 inside r_H.
- **P5 (rate law and the deletion map).** Early-window λ(Ψ) ∝ Ψ^α with
  α ∈ [0.8, 1.3] (b_enc ∝ μ/σ_e² against a fixed conjunction geometry).
  Held-out arithmetic (not run yet): mapping real swarms onto Ψ with
  per-body μ_g = 2Gm and their actual σ_e puts ships (m ~ 10⁻²⁴ M★,
  σ_e ~ 10⁻⁶) at Ψ ~ 10⁻⁶ and asteroid-belt bodies (m ~ 10⁻¹² M★, σ_e ~ 0.1)
  at Ψ ~ 10⁻⁹ — both far below the λ·⟨Δa/a⟩ < 10⁻⁸/orbit deletability line
  that I expect to measure at Ψ = 3e-6; i.e. mutual gravitational encounters
  between small bodies are a deletable component almost everywhere, and the
  pairwise encounter tier's live domain is a narrow Ψ band.
