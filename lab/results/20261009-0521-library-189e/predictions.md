# predictions.md — run 20261009-0521-library-189e

Written **before** the decisive experiment. Nothing below was tuned on the probe data.
Model: two coplanar Kepler orbits (same primary, μ=1, a1=1), brute-force truth = fine
time-grid min distance per synodic window → miss sequence d_k, k=1..K=30. Prediction =
1D radial-separation surrogate S(λ)=|r1(λ)−r2(λ)| over longitude (elements only, no time
integration) + continued-fraction candidates k with ‖k·ω_frac − λ_target/2π‖ minimal,
ω_frac = frac(n1/(n1−n2)). These cases are held out: random a2/a1 ∈ U[0.90,1.10],
random phases/apsides, e drawn per band — none inspected before writing this.

- **P1 (small e ≤ 0.05, 66 seeds):** median percentile rank of d_{k_pred} ≤ 10%
  (CF picks a top-decile conjunction); ≥ 60% of seeds rank ≤ 10%; median
  d_{k_pred}/min_k d_k ≤ 1.5. Fermi: separation |a1−a2| ~ 0.01–0.1 while radial
  excursions ~ e·a are comparable or larger, so d_k is strongly longitude-dependent
  and the return structure should dominate.
- **P2 (degradation, 66 seeds each):** median rank ≤ 25% for e ∈ (0.05, 0.15];
  ≤ 35% for e ∈ (0.15, 0.3]. Timing wobble (equation of center, ~2e) smears the
  surrogate; I expect monotone degradation, not collapse — the quasi-periodic return
  is topological, not numeric.
- **P3 (belt census, N=500, a ∈ [0.95,1.05], e ≤ 0.05, 124,750 pairs, held out):**
  in the adjacent tier (|Δa|/a < 0.02) ≥ 50% of pairs carry a sharp convergent
  (q ≤ 13, |ω−p/q| < 1/(2q²)); across all pairs, sharp-convergent ∪ envelope-disjoint
  (|a1−a2| > a1e1+a2e2) covers ≥ 70%; the "neither" skin < 30%.
- **Controls, both sides.** Positive (instrument): on 1000 random (ω, τ), the
  argmin_{k≤30} ‖kω−τ‖ is always achieved by a convergent/semiconvergent denominator
  or small multiple — else my candidate set is broken and the run is VOID, not KILL.
  Negative: a uniformly random k has median percentile rank ≈ 50% on the same d_k.
- **Degeneracy probe (r4-v2 lesson):** period ratio set to exact (p/q)^{2/3} + ε for
  q=7, ε ∈ {10⁻⁶, 10⁻⁴, 10⁻²}. Prediction: ε→0 pushes k_true toward multiples of q
  and makes the calendar ill-conditioned (argmin nearly flat); at ε=10⁻² structure
  returns. Exact commensurability must be detuned in any rung metric that uses argmin.
- **Kill criteria for the lesson (not the method):** L1 (Feynman's box of tools →
  CF conjunction calendar) is killed for this regime if median rank > 30% in the
  small-e band, or ≥ 50% of seeds have d_{k_pred} > 2× min_k d_k.
