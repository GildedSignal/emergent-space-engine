Working...
Check complete. Deliverables: `metrics-check.json` (reproduced numbers) and `check.md` (abstract + reasons) in the run folder; nothing else touched, no git commands.

**Verdict (verdict.py, my metrics vs author's): KILL — kick-avg and hill-torus die on precession; truth passes; no-tide fails exactly one way; zero disputed outcomes.**

What I did and found:

**Reproduction — bit-exact.** All dossier commands in a clean tree: `truth.py` identical in all 256 rows including nfev (44,430,563; 288 s vs 290 s), `verify_secular` 3.94e-15, 81/256 declared tori, metrics identical (kick-avg prec 0.5536/τ₀ 0.0036, hill-torus 0.1333/0.046, no-tide 0.0), tolerance ladder 0/0/0.00%. Aggregates recomputed independently from `table.json`: all match, including the 25 kick failures at a/R_H ∈ [0.171, 0.299] and compiled_fraction 11/239.

**Independent oracle.** My own barycentric-inertial integrator (different formulation, my osculating elements) on 25 adversarial seeds (all 4 chaotic, both escape edges, deep seeds, domain edge, largest tori, smallest |ν|): every non-chaotic class and every non-chaotic ν agrees. The only disagreements are chaotic-flagged seeds — which is what the flag is for, and none sit in a scored domain.

**Three adversarial findings** (in `check.md`):
1. **kick-avg's de/dt sign is mirrored** against the Hamiltonian in its own docstring: the truth's e-trace correlates −0.89 with the shipped code and +0.89 with the flipped sign, both senses. The author's deep-see validation couldn't catch it — the mean precession rate is sign-insensitive to the 4th decimal. Corrected: prec 0.5714, τ₀ 0.0039 — KILL unchanged, but the shipped candidate isn't the documented model.
2. **The 10% window is meaningful**: only 4/155 bound seeds drift >10% half-to-half, and none of the 25 kick failures — the precession KILL is physics, closing the dossier's own hedge.
3. **The retro "zero crossing at 0.3 R_H" is wrong**: the truth's rate plateaus at −0.027 there (turning point); the real zero crossing is 0.51–0.57 R_H. Wrong mechanism sentence, unaffected numbers. The hill-torus e-grazes-zero mechanism is confirmed directionally (passes keep min|z| ~0.07 vs fails ~0.02).

**Predictions** predate the decisive run (mtime order verified); hits and misses are as the dossier reports. Novelty holds against HISTORY/law.md — this rung splits law.md's single τ₀ = 0.08 into a class edge (~0.085) and a precession edge (0.0036), which is the measurement the regime selector actually needed.
