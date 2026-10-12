Working...
Check complete: **Grade: gold** — written to `check.md`, nothing else in the run folder touched (all reproduction done in `/tmp/check2`).

**What I verified:**

1. **Reproduction, bit-exact.** Built `window_clock.c` myself in a clean copy: 12 decisive belt cells, the p8 sweep cell, encounter u8/w0.5, and a u2048 truth part all byte-identical to `work/`. `analyze.py` regenerates every dossier number (p-K ladder +33.0/+10.0/+2.49/+0.50%, Δė 0.11→0.01, Jacobi 1.0× floor; ablations 2.5×/195×/90×; W-sweep; encounter inversion 2.43/2.78/0.60; pure-grid +2.0%).
2. **Provenance.** `predictions.md` (13:56:03) predates final code (13:56:44) and all decisive CSVs (13:59+). Truth seeds 0–15 md5-match the original run's committed `belt-truth.csv`; `work/orig/` matches the published branch (77443410). PB2–PB5 hold; PB1's letter miss at K=8 is self-reported and the kill criterion honored (K=8 demoted, closure claimed on the monotone trend, not one cell).
3. **Adversarial (4 own cases).** K=3: +48%/4.65 MADs — confirms the harmonic-alias mechanism and the K≥4 boundary. W=2.5 at K=16/32: −3.5% saturated, so the +0.5% headline is W-specific. Resonant under p8/p16 (the lens's named blind spot): clean (−2.1%/−0.6%), no phase-lock pathology.
4. **Gold rationale.** It is the first checker's pre-named experiment, executed with a reproducible record: the premise "the averaged term must be continuous" is refuted, tick-anchoring killed at every length, the seg fix-family deleted by phase anchoring, and the deployable rule (K ≥ 16 percent-level, K=2 forbidden) adopts in one step with no new component.
