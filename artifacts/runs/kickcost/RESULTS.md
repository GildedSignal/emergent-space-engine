Exact lazy panels and fit cleanup meet the frozen job criteria. Shared shape is REJECTED. No OOM gain demonstrated; no consistent marginal RAM improvement.
Stage order: baseline → lazy panels → shared candidate → final exact fit. Pairs below are N=100000 / N=1000000.
Flown FIT µs/rebind (L8 burn, RTF 100): 80.4/84.4 → 50.2/51.8 → 43.1/43.8 → 47.4/47.6.
Marginal peak B/body, 20 s coast, (footprint(N)−footprint(0))/N: 1355/1137 → 1295/1111 → 1455/1125 → 1436/1122.
G1,G2,G3,G4,G5,G6,B19: PASS → PASS → PASS → PASS.
B13: 60/64 → 60/64 → 47/64 FAIL → 60/64. The broader tool labels 60/64 FAIL; it meets this job's frozen floor.
B17: TIMEOUT → TIMEOUT → TIMEOUT → PASS (55.55 s; regime 34/34, controls 5/5).
Release tests passed/failed: 153/0 → 155/0 → 146/9 → 155/0; 3 ignored at every stage. Final exact Cargo invocation also exits 0 (32 capped binaries; package cwd preserved).
Replay-all regressions: 0 → 0 → 0 → 0; none skipped. Final recorded-flight digest values also match the baseline.
Frozen flight digests: baseline/panels/final IDENTICAL 8/8; shared changes readouts as expected. Zero schedule disagreements at every stage.
N1, million bodies, coast and burn (existing post-warm-up window): PASS at all four stages. Final worst frames 7.885 / 10.563 ms, zero lag, refusals and frames over 12 ms.
Shared single-arc error: fixed repeated-cycle bias, max |ΔT/T| 5.94084e-4 and |Δadvance/advance| 1.58644e-4 on 256 curves; 256 exact event reconstructions and 768 cycle checks. This is NOT a no-walk certificate across refits: nine integrated tests fail.
The shared grid can replace eccentricity 3.55e-15 with 1.22085e-4. It passed isolated period bands while failing B13, bounded motion, the origin's response to kicks and the HUD countdown. Do not activate the patch.
At a million, the final fit spends inverse 3.224, shape construction 8.829, locating the event/needed prefix integration 30.865, duplicate reconstruction 0.069 µs (previously 4.028); total 47.636 µs. Remaining time is adapter/orientation work and retries.
Largest remaining deletion target: avoid reference-periapsis-to-event quadrature with an event-anchored or analytic generator. UNBUILT; it needs its own derivation/qualification, and reordered scaled sums cannot be assumed bit-identical.
Lazy panels live in 40cb1ea1; final fit and rejected evidence live in the commit containing this file. Shared delta applies to shared-base-commit.txt; its useful cell reuse and exact anchors are retained as a reproducible failed configuration.
The first bound-only attempt is kept in lazy/: N1 burn FAIL lag 0.570 s; it omitted passage laziness and was superseded, never relabelled green.
Timings and footprints are observational on the running M1; machine load, power, swap and available thermal status accompany raw logs. Instrumented flights are excluded from N1 and memory comparisons. See measurements.json and REPRODUCE.md.
