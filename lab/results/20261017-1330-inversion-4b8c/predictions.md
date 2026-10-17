# Predictions (written before the decisive run)

Mechanism hypothesis from code reading (no measurement yet): `drain_scans` (universe.rs:1186)
answers held scans only while the frame's wall budget has `2·max(scan_ns, 750 µs)` left; under
wall pressure it drains nothing. Each player item captures one scan (`encounters_for_player`,
universe.rs:772) holding `binding_at(j, t)` for every apsidal-filtered candidate in the doll
(encounter.rs `Held::capture`); t moves per scan, so each scan pins fresh historical entries.
The backlog is capped at `SCAN_BACKLOG = 2048`.

Arms: `xtask universe --bench --seed 1 --rtf 100 --unpaced --threads 1`, members {100,400,800},
engine-ms {5.0 control, 0.2 starved}, seconds 40–55. Instrument: per-300-frame
`held_scans` + VmRSS, print-only.

- P1 (control): at engine-ms 5.0 the backlog stays small (< 100) and RSS is flat over ≥ 2,500 game-s.
- P2 (starved): at engine-ms 0.2 the backlog climbs monotonically to the 2048 cap; RSS grows with
  it; the cut's settle flushes all scans (bulk drop ≥ 90% of the growth, held → 0).
- P3 (law untouched): the digest at the canonical cut is identical between control and starved arms
  (same seed, frames, input log, cut).
- P4 (scaling): the RSS plateau at the cap divided by 2048 (per-scan bytes) grows ∝ members
  (100 → 400 → 800): the cap is N-linear, not the "about 10 KB each" of the comment.
- P5: the starved arm's presented tick lags the control's (the wall path changes presentation only).

Kill criterion: if the starved arm's backlog never grows (or RSS grows with backlog flat), the
prune-starvation/held-scan mechanism is wrong for this scene and the dossier says so.
