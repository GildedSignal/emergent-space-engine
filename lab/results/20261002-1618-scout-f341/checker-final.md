Grade: silv**Grade: silver.** Written to `lab/results/20261002-1618-scout-f341/check.md`; nothing else in the run folder touched (all reproduction and attacks ran in `/tmp`).

**How the check went:**

1. **Reproduction — exact.** The decisive suite re-ran in a clean copy: every number in `run-log.txt` and `results.json` bit-identical (33.5 s vs 36.2 s). The `--smoke` run reproduces the pre-decisive amendment's recorded numbers. `patch.diff` is empty; the falsifier is self-contained, and its kick accounting is honest (GP charges sweeps×nodes including the final sweep; drifts free).

2. **Predictions — held in order.** `predictions.md` (16:36:28) predates the decisive run (16:40:25); the four failed predictions fail exactly as the scorecard records. One nit: `falsifier.py` was edited at 16:39:45 (after predictions, before the run) and is untracked, so the pre-edit text is unrecoverable — I read it as the amendment's finalization since everything reproduces, but noted it.

3. **Truths independently validated.** The dossier's claimed "RK4 cross-check" has **no script in the folder** — so I built one (three of my own bugs fixed along the way: miswired RK4 stages, a missing Kepler term in the flyby ODE, a stale E₀ across scenes). Final: M2 precession RK4 vs LF-2048 agrees to 7×10⁻⁶; F1 ΔE to 1.2×10⁻⁴; at periapsis 3 the LF ladder and RK4 converge to the same limit.

4. **Five attacks, no claim broken within the frozen gates:** 500-orbit compounding (prec 2.4%, flat Jacobi exponent), e₀=0.6 (1.12%), retrograde 0.45 R_H — inside B14, untested by the author (1.62%), resonance at B17's μ=10⁻³ edge (pump 0.998), flyby at 3 radii (GP-4 still B13-level at 20 reads). New findings: a **secular e-walk at 16/orbit** (mean |Δe| quadruples by 500 orbits — the precise case for the queued correctors at 16), Jacobi 3.5×10⁻⁴ > 10⁻⁴ at 500 orbits, and a baseline ambiguity (`ctx.rs` defaults to 128/orbit while `step.rs` docs say 1/64 — if 128 is real, the cut is 8×, understated).

5. **Why not gold:** a measured 4× on a float replica (single seed, 2D, Newtonian tide, no integer law) is one frozen-criteria integer rung from adoption, and one revised held-out prediction failed by a hair. The named gold experiment: B13/B14/B17 at `step_log2` 4 and 5 on the engine's own scenes, planted negatives included.
