Working...
Check complete. `check.md` written: **Grade: silver.**

**Reproduced (clean tree, everything bit-exact):** `quad.json` (ṗ_coh exactly μ-linear, ratios 3.333/10.0), `calib.json`, two fresh held-out scans (band/θ_net/T_age identical to saved arrays), and — after recovering the author's c_H definition (median band at exact resonance ÷ μ^(1/3), mean over μ) — every number in `final.json`: capped-law stats (n=327, med 0.884, 99.4%), P4a = 0 under both uncapped and capped forms, κ values, the W crossing (0.0100/0.0230/0.0229 vs B17's 0.0112/0.0250), and the regime boundary (1.20/1.04/0.52). Half-step truth rerun: bands converged to 0.3%. `predictions.md` mtime precedes all four held-out scans; patch.diff empty.

**Why not gold:**
- The headline capped law is **post-hoc** — P1 as written failed (165 violations) and the cap c_H is fitted on the same truth it's scored on; P3 failed 3 of 4 held-out cases (the dossier's "2 of 4" wrongly counts the calibration case — held-out truth is 1 of 4).
- `final.json` has **no generating script** — the exact record gap that kept runs at silver on 5 October.
- My adversarial cases bound the domain: **3:2 μ=3e-3** (the unscanned corner) under-predicts excursion 16× and degenerates to "unsafe everywhere"; **4:3 μ=3e-4** breaks the guard itself (4 P4a violations); **4:3 μ=1e-3** breaks the μ^(1/3) cap entirely (c_H = 18.8, e→ejection). e₀=0.05 is robust (c_H 1.117→1.04, coverage 1.00) — the breaking axis is resonance strength, not eccentricity.
- Engine-facing premises (ṗ_coh = the kick layer's own quadrature) are asserted, not measured against the plane.

**The one experiment for gold:** wire the certificate into the plane's kick layer, delete the classifier and W table, and run B17's gate on r4 v3's cases plus a 4:3-class geometry — unchanged behaviours with zero added work makes it adoptable in one step.
