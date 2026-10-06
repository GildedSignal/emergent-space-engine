# Predictions — 20261006-1738-second (written 17:50, before the decisive 30 s sweep)

State of knowledge when written: instrumentation (max-per-kind in `Stats`, player-item phase split,
drain member count) is built and was smoke-run only on **seed 1, m480/l15, 5 s** (tail config, short
cut). There it showed: player max item 36.1 ms, of which hand-out drain 34.3 ms over 22 members;
fleets-catch-up 0.8 ms; encounters 3.8 ms; ship-lane pull 2.4 ms; step+apply 1.3 ms; fleet max item
0.7 ms; standalone hand-out max 2.9 ms. The decisive runs below were **not** run at 30 s or on any
other seed when this file was written.

The held-out cases and my predictions:

- **P1 (kind, every seed).** On every seed at m480/l15, the most expensive single item is the
  *player* item, and its dominant phase is the hand-out drain (≥ 60% of the item). No fleet, ship,
  planet or moon item exceeds 3 ms on any seed.
- **P2 (mechanism vs magnitude, seed spread).** The checker found seed 2 at m480/l15 has no giant
  (engine max 10.5 ms). I predict: giants (a player item > 20 ms) appear on a minority of seeds
  (1–3 of 6); on *every* seed the max player item still exceeds 2× the 5 ms budget (> 10 ms), i.e.
  the mechanism (the drain is unbudgeted) holds everywhere, only the batch size varies.
- **P3 (drain composition).** The giant drain is many members, not one slow bind: the max drain
  carries ≥ 10 members at ~1–2 ms each (per-member bind+catalogue-insert+plan), not 1–3 members at
  10+ ms each.
- **P4 (digest control).** With the instrumentation patch in, the 30 s m480/l15 seed-1 run
  reproduces the original run's e digest `bc132cb0…` at cut_tick 609076340 (measurement fields only;
  no outcome reads them).
- **P5 (loaded vs quiet).** The max item is CPU time, not contention: under a 6-spinner load on this
  8-vCPU box its magnitude moves by < 1.5×; hitch counts may rise slightly.
- **P6 (paced vs unpaced, this box).** Same scene, same seed, paced/unpaced cpu p50 ratio ≤ 1.5
  (the author's 2.7–5× was a shared-window contention artifact, as the checker argued).
- **P7 (budget dial).** At --engine-ms 20 the same scene converts deferred hand-out work into
  bigger drains/hitches (the original's 1:1 dial→hitch finding), with the player item still the
  max item; i.e. the dial changes when the drain runs, never that it is unbudgeted.

What would falsify the named attribution: a seed where the max item is a fleet or ship item ≥ 20 ms,
or where the player item's dominant phase is encounters/step rather than the drain.
