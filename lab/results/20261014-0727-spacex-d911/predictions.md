# Predictions (written before the decisive run `encounters kick2`)

Scene: shipped belt n=10⁴, ρ=1e-4, σ_e=1e-2, seed 20261050, horizon 1000 orbits, 100 kicks,
eps ∈ {1e-7, 1e-5} (Δa/a). Held out: I have seen only the shipped `kick` baseline on this
machine (812.8 pairs/kick, 7.2 ms/kick, changed 0.24%→8.8%, flipped≈changed, slack-skip
94.6%→0.25%). None of the quantities below has been measured by me.

1. **Knife edge.** flipped_in (silent→hits) dominates the changed fraction, and ≥80% of
   flipped_in pairs already have a first hit within `4·rel_dt·horizon` beyond the horizon edge
   before the kick (the flip is phase drift pushing a near-edge passage across a fixed edge,
   not an orbit-geometry change).
2. **At-risk population.** The fraction of silent pairs with such a near-edge ext hit is of
   the same order as flipped_fraction at each eps (it is the pool the flips draw from).
3. **Passage-clock transform.** For pairs armed before and after, hit times move
   multiplicatively anchored at the kick: t_new ≈ tk + (t_old − tk)(1 + c·rel_dt) with the
   implied c concentrating inside [0.2, 5] for ≥90% of matched hits, and the median residual
   of that one-parameter prediction < 5% of the synodic period. If c is wild (small
   denominators), the per-pair due certificate is unsound under kicks and this kills the
   O(1)-update representation.
4. **Edge churn.** Candidate-set membership changes (cone entries+exits) < 5 pairs per kick
   at both eps (the cone is nearly frozen per kick; the churn is in time, not geometry).
5. **Cost anatomy.** Window/section setup (evals) plus Diophantine first-hit (queries) carry
   ≥ 80% of the 8.9 µs/pair; exact checks are a small minority — so an O(1) per-pair update
   plus exact re-derivation only for churn composes toward the ~10³ cut.

Kill criterion for my claim: if knife_share < 50% at eps=1e-5 (flips are geometric, not
edge-drift) or the transform residuals are not absorbable (median residual > 20% of synodic),
then per-pair due certificates cannot ride kicks and the 10³ must come from aggregation
(per-body tubes), not cheaper per-pair maintenance. I will report which.
