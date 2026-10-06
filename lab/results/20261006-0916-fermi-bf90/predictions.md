# Predictions (written before the decisive runs)

The question: at 10⁹ bodies on one 8 GB M1, which budget term breaks first, by how many
orders, and is the board's "190 cores" headline the right number? All runs below are
x86 cloud (orders of magnitude only, per the lab rules); the M1 numbers are the repo's.

Model (per game-second, RTF 1): bill = N · (kicks/orbit)/T_orbit · cost/kick, plus the
O(N) terms (view gather, encounter setup), plus memory = N·bytes/body.

Anchors from the repo:
- B9 red-team gloss (redteam-out.md #14): "0.19 core per 10⁶ ships on a 90-min orbit".
  Reverse-engineered: 512 events/orbit · 2 µs/event / 5400 s = 1.9e-7 core/body.
- Plane, M1 (HANDOFF): kick = 29 µs (15 of them rebinding fit+compile); the player's
  encounter check = 190 µs/item; view gather = 83% of a light frame.
- H0190: 32 kicks/orbit; 0.3 with orbit-averaged tides (the adopted lever).
- shipmem gold (components-98bc): 0.126 bits/body for a belt program; tube = 16 bytes.

## Predictions, each falsifiable by the runs below

P1 (kick-bench on x86, `universe --kick-bench --seconds 5`): median kick cost
10–60 µs (M1 says 29), and the rebind/compile share ≥ 40% of it. Distinct-kick
shape-collision rate on the exact key ≈ 0 (the 5 October artifact lesson).

P2 (designed-kick floor microbench, i128 fixed point, shared doll moments, 12+12-bit
memo probe, no rebind): 50–500 ns/kick single-thread — i.e. the law's 2 µs/event
target sits ≥ 4× above the arithmetic floor, so cost/kick is a compiler problem, not
a physics bound.

P3 (reconciliation): "190 cores" = B9's ceiling cadence (512/orbit) priced at the 2 µs
event cost. Today's honest pairing (32/orbit · 29 µs) gives ~170 cores at 10⁹ — close
to 190 only by cancellation (cadence 16× better, cost 14.5× worse). The designed
pairing (0.3/orbit · 2 µs) gives ~0.1 core. So the headline is right today for the
wrong reason, and the plan's "10–100× less" is already banked in the design.

P4 (which term breaks first at 10⁹, RTF 1, 90-min-orbit populations): memory as stored
tubes is dead by ~2–3× (16 GB > 8 GB); populations+scars pass unless the actively-kicked
fraction exceeds ~10⁷ bodies. Bandwidth passes with ≥ 100× headroom (~64 B/kick).
The O(N) terms break by the most: an O(N) view gather at even 1 ns/item is 1 s/frame
(dead by ~60× at 60 Hz); at today's 190 µs/item it is dead by 7 orders. Encounter setup
passes only under q-candidate-degree/taleb-09b5 (work tracks real encounters).

P5 (scene mix): the kick bill is set by the innermost populations (T_orbit in the
denominator); a galaxy whose 10⁹ sit on ≥ year-scale orbits pays ≤ 10⁻³ core in kicks,
so the headline's "all in 90-minute orbits" is the adversarial case, not the goal case.
