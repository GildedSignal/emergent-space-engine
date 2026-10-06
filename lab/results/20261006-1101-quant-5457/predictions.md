# Predictions — 20261006-1101-quant-5457 (written before the decisive sweep)

Question: what does one player burn cost the frame (dose-response, throttle 0.35 g → 11,560 g), and does
the burst stay inside the engine's 5 ms budget or leak into the ungoverned tail (gather/serialise)?

Runs (all `xtask universe --bench --seed 7 --rtf 100 --seconds 30`, paced, 5 ms engine budget):
`--coast` (no decisions at all), `--level 0`, `--level 8`, `--level 8` again (digest + noise control),
`--level 15`. Burn pattern is fixed: keys held frames n%240 < 20, so burn frames are 7.5% of 1800.

Held-out predictions (not tuned on):
1. **Dose.** Mean CPU-ms of burn frames rises with level; at level 15 the burn-frame CPU is ≥ 2× the
   coast frames (a 33 game-second burn at 11,560 g rebinds and re-kicks the player's orbit repeatedly).
2. **Bound.** The burst stays governed: CPU hitch counts above 16.7 ms stay 0 at every level, and
   overflow frames do not more than double from coast to level 15. If CPU hitches appear in burn
   clusters, the budget leaks (a strike against plane.md foundation 7).
3. **Tail owner.** The view gather owns the frame tail at every level (share ≥ 50% of summed time);
   impact changes the engine part, not the tail. The worst wall hitch is a stall (wall ≫ CPU).
4. **Decay.** The burn's excess CPU cost decays back to coast level within ≤ 60 frames after each
   20-frame burn ends (well before the next cluster at frame 240k).
5. **Determinism.** The two level-8 runs give byte-identical digests; every other run differs.
6. **Survival.** The player stays alive at level 15 (Δv ≈ 0.0125 c per burn, far from the γ ≈ 2000
   kick-refusal limit); rtf lowest-1% stays above half the median.

Kill criteria (frozen now):
- **Impact is free** if burn vs coast cost differs < 10% at every level (CPU-ms, engine part): weak
  result, report as such.
- **The budget leaks** if CPU hitches > 16.7 ms appear inside burn clusters, or overflow grows > 2×
  from coast to level 15: strong result against the budget premise.
- **The gather prior breaks** if the engine's share exceeds the gather's at p99 under burn load.

Machine honesty: shared Linux x86, other lab runs may compete; CPU-ms (thread time) is the compute
measure, wall-ms only the service level; orders of magnitude only, the integrator re-measures on M1.
