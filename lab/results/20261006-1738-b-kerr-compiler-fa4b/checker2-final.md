Working...
Check complete. `check2.md` written; tree restored pristine (nothing outside `lab/results/` modified, no commits).

## Verdict: **Grade: gold**

**Reproduced bit for bit** in a clean tree with `work/patch.diff` applied by me:
- Full gate run `G1–G6,B16,B19`: every number, count, and digest identical to `gates-after.txt` (only wall-clock differs: 0.26 s vs 0.27 s). B19 passes all six criteria; every Schwarzschild gate unchanged.
- Module tests 10/10; whole crate suite green; `gen_tables.py` regenerates `golden.json` identically; controls behave on both sides (echo passes; `planted-proonly`, `planted-penrose`, `planted-rcapture` fail).
- The 7 `xtask` test failures **pre-exist on pristine main** — verified by stashing the patch and rerunning them.

**Predictions**: `predictions.md` (18:30:01) precedes the decisive run (18:30:36). P2's first run failed retrograde fates via a pre-existing adapter bug (`scalar()` refused negative L/b); the fix is sign plumbing at the judge boundary, disclosed with both runs kept — not tuning on the frozen seeds.

**My attacks** (independent methods, three beyond the gate's domain):
1. Photon capture boundaries: my hand-derived b_c (double-root algebra, bisected) matches the author's closed forms to 30 digits, and `photon_fate` flips within ±1e-11 of it at all six (χ, sense) points.
2. E=1 retrograde boundary: flips within 1e-9 of my analytic L_mb = a − (1+√(1+a))².
3. Whirls at χ=0.9999, e=0.9, p=1.001×separatrix (104 rad advance): module matches my 40-digit quadrature to ≥10 digits.
4. Bonus settled independently: Kerr epicyclic frequencies give Δφ = 2π(1/κ−1) → odd part −8πχ(M/p)^{3/2}, refuting the prior run's −12π guess.

**Novelty**: H0214 froze B19 with the named gap "no Kerr compiler yet"; the prior silver built only the float reference. **Missed by the author**: `isco(a=1, prograde)` returns 6.0 at the extremal limit (sign-blind triple root; unreachable through the judge), and `cycle` at the CYCLE_MAX cap degrades silently.
