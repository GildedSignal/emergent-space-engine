# Predictions (written before the decisive runs)

The dashboard (`xtask universe --bench`) has only been read by the integrator near its defaults
(members 48, base throttle, rtf as flown). Everything below is a held-out extreme I have not run:
member count ×10 and ×100, throttle level 15 (11,560 g), engine overload (rtf 1e4), and unpaced
capacity runs. Written 6 October, before any run of the matrix.

- **P1 — the engine budget bounds the engine tail.** In every paced run, including rtf 1e4 overload,
  the engine's CPU per frame stays within its 5 ms wall budget up to scheduling noise (prediction:
  p99.9 ≤ 7.5 ms); overload shows up as `overflow_frames` > 0 and a *smooth* rtf dip, never a frame
  whose CPU explodes. Falsified if any paced run's engine p99.9 > 7.5 ms or its worst frame CPU
  exceeds engine + view + serialisation by more than 2× (i.e. the budget did not bite).
- **P2 — the unbudgeted view binds at scale.** At members 4800, view_gather + view_json are together
  > 50% of frame CPU and the worst hitch is view work, while the engine stays inside budget.
  Falsified if the engine share dominates at 4800.
- **P3 — member cost is linear, the tail is battle-shaped.** Engine CPU per frame grows with members
  within a factor 2 of proportional (48 → 480 → 4800), and p99.9/worst ≫ p50 in battle runs
  (encounter-shaped tail, not a smooth distribution).
- **P4 — one decision is a burst.** At level 15 the worst hitch lands on or within 3 frames after a
  scheduled burn (from the decisions log) in at least half the runs; and the level-15 worst-frame
  CPU is ≥ 1.5× the level-0 worst at the same members.
- **P5 — capacity order of magnitude.** At members 4800 the paced run cannot hold 60 Hz
  (p50 > 16.7 ms or hitches/hour > 1000); at 480 it can. N* is between 480 and 4800 members.

All are orders-of-magnitude claims on shared Linux x86 (lab rule): the integrator re-measures on the
M1. Machine state is recorded by the bench itself (`machine_before`/`machine_after`).
