Working...
Check complete. `Grade: silver` written to `lab/results/20261019-2339-inversion-1d47/check.md`, the author's proposed wiki page corrected in place.

**What reproduced:** the burst deletion is real — regen (exit 0) lands inside every disclosed band (10⁵ max 793.4→14.4 ms, 2×10⁵ 1,649.9→14.8, p99 into budget, stale 3,803/4,692 with the gate vs 0 without, refusals/dead 0), and the OFF digests match the M1 record bit for bit. Predictions were pre-registered (mtimes verified); P1/P3/P4/P5 held.

**What died:** the "bookkeeping, not a law / nothing to re-freeze" half. Three findings:

1. **The 14/14 digest identity is vacuous.** I probed the digest scenes themselves: stale = 0 on *both* arms in every belt/wave case — those small scenes never defer, so the identity was guaranteed a priori. P2's "constructive failure" was instrument blindness, not innocence.
2. **At the rungs where the deferral fires, the gate breaks the digest's schedule-invariance.** Using the shipped canonical-cut contract (`frame_to(limit=cut)` + `settle(cut)` — `check_cut` at 10⁵ and 2×10⁵): OFF is stable across reruns; ON is **bistable at both rungs** (10⁵: `ad732607…`/1770 ×3 vs `75543d72…`/1775 ×1; 2×10⁵: `bde05587…`/226,894 ×2 vs `61a8a10d…`/226,883 kicks ×1). The digest chains the encounter log, and the encounter sets move — "no encounter can flip" is refuted as stated (the light-cone fence is real in code, but it doesn't make the reads free).
3. **An instrument trap worth recording:** `limit = i64::MAX` (nladder's usage) lets the breaking frame overshoot the cut and resolve past-cut items — which also explains the author's undisclosed run-to-run `fixprobe` digest drift.

**To gold:** the author's own fence implies the digest-clean form — pull only ships within the scan's reach (never stale by the fence), leave the far wave to the queue — flown at 10⁵/2×10⁵ with the canonical-cut instrument. The gate as-is owes a digest re-freeze.

Tree state: author's patch applied (post-regen), my instrumentation reverted; no commits made.
