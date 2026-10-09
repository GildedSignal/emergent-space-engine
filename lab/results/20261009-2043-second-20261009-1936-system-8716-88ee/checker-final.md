Working...
Check complete. `check.md` written to the run folder — grade: **gold**.

**What I did:**

1. **Reproduction** — all six shipped commands (`equiv`, `equiv3`, `truth3`, `sweep2`, `scale2`, `truthres`) in a clean tree, empty patch.diff: every output file byte-identical to the author's. Timings match stated budgets (equiv 48 s, truth3 78 s). `unified_old` verified verbatim against the original's `unified` (name/docstring only), so the old-defect reproduction is honest.

2. **Pre-registration** — file times confirm predictions.md (20:48:04) precedes every result file (20:53+); the 5(eᵢ+eⱼ) constant untouched; the dev smoke scene (seed 99) appears in no registered command. All six predictions held, including the honest directions (P4 beyond-domain, P5 re-reporting the original's falsified √N·log growth as still falsified).

3. **Soundness** — verified the domination argument factor-by-factor in the code (dn_bound = exact sup over bin occupants, eb ≥ ēᵢⱼ, span ≥ Rᵢⱼ + skin_u, floor-monotone bin coverage, |ΔU| = inner boundary on the bin side).

4. **Seven adversarial classes of my own** — one-bin concentration, const-p e = 0.7, H = 64, exact duplicates, N = 2, five e-boundary seeds: all 0 drops / 0 adds, recall 1.0. The old index fails two classes the author never tried (832 drops on duplicates, 9,072 at H = 64).

5. **Novelty** — the exact per-bin |Δn| bound appears nowhere in HISTORY/board; r8's kills were cost-side, not this structure.

**One blemish flagged (didn't cost the grade):** the dossier's sweep ratio "0.049×–0.80× of cone-only" contradicts the shipped sweep2.jsonl — actual is 0.70–0.91× (0.049 is a C(N,2)-denominator slip); "far below cone-only" only holds on belts/mixed (~0.5×). All decision-relevant numbers regenerate, so it's a prose label error, not a record failure. Also noted: the fixed-arc fleets don't cleanly test the original's fixed-volume prediction 5.

Nothing else in the run folder was changed; no git operations.
