# Predictions (written after the 10^4 validation arm, before the decisive arms)

Validation arm (tuned on): `10000 burn 20 1000 12`, ES_WAVE_PROBE=1. Worst frame f891:
47.7 ms, ONE top-level item (the player's, items_by_class [0,0,0,1,0]), 904 nested ship
kicks inside it, `item: kick (clock)` 41.4 ms of the 47.7. Neighbour frames clamp at the
12 ms budget with ~220 top-level events. Mechanism read off the code and confirmed there:
`resolve_body(player)` in the root doll calls `pull_ships(key, !in_root)` = every due ship
of the player's doll (in root, that is the whole belt), nested `resolve_body` calls that
never see the budget; the player's light distance is zero, so its item is first in deadline
order and the first-item escape starts it even on a spent budget.

The decisive arms (not tuned on): `50000 burn 24 1000 12`, `100000 burn 24 1000 12`,
`200000 burn 24 1000 12` (ES_RSS_CAP_MB=1750 on the last), and one rtf control
`100000 burn 26 600 12`.

- **P1 (mechanism, all rungs).** At every rung >= 5x10^4 the worst wave frame is again ONE
  top-level player item carrying >= 85% of the frame's wall as nested ship kicks
  (items_by_class[player] = 1, ship items_by_class = 0, kicks >= 100x the top-level item
  count). Kill: any worst frame whose wall is instead spread over >= 50 top-level items,
  or owned by rekey/prune/scans/encounters stages.
- **P2 (K-law).** max_ms is K-linear at fixed rtf: the per-kick nested cost stays ~50-60 us
  and kicks-per-gulp scales with K, so max_ms(5x10^4) in [0.19, 0.32] s, max_ms(10^5) in
  [0.38, 0.65] s, max_ms(2x10^5) in [0.8, 1.5] s, and the ratio 2x10^5 / 5x10^4 in [3.3, 6.0].
  (Anchors: 47.7 ms at 10^4 here; 414 ms at 5x10^4 and ~1.29 s at 2x10^5 on other runs' arms.)
- **P3 (rtf, held out).** The gulp is cadenced in game time (the player's own item), so
  max_ms at rtf 600 lands within +/-35% of the rtf-1000 arm at 10^5.
- **P4 (arithmetic, unflown).** On the measured constant (~4.7 us per body per gulp), the
  worst wave frame at 10^6 is 4.5-7 s in ONE frame (unflown: build 2.34 GB > this box's cap),
  and at 10^9 a root-doll player is a ~5 ks frame: the scan's O(doll) read set, not per-frame
  walks, rekey or the queue, is the term that breaks first as the plane grows.

What would make the mechanism reading wrong: a worst frame whose items_by_class shows many
ship items resolved as TOP-LEVEL items (the budget loop itself overrunning), or the wall
living in `rekey`/`prune`/`encounters: held scans answered`.
