# Predictions — 20261008-0615-taleb-40c0 (written before the decisive matrix)

Question: does the shipped plane's digest at a canonical cut (40,000,000 ticks, the flight
scene with a fixed decision log) depend on the schedule path taken to reach it? Paths: one
unlimited `settle` (reference), 1-event budgets, 8-event budgets, wall-clock budgets,
starved frames (4 events/frame at 60 Hz rtf 100), rich frames (unlimited per frame),
frames with observation reads, checkpoint at T/2, and threads 1 vs 8. Seeds 11, 22, 33;
each case also run twice (same-path repeat determinism).

The claim under test (plane.md foundation 2 and 7, AGENTS.md Truth): "outcomes are
independent of schedule ... any budgeted order gives identical bits", "one digest ...
independent of schedule, budget, threads and observation".

Pre-registered predictions, with the seam each one risks:

- **P1 budget granularity** (direct = events1 = events8 = wall = ckpt, per seed): the law is
  per-body integer and the calendar has deterministic ties, so only the resolution *order*
  changes. HOLD expected (0.8). Risk: `advance`'s deferred/horizon bookkeeping losing or
  duplicating an item across a budget break (a dropped event is invisible in the digest's
  counts only if it never happened — the counters would differ too, so a counter mismatch
  at equal digests is impossible; a *state* difference is what I watch).
- **P2 frame presentation** (frame-starve = frame-rich = direct): `frame_to` advances `now`
  to the horizon (which lags under overflow), and `prune()` runs every 64 frames based on
  `now`. If the digest reads anything pruned, or a decision's `take_due` window shifts with
  the presented time, digests split. HOLD expected but weakest of the "careful design" set
  (0.65).
- **P3 threads** (direct thr=1 = direct thr=8): `resolve_wave` claims ships' items are pure
  functions of their own records. Risk: `encounters_for_player` folds into `enc_digest`
  in *find order*, and the digest ends with `enc_digest`; also stats ordering. (0.55 — I
  genuinely do not know.)
- **P4 observation** (frame-obs = frame-rich): `readout` is documented pure; the gather
  must never write. (0.85.)
- **P5 same-path repeats** (each case twice, identical): the only path at risk is `wall`
  (its split follows wall time), and the claim says even that must not move bits. (0.9.)

Kill criterion (frozen before the run): any two paths at the same (seed, cut) that disagree
on the digest falsifies the premise — a reachable silent-nondeterminism ruin in the
canonical history. If counters (events/kicks/encounters) differ while digests match, that is
still a schedule leak into the digest's inputs and counts as a fail for the counters'
independence claim but not for canonical outcomes; I will report both separately.

What would make a "all equal" result uninteresting: I have only x86, one machine, no GUI
loop, no GPU dense order, no cross-hardware run. The result would close the *schedule*
seams named in the claim on this machine only, and the dossier says so.
