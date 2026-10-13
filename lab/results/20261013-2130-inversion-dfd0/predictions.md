# Predictions (written before the decisive run)

The inversion: the flight recorder merged 13 Oct (73c98a46) with the decision-tick hole unfixed
(session.rs:119 logs at the presented tick; the a342/a004 `sched`+quantum port is absent from the
tree). The decision-log page's open direction 1 said the recorder "must not merge before this
does". Predictions for the shipped recorder, same session (seed 3, rtf 100, one script, one dt
pattern), only the engine's wall budget differs:

1. **The fork appears in the files.** Rich arm (engine_ms 8, slack at 400 members) and starved
   arm (engine_ms 0.05) produce two flight files whose logged input ticks diverge — the starved
   arm's ticks lag, the lag growing with wall time (40c0's law; a004's arms diverge the same
   way). At least one decision's tick differs; the last differs most.
2. **The digests differ** (two canonical truths for one player session). A loss flip (one arm
   lost, the other alive) is possible at ~430 game-s with this script but not guaranteed; the
   digest fork is the certain half.
3. **The gate blesses both.** `replay()` returns `same()` for each file, and `--replay-all` on
   the pair exits 0: per-file exactness holds (it is the law's property); nothing checks that one
   session yields one flight.
4. **Held-out (load-shaped, not seed-shaped):** the same pair at 150 members (budget bites less)
   shrinks the tick fork monotonically; the same pair at 400 members on a busier box widens it.
5. **Control on the other side:** file A replayed at a different thread count still matches its
   recorded digest — the replay instrument is exact; the difference lives in the recording.

Kill criterion for the claim: if rich and starved files come out bit-identical (same ticks, same
digest), the shipped recorder does not freeze the hole on this scene and the dossier says so
(the hole would then need harder starvation than a wall budget — a004 drove it with
`Budget::events(2)` directly).
