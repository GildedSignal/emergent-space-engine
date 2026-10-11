# Predictions — run 20261011-2028-dynamics-7807 (written before the decisive sweep)

Exploratory tuning so far: three points at ρ=0.01 (σ_e ∈ {0.005, 0.07, 0.3},
N=2048, seed 5). The decisive runs below (full κ grid × ρ, formation, N-scaling)
have not been run. κ = σ_e·ā/Δa (thermal crossing depth).

- **P1 (form of the candidate fraction).** frac_pairs(κ) = min(f₀(ρ) + c·κ, 1)
  with c ∈ [2, 4] and a ρ-floor f₀ ∝ ρ: at ρ=0.003 the cold intercept falls to
  ≈ 0.017–0.02 (from 0.058 at ρ=0.01).
- **P2 (phase boundary).** frac crosses 1/2 at κ*(ρ=0.01) ∈ [0.15, 0.25], and
  κ*(ρ=0.003) agrees with it within 20% (the boundary is set by the cone, not ρ).
- **P3 (encounter rate).** enc(κ) is non-monotone: a minimum near κ ≈ 0.1–0.2,
  then a steep rise enc ∝ κ^α with α ∈ [1.5, 4]; enc scales linearly in ρ at
  every κ.
- **P4 (the tier's cost multiplier).** W = candidate setups per real encounter
  peaks in the intermediate band κ ∈ [0.05, 0.3] — where a main-belt-like
  distribution sits — at W ∈ [300, 3000], and falls at both ends (cold: ρ-floor
  candidates without slow crossings; hot: every pair encounters).
- **P5 (formation control, must hold).** At Δa/a = 0.0015 (a fleet band),
  frac = 1 for every σ_e, cold included: taleb-09b5's co-orbital case is the
  κ → ∞ limit of the same cone-swallowing, not a separate phenomenon.
- **P6 (N-scaling control, must hold).** At fixed κ ∈ {0.10, 2.0}, W is
  independent of N within ±20% over N = 1024…16384 (candidate work tracks real
  encounters along the temperature axis as it does along density; the danger is
  the per-body fraction frac and the total O(N·frac·N), not the ratio).

Kill criterion for the run's premise: if frac_pairs does NOT collapse onto κ
(same frac at all N and both ρ after subtracting f₀), the "one dimensionless
number picks the tier" claim is dead and the dossier says so.
