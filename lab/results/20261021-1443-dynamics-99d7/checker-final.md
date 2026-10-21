Working...
Check complete. Verdict written to `lab/results/20261021-1443-dynamics-99d7/check.md`; tree restored (only `lab/results/` differs).

**Grade: gold.**

**What I did:**

1. **Reproduction** — applied `work/patch.diff` to a clean tree, built, and re-ran the decisive arms myself: zone31 s1/s2 and bridge s1/s2 at step 4, `belte`, and the strong control all reproduce `regen.log` **bit-for-bit** (draws, per-ship Jacobi, Δe, kick counters), including the bridge s2 outlier 6.3e-5 and the strong-control death. Verified the instrument really is cbe6's `beltcad` verbatim by diffing against cbe6's own branch (scene, LCG/SEED dial, Jacobi expression, sampling, readout); re-derived the cadence semantics (32.9 counted kicks/ship/planet-period at step 4 = 2 combs × 16/pp) and ddeb's p = 0.334 independently (E[(a/5.2)^1.5] over [2,3) = 0.336).

2. **Predictions** — pre-registered with priors; all four named held-out cases held (seed 2, 400p, exact-resonance grid, 5:2). The decisive outcome was the author's own p = 0.15 branch, and the refuted mechanism sub-prediction is disclosed. One letter-miss: P1's "cbe6 to the digit" at strong step 5 failed (a death, one octave early) — disclosed in Evidence, though the Predictions header spins it as "held".

3. **Six adversarial cases**, one outside the author's range: 4:1 and 7:3 zones (the cells composed at 16 but never flown) **PASS** (2.3e-5/1.7e-5, Δe step-independent); third seed both arms PASS; 1,000 periods flat (2.2e-5, no walk); exact commensurability at e = 0.30 for 400 periods PASS (6.8e-5); 5:2 seed 2 PASS; and **e = 0.40 — the belt law's support edge — FAILS at 16 (2.5e-4)**, which lands inside the census's e > 0.23 carve-out already priced at 256: the domain edge is real, the claim's stated domain holds.

4. **Page corrections** (in the author's `wiki/kick-cadence.md`): the composed "550×" charged the 0.26% strong-tide class at 16 where cbe6's own control dies — corrected to **≈515–550×** with the caveat (the 7× row move is unaffected); two corrupted run ids restored to the real branch names (`20261010-2052-library-2d94`, `20261010-2141-dynamics-cd52`); my closing probes added as a checker bracket. Budgets hold (149 lines, 6-line current best, runs append-only).

5. **Novelty/goal** — cbe6 flew only the clean belt; ddeb counted and named these arms unflown; nothing in HISTORY or the wiki had measured them. The run refutes a premise upward (pendulum flag = birth label; 256/64 floors 16×/4× over-provisioned), moves the board's top macro row 7× (115 → 16.2 events/body/belt-orbit, headroom 78× → ≈515–550×), and adoption is a two-constant table edit with zero engine change. Not three agreeing golds yet (ddeb ungraded) — page stays open. Gold is subject to the blind second checker.
