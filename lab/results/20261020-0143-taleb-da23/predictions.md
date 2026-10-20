# Predictions (written before the decisive run)

The stride gate (`Config::stride_gate`, default off): `alone_at`/`final_through` grow every
finality reach box by v·(stride_max+1)·window, so a region can turn final through t only if no
neighbour's live-or-next stride (start < t, span ≤ (stride_max+1) windows) can have its
certificate hull touch it. Mechanism: the finality assert fires iff a rollback restores an
affected lineage below its published fin_hi; every such restore comes from a stride that started
below t, and every such stride's hull lies inside the grown box (e517's PRE/HAZ projection uses
the same hull bound), so coalescing on it blocks the finalization instead.

Cases NOT tuned on (smoke draw only: one battle seed 11, both arms, no fire):

- **P1 (fires die).** On the c749 fire protocol (galaxy 8704/24 fleets, margin 0.5, seeds
  11..31 + replicates of s11/s23, 4.5 s draws, one process per draw) the shipped arm fires
  (exit 101, FIRE line, PRE D > 0 preceding) at its pooled incidence (~2-5 per 16 draws); the
  gated arm fires 0. If the shipped arm fires 0 in this window (incidence is a wall-clock race,
  load-coupled), P1 is UNRESOLVED, not passed.
- **P2 (no starvation, bounded cost).** On every draw where the shipped arm does not fire, the
  gated arm finishes the same scene (regions collapse, no timeout, no stall) with present
  within 10% of the shipped arm on the same seed, and deadline misses not worse than 2×.
- **P3 (the state law holds under the gate).** On the gated arm every HAZ line shows A ≤ 0 or
  "-" (never armed), every RB line m ≤ 0, and no FIRE line, on all classes flown (battle, gas
  churn min_region 1, streams, adversarial min_region 8, margin-2.0 negative).
- **P4 (churn class, the 01e7 crash family).** gas 8192 spread 2, min_region 1, rate 600 (the
  keeping-up rate where 01e7/bc0f crashed 3/9 at scene start): gated arm 0 fires in 6 draws,
  present not below half the shipped arm's (load-coupled present varies; the claim is the
  order of magnitude, not the exact number).
- **P5 (finality lag is the cost, and it is bounded).** `final lead max` on the gated arm
  stays > 0 on battle draws (finality still runs ahead of the frame's needs; no livelock of
  publication), while smaller than shipped (expected: one stride's light travel, ≤ ~336
  chronons at the shipped stride_max).

What would make the gate wrong: a fire on the gated arm with D > 0 (the projection bound
misses a hull — e.g. a stride longer than (stride_max+1) windows after merges inherit a bigger
stride), or starvation (present collapses, deadline misses explode) on the churn family.
