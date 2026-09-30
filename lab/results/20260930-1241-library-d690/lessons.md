# Five lessons from Julien's library — aimed at bottleneck 0 (representation), 3, 4, 5

All quotes retrieved verbatim from the Readwise API (`work/readwise.json`), 30 September 2026.

1. **Taleb, *Skin in the Game*:** "Outcomes are paradoxically more stable under the minority rule—the variance of the results is lower and the rule is more likely to emerge independently across separate populations. What emerges from the minority rule is more likely to be black-and-white, binary rules."
   - Mechanism: absorbing commitment vs continuous renegotiation — an agent that flips once stops generating variance; graded agents diffuse their aggregate forever (a compounding error).
   - Change (B0): AI/faction decisions enter the automaton as absorbing threshold flips on a dimensionless number (dyadic thresholds), never graded utilities; recompute only when the threshold is crossed.
   - Cheapest test (done, `work/experiment.py`): matched-activity toy at N=10³–10⁶ — binary aggregate is 6–17× tighter across populations and its sustained time-SD is 3–4.5× lower; no heavy-tail inversion (p99/p50 ≈ 1.0–1.2 both).

2. **Asimov, *Foundation and Empire*:** "The laws of history are as absolute as the laws of physics, and if the probabilities of error are greater, it is only because history does not deal with as many humans as physics does atoms, so that individual variations count for more."
   - Mechanism: relative aggregate fluctuation ~ 1/√n; once below the stored quantum, individual identity is unobservable noise — the aggregate law becomes exact.
   - Change (B3/B5): occupancy rule — per cell, if n ≥ n* = (1/ε_count)² store integer counts and individualize only inside the player's information horizon. ε=2⁻⁸ → n* ≈ 6.6×10⁴ ships/cell; ε=2⁻⁴ → n* = 256. Choose the coarsest player-differentiable count quantum; n* follows (verified 1/√n to 5.8%).

3. **Taleb, *Incerto*:** "You can expect blowups and explosive errors in fields where there is a penalty for simplicity."
   - Mechanism: cheap-but-penalized designs pay in compounding error (probe 1's walking energy, probe 2's shell crossings); unpenalized cheap designs (r2's exact 32+32 carries) never pay.
   - Change (B0): freeze a representation-selection gate — a candidate is admissible only if its cheap update is exactly representable (integer increments on the law's own grid); any candidate needing correction terms for cheapness is rejected as a bandaid (P19).
   - Cheapest test: exact self-consistency check (coarse-scaled fine path == cheap path) per B0 candidate, before any physics gate.

4. **Ries, *The Lean Startup*:** "They will ask to go back to the old way of working, in which they had the opportunity to 'stay efficient' by working in larger batches and passing work between departments."
   - Mechanism: large batches look locally efficient and concentrate variance at handoff boundaries — exactly probe 2's energy spikes at cell-boundary crossings.
   - Change (B2/B4): every cell-boundary handoff and kick exchanges the smallest native unit (one exact integer increment, a monoid message), never bulk state; the allocator must never coalesce the causal frontier into ticks to amortize — that is the "stay efficient" trap (P14).
   - Cheapest test: two-cell AVI toy, energy-error p99 vs handoff batch size (1, 8, 64 increments) — expect p99 to flatten as batch → 1.

5. **Graham, *Black Swan Farming*:** "Without visual cues (e.g. the horizon) you can't distinguish between gravity and acceleration. … The solution is to ignore what your body is telling you and listen only to your instruments."
   - Mechanism: the equivalence principle as an operational test — a local frame is right when an interior observer cannot feel it.
   - Change (B0): the acceptance invariant for a sheet: interior geodesic deviation below one position quantum per light-crossing, all curvature carried by the boundary river flow. A sheet that can be felt from inside is wrong at any price.
   - Cheapest test: two slow nearby worldlines inside a candidate sheet stay within one position quantum while the same pair straddling the boundary tracks the river exactly.
