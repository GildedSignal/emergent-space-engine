# Predictions (written before the decisive runs)

The probe: `ES_DORMANT=1` holds fleet hand-outs as dormant `Leaver` records (4 words + tick,
no body, no queue entity, no scan candidate) instead of binding them. Wakes: (a) at the player's
item, a drift-bound gate — wake iff the leaver's exact hand-off position can yet come within the
player's encounter reach, `|x_leaver(t_h) − x_player(t)| ≤ near + 4·(|v_leaver|+1)·(Δt + h)`; (b) at
`settle` (the digest's cut), all. `ES_PLAYER_ANGLE` moves the player around the fleet's circle
(shipped: ~20 km ahead of the fleet; far scene: the opposite side, ~14,000 km, co-orbital so the
separation is constant). `--members` clamp lifted as in 20261013-1915-fermi-367f.

Cases not tuned on (the decisive matrix, seed 1 and 3, 8 s, paced 60 Hz, threads 1):

1. **Digest identity.** Shipped vs dormant, same scene/seed/cut: I expect **bit-identical
   digests in all four cells** (near/far × dormant/shipped). This tests the shipped comment
   "when it is made changes no outcome" at the digest level for the first time. If it fails,
   that is a canon leak (a hidden wall-clock dependence in the hand-out path) and the run's
   finding, whatever the cost numbers say.
2. **Near scene (player 20 km ahead): no win, by construction.** The gate wakes every leaver at
   the first player item after hand-out: bodies, standing bytes and the hand-out stream ≈ the
   shipped arm; the rung stays collapsed at 1,500 members/rtf 100 (449/480 overflow class).
3. **Far scene (opposite side, co-orbital): the hand-out stream leaves the flying budget.**
   Prediction: most leavers stay dormant through the whole 8 s flight (co-orbital separation
   ~14,000 km vs a gate radius of v·Δt ≈ hundreds of km). Consequences to check:
   - `bodies` before the settle ≈ the shipped birth count (~28) against shipped's 28 + leakers
     (hundreds at 1,500–4,000 members);
   - the fleet item's µs and the overflow frame count at the 1,500-member rtf-100 rung drop
     by the hand-out share of events (fermi measured hand-outs ≈ 67% of battle-regime events
     at 4,000/rtf 1) — I predict overflow frames fall by ≥ 2× at 1,500 members, and the
     1,500-member rung becomes flyable;
   - the deferred binds land in the settle (unpaced): its wall time grows by leakers × ~0.5 ms.
4. **Gate cost.** Per player item per dormant leaver I expect tens of ns (one distance eval on
     f64s) — invisible next to the shipped O(all-bodies) scan's 33 ns/body it replaces for
     dormant members (they are not candidates at all).
5. **Soundness residue.** The gate's bound ignores acceleration (padded ×4 in speed) and has a
   staleness cap; a missed encounter would show as a digest break in cell 1. The far scene at
   seed 3 is the held-out seed; the near scene is the gate's positive control (all wake).

Kill criteria for the configuration: digest differs in any cell (unsound gate or non-identity
replay — report which); or the far-scene fleet turns out light-frozen (leavers ≈ 0 in both arms:
scene invalid, not a lever).
