Working...
Check complete — verdict written to `lab/results/20261009-2257-constraint-842c/check.md`, nothing else in the folder touched, no commits, temp build removed.

**Grade: lead.**

What I did and found:

**Reproduced (clean rebuild, patch.diff empty):**
- Both sweep digests bit-identical (`41343a14…` m48, `3db02d3d…` m400); every dossier table row matches its JSON; paced shares 69.5/17.8/9.0/3.8 confirmed.
- Strengthened the linearity claim with three extra points (`--members 4/100/250`): 5 points, slope 5.56 µs/emitter/frame, R² 0.9988, fixed intercept 0.32 ms.
- Code claims verified: `angular_radius` computed and dropped from the wire (`view.rs:290`, `session.rs:147–158`), gather filters nothing, engine budgeted at 5 ms while the gather has no budget path; space gates PASS; kick bench reproduces.

**Falsified (adversarial cases):**
1. **The member radius is 738–1477 m, not "~28 m"** — `scenes.rs` radii `q/2..q` with `q = 2²⁰`, root unit 1476.6 m. At the author's own half-pixel floor, 200/343 members sit **above** it (the nearest are 38–77 px across); the honest cull bound is ≤ 54%, not ~99%. The probe's angular counters read 0/N (field not on the wire) — a control reading zero, unexamined.
2. **Pooling also fails**: members surround the player and fill 341/343 distinct pixel cells — "overlap in a few pixels" is false.
3. **The sweep is two configs**: `--members` is clamped to `[4,400]` at CLI parse (m400/m1600/m6400 share one digest); the 428-body cap is the clamp, not the fleet dissolving (every run's fleet dissolves).
4. **Predictions not held out**: P3's outcome was already in `bench-m400.json` eight minutes before `predictions.md`; P2's distance data was in hand; P2's "stronger" re-reading is the radius error.

**Novelty**: H0210 already recorded "the view gather is 83% of a light frame"; plane.md §7 already forbids an unbudgeted gather; the kick numbers match the 5 October taste log. The surviving residue — view ≫ engine in the median frame, 5.56 µs/emitter, engine tail p99 5.4 ms over budget, 2.6 events/s/body — is measurement context for the budget-the-gather step the spec already mandates.
