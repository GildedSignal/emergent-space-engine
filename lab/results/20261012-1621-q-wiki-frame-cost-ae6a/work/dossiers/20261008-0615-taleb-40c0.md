# Dossier — run 20261008-0615-taleb-40c0 (lens: Taleb)

## Claim

The plane's engine core keeps its truth claim — one digest per canonical cut, bit-identical
across nine adversarial schedule paths (event-starved budgets, wall-clock budgets, frame
presentation with pruning, checkpointing, observation reads, 8 threads), 3 seeds, repeats —
but the shipped interactive loop logs the player's key changes at the frame's *presented*
tick (`xtask/src/universe/session.rs:80`, `input(now, keys)`), so the same physical play
writes different canonical histories at different frame rates and under different load
(measured at one cut: encounters 68–102, contacts 0–14, kicks 6 474–6 481, four distinct
digests per seed): the one reachable wall→canon leak, silent, and its effects reach the
canonical encounter/contact history, not just the log bytes.

## Bottleneck

Not a compute lever: the survival-first item. AGENTS.md Truth line 1 ("Canonical outcomes
are exact and independent of cache, partition, observation, schedule and hardware") and
plane.md foundations 2 and 7; HANDOFF "Risks to attack first" names silent nondeterminism
as a ruin state and nothing in the queue or the 6 October–8 October run record audits it
(the recent runs cover encounters concentration, H_live, builds). Expected gain: closes the
first named ruin path for the core (measured, negative), and finds the leak where the wall
still enters the canon, with a one-line fix direction. What it deletes: any fear that the
event core's queue/budget/threads machinery leaks schedule into outcomes — at this scene
scale it does not.

## Evidence

Machine: Linux x86, 8 vCPU, load 0.4–1.0 during runs, 15 GB RAM (state.txt). Scene: the
plane's own flight scene (`scenario::plane`, `Order::Sparse`, 1 024 fleet members), cut at
40 M ticks (matrix) and 80 M ticks (play/control); a fixed decision log of three key
changes. Binary: `determinism.rs` (this folder; also `work/` holds raw output). Build:
`CARGO_TARGET_DIR=/tmp/x-target cargo build --release -p emergent-universe --bin determinism`.
Each run ≤ 5 s.

**1. The core is schedule-independent (matrix, `work/matrix.txt`, 54 runs).** Per seed,
ONE digest across: `direct` (unlimited settle) = `events1` (1-event budgets, ~12 k calls) =
`events8` = `wall` (0.2 ms budgets) = `ckpt` (settle T/2 then T) = `frame-starve`
(4 events/frame at 60 Hz rtf 100, chronic overflow) = `frame-rich` = `frame-obs`
(readout of every body every 32nd frame) = `direct-thr8` (8 threads, `resolve_wave`).
Repeats identical, including `wall` (whose split follows wall time — the claim says even
that must not move bits, and it does not). Only the presentation counters `events`/`slices`
differ (fleet slicing is per-frame work), never `kicks`/`encounters`/`contacts`/`decisions`.
Reproduce: `for rep in 1 2; do for seed in 11 22 33; do for case in direct events1 events8
wall frame-starve frame-rich frame-obs ckpt; do /tmp/x-target/release/determinism $case
$seed 1 1024 40000000; done; done; done` and the same with `direct $seed 8 …`.

**2. The interactive loop's decision tick is wall-derived and moves the canon
(`work/play.txt`).** Same physical key timeline (changes at wall 0.5 s, 1.7 s, 3.2 s),
one cut (80 M ticks):

| path | seed 11 digest | enc | contacts | seed 22 enc/ct | seed 33 enc/ct |
|---|---|---|---|---|---|
| play60 | 047817bb… | 100 | 4 | 97 / 9 | 80 / 0 |
| play30 | 53271800… | 102 | 6 | 101 / 13 | 82 / 0 |
| play144 | 7f84c5ac… | 100 | 4 | 97 / 9 | 78 / 0 |
| play60-starve (2 events/frame) | f7e17f7e… | 68 | 14 | 44 / 0 | 115 / 0 |

Every digest distinct; `play60-starve` is the ruin form: **same machine, same frame rate,
different load** — the lagging presented `now` moves the decision ticks and rewrites
encounters (100→68) and contacts (4→14). Nothing errors; the history is simply not
regenerable from the physical input timeline. Reproduce: `for seed in 11 22 33; do for case
in play60 play30 play144 play60-starve; do /tmp/x-target/release/determinism $case $seed 1
1024 80000000; done; done`.

**3. Control: the `input()` path itself is canonical (`work/` stdout above).** `input()`
taken at FIXED canonical ticks through the frame loop gives digests identical to `direct`
(scheduled) at the same cut, all 3 seeds (`49a1b20b…`/`264b1bee…`/`9fbcaa5f…`). So the
divergence in 2 is the wall-derived tick values alone — the mechanism, isolated.

Replay path is clean: `xtask/src/fly/server.rs` replays recorded `(tick, input)` logs with
a digest check; the leak is only in the live loop (`session.rs:80`) and the bench
(`kick_bench.rs:68`).

## Predictions

`predictions.md` was written before the matrix. All five pre-registered predictions HELD:
P1 budget granularity, P2 frames+prune, P3 threads, P4 observation, P5 repeats (P3 was the
one I genuinely did not know; `resolve_wave`'s key-ordered apply is why). The predicted
counter-vs-digest split appeared exactly as pre-registered (events/slices move, digests do
not). The play-path seam (section 2) was found *after* the matrix and was not
pre-registered; the control pair (section 3) was run to isolate it.

## What would make it wrong

The play probe runs at rtf 100, where one 16.7 ms frame is 1.67 game-seconds: at rtf 1 the
tick jitter shrinks to ±8 game-ms per decision and I did not measure whether a contact
still flips at that scale (the mechanism stands, the magnitude at real-time pace is
unmeasured). Only x86, one machine, one scene family, 3 seeds, `Order::Sparse`, no GPU
dense order, no real browser loop (the loop was emulated at exact frame cadence; a real
loop's jitter is worse, not better). If the wall-quantized decision tick is judged an
intended part of "the player is the wildcard" (session.rs documents the choice), then the
finding reduces to: the Truth section's letter holds only *given the log*, and the log
itself is machine-dependent — a documentation-level fix instead of a code fix.

## Cost of adoption, fit with PRINCIPLES

Fix direction (not built): derive the decision tick from the *scheduled* game time
(`frames_seen · dt · rtf / TICK_SECONDS`), quantized to a decision quantum (e.g. the
player's own step grid), and log that — two lines in `session.rs`/`kick_bench.rs`; the
regression test is this probe's `play60`/`play30` pair asserting equal digests. Fit:
"Canonical outcomes are exact and independent of … schedule and hardware" (violated at the
one seam, restored by the fix); #13 "errors never compound" — a flipped contact compounds
into the battle's history; #5 keeps the player the *only* wildcard (their intent stays,
the machine stops being a second one). PRINCIPLES line for the lens: "its risk of breaking
makes anything you do to improve it inconsequential unless you first reduce that risk."

## The lens (what Taleb made me miss)

The lens went ruin-hunting and found the ruin outside the engine core, in the glue the core
cannot protect against: a speed lens would have stopped at section 1 ("identical bits,
claim verified") and shipped the negative result. What it missed: no cross-hardware or M1
run (x86 only), no measurement at real-time pace, and it nearly missed that `events`/
`slices` counter drift is presentation work, not state — the digest-vs-counters split had
to be pre-registered to be read correctly.
