# Author fi`patch --dry-run` confirms the patch applies cleanly to the HEAD tree; `git diff --check` is clean. The run is complete: predictions pre-dated every decisive JSON (mtimes 05:28 vs runs 05:31+), digest controls passed both ways, and every dossier number regenerates via `analyze.py` from the saved JSONs.

**The claim, in one sentence:** With the stage timers on the code path the kick bench actually samples — the legacy split `fn kick`, 9180 of 9192 kicks, with the energy-register path (`kick_clock`, just 12 calls, rebind 59.6% = the prior run's mislabelled table) counted separately — the rebind is **84.6%** of a real kick (mean 79.4 µs, independently corroborated at 84.8% by the engine's own 9213 kick calls) and is compute-bound (only 1.20× cache-cold while readout/forces go 2.8–3.1×), so the jet/re-anchor lever addresses ~85% of kick cost, not 59%; but the prior run's mean (52.6 µs) and capacity (1.27×10⁵ ships/core at rtf 100) were wrong — the true cadence is 1.32×10⁻² kicks per *active* ship per game-second (mean 232 ships, not the 2046 target), putting the resolver's saturation near **9.5×10³ ships/core, five orders short of 10⁹** — every number now regenerating from the shipped record.
~5 orders per core, not 3.

Everything is in this folder: `predictions.md` (pre-registered; one honest miss — my mean band
inherited the prior run's wrong 52.6 anchor), four run JSONs + digest controls, `analyze.py`
(reproduces every number in `dossier.md`), `work/patch.diff` (instrumentation only; clean vs
patched digest `dac49af3…` identical; m2000 replay `ca74ff5a…` and memo bit-identical to the prior
run), and the prior run's JSONs under `work/prev-*` for comparison.

Open for the next run: law v2 (`kick_clock`) is still unbenched at scale — 12 samples here; it
needs a bench that samples clock bodies when their Boundary sorts first.
