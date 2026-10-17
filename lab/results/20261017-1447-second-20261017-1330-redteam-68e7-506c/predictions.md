# Predictions — 20261017-1447-second-20261017-1330-redteam-68e7-506c

Written before the decisive run. Disclosed dev state: the harness compiled clean and was
smoked on s0 (ladder scene) and h3 (this run's held-out battle draw) through the starved
path, and the allocator arm on islands1 and galaxy, to validate mechanics only (controls
behave: shifted agrees, late breaks). Nothing below is tuned on those smokes beyond "the
harness runs"; the decisive suite covers all 11 battle scenes and all 3 allocator scenes,
none of which (except the four named) has ever run starved.

Held-out cases for the decisive run:
- battle: s1–s7, h1, h2 starved for the first time (r5 ran them unstarved; identity of the
  *starved* schedule there is the prediction), and h3 in full;
- allocator: islands2 (never run in any form by me);
- a second full execution of both harnesses (row byte-identity except wall fields).

P1 (starved sparse ≡ lockstep reference): every scene, both fixed-1 and seeded-random
budgets, identical_fraction = 1.0. The starved schedules make 10²–10⁷ advance calls
(s0 rand ≈ 370, h3 f1 ≈ 1.2×10⁷ in the smoke) — the slicing is real, not cosmetic.

P2 (starved lockstep ≡ sparse reference): every scene, identical_fraction = 1.0 (one
chronon per advance call; 4096 calls at horizon 4096).

P3 (cross-thread + starvation): sparse t4 starved-random ≡ lockstep t1 unbounded on every
scene.

P4 (competing load): the loaded run (3 spinning hogs) ≡ the unloaded reference on every
scene; the loaded starved call-count equals the unloaded same-seed call-count (the budget
stream is wall-clock-blind); the slow factor is ≥ 1.1 on the heavy scenes (contention was
real, not nominal).

P5 (allocator arm): all 27 cells (3 scenes × workers {1,8} × sabotage × budgets {1, cal},
plus 3 loaded cells inside those counts) ≡ one Chronon over the union; the budget-1 cells
show ≥ 1000 units (starvation slicing real at the scheduler level); at least one cell
rolls back (sabotage exercised) and identity survives the rollbacks.

P6 (controls): both-shifted starved agrees on every scene (a changed law, not a changed
schedule); one-order-late breaks on every scene (identical_fraction = 0.0).

P7 (record determinism): a second full execution writes byte-identical rows except the
wall-clock fields (secs_*, slow).

Kill criterion (written before the run): any P1/P2/P3/P4/P5 identity divergence means the
tie rule's budget clause ("every schedule, budget and thread count pops the same sequence")
is false on shipped code — a law bug, not a harness artifact, because the planted negative
proves the comparison detects real differences. That would be a clean refutation of the
premise's budget axis, reported as such.
