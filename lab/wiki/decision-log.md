topic: decision-log
status: open
closed-by:
valid-while:
updated: 20261013-2130-inversion-dfd0

# The player's decision log: canonical ticks for a wall-world press

Split from frame-cost's "one live contract hole" (20261013-1249): the question deserves its own
page because it is Truth, not cost — and because the flight recorder (in flight) will freeze
whatever the loop logs today.

## Current best

**The recorder merged ahead of the fix and froze the hole: one player session, flown twice on
one machine, records different canonical flights, and the new `--replay-all` merge gate blesses
every one of them (20261013-2130-inversion-dfd0).** The flight recorder landed 13 October
(73c98a46, "decisions are logged at the tick they take effect") with the a342/a004 port still
absent — `session.rs::step` passes the frame's presented tick (`u.now`) to `input`, so the
logged tick is "what the budget left behind", the exact hole below. Measured on shipped code
(one test added to the recorder's own frozen `flight_tests.rs`, same seed/script/cadence, only
the engine's wall budget differs): the six decisions' ticks fork by 8.2M ticks (≈ 67 game-s) at
400 members, 19.7M (≈ 161 game-s) at 150, and 13.4M (≈ 110 game-s) at **8 members with the
frozen test's own budgets (0.5 vs 8 ms)** — the recorder's own frozen test flies this script at
those budgets and checks only that each file replays to itself, so it has been certifying
contradictory flights since it was frozen (its control is one line short of the Truth
criterion). No starvation knob needed: the *same* arm re-flown gives another digest
(`dd39afb7…` then `4ed7ae25…`, m400 rich, nothing changed but box load), and under a biting
budget two presses 40 frames apart can log at the *same* tick (2,121,741 twice, starved m150,
first execution — sub-frame intent silently aliased). All six files: `replay()` `same=true`,
4-thread replay exact, and `--replay-all` exits 0 over the six contradictory truths ("6 same, 0
regressions"). The gate is a fine law-change detector (per-file exactness is the law's
property); what it cannot see is that the recorded canon itself is machine noise — the three
committed flights in `artifacts/flights/` carry it, and every future re-recorded suite can
coin-flip "new loss" regressions on machine load (a004's warning, now structural). The fork
tracks the *differential* delivered engine time between runs, so it is widest when one run
keeps up and the other does not (the 150-member fork exceeds the 400-member one: lighter scenes
widen it under equal starvation; the pre-registered "shrinks at 150 members" was wrong, reported
as missed).

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

- "The recorder's flights are canonical regression truth": one session, six flights, all
  blessed — the recorded canon is a function of machine load at record time
  (20261013-2130-inversion-dfd0).
- "The hole is a bounded offset" — refuted: ×7.5–7.8 per 3× flight time to 18 AU, contacts
  6 vs 54 (20261013-1249).
- "Quantizing the presented tick fixes it" — refuted by 20261012-2257-scout-64e4 (adjacent
  pacings straddle any fine grid: raw ticks 19,912,096/20,250,432 either side of 19×2²⁰; 40c0
  proposed the load-independent timeline instead); the tick must come from a load-independent
  timeline (`sched`), then a quantum coarser than the frame-cadence sampling spread.

## Open directions

1. **Adopt the port, then refresh the recorded corpus** (20261013-1249's patch: 30 lines in
   `universe.rs` + 4 in the loop + the `decision_tick` test; the universe suite passes on the
   patched tree). The recorder merged before it (73c98a46), so the order the page demanded was
   violated: after landing, re-record or transform `artifacts/flights/` (they replay exactly
   either way; the port fixes future recordings). Add the one-line Truth criterion to
   `flight_tests.rs`: the same session at two budgets yields one flight (this run's probe).
2. **Delete the straddle**: snap the quantum to the input event's own wall timestamp (it
   travels with the input; the frame's sampling spread never enters) instead of the frame's
   `sched`. That would make every press identical across frame rates, at the cost of trusting
   the client clock to quantum resolution.
3. **The recorder's rtf rule**: freeze rtf per flight or log rtf changes as decisions
   (the quantum is rtf-dependent; `Recorder::current` stores the current rtf, replay uses the
   last — read in code by 20261013-2130, not flown).

## Contradictions

- None open. 20261008-0743's grade is "missing" (ungraded run), not disputed; its fix is now
  independently reproduced on a tree five days of merges later. The inversion run's "fork grows
  at 150 members" vs its own pre-registered "shrinks" is resolved in the run's dossier: the
  fork is differential engine time, widest when one run keeps up — kept as a domain note.

## Runs
- 20261008-0615-taleb-40c0 (gold, per docs/HISTORY.md): the presented-tick log breaks
- 20261008-0743-second-20261008-0615-taleb-40c0-a342 (ungraded): the `sched` + decision-quantum
- 20261013-1249-taleb-a004 (this run): the hole compounds (18 AU, contacts 6 vs 54); the fix
- 20261013-2130-inversion-dfd0 (pending grade): the recorder merged ahead of the fix; one
