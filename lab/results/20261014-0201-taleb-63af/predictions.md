# Predictions (written before the decisive ladder; calibration disclosed)

Calibration used to build the instrument (allowed tuning, not held out): smoke runs of
`fit g-s1e-2-r1e-3 1`, `fit g-mid 1`, `fit g-hi 1`, `fit p-keys 1` — these fixed the model
form `λ_i = C·(k + e_i)·a_i^-1.5`, the scene list, and the window sizes. Everything below is
about cases NOT used for that: held-out seeds 2 and 3 of every generic spec, and the specs
not smoke-run (g-s3e-3-r1e-3, g-s3e-2-r1e-3, g-dense3k, g-wide, g-hot, p-coorbital).

## The claim being tested

nladder's open direction 5: "a dense belt where conjunctions cluster on bodies could still be
heavy-tailed without a driver — unmeasured; it is the one scene class that could revive a
measured rank." If it revives, the live set is rank-shaped at 10⁹ and sticky promotion is a
slow ruin; if it dies, promotion sizing stays a birth-constant content decision.

## Predictions, held-out

P1 (rank): on every generic spec and held-out seed, ρ_model ≥ 0.85 × ρ_model_sim
   (the two-parameter birth-constant model captures per-body ranks to within counting noise).
P2 (shape): measured Gini − model-Poisson Gini ≤ 0.06 on every generic scene
   (the p-keys smoke already reads a gap of 0.30; that is the instrument's "tail exists" line).
P3 (dispersion): disp_resid ≤ 3 × disp_poisson on every generic scene (smoke: 1.5–2×;
   p-keys control: 22×).
P4 (concetration scale): top-decile share ≤ 0.28 on every generic scene. The plane's battle
   reads 0.47–0.56; the belt must sit far below the plane, or the plane's concentration is
   not special.
P5 (avalanches): Fano ≤ 2 on every generic scene (the plane's steady stream reads 8–28).
P6 (the certificate's form): fitted k grows linearly with the spec's Rayleigh mean
   ⟨e⟩ = σ_e·√(π/2): k ≈ 1.0–1.5 × ⟨e⟩ + O(ρ). If k needs a different form per spec, the
   "birth constant" story weakens to a per-scene fit.
P7 (hardest case): g-wide (σ_e = 0.2, a ∈ [0.5, 3]) is where I expect the model to lose the
   most rank correlation (crossing orbits, crude a^-1.5 synodic factor) — prediction:
   ρ_model ≥ 0.6 × ceiling there, and if any scene breaks P1–P3 it is this one.

## What would revive rule 2 (kill my claim)

Any generic scene with: disp_resid > 5× its Poisson floor, or Gini gap > 0.10, or
top-decile > 0.35, or a held-out seed with ρ_model < 0.7 × ceiling. Then the belt mints a
real per-body tail with no driver and the promotion design must size for a rank, not a rate.
