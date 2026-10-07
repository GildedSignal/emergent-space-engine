# Predictions (written before the decisive experiment)

The measured ground so far (bench, rtf 100, paced, 30 s, seed 1, threads 1, members 48, Linux x86):
frame p50 4.37 ms = view_gather 3.45 ms (69.4% share) + engine 0.24 ms p50 (17.5% share; p99 5.24 ms — the 5 ms budget bites, 45 overflow frames) + json 0.43 + wire 0.19.

The decisive experiment decomposes the gather (the frame's largest claim) on the same scenario:
`lab/results/20261007-0528-constraint-6094/gatherbench/` — a standalone bin that replays the same
frame loop (`frame_to`, 5 ms engine budget, rtf 100) and instruments `gather_cached`.

## Held-out predictions (not tuned on)

1. **Readout dominance.** The bodies' light-cone crossings (Newton on `state_rate`) take > 60% of the
   gather's time at members = 48; a readout costs 20–40 µs, and the cache holds readouts to ≈ 1 per
   body per frame (the code's claim, never measured on the plane).
2. **Fleet-path slope.** The fleet members' extrapolated path costs 5–15 µs per member per frame,
   linear in members (no Newton there), so at members = 400 the gather roughly doubles.
3. **The view's surprise rate is near zero.** With perceptible quanta fixed in advance — direction
   > 2×10⁻³ rad (≈1 px at 1080p), any colour channel > 1/255, luminosity > 1% relative, angular
   radius > 2×10⁻³ rad — fewer than 5% of `seen` entries change perceptibly between consecutive
   frames at rtf 100. The gather re-derives > 95% unchanged information every frame.
4. **Engine demand vs gather.** Unpaced with the engine budget lifted to 1000 ms, the engine's median
   per-frame demand stays below the gather's median (the engine is budgeted and mostly idle; the
   gather is unbudgeted and always full price).

## What would kill the claim ("the view gather is the frame's constraint")

- Prediction 4 inverted: the engine's median demand exceeds the gather's → the engine is the
  constraint and the board's kick focus is right at plane level too.
- Prediction 3 inverted: most entries change perceptibly per frame → per-frame recompute is honest
  work; the constraint is then the readout's cost itself, not the recompute.
- The gather's share falling below the engine's on the tail frames only (p99), with the median
  gather < 1 ms → smoothness is an engine-budget problem, not a view problem.
