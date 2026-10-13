# Dossier — 20261013-1249-taleb-a004

**Claim.** The engine's one live ruin channel — the interactive loop logging the player's key
changes at the frame's *presented* tick (`xtask/src/universe/session.rs`, so machine load and
frame rate rewrite canonical history) — **compounds**: on identical inputs, a loaded machine's
history separates from an idle one's by 0.31 AU at 415 game-s, ×7.5 per 3× flight time, to
18 AU and contacts 6 vs 54 at 3,734 game-s; and the a342 decision-quantum fix, ported here to
the current tree and wired into the shipped loop, **closes it** (one digest across 30/60/144 Hz
and load, at rtf 100 and 1, at 48 and 400 members) at a measured input lag of 0.05–0.15 s wall
(bound: the 0.25 s quantum), with its one declared ambiguity (a press straddling a quantum
boundary) reproduced deterministically.

**Bottleneck.** Not speed: Truth itself ("Canonical outcomes are exact and independent of cache,
partition, observation, schedule and hardware"). This is frame-cost's named "one live contract
hole", now measured as compounding rather than a bounded offset, and now blocking a job that is
in flight: the flight recorder (HANDOFF, `wt/recorder`) will freeze these load-dependent input
logs into `artifacts/flights/*.json` and make `--replay-all` a pre-merge gate — a gate whose
"new loss or refusal" flag would then be a function of the machine's load the day it ran
(measured here: contacts 0 vs 4 and 6 vs 54, encounters ±33%, on identical player inputs).
The gain is deletion of an entire failure class, not a speedup; per-frame cost of the fix is
one integer add (arm wall times identical within noise: 162–168 ms rich, 162–166 ms starved).

**Evidence** (all from `regen.sh`, ~15 s of runs, deterministic `Budget::events(2)` load arms;
full output in `work/matrix.txt`, verdicts in `work/summary.txt`):

- **The hole, post-merge tree, through the shipped loop's exact two lines** (probe
  `crates/universe/examples/ruin_probe.rs`, seed 11, cut 84M ticks = 415 game-s, rtf 100,
  48 members, presses at wall 0.5/1.7/3.2/4.1 s): four arms → **four digests**
  (`3d59ae6d…` 60 Hz rich, `c1a4368f…` 60 Hz starved, `deb0bafc…` 30 Hz, `6f144c13…` 144 Hz).
  The starved arm logs the first press at tick 5,767,303 instead of 10,151,250: the presented
  time had lagged 21.6 game-s in half a wall second of chronic starvation. Encounters 43 vs 29.
- **Compounding** (raw 60 Hz rich vs starved, same inputs, player separation at the cut):
  84M ticks: 3.16e7 doll units = **0.31 AU**; 252M: 2.36e8 = 2.3 AU (×7.5); 756M: 1.83e9 =
  **18 AU** (×7.8) — steady ×7.5–7.8 per 3× time, no saturation to 18 AU (beyond the system),
  encounters cross over (43>29 → 121<133), **contacts 6 vs 54** at the top. The cause is a
  constant 21.6-game-s decision shift; the effect grows without bound. "Divergence is not a
  joke and it compounds" — here it is, measured.
- **The fix holds on the current tree** (a342's `sched` timeline + `input_frame` on a 0.25 s
  wall decision quantum, ported in this run's patch; five days of merges including the clock
  merge since a342 built it): all four arms (60 rich/starved, 30, 144) → **one digest**
  `711b3acf…`, identical ticks `10151272,35529452,65983268`; the load-only pair at rtf 1 →
  one digest `c67a78c3…`; at 400 members the load pair → one digest `327a3ea9…` (raw there:
  two digests, encounters 49 vs 30, contacts 0 vs 4).
- **No regression**: the decision-tick tests pass and the universe suite passes on the patched
  tree (69 passed, 0 failed, 2 ignored clock flights, `cargo test --release -p emergent-universe`,
  run twice here); `xtask` (the wired session and kick_bench) builds clean.
- **The honest limit, deterministic**: a press at wall 0.26 s (10 ms past a quantum boundary):
  30 Hz logs tick 5,075,636, 144 Hz logs 10,151,272 → two digests (`94f32d9a…` vs `711b3acf…`).
  At 144 Hz this press is *the same decision* as a press at 0.50 s: sub-quantum intent is
  declared indistinguishable.
- **No regression**: the decision-tick tests pass and the universe suite passes on the patched
  tree (58/58, `cargo test --release -p emergent-universe`, run once here); `xtask` (the wired
  session and kick_bench) builds clean.

Commands: `bash lab/results/20261013-1249-taleb-a004/regen.sh` (everything above);
single arm: `cargo run --release -p emergent-universe --example ruin_probe -- raw 11 60 1 84000000 100 48 std`.

**Predictions.** `predictions.md`, all six HELD (`work/summary.txt`): the hole live with ≥3
distinct digests (4), encounters ±5% (−33%), superlinear growth >3× per 3× time (7.5, 7.8),
one digest under the fix at both rtfs, lag within one quantum, the 0.26 s straddle breaking
30-vs-144, 400 members behaving like 48. Nothing I pre-registered failed.

**What would make it wrong.** The straddle is structural to any log derived from when frames
sample a press: two frame rates disagree on a press that lands within ~one frame period of a
quantum boundary (here ~13% of presses at 30 Hz worst case). If the recorder needs
every-press identity across frame rates, snap the quantum to the input event's *own* wall
timestamp (the browser event time travels with the input; the frame's sampling spread then
never enters) — that is the named follow-up, not a defect in this port. Second residue: the
quantum is rtf-dependent, so an rtf change mid-flight (the page allows it) re-anchors the grid;
the recorder must freeze rtf per flight or log rtf changes as decisions. Third, disclosed: a
decision whose snapped tick falls beyond the cut never lands (the 4th press at the 84M cut).

**Cost of adopting.** The patch: +30 lines in `universe.rs` (the `sched` field, the quantum,
`input_frame`), 2 lines in `session.rs`, 2 in `kick_bench.rs`, one test file; no per-frame
measurable cost; input latency bounded by 0.25 s wall (measured ≤ 0.15 s). PRINCIPLES: Truth
("independent of … schedule and hardware") — restored; #13 "Errors never compound … divergence
is not a joke and it compounds" — the hole measured doing exactly that, and the fix deletes the
compounding channel; #5 "the player is the only wildcard" — the log returns to being the
player's intent, not the machine's mood.

**The lens.** Taleb: ruin before optimization — this closed the one reachable ruin state
(silent nondeterminism across hardware) before any nanosecond was shaved; the barbell held
(exact integer spine untouched, cheap deterministic probes). What the lens may have missed:
it says nothing about how to build, and the fix's price (input latency, sub-quantum blindness)
is a playability judgment the integrator owns, not a robustness fact; I measured the price but
did not fly it.
