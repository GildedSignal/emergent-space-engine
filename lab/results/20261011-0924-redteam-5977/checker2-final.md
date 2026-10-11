Working...
Check complete. Verdict written to `lab/results/20261011-0924-redteam-5977/check2.md` (only file added; author's folder otherwise untouched; check.md never read).

**Grade: gold** (blind second checker).

**What held under reproduction:**
- `falsifier.py` regenerates `falsifier-results.json` with **zero numeric differences** (9.5 s, single process, <200 MB); `work/patch.diff` empty — no tree edits.
- All headline numbers confirmed: delay 3.14–7.31M, phase error 4.33–10.07° (median 5.13°), memo residual max 50.1°, controls 0.101% / ≤0.011°.
- **Independent truth check**: a first-order r-space quadrature of the null travel time agrees with the script's φ-ODE to 10⁻⁹–10⁻¹⁰ at the claim's endpoints (Φ=0.3, 2.7). Φ=1.5 differs 0.2% — a near-tangential-emission degeneracy, not load-bearing.
- **Letter claims verified against the docs**: law.md:53's memo is direction-only; no gate B0–B19 judges retarded time; B11's allowance `(1% + 2·8/p)` verbatim; r5/r6 absent while law.md assigns them to GLM; representation.md §1 still teaches the killed Minsky/Binet map. Novel vs B16 (direction-only) and H0183 correctly cited as the oracle-side Shapiro source.
- Predictions: P1/P3 held, P2's inequalities held (stronger sign-unsafety found), P4 missed one point (p=25) and was disclosed — the miss overstates the attack, not under it.

**My adversarial extensions:** error rises monotonically toward conjunction to 9.9M / 13.6° (headline is conservative); far-field error decays to 4×10⁻⁴° (no numerical floor); and **the stated fix is under-specified** — at matched b, delay differs 4.58 vs 3.72M between scenes in one doll, so a `delay(b)` column alone leaves ~1.2° (≈12× the dossier's own 0.1° criterion); the memo key needs geometry. Also: the p=12 headline quotes B11 outside its frozen domain (p 20–1000), though in-domain points carry the padding argument.

Gold rationale: a premise on the "must be perfect" surface (principle 30) shown wrong with two-sided controls, guards verified absent, clean record, and adoption (the r6 criterion) is one step — the memo's final shape is the integrator's design call, informed by my A4.
