# Dossier — the locals' storm: grid lock, not begin lock

## Claim

The ladder locals' standing storm (the frame's binding N-independent term, 334-335 events/frame
pre-wave at every N) is **the shared block-step grid, not the shared clock begin**: the
begin-stagger the page conjectured as "the same one-step first-kick spread, one law, one lever"
is refuted by the letter (max 335 unchanged, same storm frames), and the law's own form — a
per-body dyadic translate of each local's block-step grid — flattens the storm 2.0-2.4x at both
seeds (max 335 -> 141 at seed 1, 359 -> 177 held-out seed 7), N-independent from 600 to 10^5,
worst frame 12.9 -> 6.7 ms, with the OFF arm bit-identical to pristine main.

## Bottleneck

Board item 1 (bodies in the flyable engine, the furthest gap): after the wave cure
(7da3/917c), the frame's binding N-scaling term is the locals class (nladder open direction 1;
917c's checker correction: the 12-ms letter extrapolates to ~6x10^5, locals-driven). This run
kills the conjectured free cure and prices the real one. Gain: ~2x on the frame's worst term
(the storm's 335 events x ~29.3 us/event M1 = 9.8 ms of the 12-ms letter, at every N); it
deletes nothing, but moves the locals-driven letter break out by the same factor. It composes
with ed3a's belt stagger (disjoint populations: doll-0 ext-clock vs doll!=0 block steps).

## Evidence

All on this Linux box, `crates/universe/examples/nladder` (patched to build on Linux: the
macOS `proc_pid_rusage` footprint call is cfg'd, with a /proc fallback — a print-only path),
budget-free (`budget_ms` 1e6), rtf 1000, coast, 12 s wall = 660 measured frames = 11,000 game-s.
Numbers are the deterministic event columns (counts identical across repeats; ms are this
box's, orders of magnitude only).

| arm | max ev/frame | p99 | p50 | worst ms | kicks | events |
|---|---|---|---|---|---|---|
| OFF, N=600 | **335** | 229 | 28 | 12.9 | 17,209 | 35,660 |
| OFF, N=1e4 | **335** | 229 | 28 | 11.7 | 17,209 | 35,660 |
| OFF, N=1e5 | **335** | 229 | 28 | 11.7 | 17,209 | 35,660 |
| OFF, N=0 (no locals) | 60 | 43 | 6 | 4.5 | — | — |
| BEGIN, N=600 | **335** | 229 | 28 | 13.1 | 17,209 | 35,686 |
| GRID, N=600 | **141** | 131 | 52 | 6.7 | 17,257 | 37,944 |
| GRID, N=1e4 | **141** | 129 | 52 | 4.7 | 17,258 | 37,938 |
| GRID, N=1e5 | **141** | 129 | 52 | 5.1 | 17,260 | 37,951 |
| OFF, N=600, seed 7 (held out) | **359** | 244 | 51 | 13.7 | 16,366 | 45,277 |
| GRID, N=600, seed 7 | **177** | 168 | 114 | 8.1 | 16,403 | 78,254 |

- The storm: OFF worst frames (79, 264), (317, **335**), (475, 258), (634, 334) — a standing
  train, period exactly 317 frames = 5,283 game-s, event counts **bit-identical at N = 600,
  1e4, 1e5** (pure locals: 300 of `ladder_locals` = (extra/2).min(300), plus ~35 others).
- BEGIN (the conjecture's letter: first plan begins hash-spread, grid untouched): storm
  frames and counts unchanged (317: 335; 634: 334). The begin spread moved only first-fire
  residues (frame 79: 264 -> 290) and added 26 stub events: the population re-locks onto the
  shared dyadic grid within one step, exactly as `step::aligned`'s block-step rule implies
  ("every interval of a power of two starts on a multiple of its own length ... every pair
  shares boundaries").
- GRID (each doll!=0 ship's grid translated by o = hash(id) mod step, dyadic, deterministic,
  re-phased on rebind): the standing train is gone — GRID worst frames are 74-92 (the genesis
  transient: first kicks spread over ~20 frames), not 317/634; max 141 flat in N.
- OFF gate-neutrality: with `ES_STAGGER_LOC` unset the deterministic columns reproduce the
  pre-patch binary's exactly (335/229/28, kicks 17,209, storm frames 79/317/475/555/634) at
  every N flown, and the patch's only other edit is the Linux footprint print.

Reproduce: `lab/results/20261016-0504-components-4534/regen.sh` (build + all arms above,
< 2 min after the build; the whole regen fits in 15 min).

## Predictions (predictions.md, written before the staggered arms)

- P0 (storm reproduced, N-independent, recurring) — held.
- P1 (BEGIN does not transplant; the grid re-locks; standing storm returns) — held, and it
  kills the page's open-direction-1 letter ("the same one-step first-kick spread ... one law,
  one lever").
- P2 (GRID flattens to <= ~120 max, >= 2.5x, kicks within ~2%) — **half-held, and the misses
  are named**: seed-1 max 141 (2.37x, under the 2.5x letter) and the held-out seed 7 lands at
  177 (above my own 150 kill bar) with the *event total* +6% (seed 1) / **+73% (seed 7)** —
  the phase shift changes more than phase: kick ticks move, tube states at kick move, and
  with them the boundary/exit/capture structure downstream (seed 7: slices 12,837 -> 45,751;
  boundaries and opens near-unchanged, so the growth is in the frame-loop's slice/event
  machinery, not kick cadence: kicks +0.2-0.3% everywhere). Unresolved here; the diagnosis is
  the next rung, and until it and the behaviour gates fly, this is a measured lever, not an
  adoption.
- P3 (OFF == pristine; ON arms differ, a schedule law change as with ed3a's) — held.

## What would make it wrong

The storm could be something other than block-step grid lock on a population with one
dominant step octave (the mechanism is read off `step::aligned` + `step_for`, and BEGIN's
null result + GRID's flattening are the two-sided control, but no per-body step histogram was
taken). The flattening could fail on burn arms (thrust steps cap `want` and re-plan
differently) and on the fleet's members (doll!=0, kind Member/Ship interactions unseparated
here). The seed-7 event inflation could be a genuine behaviour change (the adoption blocker,
same class as ed3a's direction 2: B13/B14-class legality gates under the shifted phases were
not flown — no rung here can fly them in one window). Cost of adopting: ~30 lines in
`step.rs`/`universe.rs`, env-gated, OFF bit-identical; the M1 re-measure and the gates are
the integrator's.

## Fit with PRINCIPLES

- "the right representation always just feels right it does the job like cutting butter in
  summer" / #19: the begin-stagger was a bandaid on the wrong lock; the grid translate is the
  one-lever form on the law's own grid.
- #12 (smoothness; "i care about the p95/99 results"): max/p99 are what moved (12.9 -> 6.7 ms
  worst, p99 events 229 -> 131), at +0.3% kick count.
- #15 local laws: the translate is per-body, constants-only at genesis, no central schedule.
- #20/#21: two seeds, one held out; rough first — the misses are reported, not tuned away.

## The lens

First principles on one component (the secondary dolls' kick schedule) found the floor
mis-named: the page priced the locals as "the same first-kick spread" (a begin problem) when
the shipped representation makes it a *grid* problem — the falsifier was 15 lines. What the
lens may have missed: the neighbours (the event totals moved at seed 7 — cost pushed into the
slice machinery), the burn and fleet arms, and the legality gates; a local optimum that
flattens frames can still change what the engine does between them.
