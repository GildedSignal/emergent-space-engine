Working...
Check complete. Written to the run folder: `metrics-check.json` (my reproduced numbers) and `check.md` (abstract + reasons). Nothing else in the folder was touched; author artifacts verified untouched by mtime.

**Verdict (verdict.py): KILL — nf1 and nf2 fail every behaviour criterion** (pump [0.44, 1.93] vs [0.8, 1.25], libration amplitude 0.28/0.26 vs 0.8, regime 17/18, controls 2/3). Positive `truth-1200` passes; both negatives fail as required; no author/checker dispute.

What I established, in order of load:

1. **Oracle sound.** Truth ladder 600/1200/2400 regenerated **md5-identical** from the delivered scripts; converged (worst rel emax diff 1.4e-4). Independently verified with my own from-scratch barycentric RK4: 2:1-μ3e-4-0 emax 0.07259 vs 0.07270 with identical libration amplitude 1.1973; ctl2.55 identical. Kepler round-trip 3e-12. `metrics.json` recomputes exactly from stored series.
2. **The kill is real.** Pump ratio sweeps monotonically with detuning at both resonances and all three μ — the law's island is displaced in n₁ relative to the truth's. Structural, not noise; exact-commensurability cases pass (dev-tuning shows through), held-out detuned cases fail consistently.
3. **But the delivered code is not the code that produced the artifacts.** `run_all.py laws` crashes on case 1 (cycle compiler burns 800k evals); my term-by-term reimplementation fails the same case and diverges on one it compiles (closed=False vs stored True; |Δe| 8.8e-3). `r4v3.py`'s mtime (05:25) postdates the artifacts (05:11). No dossier, no required phase portrait, `author-final.md` still "Working…".
4. **Frame defect named.** The canonical resonant pair conserves L̂₁ = Λ₁ − jΓ₁ with K = −m₀²/2Λ₁² − (j+1)n₂Γ₁ − R̄; the code uses Λ₁ + jΓ₁, +(j+1)G, +R̄ — the mirrored invariant line is exactly the axis the failures run along. My corrected-frame build also fails (pump [0.00, 1.84], regime 7/18, 11/21 compile failures at a bounded budget), so the corrected construction with a robust cycle compiler is the named next experiment, not a demonstrated pass.
5. **Adversarial:** arc-g8 crashes at μ ≥ 3e-4 and understates its own cost (evals of a truncated run over the full-run orbit count); predictions.md pre-dated the decisive run and its held-out predictions failed badly.
