Working...
Check complete. **Grade: gold** — written to `check.md`, with three corrections applied to the author's proposed page.

## What I verified

**Reproduction**: `regen.sh` regenerates `run-record.txt` bit-identically in 8.5 s; every dossier number (V1–V7, adjudication rows, contour brackets, P5=25.5, P7=21/21 vs 0/21) regenerates. de98's stored `eob_data.json` (fetched from its branch) independently confirms V4's exact reproduction (+13.092%/+5.419% raw) and the corrected column (+0.24% @30M, +0.70% @50M).

**Foundation audit** (my main attack): fetched the arXiv TeX of 1212.3169 and 1406.6913 and verified every constant — a₄, z₃, tortoise ⇒ A²/D, the energy map (exactly invertible, a perfect square), a₅^c/a₅^log, and the D = 1−6νu²+**2(3ν−26)**νu³ sign I initially suspected from other EOB papers; the cited primary source has this sign and the code matches it.

**Adversarial probes** (all outside the tested range, all confirm): 1%-crossing at 65–70M from off-grid p̄=55–200; e=0.95 stays e-mild (no cap hit); ν=0.15 linearity ratio 15.2–15.3; structure test extends ∝u below 80M; the 45/2-vs-27/2 j⁻⁴ corollary is **exactly right** (I retracted my own 39/2 — wrong circular j²; the code's r²/(r−3) checks against ISCO j²=12). Also mapped an inherited quadrature corner (e≲3×10⁻³, p̄≳300M) that touches no shipped row.

**Four secondary slips found, none load-bearing**: de98's corrected 20M value is −3.08% not −2.7% (page fixed); V4's caption swaps de98's stored 30M raw/baseline; "ratio 8.3≈3³" is the relative residual (absolute is 3³, physics right); "~1.3× at p̄≥15M" convention agreement is false at 15–20M low-e (up to 3.96× — page corrected). Predictions were genuine (held-out failures honestly reported; the load-bearing P2 held to 0.02 points).

The run resolves the wiki's standing ecfd-vs-de98 contradiction, deletes two wrong numbers, and hands r3 v4 a validated 8 s oracle in place of the prescribed 1.5 s numerical-GR reference.
