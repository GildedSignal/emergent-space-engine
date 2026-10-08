Working...
Check complete. `lab/results/20261008-1252-spacex-d4e7/check.md` written; tree restored (patch reversed, probe variant removed); nothing else in the run folder touched.

**Grade: silver** (agreeing with the author's self-grade, with the gold experiment sharpened).

**Reproduced:** all three dossier commands bit-identically (main table, seed control ±0.01 GB, m=2¹⁸ size control), each ≤ 8.2 s at 3.4 MB RSS. Truth physics independently verified via scipy quadrature of the Laplace coefficients (e_F 0.0235–0.0342, g 1.00e-3–3.77e-3 rad/orbit — 4 digits). predictions.md (12:58) provably precedes all outputs (13:01–13:08).

**Five adversarial cases:** near-perturber belt (α 0.85–0.95 — step-and-flatten robust, RK4 leak grows 13.8→49 bits confirming the cadence mechanism), e_J=0 (E/L scars vanish — amplitude mechanism confirmed), joint 3-column encoding (−2 bits only, encoding was fair), signed wrap reduction (−1 bit), and a column dump.

**Two findings the author missed:**
1. **2π rate mislabel** — the run's secular phase advances at exactly 2π× its own printed control (measured 0.628 rad vs 0.09996 at T=100; `n = 2π/a^1.5` should be `1/a^1.5`). All time labels are mislabeled by 6.28×; the P1 "one wrong constant" post-mortem is actually two constants (e_F explains the level, the 2π the timescale). Every saturation number stands — the control was a printed formula, never wired to the dynamics.
2. **ϖ column decomposition** — ~20 of its 33 bits are a Poisson-gap ramp the shipped codec can't compress but a parametric generator reabsorbs; with it the naive wall drops to ~63 bits ≈ 7.3 GB, just *under* 8 GB, leaving E+L ≈ 51 bits as the irreducible core. Thin margin for the b-h-live build before the unmeasured residue.

**Gold path:** measure the residue (resonances, encounters) against a law-exact compiled generator, with the control wired and the ϖ scar in its signed representative.
