Working...
Check complete. **Grade: silver** — written to `lab/results/20261013-0236-inversion-57ce/check.md`.

**Reproduction.** regen.sh exit 0; I re-applied `work/patch.diff` in the restored tree, rebuilt, and reran A8/A5: digit-for-digit identical to the author's `out/` (wall stripped); B8's tail E = 4.288858767 matches exactly. Engine attributions verified in code: `step.rs::boundary_clock` kills silently at `r < surface` / `r > 2^leave_log2` (no fault field), and gate C1's oracle is the same `u^t` formula the probe uses (`tests/clock.rs:90-92`). predictions.md (02:44) predates the original out/ (~02:53): P2/P3/P5 held, P1/P4 falsified and reported as falsified.

**Attacks (5, several outside the author's grid).**
- **A6** (untested gap): crossing safe — E−1 = 7.0×10⁻¹⁰, relerr 1.2×10⁻¹³, 0 refusals.
- **A1** (below range): also dies silently at the surface (r 1.0516×10⁹ < 1.1306×10⁹, fault=None) — the crash regime is the whole gentle half L1–L4, death ticks monotone.
- **B5/B15** (capture probe beyond the author's single B8): no capture at any level — E rises to 1.13 / 4.29 / 196, 0 refusals, alive. The pump owns the arrival maneuver at every throttle.
- **Seed 2**: bit-identical player flight — `plane` spends its rng only on the 23 free ships; the player/planet orbits are literals. The seed axis is null for this probe, so "one seed" understates the coverage.
- The pump tail's "zero refusals, alive" wasn't printed by the probe; I reran with the record printed: refusals=0, alive, fault=None — confirmed, no longer inferred.

**Why not gold.** Two of five predictions falsified; no 10× move, deletion, or refuted standing premise (the page's "parabolic edge is safe" is *confirmed in flight*) — the author concurs ("nothing to adopt"). The one experiment to gold: the downward Passage→Cycle capture via a timed flip burn, the page's own named next experiment.

**Page corrected in place:** "scale exactly as 2^−level" → measured ratios 9.3/7.4/14.6 vs 8/8/16; crash regime extended to L1–L4 with checker attribution; t-range restated as event_time; Domain now states the seed cannot move the player (nose/scene/input patterns are the live axes); the inherited garbled Runs tail deduped; the run's entry annotated silver with my extensions. Tree restored (patch reversed, scratch example removed); nothing else in the run folder touched.
