Working...
Check complete. **Grade: lead** — written to `lab/results/20261005-2231-q-secular-008e/check.md`; nothing else in the run folder touched.

## What I verified

**Reproduced:** `metrics.json` regenerates **bit-identical** from the stored artifacts (re-ran selector 0.6 s, LL 1.2 s, analyze 1.6 s); my planets-only re-run of the shipped WH reproduces the stored truth planets to 1.2e-9; `predictions.md` (23:22) pre-dates the decisive outputs (kick 23:31, rings 23:39, truth 23:42); my independent re-implementation of the frozen estimators gives the same 0.0 / 20.5% / 25.6%.

**But the truth is not the declared scene.** `wh_run.py`'s `accel()` ends each pass with `out[j] = 0.0`, which wipes row `j`'s accumulated kick from the *previous* pass — **Saturn is never kicked**. It coasts on a fixed unperturbed ellipse for all 23.7 kyr:

- stored `truth_zp`: |z_S| = 0.0537 ± 0.0003, arg drift −0.009 rad over the whole run;
- two independent exact-physics integrations (heliocentric and barycentric DOP853, different coordinates and code, agreeing with each other to 1e-9): |z_S| swings 0.054 → **0.007** → 0.040;
- single-step microscopy: one DKD step matches the exact ODE to 2e-11 — the scheme is textbook, it just integrates different equations than claimed;
- the h-convergence pair (2e-6) is same-bug cancellation; the bug is invisible in the single-planet p2 scene the code was validated on.

Consequences: the dossier's "5× Saturn driver" culprit **is the bug** (exact 0.0399 vs α²-LL 0.0102 vs α¹-LL 0.031); belt z is corrupted ~2e-4 by 3% of the run, growing to the pass-bar scale — the 20.5% kill fraction is measured against a wrong reference. The kill may survive a corrected truth (rings' errors are ~5–10× the corruption) but is undemonstrated. The one-line fix plus a ~40 min re-run (and the author's own launched-but-unfinished truth-driven `rings_tc`) decides it — that is the experiment the next run should pick up. The selector (80.3%, prediction held), the frozen estimator machinery, and the pre-registration discipline all survive untouched.
