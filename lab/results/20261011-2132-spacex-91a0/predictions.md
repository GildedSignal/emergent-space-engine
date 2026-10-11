# predictions.md — 20261011-2132-spacex-91a0

Written before the decisive runs. The runs measure H_live (live distinguishing information)
on the flying plane, per game-second, for the two populations (fleet members in the frame;
ships as tubes), coded by a two-level shared-program coder. Cases below are NOT tuned on.

## P1 — fleet velocity distinctions are transient, not steady-state
The battle's contacts decorrelate members in the first game-seconds; after the battle cools
(contacts_this_s → 0) the number of distinct velocities plateaus and
floor_bits_per_member_velocity stays flat (no per-game-second growth). Predicted plateau:
log2(N) + spread ≈ 20–30 bits at N = 400; roughly flat over ≥ 10³ game-seconds.

## P2 — position bits grow logarithmically, not linearly
With velocities fixed after the battle, relative positions spread ballistically: the range
per dimension grows ~linearly in game time, so its log2 (my coder's cost) grows ~log2(t):
slope per game-second falls toward 0. The stock never crosses 64 bits/member on any linear
extrapolation that respects the log shape; a naive linear fit over a short window would
overstate it.

## P3 — ships: all distinct keys, ~constant floor
The 23 ships (plus fleet leavers) each hold a distinct catalogue key; floor_bits_per_ship
≈ 32 (angle) + 8 (time) + log2(distinct) + shared/N ≈ 45–55 bits, roughly constant in game
time (kicks change keys rarely — kicks_this_s ≈ 0 for most seconds at these rtf).

## P4 — the decision: the 8 GB budget is not threatened by H_live growth
Net H_live flux per game-second ≈ 0 in the steady state for both populations; the law's
"+62 bits per kick, −60 per reabsorption" describes active transients (contacts, kick
epochs), not an unbounded leak. The measured memory bottleneck is the store, not the
information: plain storage per body (engine-reported bytes_per_body, ~2×10³) sits ~10²×
above the information floor (~10¹ bits). So populations-as-programs (shipmem) remain the
right lever for 10⁹ in 8 GB, and the gate to write is on bytes-per-body convergence to the
floor, not on H_live growth.

## What would make this wrong
- floor_bits_per_member_velocity or per_ship grows with a positive steady slope (≥ 0.1
  bits per body per game-second) after the transient: then H_live is an unbounded leak and
  the populations plan needs scar compaction by design, not just better coding.
- Contacts keep firing indefinitely in the frame (sustained battle): then P1/P2 measure a
  battle scene, not the plane's steady state, and the run must say so.

## Held-out cases (not tuned on)
Seeds 7 and 99 at rtf 100, plus members 400 vs 48 (population-size dependence of the
plateau and of contact counts). Also the log-shape check in P2: fit the position floor
against log2(game_s), not just game_s.
