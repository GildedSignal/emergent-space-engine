Working...
`check2.md` written — **Grade: gold**. Summary of the check:

**Reproduced** — `python3 probe2.py A B C D E F G` in an isolated copy: bit-for-bit identical to the author's stored results (0 diffs across all aggregates and per-pair records, excluding wall time). Every dossier number verified: skin retriggers 12.9/254.8/581.8 intervals (ρ=1e-4/2e-3/5e-3), phase quanta 13.0/263.2/449.2 tracking ρ/eps, as-stated work 0.010–0.89× scanning in every kicked config (1.1–96× loss), frozen control never breaks, C's ψ misses 1323/2817 hits, E's 3.97M vs 41,349 evals/encounter.

**Verified by code-reading** — both defects the author found in the original: `probe0.py`'s `kepler()` never rotates by ϖ (frame mismatch, error O(a·e)≫R), and the 33–146× counted phase tests while its own window cost a 49k-eval scan (frozen honest accounting: 5.2×, reproduced).

**Adversarial** (5 own cases) — determinism (two runs identical); circular wide belt H: the non-reversal corner is hit-starved (0 hits), confirming "too thin to certify"; circular tight belt K: non-reversal *with* 15,965 hits — ψ misses **zero**, FA 1.2% (boundary is the reversal condition, not kicks); e≤0.3 extends the failure; eps=1e-7 confirms retrigger ∝ ρ/eps (143 vs 129 predicted).

**My one correction** — the surviving ψ direction's 18–24× headline charges only pad-band verifications; core-band false alarms (7–27% of intervals) ride free. Fairly charged, the win is 3.6–4.4× — the same unit-artifact class the author convicted the original of, but on the secondary quantity the author already demoted to a lead. The gold content — the named experiment killing the three-number record under real kicks — stands.
