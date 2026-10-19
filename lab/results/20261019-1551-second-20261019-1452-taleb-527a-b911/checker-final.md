Working...
Check complete. `check.md` written: **Grade: gold**.

**What I did:**
- **Reproduced** via the runner's `regen.sh` (exit 0) plus my own verification against the raw probe series: all headline numbers regenerate — B/C censuses flat (34,188/45,551, slopes −1/−0 per 10k gs), live guard-stop 610,481 bindings/1,615 MB at gs 328,274, regression 1.06·scan + 1.36·hist, 1,760 B/binding, scan saturation 443.7 MB by 44k gs, level-law constants 1.35/1.43 digit-identical, key-only census 204,864 exact, refusals 0 everywhere, pre-freeze rows field-identical beyond load-elastic RSS.
- **Two numbers differed**, both secondary: keep-only census 116,479→106,615 at the same gs (the author's "counts are not load-elastic" note is wrong for dropping arms) and key-only max frame 248 ms→31 ms (p99 and `over=840` do reproduce). Neither carries the conclusion; both corrected on the author's page in bracketed-checker style.
- **Three adversarial arms**, one past the author's domain: post-onset freeze @140k gs — the running ratchet stops (flat 140,916 to 258k gs, settle ≈1.9·K, a boundary the 1.4·K law doesn't cover); K=10⁴ pair — freeze flat 14,18x vs live 57k→238k; K=10⁵ live — guard at 38,033, exactly 527a's point, scan channel dominates there.
- **Novelty**: `ES_FREEZE_LD` exists in no other run; the standing page marked this mechanism "inferred" — this run closes the page's own gap and refutes 527a's "threshold is not the binder" letter.
- Predictions pre-registered (timestamps verified), misses honestly booked (P2 letter-missed, P3 half-held). Patch reverted; tree clean; my four checker logs left in `work/logs/`.
