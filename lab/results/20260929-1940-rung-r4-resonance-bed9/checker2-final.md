Working...
Both deliverables are written; the author's folder is otherwise untouched and no git commands were run. Summary of the check:

## Verdict on reproduction: exact
Every author number reproduces bit-identically in a clean copy (`truth_summary.txt`, `metrics.json`, per-case log, machinery checks, walls). `verdict.py` on my `metrics-check2.json`: **PASS** — candidates pass, negatives fail `pump,ctrl`.

## The finding that overturns it: the kick field is sign-inverted
`tidal_acc` implements $\frac{m_2}{R^3}(\mathbf{r} - 3(\mathbf{r}\cdot\hat h)\hat h)$ — the **negative** of the Newtonian quadrupole (octupole too; equivalent to $m_2<0$). Four independent proofs:
1. Series expansion of the exact tidal field.
2. Exact impulse at R1's first conjunction: **+1.89e-2** exact vs **−1.41e-2** code (negated: +1.41e-2, within the l≥4 truncation residual).
3. Anti-parallel dot products at generic points.
4. Behavioural: the corrected sign reproduces exactly what the author's version misses — C3 phase-lock (conc 0.85 vs truth 0.87, author's 0.19) and R1's libration centre (176° vs truth 157°, author's 355°).

**With the physical sign, both candidates are killed by the same frozen gates** (pumphi 1.51–1.56, C3 ctrl 0.44–0.45; formal `verdict.py`: KILL). The shipped PASS survives only because max-e and |⟨e^{iψ}⟩| are nearly invariant under field negation — the even-harmonic resonance mirrors about ψ→ψ+π.

Also flagged: R2's reconstruction never reaches the rung's frozen truth conc 0.867 under any reading of "w2 = 4.0" (0.51/0.20/0.31); adversarial detuning (ratio 2.05, μ=1e-2) over-pumps 1.6–1.8× even with the author's sign; the author's `dE` oracle omits all test-particle terms (weak, but covered by convergence plus my independent RK4 cross-check, which confirmed every oracle value to ≤0.03%).

`check2.md` recommends treating the PASS as void of adoption value: rerun with the corrected sign, freeze a phase criterion with an upper bound (the author's own "what would make it wrong" asks for it), and use the red-team's real ICs for R2.
