# Predictions — 20261020-0440-library-3c03 (library lens on allocator-ratchet)

Question: da23's stride gate v2 leaves one fire topology (gate s19: `PRE id=51 s=960 e=976
D=(32,44,944)` → `FIRE id=52 s0=944 fin_hi=976`). da23 names three suspects: (a) the
truth-hull radius (`truth.r` vs the coalesce radius), (b) finalize-round base staleness,
(c) a merge path raising `fin_hi` without an `alone_at` decision. I add a fourth from
reading the gate: (d) gate part 3 pushes every live truth into `alone_at`'s coalesce as an
**ids-empty** pseudo-member ("it merges groups, joins none") — a truth that touches exactly
ONE group contributes no ids, so `filter(e.ids.len() == 1)` still calls that group alone:
the decision publishes `fin_hi = t` past a truth start it itself counted as touching.

Instrument (print-only, env `ES_FIRE_WHY=1`, on top of da23's patch, gate arms unchanged):
- `fin_why` chain: every `fin_hi` raise logged with its site — `frontier` (finalize's
  unconditional advance), `alone` (finalize_shared decision), `bisect` (slow path),
  `merge` (regroup's inherited union_parts / make_region).
- `DECIDED id t grp=[..] truths=[(id,start)..]`: at every finalize_shared decision, the
  exact coalesce group (own union-find over the same ents and predicate) and every truth
  pseudo-member that merged into it.
- `FIREWHY` at da23's FIRE line: the fatal region's chain, fin_parts (tick, owner, giant),
  verified/rmax, and the group recompute at `t = fin_hi` on current state.
- arm `gate=2`: gate v2 with the one-line (d) fix — the truth pseudo-member carries
  `ids: vec![tr.id]` — behaviour change ONLY in arm 2; arms 0/1 byte-identical to da23's.

Protocol: `exposure battle 19 2400 32 8192 0.5 24 8704 4.5 <arm>` (da23's fire protocol,
his hottest seed), draws until fire (incidence is a wall-clock race; paired same-window),
plus the 7 other battle seeds once each on arm 1 vs arm 2, plus the churn class
(`exposure gas 11 600 1 8192 2.0 12 4352 4.5 <arm>`, min_region 1 — da23's unflown P4).

P1 (mechanism of the survivor): FIREWHY shows region 52's `fin_hi=976` was set by the
`alone` path (an `alone_at` decision at t=976), NOT by `merge` inheritance and NOT by the
`frontier` advance. [da23's (c) would show `merge`; his (b) would show the blocking group
appearing only in a later round's DECIDED lines.]

P2 (which of a/d): the DECIDED line at t=976 for region 52 lists truth (44, 944) inside
its group — the truth TOUCHED and the gate still called the group alone (the ids-empty
hole (d), not a radius deficit (a): with (a) the truth would be absent from the group).

P3 (no drift): FIREWHY's recompute at t=976 still shows truth 44 touching region 52's
group (the miss is structural, not state-movement between decision and clash).

P4 (the fix): arm 2 (truth ids) kills the survivor class — 0 fires on ≥ 8 gate-protocol
draws incl. s19 ×3, every RB line at m ≤ 0, final lead max > 0 (no publication livelock),
present within the gate-v2 band (no new starvation beyond da23's 15–40%).

P5 (da23's unflown P4, churn class): the gate (either form) does not starve the 01e7
family: `gas` min_region 1 completes on both arms, present_end within 2× of shipped.

Kill criteria: any fire on arm 2 with truth-touch in its FIREWHY (the fix fails its own
mechanism); or arm-2 present collapsing > 2× below arm-1 on the battle class (the fix
trades the crash for a stall — adoption then needs the disarm channel, not the ids fix).
