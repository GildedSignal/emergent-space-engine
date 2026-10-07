Working...
Check written. Summary of the verification:

**Grade: silver** — `lab/results/20261007-0621-scout-6e10/check.md`

**Reproduced bit-for-bit** in a clean tree (empty patch.diff — author touched nothing outside its folder): both scripts regenerate the stored outputs identically (5.8 s, 485 MB RSS; `stock_vs_flow` → 44.82 bits, 33.2× overcount). `predictions.md` (06:28) precedes the decisive run (06:39); the JSON regenerated at 06:42 is identical to the logged capture — no post-hoc edits. Both controls pass exactly.

**Numbers verified analytically, not just re-run**: 40.22 chaotic bits = 2·log₂(σ√(2πe)/q); carry 2.105 ≈ √(12/12)·4.13 = 2.04; M-column's 0.255 = initial-quantization entropy; battle λ=6 → 48.8 analytic vs 48.9; all `ledger_1e9` figures re-derive. Premise confirmed verbatim in law.md:13 ("about +62 bits per kick and −60 per reabsorption"); no H_live measurement exists anywhere in HISTORY.md or prior runs.

**Adversarial findings** (all in check.md):
- **A1**: the smooth "0-bit" pole is program-relative — a sin(2M0) smooth kick leaves 39.0 bits, indistinguishable from chaos, under the run's own basis. The 0-vs-40 typing is event × program, not intrinsic.
- **A2**: heavy-tail caveat is mis-signed (Gaussian formula *overestimates* by 2–17% at matched σ); pole robust.
- **A3**: correlated roundings make the carry walk superdiffusive (var/rounding ≈ 1 vs 1/12; 10× roundings → 10× σ), but the sub-GB conclusion survives; the real law's exact-integer drift makes the carry an allowance, not a floor.
- **A4**: q16 prose arithmetic understated (24.2 bits not 21; 3.69 GB not 2.7).

**Why silver, not gold**: the rubric requires held-out predictions to hold — P2 and P3 failed (honestly, and P3's kill criterion fired on the author's own war-cap claim, which was deleted); and the poles sit on invented distributions (50/50 coin-flip split, chosen σ scales). The stock-vs-flow structure is verified independent of those choices; the mix is not. One experiment to gold: run the queued `b-h-live` build to measure real kick mixes and basis shapes on the engine's own path.
