Working...
Check complete. `check.md` written to the run folder; tree restored (worktree removed, nothing else in the run folder touched).

**Grade: silver** (as second checker, blind to the first).

**Reproduced:** patch applies to `a838a28`; all four decisive runs regenerate every non-timing field bit-for-bit (counts, bytes, digests, samples); unpatched kick-bench digest equals patched (`eccc7f5a…`); replay digest deterministic across the author's and two of my own repeats; the boundedness/accounting test passes; predictions.md (20:56) precedes the data (21:11–21:13).

**What holds:** the removal side is now measured — first measured compact-machinery costs, first measured packed footprint (14–62 B/member vs the plane's 4.4 KB/body), squarely on the 10⁹-in-8 GB bottleneck. The exact-Q48 side's death is solid by measurement: ≥0.28 cores even at the information-floor capacity model, 5–11 cores by rows.

**What breaks gold:**
- The decomposed model's 0.18 µs/row marginal is a units slip — 141 µs ÷ 757 *updates* while only 34 *rows* were sealed. My discriminator (`rtf 1000, 10 s`: constant ~355 updates/window, rows 15→32, cost 117→142 µs, repacks fixed) shows cost tracks rows at ~1.5 µs/row, ~8× higher. Corrected coarse duty at 10⁹: ~0.05–0.17 cores — under the 0.2 kill line but with ~2× margin, not the headline's ~10×.
- The pre-registered kill letter fired on the direct linear scaling in **3 of 4** runs (dossier says 2 of 4; it drops m400's 0.325), so P1 "held" rests on the unmeasured MAXG-occupancy assumption plus the flawed marginal — the ~2 % claim is still model-bound, not "closed by measurement".
- Two table denominators (s7: 1449 vs 1506; rtf1000: 769 vs 827) don't regenerate from the stored JSONs; the wiring half of the brief (--bench/page) was skipped (disclosed).

**For gold:** measure row/repack marginals at one synthetic 65,536-member group at the same per-ship rebind rate — that replaces both scale models with a measurement at the real 10⁹ group shape and decides the kill line without a model.
