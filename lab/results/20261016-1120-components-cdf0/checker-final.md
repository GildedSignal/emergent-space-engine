Working...
Check complete. **`Grade: silver`** written to `lab/results/20261016-1120-components-cdf0/check.md`; the author's `wiki/scan-queue.md` corrected in place where it overstated.

**What I did:**
- **Reproduced** from a clean tree (applied `work/patch.diff`, rebuilt, flew all four flights): every deterministic cell matches bit-exact — captures 2095 with fallback 546/416/183/0 (26/20/95/0%), reads/hit 15/73/481/46, µs/read 4.4–9.0, min-miss/reach med 1.03e3/1.03e3/487/1.01e3 (min 11.3), root doll 6 ids → 5 candidates, 0 hits, min-miss 97.4; kicks match the published ladder to 3 digits, refusals 0.
- **Attacked out of range:** N=10⁴ burn (fallback 0%, reads/hit 46 — the fallback disease ends between 10³ and 10⁴) and N=10⁵ coast (fallback 0% vs 95% at 10³, while the answer half persists: kept 183, reads/hit 267, min-miss 487). Both hold the author's mechanism.
- **Found the record's flaws:** the capture-half mechanism (`bodies/4 + 64` fallback) was a2c1's first (20261014-1511, silver, `nladder.md`), uncited — the "Nobody had decomposed S" premise is wrong for that half; a2c1's `speed_cap` window poisoning is a cause the run never names; "28–2,128 bodies / threshold 71–597" is wrong (flown max 1,076 / ≤333; mechanism unaffected); `analyze.py`'s CAP regex is stale (`cap_us=` missing) so the regen aggregates print `doll=-1` and the per-doll table cells regenerate only under a corrected join — which I verified reproduces them.
- **Predictions:** P1/P3 held, P4 half-held, P2 failed by its own pre-registered kill clause and is honestly reported as failed.

**Silver, not gold:** the cure (angular key certificate) is priced with three orders of measured slack but not built, and the belt-bin flight (player inside the belt) is absent. The one gold experiment: build the integer angular certificate, fly the ladder plus a belt-bin flight, show digest-identical outcomes with S < b/2 — that closes scan-queue's open direction 1 as written.
