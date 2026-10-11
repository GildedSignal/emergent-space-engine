Working...
Check complete. **Grade: silver** — written to `lab/results/20261011-2028-second-20261011-1917-redteam-fb64-7521/check.md`; nothing else in the run folder touched (all shipped JSONs re-verified unchanged).

**What I did (45-min window):**

1. **Reproduction** — all six modes (`attack.py calibrate/sweep`, `attack2.py quad/sweep2/imgmemo/calibrate2`) regenerate the shipped `results-*.json` **bit-identically**; every dossier table matches its JSON. Predictions predate the decisive runs.

2. **Third-method oracle** (scipy DOP853 r-space null rays — independent of both the RK4 tables and the author's GL quadrature):
   - Confirms the +414 M arrival-interpolation corruption (orig−scipy **+368.8 M** at r_e=1000, b=21.6; fixed table +9.5e-3 M) and the r_e≥20 leak.
   - Confirms the prototype at the named scene: A_phi-keyed memo at r_e=8 physically ≤6.8e-4 rad worst-frame (2× under floor), robust at fresh phases (2.7/5.9: 100%/94% ≤ floor); b-keyed and per-family memos fail as claimed.

3. **The refutation that decides the grade**: the author's headline — "the silver's strong-field rows were correct all along; the checker's corrections were artifacts" — is wrong. Their "checker-style" table used 2000 α; the checker published **4000 α**. At 4000 α the checker's numbers reproduce *exactly* at r_e=6 (delay 38.604, err_fix 9.55e-2) and r_e=8 (err_design 0.0607, err_fix −9%); refinement on the author's own fixed tables (4k/8k/16kα) stays at 38.6–40.9 M, and my scipy root arbitration gives median delay **38.60**. The silver's r_e=6 "14× collapse" row is an under-resolved-image artifact; P8-at-6 is grid- and phase-fragile (0.07–0.12 at 2000α across phases, ~0.5 at ≥4kα). The mechanism story the author killed (A_t leakage) stays dead — but the checker's *numbers* stand, via image-set resolution.

4. **Record gaps**: the three-table adjudication, phi0 rows and 13.7× order check have no shipped mode — the exact non-regenerable-record gap that has sunk silvers before.

**One experiment for gold**: rerun the adjudication at 4000α + independent root enumeration, flip the r_e=6/8 record back, restate prototype margins with the physical bound. The prototype itself needs nothing further at r_e=8.
