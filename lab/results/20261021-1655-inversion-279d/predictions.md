# Predictions (written before the decisive matrix ran; smoke run's digest known: 8e1882ff…)

Scene: `plane_extra` N=10⁴ (belt), seed 1, coast (no inputs — one trivial log), rtf 6000, cut at 20 s
game time (24,363,053,610 ticks), digest after `settle(cut)`. This is c8d5's drift point ("digest is
wall-coupled at rtf 6000", 20261020-0143, never diagnosed).

The contract under test (universe.rs `frame_to` doc + bench digest_note): *same seed, same log, same
cut ⇒ one digest, paced or not, on any budget.*

Cases (not tuned on — the arms are the test):

- **P1 (contract holds globally):** every clean arm (unlimited, events-25, unpaced 12 ms, unpaced
  0.5 ms, paced 12 ms; ×2 reps) prints digest `8e1882ff…` (the smoke run's). Then c8d5's drift was an
  artifact of their patched harness (keep probe / gather cadence), not shipped code, and the hole is
  closed on main at this scene too.
- **P2 (wall leaks through the budget):** the budgeted arms drift run-to-run at the same cut (two reps
  of one arm differ), while `unlimited` and `events-25` are stable. Mechanism guess if so: something
  inside `advance` mutates canonical state as a function of where the wall stopped the frame (fleet
  battle caps from queue order, held scans, prune cadence) rather than only deferring work.
- **P3 (event granularity leaks):** `unlimited` ≠ `events-25` at the same cut (both stable per-arm).
  Then the queue's order is not "only a schedule": pull-driven resolution has a tie the order decides.
- **P4 (load leaks):** under 6-spinner CPU load the paced/unpaced 12 ms arms differ from their clean
  reps (wall noise alone moves the canon). Prediction if P2 holds: loaded arms differ more often;
  if P1 holds, loaded arms still print `8e1882ff…` and the contract survives noise.
- **P5 (counters localise):** whichever arms disagree, `kicks`/`encounters`/`contacts` in the same
  line differ too if the divergence is in event *counts* (battle caps / scans); if counters are equal
  but digests differ, the divergence is inside per-body state (plan/carry/residual) — a subtler class.

Expected either way: `presented_at_end` differs across arms (benign, it is the presented path, not canon).

## Attribution round (written before reading burn/gather matrix output)

The clean matrix passed 10/10 (one digest `8e1882ff…`, presented-at-end spanning 0.34–24.36e9). The
two remaining candidate mechanisms for the lab's reported drift (c8d5 "wall-coupled at rtf 6000";
26fc-checker2 "dies on most wall schedules"):

- **P6 (input placement — the example-harness hole):** arm `input=presented` (the exact
  `nladder`/`keep_probe` line: `p.u.input(p.u.now, word)` at frame 60) forks the digest across reps
  under a biting 12 ms budget (the decision lands at a wall-dependent tick); arm `input=scheduled`
  (one canonical tick, the shipped `xtask universe --bench` pattern) gives one digest across reps.
  Prediction: P6 holds — 3 reps of `presented` give ≥2 distinct digests; 3 reps of `scheduled` give 1.
- **P7 (the instrument, not the engine):** every run prints `digest_presented` (c8d5's instrument:
  digest where the wall left the flight) beside `digest` (at the canonical cut, after settle).
  Prediction: `digest_presented` differs across reps/arms even when `digest` is identical — the
  reported "wall-coupled digest" is the digesting of an open-ended flight, not a schedule leak in
  resolution.
- **P8 (observation):** gather every 60 frames in the loop (`gather=60`, the game's cadence) changes
  no canonical bit: same digest `8e1882ff…`-family (burn arms will differ from coast's, coast+gather
  must equal coast's `8e1882ff…` if the gather is truly read-only).
- **P9 (noise stress):** paced 12 ms arms under 6-spinner CPU load still give one digest per
  (input=scheduled) arm; loaded `input=presented` forks more than unloaded.
