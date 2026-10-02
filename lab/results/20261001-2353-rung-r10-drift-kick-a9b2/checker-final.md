Working...
Check complete. **Verdict: KILL of `symba` and `wh-fixed`** — verdict.py agrees between my metrics and the author's on all 20 outcomes; the rung is valid (truth passes every criterion, soi-switch fails jacobi/class/prec as a negative must). The BrokenPipeError above is just `head` closing the pipe; the full verdict ran clean earlier.

**Reproduction: exact.** Rebuilt `r10.c` and re-ran all four configurations in a clean tree: `raw-truth.json` zero value differences; candidate raws value-identical; `metrics.json` and `report.txt` regenerate **byte-identical**. My independent Python implementation of all five metrics (own growth-exponent fit) agrees to the last digit, and my fit on the picture series matches the C exponents to 3 decimals.

**Independent oracle checks.** Jacobi constant verified against the textbook rotating-frame form (1.4e-16); sampler verified as an exact port of `sample.rs` (seeds, `HANDOFF_KEPT`, formulas); reference verified as the repo's actual B12/B14 reference (`restricted.rs`). Adversarial probes: `diag` confirms the mechanism (|ΔC_J| flat ~2.2e-06 between transits, jumping exactly at ZONE 0→1 window entries); a deep moon shows symba within 10% of the reference's apsidal rate while wh-fixed is structurally OFF (confirms 0/53); an extreme retrograde birth agrees on class everywhere.

**Discrepancies found — none change a graded number, all in check.md:**
1. The dossier's selftest claims ("round-trip ≤ 3.4e-11; far-field symba == wh-fixed") are **false for the shipped code** (prints 2.0e-06 / 4.99e+04; the selftest moon escapes) — the far-field check belongs to the first build and can never pass on the unified KDK skeleton.
2. `r10.c` was edited after the candidate runs (T−4 min vs raws at T−11…6 min) — a moons.rate `0`→`null` serialization change, verified numerically inert, but undisclosed.
3. Dossier says "18–40 SOI crossings"; its own report says 6–40.

**Criterion weakness (the rung's):** the 1e-12 Jacobi floor sits below the reference's own 1.3e-9 drift, so truth's exponent is 0 by convention (disclosed); the candidates' exponents come from their own C_J series, so the KILL stands regardless. Predictions were pre-registered (T−12 min) with mostly honest accounting; the two clear misses are the rung's answer.

Artifacts written: `metrics-check.json` (identical numbers to the author's, justified by exact reproduction) and `check.md`; nothing else in the run folder touched, scratch binary removed, no git commands run.
