Working...
Check complete. Deliverables written: `metrics-check.json` (validates; verdict standalone = KILL on `steady` only, with the positive control passing — no VOID) and `check.md`. Verdict with the author's absent file = DISPUTED, as the pipeline will record.

**What I found:**

**Procedural.** The author died at its 90-min limit (20:17:41) having never produced `metrics.json` or the picture — the dossier (19:31) cites numbers from a file that never existed. It relaunched casea/b/c as orphans 9 s before death; those finished during my check, and I reproduced everything rerunnable exactly (a13: truth 25 / meth 44 / skipped 18 / missed 0; cased: 1.0019 / 1.0000 / 823.3 bit-identical).

**The rung's truth spec was not implemented.** `PAIRSAMP=1500` (of 163 152 radial pairs on a13 — my independent recount), `PAIRBUDGET=3`s silent skips (18+42 pairs), 2 of 20 belts, `NSAMP=8` with 4 skipped for the steady rate, 2 of 3 ladder points, casec producing zero output in 19+ minutes. The skip set is wall-clock dependent — the "truth" isn't even reproducible.

**The crate itself survived every attack.** All 71 "false" events sit on budget-skipped pairs; all 140 method events across three belts (incl. my own adv-equalperiod run exercising the Full-section path) dense-verify as real sub-ρ minima; on every fully-processed pair truth = method exactly, missed = 0. Fair `checks_per_encounter` = 1.157. My mini-ladder gives scale exponent 0.987 (negatives 1.970). The `steady` failure (5.67) traces to a 4-pair/3-encounter denominator; two independent cross-checks put the fair ratio at ≈ 1.3–1.4 [INFERENCE, labeled].

**Caveats filed:** `other_certificates_touched` and the oracle's `steady_ratio` are hardcoded — criteria that cannot fail; 17 belts, c-n100000 and a real isolation probe remain untested.

Additions declared in check.md: four checker probes under `harness/examples/`, `check.md`, `metrics-check.json`. Nothing of the author's modified.
