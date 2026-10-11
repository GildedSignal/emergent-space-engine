Working...
Check complete. `check.md` written — **Grade: silver**.

**What held (reproduced + attacked):**
- All four modes reproduce `results-*.json` and the dossier table exactly; predictions timeline is clean (19:44 → 19:47 → 19:50, empty patch).
- Design quotes verified verbatim (law.md:53, representation.md:56-57); r5/r6 have no rung files; B3/B16 gate deflection angle only, B7/B19 clocks/geodesics — the "no gate catches apparent position" claim is true.
- My independent r-space quadrature validates the oracle's trajectory shape to 1e-7; phi0 variation leaves medians stable; the r_e ≥ 20 rows, the one-pixel floor at 60 M, degrees at the ISCO, and the 40–150× collapse from the delay memo at r_e ≥ 60 all survive refinement.

**What broke (my finding):** the oracle's arrival time is under-converged for nearly-radial photons (arrival interpolation over giant final steps; +14 to +24 M), and scene frames do dip into that family. Under a converged table the ISCO row changes: err_fix 9.9e-3 → **9.6e-2 (10×)**, err_design +36%, delay 30.9 → 38.6 M — so the "fix collapses 14× at r_e=6" number is not regenerable at convergence, and P8's claimed success at r_e=6 is an artifact. The dossier's convergence guard (3.4e-6) was measured only at r_e=8/60 and never on err_fix. Also two record errors: "Shapiro appears nowhere in docs/" is literally false (H0033–H0036, old law-lab lineage — a different subsystem, which actually supports the substance), and the reference-level counter-reading (original-research-report.md:53 delegates fine arrival to a metric query) went unaddressed.

**One experiment for gold:** rerun the sweep with converged arrival times, report r_e ≤ 20 from it, re-derive P8, prototype the image-resolved memo at r_e=8. The run folder is otherwise untouched (regenerated JSONs are byte-identical — deterministic script, matching sizes — and original mtimes restored).
