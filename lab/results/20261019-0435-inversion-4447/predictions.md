# Predictions (written before any flight, including calibration)

## The question

Does the burning player's resident memory on the shipped ladder **saturate or ratchet** in play
time? The record is in direct tension and nobody has flown a burn past 45.5k game-s:

- d839's checker (3×10⁴, burn, 45.5k gs): RSS 150→571 MB over 15k–40.5k gs (~13–16 MB/1k gs),
  then "flat" over the last 5k gs; held 38→193. Read as: "a play-time ratchet in the MINT
  channel".
- dcf1 (3×10⁵, burn, ~1.6k gs): VmHWM slope 0.026 MB/game-s, K-flat; "8 GB ~300,000 game-s out".
- b8e2/2403: the held-scan queue is a single server; growth is linear while oversubscribed;
  SCAN_BACKLOG 2048 bounds the held *count*.

The inversion: if the ratchet is real, the frozen one-hour/4-GiB play budget (HANDOFF: "the
approved plan's budgets (4 GiB, 30 FPS at 1080p, one hour, 20 GiB) are open, not dropped") is
breached by a plain held burn; if it saturates, dcf1's "300,000 game-s out" is dead as a ruin
claim. Either result moves the record.

## Arms (all: seed 1, rtf 100, engine budget 12 ms, K = 10⁴, quiet box, my patched nladder —
Linux /proc footprint + env-gated LADDER_PROBE / LADDER_CAP_S / LADDER_RSS_MB, off = shipped loop)

- A1 (decisive): burn, wall cap 420 s, RSS guard 1,600 MB — target ≥ 100k game-s (2.2× past
  d839's flattening point).
- A2 (negative control): coast, same binary, same length. Must stay flat; if it grows, VOID.

## Pre-registered predictions

- **P1 (the decisive axis):** d839's "then flat" is flight-end truncation, not saturation —
  the growth resumes or persists past 45.5k gs. Predict: slope over the final 40% of the flight
  ≥ 2 MB per 1k game-s. Falsified if final-40% slope < 0.5 MB/1k gs AND max RSS within 5% of
  its value at 60k gs (a true plateau).
- **P2 (mechanism):** the growth rides held_scans (net accumulation > 0 in the growth phases,
  RSS per held of constant order 0.1–3 MB), not a per-body term: at K = 10⁴ the per-body law
  (2402 b_per_body ≈ 2.3 kB) would add ≤ 0.02 MB/1k gs at the belt's measured event rates —
  two orders below the d839 slope.
- **P3 (control):** coast stays within ±2 MB over ≥ 60k game-s. If it grows, the instrument or
  the box is broken: VOID, no claim.
- **P4 (the frame channel):** over-budget frames do not decrease as the flight ages (the queue
  eats the drain margin): predict the last 30% of frames has ≥ as many over-budget frames per
  1k gs as the 5k–15k gs window.
- **P5 (held-out, the scene's own horizon):** if the player leaves the belt's neighbourhood on
  the burn (near set empties), mints stop and the growth flattens for that reason — I predict
  this does NOT happen before 100k gs at K = 10⁴ (the belt spans 2–3 AU and the scan's window
  keeps registering), so the flattening-vs-ratchet verdict at 100k gs is a queue verdict, not a
  scene-exhaustion artifact. If held → 0 with the player far out, the verdict is "scene-bounded"
  and I report it as such.

## Kill criteria (frozen before the run)

- **Ratchet (ruin):** final-40% slope ≥ 2 MB/1k game-s ⇒ 4 GiB breached at
  (4096 − RSS@60k)/slope game-s; report as wall-seconds at rtf 100 and against the one-hour
  play budget.
- **Saturated:** final-40% slope < 0.5 MB/1k gs and plateau within 5% ⇒ dcf1's extrapolation is
  dead; report the ceiling and the mechanism (held plateau vs the 2048 latch vs drain
  equilibrium).
- **Ambiguous band (0.5–2 MB/1k gs):** decaying staircase; report both bounds, no strong claim.
- The control (P3) failing voids everything.
