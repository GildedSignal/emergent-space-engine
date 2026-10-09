# Predictions (written before any bench run; only code read, no numbers seen)

Question: does anything in the plane (canonical engine work per game-second, view-gather cost,
frame-time tails, memory) **grow with game-time horizon**? Tests stop at ≤ 60 s wall; the player
plays an hour. The horizon is reachable inside the ≤ 60 s rule by raising `--rtf` at fixed wall
seconds (the bench's own digest machinery guarantees the cut is canonical whatever the pacing).

Ladders (all `xtask universe --bench`, seed 1 unless said, default members 48, budget 5 ms):
- **A (session length at the flying rate):** rtf 100, unpaced, seconds 5 → 55 (game horizon
  500 → 5,500 s ≈ the player's hour and a half), plus one paced 55 s run (real 60 Hz wall).
- **B (horizon at fixed wall):** unpaced, seconds 30, rtf 1 → 1e5 (game horizon 30 s → 3e6 s ≈ 35 days).
- **C (adversarial):** rtf 1000, seconds 55, members 400 (the fullest frame).
- **Controls:** exact rerun of A/seconds=30 → identical digest (negative); seed 2 → different
  digest (positive). Both sides, per the rung rules.

## Predictions, held-out (I have not run the bench at all)

- **P1 — engine cost per game-second is flat in horizon** (within ~1.5× from rtf 1 to 1e4 at
  fixed seconds): the law is compiled drift plus sparse events; nothing walks a history per tick.
- **P2 — the view gather is the fragile end.** Gather p99 per frame grows with session depth
  (light-cone lookback, Newton guesses, rebind chains): I predict visible growth, more than the
  engine's, but bounded (< 5×) from horizon 500 → 5,500 game-s. If it grows > 5× or superlinearly,
  the readout is the growing liability (the b-readout-cost premise, quantified).
- **P3 — frame-time tails stay bounded in ladder A** (worst/p50 < 20×) because the 5 ms engine
  budget clamps canonical work; but **overflow_frames > 0** appears in ladder B at rtf ≥ 1e4
  (backlog bursts the frame cannot absorb).
- **P4 — the cut settle is the unbounded synchronous claim.** Settle wall (process wall minus the
  frames' wall) grows with the deferred backlog and dominates process time at high rtf. I predict
  it crosses the frames' own wall somewhere around rtf 1e3–1e4. Quantifying where is the deliverable:
  the settle is §7's "nothing takes an unbounded synchronous claim on the frame" — at the cut.
- **P5 — memory is flat.** RSS (first/max/last within each run, and across rungs) and
  `bytes_per_body` within ±20%; no history accumulation leaks into RAM at these horizons.
  Monotone RSS growth with game time would be the swap-death path (ruin), not a tuning matter.
- **P6 — the scripted player survives the hour** (player_alive at 5,500 game-s, no lost bodies).
  If it dies at depth, the scripted flight has a horizon cliff: a different fragility, to report.

## Kill criteria (decided now)

- "Nothing grows with horizon" is **killed** if engine-per-game-second, gather p99, or RSS grows
  monotonically by > 2× per 10× horizon beyond the first decade: I then name the component and
  the game-time at which it breaches the 16.7 ms frame or the 8 GB budget (extrapolated, marked as such).
- "The plane survives player-scale horizons" is **supported** if P1, P3(bounded), P5 hold and the
  controls behave; the settle's growth is then the one named exception to bound.
- Numbers are Linux/x86 shared-runner: orders of magnitude only, per lab rules.
