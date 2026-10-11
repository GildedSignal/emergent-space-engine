Working...
Check complete. `check2.md` written; tree restored to its found state; `check.md` never opened; nothing else in the run folder touched.

**Grade: gold** — second checker, blind to the first.

What I did in the 45 minutes:

1. **Reproduction (clean tree, patch applied):** all 12 fast scenes + n1k byte-identical to the stored record (mod `sweep_s`/`meth_s`); raw `lbar` column matches the b292 record on all 9 original scenes; `taleb adj` reproduces the gold's numbers byte-level (disputed 197, missed 4, extra_true 193, rank_max 4, rank_probe 40 encounters); `summarize.py` reproduces the dossier table row-for-row.
2. **Provenance:** `orig-patch.diff` + `second-author.patch` = the shipped `invert.rs` exactly (`cmp` clean); `taleb.rs` verbatim. Rebuilt the **original b292 instrument** and regenerated c0/w1/d30 byte-identically from it, including the previously missing c0 line.
3. **Independent attack:** re-implemented Rng, fleet2, Body and `circ_rank` in Python and found closest approaches by my own scan — all four worst pairs match exactly in both rank columns (w1 [9,11]: mod 59 / raw 82, d = 4.131e-5). This breaks the same-harness objection for the fix. Fleet arithmetic re-derived: 11.4 TB (29% of quadratic) at formation density; 64 GB spread = 200× the gold's model.
4. **Predictions:** all nine held exactly, written before the runs by file time and log order; kill criterion pre-stated, not triggered.
5. **Adversarial finding of my own (recorded in check2.md):** the truth sweep's adjacent-bin-only check is marginally unsound at e ≈ 0.5 (angular bound 2.0e-4 vs bin 1.92e-4), so the e5 completeness carries an asterisk the dossier omits; and the raw metric under-reported as well as inflated (e10 worst: raw 59 vs mod 98), so the b292 numbers were direction-unsafe both ways.

The core refutation — the gold's rank-4 / O(n·4) premise dead on every order metric, λ̄-mod 28 max / 61.1% > 4 in the gold's own scene, distance-rank 10 at 5× density — stands on a regenerating record and survives independent reimplementation. Adoption is a re-aim of the unmerged `b-coorbital-cert` build: zero merge cost.
