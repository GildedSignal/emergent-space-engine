Working...
**Grade: silver** — written to `lab/results/20261003-2306-redteam-4570/check2.md`. Nothing else in the run folder touched; my scripts stayed in `/tmp`.

**What reproduced:** both scripts bit-for-bit; the port verified line-by-line against `view.rs` (window, clamp, cap, bracket, cold guess at :257); every doc claim checked out — 83% bottleneck (HANDOFF), B15's 0.9c stream (law.md:67), r5/r6 named in representation.md §7 but absent from `lab/rungs/`, Minsky drift vs law.md:20, ~50 ns vs 29 µs (580×), B11's `5/a² ≤ 5×10⁻⁴` judged band. predictions.md preceded the outputs by mtime; P1/P2/P4/P5 held.

**What my attacks found:**
- **The remedy as written is falsified.** The "combined fix" (`−(1+n·β)−ε` + unclamped slope) had no saved artifact, so I rebuilt it: cost claim reproduces (1.01–1.05 everywhere), but in the author's *own* head-on warm scene it returns a wrong tick on **50/100 frames** — the ε widens the window into float noise, accepting a tick whose successor still has g ≤ 0. That fails the author's own proposed r6 criterion (tick identity). The sign-corrected constant `−(1+n·β)(1−10⁻⁹)` keeps 1.02–1.05 readouts with **0 wrong in 15,000 randomized frames** — one line, corrected.
- Shipped code: 0/15,000 wrong in randomized sweeps — its correctness claim strengthens.
- Accelerated flyby (perigee swing): 2.04 → 1.05, cost claim survives acceleration; circular orbits turn out degenerate at centre-observers, so orbit coverage stays thin.

**Why not gold:** 2–3× per relativistic emitter, not 10×, no component deleted; frame-level gain unmeasured (readouts ≠ ms); the fix needs my correction before adoption. Gold path named: land the corrected constants, freeze r6 as proposed, measure on the engine.
