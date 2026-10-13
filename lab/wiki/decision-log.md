topic: decision-log
status: open
closed-by:
valid-while:
updated: 20261013-1249-taleb-a004

# The player's decision log: canonical ticks for a wall-world press

Split from frame-cost's "one live contract hole" (20261013-1249): the question deserves its own
page because it is Truth, not cost — and because the flight recorder (in flight) will freeze
whatever the loop logs today.

## Current best

**The hole compounds, and the fix closes it on the current tree (20261013-1249-taleb-a004).**
The shipped loop (`xtask/src/universe/session.rs::step`) logs a key change at the frame's
*presented* tick; the presented tick is what the budget left behind. Measured through the
loop's exact two lines (seed 11, rtf 100, deterministic `Budget::events(2)` load arms,
probe `ruin_probe`): four arms (60 Hz rich/starved, 30 Hz, 144 Hz) → four digests; the starved
arm's first press logs at tick 5.77M instead of 10.15M (21.6 game-s of presented lag in half a
wall second). **The divergence compounds**: player separation rich-vs-starved on identical
inputs grows 0.31 AU → 2.3 AU → 18 AU over 415 → 1,245 → 3,734 game-s (×7.5–7.8 per 3× time),
then saturates at system scale (checker2, 20261013-1249: 22.9 AU at 11,202 game-s, ×1.27 —
the histories stay divergent there, encounters 339 vs 405, contacts 58 vs 142; what refutes
"bounded offset" is the growth regime, not unboundedness), encounters cross over (43>29 →
121<133), contacts 6 vs 54 at the top — the "new loss" class of flag a `--replay-all` merge
gate would read as a regression is, on this hole, a coin flip on machine load.
**The a342 fix (20261008-0743, ungraded, never merged), ported to the post-clock-merge tree by
20261013-1249 and wired into `session.rs` and `kick_bench.rs` there, closes it**: a `sched`
timeline (every frame's `want` integrated — load-independent) and `input_frame`, which snaps
the decision tick up to a 0.25 s wall decision quantum. One digest across all four arms at
rtf 100, across load at rtf 1, and across load at 400 members; logged ticks are quantum
multiples. **Price**: input lag 0.05–0.15 s wall measured (bound: the 0.25 s quantum);
per-frame cost one integer add. **Honest limit, deterministic**: a press within ~one frame
period of a quantum boundary can land either side across frame rates (press at 0.26 s: 30 Hz
logs 5,075,636, 144 Hz logs 10,151,272 — two digests); sub-quantum intent is declared
indistinguishable (a 0.26 s press at 144 Hz is the same decision as one at 0.50 s). Residues:
the quantum is rtf-dependent (an rtf change mid-flight re-anchors the grid — the recorder must
freeze rtf per flight or log its changes), and a decision snapping past the cut never lands.

## Refuted

- "The hole is a bounded offset" — refuted: ×7.5–7.8 per 3× flight time to 18 AU, contacts
  6 vs 54 (20261013-1249).
- "Quantizing the presented tick fixes it" — refuted by 20261012-2257-scout-64e4 (adjacent
  pacings straddle any fine grid: raw ticks 19,912,096/20,250,432 either side of 19×2²⁰; 40c0
  proposed the load-independent timeline instead); the tick must come from a load-independent
  timeline (`sched`), then a quantum coarser than the frame-cadence sampling spread.

## Open directions

1. **Adopt the port** (20261013-1249's patch): 30 lines in `universe.rs` + 4 in the loop +
   the `decision_tick` test; the universe suite passes on the patched tree. The flight
   recorder must not merge before this does (its logs and its `--replay-all` gate inherit the
   hole otherwise).
2. **Delete the straddle**: snap the quantum to the input event's own wall timestamp (it
   travels with the input; the frame's sampling spread never enters) instead of the frame's
   `sched`. That would make every press identical across frame rates, at the cost of trusting
   the client clock to quantum resolution.
3. **The recorder's rtf rule**: freeze rtf per flight or log rtf changes as decisions
   (the quantum is rtf-dependent).

## Contradictions

- None open. 20261008-0743's grade is "missing" (ungraded run), not disputed; its fix is now
  independently reproduced on a tree five days of merges later.

## Runs

- 20261008-0615-taleb-40c0 (gold, per docs/HISTORY.md): the presented-tick log breaks
  schedule-independence (four digests per seed, encounters 68–102); the only demonstrated
  digest-breaking channel.
- 20261008-0743-second-20261008-0615-taleb-40c0-a342 (ungraded): the `sched` + decision-quantum
  fix, one digest across rates and load; never merged.
- 20261013-1249-taleb-a004 (this run): the hole compounds (18 AU, contacts 6 vs 54); the fix
  ported, wired and held on the current tree; the straddle reproduced (a342's record here
  shows only "one digest across rates and load" — the straddle is this run's measurement).
