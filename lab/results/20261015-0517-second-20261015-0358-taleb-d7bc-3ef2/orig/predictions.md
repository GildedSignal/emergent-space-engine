# Predictions (written before the decisive flights)

Scene: `plane_extra_band` (this run's patch), the player a circular 2.5 AU body of the root doll among the belt ships; L8 prograde burn held from wall second 1; rtf 100; 12 ms budget; cut 16,000 game-s; seed 1. Cap = `ES_SCAN_STANDING` (MiB), off by default (shipped verbatim).

Cases I have NOT tuned on (the record's numbers, not mine, set the expectations):

1. **P1 — the ruin reproduces, bounded:** N=10⁵, cap off, self-kill at 1,500 MB RSS. Expect SELF_KILL in under ~3 min wall, with the standing bytes climbing monotonically, each mint O(N) (~20-30 MB of capture + pinned entries; c481 measured 29.4 MB/mint standing). If standing stays ~0 or RSS plateaus under 1.5 GB to the cut, my scene fails to mint and the run is VOID.
2. **P2 — the cap holds the same digest where shipped completes:** N=10⁴ in-band: cap off completes (d7e3's checker: ~1.36 GB, one answered scan), cap 64 MiB completes with the **same digest, bit for bit**, and the same encounters count. If the digest moves, the cap changed which scans are answered, not just when — the guard is wrong (answers must keep their set and order; the digest counts held as answered).
3. **P3 — the kill disappears:** N=10⁵ in-band, cap 64: the flight reaches the 16,000 game-s cut with peak RSS under 2,000 MB (shipped dies at ~7-12 GB), peak standing ≈ the cap plus at most one mint's overshoot (~90-100 MB), and a digest exists where shipped has none on this box.
4. **P4 — the price is frames, not ruin:** the capped arms pay the answers inside frames: frames over 12 ms grow (tens to low hundreds) and worst frames reach tens to hundreds of ms, with the presented time lagging seconds; encounters counts stay equal to the uncapped arm's at 10⁴. If worst frames stay under ~13 ms at 10⁵ capped, the answers were free and P3's mechanism claim is suspect.
5. **P5 — inert where scans are small (at Home):** N=10⁵ at-Home L8 burn (band=0), cut 12,000: cap 64 never fires (peak standing far under the cap, held scans standing as shipped) and the digest matches the cap-off arm's bit for bit.

Kill criterion for the guard itself: any digest mismatch inside a completable pair (P2, P5), or peak RSS over 2,000 MB under the cap (P3), or a capped flight that cannot reach the cut within the wall cap.
