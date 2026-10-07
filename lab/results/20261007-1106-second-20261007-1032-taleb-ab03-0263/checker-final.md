Working...
Check complete. **Grade: gold** — written to `check.md` (the only file changed in the run folder).

**What I did:**

1. **Reproduction** (clean tree, empty patch.diff): all three scripts regenerate their JSONs bit-for-bit on the first try — `hlive_probe2.py` (22 s, rows identical to the shipped hlive2.json, script md5-identical), `twin.py` (178 s, twin.json identical except wall_s), `followup.py` (12 s). The twin's `frozen` rows equal the shipped record bit-exactly at 1/5/20 yr; the regeneration claim is literal.

2. **Pre-registration verified by mtimes**: twin.py 11:27:48 → predictions.md 11:28:30 → twin.json 11:33:58 (wall 173 s). The pre-registered kill criteria fired as written and were honored — three mechanism predictions falsified and reported.

3. **Four attacks**:
   - **Held-out seed 20261008** (full twin rerun): refutation replicates (resid 109.01 vs frozen 109.07; var explained ≤ 0.0077).
   - **Tail quantiles at 60 yr**: median saturates as claimed, but p99 grows 0.022→0.094 AU and >0.05 AU fraction 0.16%→3.3% (5→60 yr) — "bounded" is a median statement; recorded as the number B18b's redesign actually needs.
   - **Independent ring-field validation** (my own quadrature + RK4, no shared code): reproduces the twin's secular precession. A feared factor-2 discrepancy against the Laplace–Lagrange formula turned out to be my remembered formula being wrong, not their code — two independent code paths agree; the w/M refutation stands on correct physics.
   - **Ratio audit**: var(twin)/var(full) = 8×10⁻⁵–3.7×10⁻³; the verdict survives every amplitude definition.

4. **Warts recorded** (immaterial): the "~66×" amplitude figure matches no regenerable statistic (rms 112×, bit-mean 40.6×, median 36×); "≤0.03% explainable" understates the w/M cap (0.4%); the twin omits the averaged indirect term; "15.5 bits flat" is the E column only (4-column total reaches 22 by 20 yr).

Gold rationale: the decisive experiment named by the previous check, reproduced bit-exactly and on a held-out seed, with the instrument independently validated — it refutes the premise both ways (no secular program absorbs the belt's drift; the drift is not irreducible per-body information), and adoption costs zero code.
