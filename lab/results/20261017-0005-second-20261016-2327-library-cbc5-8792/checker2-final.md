Working...
Check complete. `check2.md` written, page corrected.

**Grade: gold.**

**What I verified:**

1. **Reproduction** — the runner's `regen.sh` (exit 0) output `regen-table.txt` equals `ledger_out.txt` on every counter, digest, promotion, hit, resident and miss rate; only timing noise differs. Binary sha256 matches; the patch delta over 0619's is exactly the claimed instrument (demote timing, mid90 probe, `ES_RETAIN_DWELL` sweep — cache policy only, proven digest-neutral on all 24 arms). Anchors regenerate bit-for-bit: 1d52 coast (131,053 / 763,888 / 100,788), 0619 burn (130,187, terminal 102,276).

2. **Predictions** — `predictions.md` (mtime 42 min) predates all flights (27 min); adjudication honest, undershoots disclosed. One undisclosed nit: predictions named dwell 10, flights flew 17 (frame = 16.7 gs at rtf 1000); immaterial.

3. **Five adversarial flights** (all outside the author's grid, one process at a time, digests checked):
   - dwell **5** burn: miss 74.8% — cliff-left plateau extends a decade down
   - dwell **80** burn: miss 71.1% — the cliff is a band in **80–100** gs, tighter than the page's 60–100
   - dwell 100 burn **seed 3**: miss 14.0% (vs 14.3% seed 1), digest identical to its own seed-3 ctl — cliff-right is seed-stable
   - dwell **10000** coast: standing resident 115,276 ≈ N — the coast dial saturates beyond ~2000 gs, re-mints exactly 1.00× retain's
   - ctl seed 3 (identity anchor)

4. **Novelty** — this is the published `lab/wiki/promotion.md`'s own Open direction 1, and it resolves the page's 0619-vs-λ×dwell contradiction; no H-entry covers it.

**The one dossier defect:** "promote p50 = 3.7–4.9 µs over every arm" is false — the re-mint-storm arms measure 5.24 (twice) and 4.96 µs. No conclusion changes (5.3 ≪ 23.1 µs budget; margin 4.4× not 4.7×; the composed-core arithmetic uses retain-arm mints). The proposed page already carries the corrected 3.7–5.3 range; I tightened the cliff bracket to 80–100 and folded in my seed-3, dwell-5/80/10000 points. Gold stands on both checkers.
