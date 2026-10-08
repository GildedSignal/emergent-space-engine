Working...
Check complete. `check.md` written to the run folder; tree left clean; nothing else touched.

## Verdict: silver

**The physics holds.** I reproduced all seven matrix configurations from `work/patch.diff` on a clean tree — m48 runs bit-identical (served 21330/31.2%, worst age 1961.872 at id 3), m400 within wall-budget jitter, saved p50 0.276–0.48 ms matching the dossier. My five adversarial cases (seed 3, m400 rtf 1, 30 s duration, rtf 10, triple repeat of the rtf 10⁴ 4K cell) all confirm the headline: the gate fails at every player-scale rtf by 15–1,962 quanta, breaches are bounded (30 s worst = 15 s worst), and the first checker's gold experiment genuinely kills the "cheapest 5×" row-cache lever. Predictions preceded the matrix (10:30 vs 10:31; runs take 1–3 s). Tests: default suite and `observation_never_changes_the_digest` pass with the patch; the jacobi failure is pre-existing on the clean tree, verified both ways.

**Why not gold — the record, not the result:**
1. **Broken fleet meter.** `RowCache::begin()` never resets `fleet_rows`/`fleet_tc_changes` and the example re-adds the running total each frame — the printed "19.4M visits" is exactly 48 × 900·901/2. Measured directly with an instrumented copy: the fleet's committed tick changes **once per gather** (~3,383 ticks), not "~450×/frame"; motions = members exactly (48/400), not "2,600–26,000 entries"; 389 handoffs, not "thousands". The exclusion verdict is unaffected (basis refuses every frame anyway), but three dossier numbers are artifacts.
2. **Non-deterministic verdict cell.** m48 rtf 10⁴ 4K flips PASS(0.34)/FAIL(1.87)/PASS(0.36) across identical repeats — the "fails 6 of 7, deterministic" claim is false at that boundary (which only strengthens the headline).
3. Contradictory draft paragraph (tests "pass" vs "untested — window cut"); prediction 1's 100× magnitude miss reported as "held".

The named gold experiment: reset the fleet counters per frame, restate the fleet-exclusion finding on the true numbers, report the knife-edge cell over repeats — my measurements indicate every verdict survives.
