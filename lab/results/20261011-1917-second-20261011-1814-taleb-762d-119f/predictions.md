# Predictions (written before the decisive grid, 19:28 UTC)

The checker's named gold experiment: decompose the stall — per members count, the scene's
events per presented game-second (density D) and the engine's events per wall-second
(throughput T) at each budget, plus one profile of `Universe::advance` at m400 — to decide
whether the budget floor is a fixed per-frame prologue (the dossier's mechanism) or
density ÷ throughput with presented time causally gated (the checker's counter-reading).

Setup: `xtask universe --bench`, seed 1, threads 1, coast (no scripted player), rtf 3,000,
10 s (600 frames). Grid: members {4, 100, 400} × engine budget {5, 1, 0.2, 0.05} ms, unpaced,
per-frame series saved. Plus the paced 60 Hz cell at m400 (0.2 and 5 ms), the original row-1
regeneration (scripted 300/3000/30000; coast 300000), and a perf profile at m400.

Honest prior: P2/P3 below were *derived from the author's own JSONs* (presented_tick_at_end
arithmetic on B-*/C-*/E-* files), so they are not fully held out; the held-out parts are the
fresh numbers (new process, today's load), the m100 column, the 0.05 ms m400 cell, the paced
m400 cell, and the perf profile — none of which exist in the original artifacts.

- **P1 no prologue floor:** events bought per frame e(B, M) is near-linear in B from 0.05 to
  5 ms at every M — no knee. Specifically e(0.05, M) ≥ 1 event/frame, and
  e(0.05)/e(5) ≥ 0.01 (at least 1% of the events at 1% of the budget). A fixed 0.2–1 ms
  prologue would give e(0.05) = 0 and e(0.2) ≈ 0. Falsified if e(0.2, 400) < 0.3 events/frame.
- **P2 the cliff is T×D, not a threshold:** run-average delivered RTF ≈ T_real/D within 2×
  in every grid cell (T_real = dash events ÷ wall seconds; D = dash events ÷ presented
  game-seconds covered). The m4→m400 delivered drop at 0.2 ms (>100×) decomposes as a
  throughput drop ≤ 30× times a density rise ≥ 10×, both measurable — not one N-scaled step.
- **P3 "0.00 delivered" is a median-frame artifact:** in the stalled cells (m400 at ≤ 1 ms)
  the run-average delivered RTF is ≥ 10× (not 0) while the median per-frame RTF is < 0.01×:
  presented time freezes for most frames and advances in jumps (≥ 90% of the game time
  arrives in ≤ 10% of the frames).
- **P4 the paced worst cell:** paced 60 Hz, m400, 0.2 ms: run-average delivered RTF between
  2× and 50× (point estimate ~8×), median frame frozen (< 0.1×), worst frame ≤ 17 ms, digest
  equal to the m400 5 ms paced digest. Outside that band the T/D model is wrong.
- **P5 rekey is a tax, not the floor:** in the perf profile at m400, rekey (the requeue /
  light_distance / heap-set loop at the top of `advance`) is ≤ 25% of engine time at 5 ms
  and ≤ 40% at 0.2 ms; per-frame rekey cost at ~371 bodies is 0.005–0.1 ms — below the
  claimed 0.2–1 ms floor. If rekey ≥ 0.2 ms/frame at 371 bodies, the prologue story revives.
- **P6 the record regenerates:** row 1 was scripted (no --coast) for 300/3000/30000 and coast
  for 300000; re-run that way, the medians come back ≈ 300/3000/30000 (each within 10%) with
  the original digests, and the corrected table (371 bodies at 0.2 ms; engine p50 0.28 →
  5.24 ms for m400 0.2 → 5 ms) regenerates from my saved JSONs with the printed commands.

Kill criteria for the corrected (density ÷ throughput) claim, any one: a grid cell where
delivered deviates from T/D by more than 2×; a knee in e(B) at fixed M (e(0.2) ≈ 0 while
e(5) ≫ 0); or rekey ≥ 0.2 ms per frame at 371 bodies.
