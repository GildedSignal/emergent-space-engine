Working...
**Grade: silver** — written to `lab/results/20261005-1404-q-plane-judge-65fd/check.md`; nothing else in the run folder touched, tree restored to pristine (`git apply -R`, scratch probe deleted).

**Reproduction (clean tree + `work/patch.diff`):** all 9 rows I ran match the author bit for bit — echo B12 3.75e-15 / B13 64/64, planted-kick 0.766 & 53/64, planted-average [0.107, 0.963], plane B12 s7 (15/15, exponent 1.026, worst inf), B13 s7 51/64, B17 s3 [0.79, 8.8] controls 0/5; unit tests 3/3; echo B14 times out at the judge's own 60.1 s (B14 machine-VOID confirmed); `MIN_STEP = 128` confirmed in `step.rs:37`; predictions.md mtime 14:26:03 precedes the table (14:26:21 → 14:37:26).

**My three attacks, all confirming the work:**
- **B17-scene fidelity** (no unit test covers μ = 3e-4/3e-3, sep = 100): t = 0 semi-major axis comes back to 0.2–0.4% (the plane's quantum, not a conversion bug), error *grows* from 3e-4·sep to O(1)·sep, controls pump e 1.75× — the adapter is faithful; the engine diverges at the finest cadence the tick floor permits there (24.6 kicks/orbit).
- **Death cause of the 7 lost B13 flybys** (replayed through the public API, 64+32-fold refine): all die at 1.56–3.18 planet radii where the reference passes at 1.32–11.08 radii — surface/planned-periapsis deaths from wrong encounter trajectories, not the adapter, not the system edge (`refused = 0`, 2⁴⁰ unreachable).
- **Controls both sides:** every planted flaw fails its gate through the same `restricted` path.

**Why not gold:** the held-out verdict predictions failed (B12/B13 predicted PASS at steps 7/5; B17 ~60% — honestly reported, safe direction, but precedent blocks gold), and the table is incomplete — B14 is machine-VOID here, against the integrator's "complete table" bar. **One experiment to gold:** the four B14 plane rows where the judge's phase fits (M1/quiet box, eccentric births for the apsides), predictions already on record.

**Notable miss I add:** B17's miniature sits beyond the plane's representation floor — cadence capped by MIN_STEP *and* t = 0 binding only ~0.3% exact — so that row measures the plane at a scale it cannot resolve; plain under-resolution already explains the divergence, leaving the author's two derived suspects untested.
