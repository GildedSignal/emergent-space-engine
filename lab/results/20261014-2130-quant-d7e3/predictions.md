# Predictions (written before the flights)

The question: the named untested exposure of bf21's `ES_PULL_CAP` — **the player inside the belt
band during the first-kick wave** (bf21 checker-2: "a player inside the belt band during a wave is
the real untested exposure"; 38bf's Unmeasured list). Scene: `plane_extra_belt_player`, the ladder
belt at N=2×10⁵, the player on a near-circular orbit at 2.5 AU in the root doll (the belt ships'
own doll), L8 burn from tick 0, rtf 100, 12 ms budget, settled at the 16,000 game-s cut — the
wave_input protocol, only the player moved.

Known already (the record, not predicted here): out-of-band (player at Home → root doll only under
burn) uncapped worst frame ~1.37–1.49 s / ~9–12 frames over; capped 11.97–12.49 ms, 0–1 over,
digest bit-identical (`c2b834bb…` at seed 1). My control re-runs that arm on this box.

## P1 — the exposure is real as a cost (uncapped, in-band, seed 1)

The monsters return and are **no smaller** than out-of-band: worst frame ≥ 100 ms, ≥ 3 frames over
12 ms. Mechanism: the pull (`pull_ships(key, !in_root)`) resolves every ship item below the
player's next item — the batch is wave density × item horizon, position-blind, so in-band changes
little there — but the **scan** now walks belt bodies as candidates (a2c1: 194 walked/call at
10⁴–3×10⁵) and the capture reads mid-wave bindings. If instead the in-band uncapped arm holds
max frame ≤ 20 ms, the exposure is cost-free even uncapped and the cap's case weakens to the
out-of-band scene only — a result either way.
**Kill:** none — both branches are informative. Direction bet: monsters present (≥ 100 ms).

## P2 — the certificate (capped vs uncapped, in-band, seed 1)

Bet: **digests differ, or encounters/kicks counters differ**, on the in-band scene. bf21's
neutrality argument was "key order makes every binding at t final before the player's item pops —
the one hole is `input` over an overdue backlog"; in-band the scan's candidates ARE wave bodies,
so the capture-at-answer-time can meet mid-wave state the out-of-band scene never touched. The
checker already called the out-of-band neutrality "scene-structural, not a law".
**Kill of the adoption-as-is:** if capped ≠ uncapped in-band (digest or counters), the cap needs a
guard before merge (named: hold the capture when the candidate's doll is mid-wave — the same
`SCAN_BACKLOG` machinery). If they are identical AND max frame ≤ 12.5 ms, the certificate extends
in-band and the adoption is de-risked.

## P3 — held-out seed 7 (in-band)

Same direction as seed 1 (monsters uncapped; capped either identical digest or not). Belt phases
differ with seed; the wave window moves a few hundred game-s; the pull's item-horizon batch is
seed-stable in size (bf21: seed 2 was 1.03×).

## P4 — counters (both arms)

Kicks ≈ 2.2–2.3×10⁵ at the cut (bf21's 225,949 seed 1 out-of-band; the belt's kicks are the
doll's clock, blind to the player's place — a ≥ 5% drift means the player's placement changed the
belt's own scheduling, itself a finding). Encounters ≥ out-of-band (the player is now a real
candidate among belt bodies); if the player dies (belt rock contact), that is scene content, not a
seam failure — report it.

## What would make the run VOID

The build failing to reproduce 38bf's control digest `c2b834bb…` out-of-band (then my scenario
refactor moved bits and every in-band comparison is suspect).
