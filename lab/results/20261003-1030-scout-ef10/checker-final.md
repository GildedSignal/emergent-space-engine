Working...
Check complete. `check.md` written to the run folder; nothing else touched (reproduction ran in `/tmp/chk-ef10`).

**Grade: silver** — real, reproduced, but with a false novelty premise and one overstated prediction.

**Reproduction:** `decisive.py` reran in 27 s and produced **bit-identical** `results-sweep.json` / `results-heldout.json`; all 8 dossier-table cells re-derived from the JSONs; predictions genuinely pre-registered (mtime chain …717→…767→…779→…800). Coefficients, Z-composition and the `inv` convention verified against **upstream rebound main**, and the inverse corrector proven exact (roundtrip ≤4.4e-15 on a state it moves by 2e-4).

**My attacks:**
- **Off-grid scan:** true thresholds n=24 (plain) vs ≤10 (order 5) — the "2×" is conservative (≥2.4×).
- **3:1 resonance (untested by author):** order 7 is 2.3× *worse* than plain at n=8 — silent degradation, same signature as the author's own corrupt3 control; gains recover to ~2× at n≥16.
- **Unshipped claims:** RK4 CJ conservation and the 200-random-drift check aren't in the repo; my reruns give 1.4e-9 (step-dependent) and 1.1e-13 — roughly hold, should ship.
- **P4 falsified as reported:** at m₂=0.3/e=0.6/n=8, orders 3 and 11 are 2.1×/3.7× worse than plain; "orders saturate within 2×" holds only at e=0.2.

**The decisive find:** the dossier's "queued, never run, no H entry" is wrong — `git log` commit `dcdde70` (2 October, "Grade: silver") already ran correctors including the **output-only form** (`whc3b`) and measured a universal 8-kicks/orbit floor at behaviour gates, with an exact-conjugation proof that the fixed-n gains are a readout relabelling. This run's Jupiter-class 1× rows confirm it; the genuinely new content is the strong-tide μ=0.23 regime, the non-asymptotic quantification, and provenance. Gold path: the author's own rung, amended to judge at **both** amplitude and behaviour gates with the resonance case as a must-NOT-degrade control.
