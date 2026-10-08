# predictions.md — 20261008-2113-scout-6652 (written BEFORE the decisive run)

Question: on tangency-grade pairs (Wide sections in `crates/encounters`), does a
travel-time-difference window W = [−max h − 2c, −min h + 2c], h(λ) = τ_i(λ) − τ_j(λ) over
the arc (each body's θ_c→λ travel time), c = ρ·(1/θ̇_i,min + 1/θ̇_j,min), decide the pair
with O(1) Kepler evaluations where `numeric_window`'s conservative advancement in s
(Lipschitz vmax_i·1.001, d_of_s with k = 32) pays hundreds?

Held-out cases (not tuned on; the decisive set is drawn fresh with fixed seeds):
1. **Evals per Wide section.** A (crate replica) ≥ 200 state evals on barely-crossing and
   merged-arc pairs; B ≤ 20. Ratio ≥ 25× on the median Wide section.
2. **Zero misses for B.** Against dense truth (fine time sampling + local refinement,
   ρ = 5×10⁻³ in units of ā), every true encounter's passage offset lies inside B's
   window, on: barely-crossing pairs (cone gap ∈ (−ε, 0)), one-sided merged arcs,
   near-identical orbits (|Δ(U,V,W)| ~ ε), and an adversarial high-e set (e ∈ [0.6, 0.95]).
   I expect A to also miss zero (it is built rigorous); if A misses, my replica is wrong,
   not the crate.
3. **No over-arming.** B's window width ≤ 3× A's width on the median pair (B must not
   flood the exact per-pair check; the firing measure scales with width/T_i).
4. **Degenerate share.** Near-identical pairs (window ≈ whole circle, or Δn below the
   tolerance) route out: I predict < 10% of tangency-grade pairs in a belt-like draw.
5. **Where B weakens.** Arcs containing an apse loosen θ̇ bounds (c grows); I predict
   < 15% of Wide sections contain an apse, and even those stay under 40 evals.

Kill criterion for the candidate (pre-registered): any missed true encounter in case 2,
or median eval ratio < 10×, kills the travel-time window as a replacement; a blown
width ratio (> 3×) demotes it to a routing prefilter only.
