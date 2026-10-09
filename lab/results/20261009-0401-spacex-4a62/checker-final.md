Working...
Check complete. `check.md` written; tree restored to its pre-check state (`?? lab/results/` only).

**Grade: gold.**

Verification performed:
- **Reproduction**: applied `work/patch.diff` in a clean tree, built, ran — output **bit-identical** to the author's `hlive.log` (only the wrapper-appended wall/maxrss line differs). Every Evidence-section number regenerates; arithmetic re-derived (1,456/16 = 91×; ≈175× over 8 GB; slices 61.5%; 2.8 events/s; 1.3 KiB/event churn).
- **Predictions**: `predictions.md` mtime 04:08 precedes `hlive.log` 04:13; P1 falsified and honestly reported, P2–P5 held — the miss is not load-bearing.
- **Adversarial** (my own, via a parameterized copy of the instrument): seed 7 — same regime (median ship ~1.6 KB); fleet ×8 density — per-ship standing bytes unchanged, events scale; 2.5× horizon — live falls 2.91→2.58 MiB, steady state is real.
- **Novelty**: HANDOFF/plane.md mark H_live "not measured yet"; the only prior instrument (`examples/plane.rs`) panics before printing bytes/body; no HISTORY entry measures this.
- **Safety**: full `emergent-universe` suite green with the patch — accessors only.

Two flaws recorded for the integrator, neither grade-fatal: the dossier's "~0.43 MiB" engine attribution is actually **0.15 MiB** (28 bodies × 5,615 B — safe direction), and "retention ≤ 11 segments" is horizon-bound (grows to 18 at 2.5× horizon, following the traveler's light-distance window).
