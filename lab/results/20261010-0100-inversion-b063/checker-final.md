Working...
**Grade: gold** — written to `lab/results/20261010-0100-inversion-b063/check.md`; nothing else in the run folder touched.

**Reproduction:** ran all three commands in a clean copy (`work/patch.diff` is empty, so nothing to apply). `harness.py` 13.4 s → `metrics.json` bit-identical to stored; `s2_hot.py` 7.8 s → identical; `probe_crossing.py` 9.3 s → dense Kepler brute force confirms 72/73 S1 truth encounters (one wrap-edge skip, disclosed). Timings match the dossier.

**Predictions:** `predictions.md` predates the decisive run by ~4 min and its paper numbers differ from the measured ones (0.17n vs 0.34n, 220 vs 73/orbit) — genuine pre-registration. P1–P6 held; both instrument-guard misses are the author's own paper arithmetic, disclosed, with instruments independently validated (conjunction truth exact to 4.5e-13).

**My three adversarial cases, all confirming the kill:** fresh seed 42 (M catch@4 = 0.00, median rank 685 = 0.34n); shallow crossing e=0.05/ϖ_B=π/3 (median 354 = 0.18n, M@4 = 0.00); per-body a-spread ±ρ/2 quasi-periodic — the case the author flagged as possibly missed (M@4 = 0.00 at every lead, median 665). Exact periodicity is not the cause; no refresh cadence rescues the M-ordering.

**Novelty/goal fit:** no H entry inverts gold 20261006-0346-taleb-09b5; HANDOFF:69 still carries the premise and both build queues carry the in-flight `b-coorbital-cert`, so the correction (certify single-streamness via the cone's own crossing outputs; k as a law of ρ·n·lead, not 4) lands before the build, at zero cost. Premise of an adopted gold shown wrong + reproduced + held-out predictions held + adversarially robust = the gold bar.

**Misses recorded:** guard thresholds written from paper estimates (should come from measured controls); k99/(ρ·n) measures 2.5–6, not the stated 1.5 (10⁶ extrapolation still order-correct); empty `run.log`; scenes all coplanar prograde — a retrograde counter-fleet would be a stronger adverse scene for the corrected gate.
