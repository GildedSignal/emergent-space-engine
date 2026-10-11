Working...
**Grade: gold** — written to `check.md` in the run folder.

**What I verified:**

1. **Record regeneration (the named experiment).** `python3 falsifier.py` from a clean copy: 27.4 s, exit 0, run three times — every physics key bit-identical to the stored `metrics.json` and between consecutive runs (only `machine`/`wall_seconds` differ). E1–E6 bit-identical to the prior record on `origin/claude/lab-20261011-1456-scout-126c` via the dossier's own comparison command → `[]`. Both orphaned keys are now live: `separatrix_valley_panels_to_1e-11` regenerates exactly (43/83/133/205/3765), and `bound_control_apo_to_peri` runs all three seeds against two independent references (DOP853 turn-event + parametrization-free sin²θ quadrature).

2. **Predictions.** `predictions.md` (16:16) predates the decisive run (16:46–16:48). P-D/P-C held; P-A panel counts held approximately; the ≤ 1e-9 accuracy targets failed by ~2.5 decades and are reported as failures with exact numbers — while every pre-registered kill line (≤ 1e-6 at δ ≥ 1e-8, ≤ 96 panels, valley-kick ≤ 1e-6) held. The honest-failure pattern, not the 1-October pattern.

3. **Adversarial (six probes of my own).** The claim survives beyond the shipped L̃²=13 single point: the whole outer-plunge family L̃² ∈ {12.1, 14.5, 15.9} holds ≤ 3.2e-7 (m=1) at ≤ 63 panels for δ ≥ 1e-8; near-separatrix bound-orbit kicks at extreme phases (f = 0.05/0.95) hold ≤ 4.2e-7 where uniform panels fail by up to 0.21; deeper endpoint r_end = 2.1 unchanged; m=4/safety/base robustness claims confirmed; below the domain (δ = 1e-12) candidate error tracks the oracle's own rtol-1e-13 shift — truth-limited, as the dossier says.

4. **Novelty & fit.** The fixed dyadic rung ladder (B9's bands on distance-to-barrier-top, σ from the complex root pair) is new and law-native, replacing the unadoptable adaptive float bisection (43× fewer panels at δ = 1e-10); it moves the queued `b-plunge-tubes` bottleneck and deletes the taste log's named silver-killer (unregenerable records) for this representation.

Caveats named for the integrator: m=2 is measured not derived (m=1 clears every kill line anyway), the integer-side claims stay inference, and δ ≤ 1e-10 is unfalsifiable against this float oracle.
