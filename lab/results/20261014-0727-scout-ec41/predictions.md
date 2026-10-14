# Predictions (written before running anything)

Question: where does the cold rail's ~1.9×10³ encounter cut at 10⁹ live, and does
per-cycle renewal (EDMD/KDS-style window certificates: re-certify a pair when its
slack is exhausted, not when any kick lands) kill the cadence factor?

Cost model under test (from effb's ledger + 90fb's law):

    cores(10⁹) = (kicks/s = 2^step_log2/P × N) × (pairs re-certified per kick ≈ 0.0346·n·X) × (cost per re-cert)

with step_log2 = 7 shipped (128–256 kicks/orbit/body).

Predictions, each falsifiable on shipped code (`encounters kick|scale|steady` + one new `cycle` probe):

1. **Degree (factor 2) is density physics, not tier artifact:** `scale n` at fixed density
   (rho = 1e-4·10⁴/n) gives cone_per_body ≈ constant in n (no growth 10³→10⁵); work per real
   encounter stays ≥ 10³ evals (6875's 2.3–3.6×10⁵ at stirred belts bounds it above).
2. **The slack budget ≫ one orbit of belt kicks:** silent_budget_median / (1.5·eps) ≥ 128
   for eps ≤ 1e-7 (belt kick sizes), i.e. a stored budget absorbs a full 2⁷-kick orbit;
   at eps = 1e-3 (battle-scale) it absorbs < 128 → renewal buys nothing there (hot rail
   stays kick-bound — consistent with the rails decomposition).
3. **Soundness:** skip_violations = 0 at every eps where slack_skippable_fraction > 0
   (0/0 like 8bfa/317c). Any violation > 0 kills the renewal certificate as unsound.
4. **Over-fire beyond the budget turns on steeply** (the calendar's lesson: conjunctions
   cluster): proposals per orbit at slack s grow ≥ linearly in s/budget; at s = budget
   itself ≈ 0 proposals by construction of the binary search. So the economy point is
   s ≈ budget, and the renewal cost, not over-fire, is the price.
5. **Composition:** at eps ≤ 1e-7, per-cycle renewal drops the re-cert stream by ≈ 2⁷
   (renew ≈ once per orbit per pair): the 7.7×10³-core ledger row falls to ≲ 10² cores
   from cadence decoupling alone; the residue is degree × per-cert (the skin's 3.6× and
   the cell partition already address it). If instead pairs/kick re-certification is
   *not* reducible to ≈ degree per orbit (i.e. changed_fraction stays high at belt eps),
   the cadence factor does not decouple and the 10³ must come from aggregation.

Kill criterion for the renewal candidate: median budget < 1.5·eps·128 at eps = 1e-7,
or skip_violations > 0, or over-fire at s = budget > 2 proposals/pair/orbit.

Held-out for the checker: seed variation (the shipped experiments fix seeds; the
checker should vary seed and n, and probe eps = 1e-8 and 3e-4).
