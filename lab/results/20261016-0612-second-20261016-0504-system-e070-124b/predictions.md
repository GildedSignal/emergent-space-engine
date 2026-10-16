# Predictions (written before the ensemble flights)

Run: 20261016-0612-second-20261016-0504-system-e070-124b, lens: second author on
20261016-0504-system-e070 (silver). The checker's named gold experiment, verbatim: "Fly
the no-locals control over a seed ensemble (≥ 8 seeds × {1e4, 1e5}) plus one wide stagger
(bits ≥ 26, offsets ≥ ~10⁴ s, verified to move ≥ half the locals' first kicks). If the
locals' worst-frame contribution is ≤ ~50 at every seed, the refutation of 917c is
complete; if seed-3-like cases are common, 917c's lever stands at the ladder's low end
and the page's open direction 1 returns with a measured domain."

Instrument: the parent's patch (applied verbatim, anchor reproduced bit-exact on this
tree: fe 479/332, kicks 55,985, wave bucket 922 = 872 doll-0 + 50 doll-2, heaviest tick
2,873,098,240) plus three additions, all inside the ES_TRACE block: the trace cap raised
400k → 2M rows (no seed truncates), the full per-bucket series (bucket, events, doll≠0
events), and every doll≠0 body's first kick tick (to verify the stagger moved kicks).
Stagger bits cap lifted 30 → 32 (2³¹ ticks = 10,568 game-s, the checker's ~10⁴ s).
Flights: `xtask universe --bench --unpaced --engine-ms 100000 --rtf 1000 --seconds 30
--extra N --seed S`, arms ES_NO_LOCALS / ES_STAGGER_LOCALS as the parent.

Seeds 1–8 × {1e4, 1e5} × {storm, no-locals}; stagger bits 26 and 31 at seed 3 (the
checker's binding seed) and bits 31 at seed 1 (the parent's seed), all at 1e4.

## Predictions

1. **1e5 (both claims hold):** at every one of the 8 seeds the belt's wave bucket
   (doll-0) exceeds the locals' worst doll≠0 bucket by ≥ 5×; locals never bind the worst
   frame at 1e5. The wave bucket's doll≠0 count stays ≤ ~80 at every seed (parent: 50).
2. **1e4 (the refutation is NOT complete):** locals-dominated frames beat the belt's
   wave frame at a minority of seeds — I predict 2–4 of 8 (seed 3 is one; seed 1 and 7
   are not, per the parent's and checker's flights). So 917c's lever returns with a
   measured domain: the ladder's low end, seed-dependent.
3. **The wave's clock is seed-independent:** the heaviest wave tick is 2,873,098,240
   (±<0.1%) at every seed and both N — the belt's first kicks fire at Δs/2 regardless of
   seed; only amplitudes move (parent: 479 seed 1 vs 671 seed 7).
4. **Stagger engagement (the checker's criterion):** at bits 31 (offsets ≤ 10,568 s ≈ 47
   local kick intervals of ~224 s), ≥ half of the locals' first kicks re-time — I
   predict ~100% of doll≠0 firsts move by roughly their offsets. At bits 26 (≤ 330 s ≈
   1.5 intervals) fewer than half move meaningfully. Engagement check: total kicks at
   1e4 drop by ≈ Σoffset/interval ≈ 300 × 5,284/224 ≈ 7,000 (55,985 → ~48–50k) at
   bits 31, and by ≲ 300 at bits 26.
5. **The wide stagger does NOT cure the comb (the lever's letter dies on main):** with
   ≥ half of first kicks genuinely spread at bits 31, the locals' worst doll≠0 frame at
   seed 3 stays ≥ 70% of the storm arm's (the interval law re-anchors to the absolute
   grid, re-forming the comb within one period — the mechanism 20261016-0504-dynamics-4c22
   measured on its own variant; here it would hold on main, at full width). If instead
   the comb collapses to ≤ ~40% of storm, 917c's one-law lever stands on main as the
   parent's stagger arm could never test it.
6. **Off-arm identity:** with every env unset the patched digest is byte-equal to
   pristine main (parent verified 5b2d998b…; my additions are inside ES_TRACE blocks and
   the bits-cap lift, unreachable with the env unset).

What would make me wrong: the wave tick moving with seed (3), the stagger re-timing
fewer than half the firsts even at bits 31 (4 — then the replan-time offset is
structurally unable to de-phase and the arm stays decorative at any width), or the comb
collapsing under a true spread (5 — then the parent's "moves the peak by exactly 0" was
an artifact of the narrow arm, and 917c's lever stands on main).
