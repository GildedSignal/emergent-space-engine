# Predictions — inversion of gold 20261006-0346-taleb-09b5 (written before any run)

Target premise (board + b-coorbital-cert spec): "every real encounter lies within partner rank 4
along the orbit" — adopted as the justification for a phase-neighbour (train) certificate at
O(n·k), k≈4, in co-orbital concentration.

Two suspected artifacts in the gold's evidence, neither tested there:

- **A1 (wrong metric).** The gold measured the partner's *distance*-rank at closest approach.
  At closest approach the partner is within ρ, so the rank counts bodies within ~ρ of the
  encounter — bounded by local ρ-density, nearly tautological. The certificate watches
  *longitude order*; the invariant it needs is the **mean-longitude (λ̄) rank** of the partner
  at contact. These coincide only if phase order = distance order.
- **A2 (aligned apsides).** Every gold scene draws ϖ within ±0.1 rad of one value and e ~
  Rayleigh(0.001). With aligned apsides the epicycles are common-mode: relative along-track
  motion is dominated by λ̄ drift, so contacts are lane conjunctions of λ̄-neighbours. Any real
  dispersed group (post-burn fleet, debris cloud, captured swarm) has spread ϖ and larger e.

Scenes: the gold's own generator, one knob at a time (nc=200, a=1±1e-5, ρ=1e-4, 1 orbit,
unbiased truth = true-longitude-binned sweep at dt=2e-5, finer than ρ/2 relative motion).
Reported per scene: encounters; distance-rank, true-longitude-rank, λ̄-rank of the partner at
closest approach (circular); required λ̄ window |Δλ̄(t*)|; and the cost of the *sound* λ̄-walk
(pairs whose Δλ̄ ever enters the ϖ-free window L̄_ij = ρ + 2(e_i+e_j) + 1.25(e_i²+e_j²) under
linear drift) vs the quadratic tier n_c(n_c−1)/2.

## Predictions

- **P1 (control, gold's adj scene: σ_λ=0.01, σ_e=1e-3, ϖ span 0.1, seed 27).**
  All three rank metrics ≤ 4 (replicates the gold); encounters ≈ 233 (my truth ⊇ theirs);
  sound λ̄-walk cost ≈ n_c·k with k ≈ 4–8 (the certificate's win case).
- **P2 (ϖ span 0.1 → π, all else as P1).** λ̄-rank at contact exceeds 4 for a material
  fraction: predict λ̄-rank_max ≥ 10 and ≥ 20% of encounters with λ̄-rank > 4, while
  distance-rank stays ≤ ~4 (exposing A1: the gold's metric cannot see this failure).
  Mechanism: epicycle reach 2(e_i+e_j) ~ 4×10⁻³ = 40ρ vs mean λ̄ spacing ~10⁻⁴ = 1ρ.
- **P3 (σ_e sweep 1e-3 → 1e-2, ϖ uniform, σ_λ=0.01).** λ̄-rank_max and required window grow
  ~linearly in σ_e (reach/spacing). At σ_e = 1e-2 the sound watch degree k ≳ 0.3·n_c: the
  certificate degenerates toward the quadratic tier exactly in the concentrated+dispersed
  (debris) regime it was adopted for.
- **P4 (spacing scaling: σ_e=3e-3 with σ_λ=0.05 vs 0.01).** λ̄-rank and k scale ∝ σ_e/σ_λ:
  bunching (the more concentrated case) is the *worst* case for the watch, not the best.
- **P5 (window soundness).** |Δλ̄(t*)| ≤ ρ + 2(e_i+e_j) + 1.25(e_i²+e_j²) + 2ρ slack for
  every true encounter (the ϖ-free walk window, e² term included, is sound). If this fails,
  the in-flight build's window is unsound — a stronger result.
- **P6 (debris scene: σ_e=3e-2, σ_λ=0.02, ϖ uniform).** The clump still exists in (a, λ)
  (concentrated: the regime the train was adopted for), but predict sound-watch cost ≥ half
  the quadratic tier and λ̄-rank_max ≳ 30: no O(n·k) certificate of this family survives;
  the 40 TB ruin arithmetic for a 10⁶-body concentrated debris cloud stands.

Kill criterion for my own claim: if P2 shows λ̄-rank ≤ 4 everywhere (all rank metrics agree),
the gold's premise survives apsidal misalignment and this dossier reports the certificate
as *strengthened* (a held, adversarially-tested invariant — still a result, silver-grade).
