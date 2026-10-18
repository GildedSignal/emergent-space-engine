Working...
Check complete. **Verdict: `Grade: gold`** — written to `check2.md` in the run folder.

**What I did**

1. **Reproduced**: ran `regen.sh` myself (18 s, exit 0). Output reproduces `run-log.txt` byte-identically modulo the timing line; JSON matches the prior regen modulo the price arm. Verified the `-orig` reference copies are md5-identical to the original 22d1 branch, so the PG/tell comparisons are against the true original. All dossier numbers regenerate: six corrected onsets, closed-form residuals ≤ 3.6e-12 s, 0 arc mismatches in 11 cells, the tell (+125.1344/+125.1206 → +0.3855/+0.3809), PG violations `[]`.

2. **Re-derived the math independently** — all four onset closed forms, the W3 root formula, and both arc predicates check out algebraically; the oblique predicate `d²(sinψ+v_y)² < R²(1+β²+2v·Ê)` is exact.

3. **Attacked outside the author's domain** — all held to machine precision: β=0.99 (Jaccard 0.1411 = √(1−β²) exact, onsets ≤1.4e-14 s), d=1000R (onset error matches closed form to 0.0e+00, converging to the claimed limit), oblique 20–135° at β 0.5/0.9 (0 mismatches everywhere), and **oblique onsets** — never covered by any certificate — matching my own closed form to ≤2.2e-15 s, which proves FIX 1's general quadratic in the regime the run never looked at. The buggy-column replication equals the original's published onsets to 0.0000 s in all 12 cells.

4. **Predictions**: pre-registered before the decisive run (file order verified); PB's planet-β sub-clause failed and was honestly reported with numbers I confirmed — a refutation that strengthens the kill (the original instrument was biased at every β).

5. **Page**: fold-in faithful; corrected one overstatement in place — the oblique qualifier's "0.53–0.99" range (my sweep: 0.46–0.99, meeting the transverse √(1−β²) at 90°). Topic stays open (not three agreeing golds).

Nothing else in the run folder touched; no git operations.
