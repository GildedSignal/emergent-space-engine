# Predictions — 20261017-0839-second-20261017-0739-taleb-9b46-5d87

Written before the decisive frames matrix. Tuning so far (allowed): one 20 s smoke run,
864 frames seed 1 rate 400 ahead 0.25 (survived, rb = 5), and the batch positive control
(864 chunk-100, crashed at the finality assert, 1/1 — the author's 2/2 and the checker's
2/2 reproduced in spirit).

Mechanism I derived from shipped code (drives every prediction): `rollback` rebuilds the
restored region via `make_region(world, …, Some(fin))`, so it **inherits its lineage's
`fin_parts`, whose ticks can sit above the restore point**; `fin_hi` is the max of those
ticks. Any *subsequent* clash whose rollback start lands below that inherited `fin_hi`
trips `assert!(r.fin_hi <= s0)` (shipped `alloc.rs:1451`). So the crash is a
second-generation conflict on an inflated lineage; it is cadence-sensitive only through
phase, not through mode. Frames mode publishes per commit (same `publish()` path the batch
harness uses at chunk ends), so nothing in the mode forbids it.

- **P1 (the asked question).** The finality assert can fire in frames mode: at least one
  arm of the grid (864 × 3 seeds × 3 (rate, ahead) cells; 14k and 28k wave; quiet 14k)
  crashes with "would revise its published tick". Kill criterion for the "live-path crash"
  reading: if no arm crashes anywhere in the grid, the hazard is batch-driver-only.
- **P2 (where it fires first).** Crash likelihood follows the conflict rate, not N: the
  864 grid (rb ≈ 5 per 8k chronons, most conflicts early in the wave crossing) crashes in
  at most 1 of its 9 cells; the 28k wave (px 29–47k, rb 6–9, thousands of merges) is the
  most likely arm; quiet 14k (rare drift conflicts) the least likely of the wave family.
- **P3 (cadence direction).** A smaller compute-ahead `ahead` (tighter coupling of the cap
  to the present) does not systematically raise the crash rate: the assert needs an
  inflated lineage plus a second clash, and both exist at every cadence. (If the rate does
  trend with `ahead`, my mechanism reading is wrong in detail.)
- **P4 (survivors behave).** Every surviving frames run reports `hard_viol = 0` and ends in
  the same end-state class as batch on that scene (864 → 1 region), and its present-advance
  curve clamps at the light-cone bound under load (accel_drops > 0 on the big scenes).
- **P5 (held-out law).** The same scene under `Law::Relativistic` (light-cone finality on:
  `fin_hi` may exceed the global frontier, so inflated lineages are easier to make) crashes
  in frames mode at 14k more readily than the Newtonian arm — my mechanism says the extra
  finality lead widens the window between published tick and replay point.

Scorecard to be filled after the matrix.

## Scorecard (after the matrix)

- **P1: killed in the pre-registered no-direction.** 18/18 frames arms survived, 0 asserts
  (grid × seeds × sizes × both laws; the quiet arm swept frontier 3,072 in the regen
  window — the whole horizon and beyond; relativistic to 8,096). The kill criterion I
  wrote ("no arm crashes anywhere → batch-driver-only") fired. The *explaining* mechanism
  (window-grid alignment) was derived after the first frames results and probe-confirmed
  after: no on-grid chunk (96/112/128 at 864, 512 at 14k) ever crashed, interior ones
  crashed 7/11 on this box (100-s1 4/4, 104 2/2, 108 1/3, 100-s2 0/2).
- **P2: wrong in every part** — no frames crash anywhere; conflict rate (rb, px) does not
  predict it; the 864 grid stayed alive at rb ≤ 6 per arm (rb 10 in a longer first-window
  run).
- **P3: held vacuously** (nothing crashed, so no cadence ranking exists). The end states,
  though, are cadence-drawn in frames too (1 to 798 regions at fixed N across (rate,
  ahead)) — the checker's cadence-knob finding extends into the live path.
- **P4: held on hard_viol = 0 (18/18) and accel_drops > 0 under load; half-failed on the
  end-state class** (not always 1 region; cadence decides).
- **P5: wrong** — relativistic frames survived everywhere (to frontier 8,096 in the regen
  window; 24,096 in a longer first-window run) with light-cone finality publishing 128
  chronons beyond the frontier — the extra lead does not open the window, because the
  frames grid (not the frontier) is the guard.

The failures are again the finding: my mechanism prior (rollback-inherited fin_hi +
re-clash, cadence-agnostic) was the wrong channel; the shipped channel is the forced
interior publish of chunked `run_to`, which frames mode structurally cannot produce.
