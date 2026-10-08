# Predictions (held out before the decisive run)

Question: at 10⁹ belt-like bodies on the 8 GB M1, which memory-budget term binds
(smooth-program stock, live distinctions H_live, their reabsorption), by how much,
and is H_live bounded in steady play?

Written before running `probe_hlive.py`. The analytic model (derived in
`fermi_budget.py`, not fitted to the probe):

- P1 (rate law). In a shear-dominated 2D belt the resolvable-encounter rate per
  body is Γ(Δv > q) = 4·n·G·m/q, with n the surface number density (Ω cancels).
  The Monte Carlo (Poisson flux of impact parameters, v_rel = 1.5·Ω·b,
  impulse 2Gm/(b·v_rel)) agrees within a factor 2 (Poisson counting noise).
- P2 (log growth). With deviations stored as a scar (state minus program), the
  per-body stock S(t) = log2(σ(t)/q) grows as ½·log2(t): the fitted slope of S
  vs log2(t) is 0.5 ± 0.1 before saturation, at any quantum. If the slope comes
  out ≥ 0.8 the "bounded" claim is wrong and I report it.
- P3 (ceiling). A fully decorrelated belt at law-native quanta
  (δa/a ~ 2⁻¹⁰, δe ~ 2⁻⁸, δφ ~ 2⁻¹⁶) costs 20–80 bits/body of marginal
  entropy (program gone). If it exceeds 200 bits/body the 8 GB budget fails
  structurally even with perfect reabsorption, and the conclusion flips to
  "memory binds by design".
- P4 (compute cross-check). The board's "190 cores at today's rates" for 10⁹
  bodies re-derives as kicks/s × ns/kick dominated only at extreme real-time
  factors: at rtf ≤ 10⁴ the kick load is < 1 core; it reaches O(100 cores)
  only above rtf ~ 10⁶. If my independent arithmetic lands more than 10× from
  190 cores at the stated conditions, one of the two is wrong and I say which.

Adversarial cases the probe must also survive (my own red team):
- close-encounter cutoff at the Hill radius (no infinite ⟨Δv²⟩),
- heavy-tailed Δv distribution: the diffusion estimate must use the truncated
  second moment, not the mean impulse,
- saturation: once σ reaches the belt's own spread, S must flatten (reabsorption
  into a re-fit program), not keep growing.
