# lessons.md — library lens, run 20261007-0711-library-9ab7

Bottleneck 4 (smoothness/allocator) + plane.md's smoothness gate: does hitch risk
follow from bench percentiles or only from the event-stream tail? Quotes verbatim
from `data/highlights.tsv`. Probe: `probe_tail.py`, `probe_rtf.py`.

1. **Size the frame from the event-stream tail, not bench percentiles.**
   "When your sample is large, no single instance will significantly change the aggregate or the total." — The Black Swan.
   Matched-percentile streams (equal p50/p95/p99.9 in a 36k bench) have once-per-hour frames 28 : 55 : 327 (light : α=3 : α=1.5); the α=1.5 bench max varies 26× between benches; Gaussian moments run 27× low.
   Change: measure the tail exponent on kick/encounter event sizes; extrapolate budget and overflow headroom at 4.6e-6, not bench quantiles.
   Test: exponent on one bench trace vs the max of a 100× longer run.

2. **Idle is capacity: run the frame like a fire station.**
   "We are made to live like firemen, with downtime for lounging and meditating between calls." — Fooled by Randomness.
   Worst RTF dip 59 → 287 → 1680 frames as ρ 0.5 → 0.7 → 0.9 under α=1.5 (1 s → 28 s visible); thin-tailed stays ≤ 80 at ρ=0.9.
   Change: utilization ≤ ~0.7 of the quantum is a smoothness decision; the idle share funds the slack skin (compute ahead) — principles 17+12, one budget.
   Test: sweep a frame-budget cap; RTF p0.1 and max dip length vs ρ.

3. **Barbell the frame: bounded loss per frame, tail defers.**
   "…so is the barbell a domestication, not the elimination, of uncertainty." — Antifragile.
   With budget + carryover (plane §7), dip depth is policy-capped whatever the tail (RTF p0.1 ≈ 0.35 in both streams); duration is the tail's exposure.
   Change: every admitted unit carries a bounded worst-case size (chunk big events; certificates carry bounds, not means — "…the degree of confidence", FoR).
   Test: queue sim with a hard slice cap; max dip ∝ cap.

4. **Ordering is second-order once tails dominate: measure before scheduling.**
   "The first principle is that you must not fool yourself—and you are the easiest person to fool." — Surely You're Joking, Mr. Feynman!.
   EDF (the plane's causal-deadline order) vs FIFO: thin tails −29% misses; fat tails ±10%.
   Change: keep deadline order (free, correct); drop queue policy as the p99 lever for burst-dominated classes (closes H0161's open limitation).
   Test: replay a bench trace FIFO vs deadline; <20% difference deletes scheduler tuning from the list.

5. **Delete with a quota before scheduling anything.**
   "Delete any part or process you can. … if you do not end up adding back at least 10% of them, then you didn't delete enough." — Elon Musk (Isaacson).
   Scheduling survives arrivals; deletion removes them: 92% of per-kick evals were window setup (20261006-0737).
   Change: gate allocator tuning behind a deletion quota — evals per real event < 10 on a bench; the 10% add-back rule guards physics.
   Test: count evals per real event before any queue work.

Field hint the engine's own tail is fat: worst/p99 = 14.5/2.72 ≈ 5.3 (sonnet-plane2) vs ≈1.3–1.7 for light-tailed frames over 36k. [INFERENCE]
