# Predictions — 20261015-1450-second-…-0757 (written before any hot-cache flight)

Build: the run's patch (seam + global `ES_RETAIN`) plus a **bounded** retention arm,
`ES_RETAIN_HOT=<cap>` (default 4096): the per-slot `RetainCache` hit path is kept unchanged
(it survives the store's record clones and is the measured 85–95%-hit path), but every mint
registers its cache in one global FIFO ring; over cap, the oldest registration is evicted
(`take()`n), so live retained entries ≤ cap always. Global `ES_RETAIN=1` stays as flown.
Arms per scene: ctl / seam (`ES_LAZY_ENTRY=1`) / retain (global) / hot (`ES_RETAIN_HOT`),
same binary, canonical-cut digest.

Scenes: coast 10⁵/20k s1 and burn 10⁴/20k s1 (the checker's two named arms), plus 10⁴ coast
20k s1 (continuity with the record's anchors) and 10⁵/48k s1 (the wall residue grows with
wave count under global retention — does it under hot?). Cap probes on coast 10⁵/20k: cap 512
and cap 65536.

1. **Identity.** Digest bit-identical across all four arms on every scene: eviction only
   changes *when* compiles happen, never values (`Orbit::compile` is pure; the digest hashes
   the demoted key, not the entry). Any difference: VOID, instrument broken.
2. **Bound holds.** `retained_now` ≤ cap at the cut on every hot flight (the ring enforces
   it structurally; the prediction is that nothing else keeps entries alive: a slot dropped
   by a kick's settle releases its Arc).
3. **Hits survive eviction at cap 4096.** Hits ≥ 80% of demoted reads on coast 10⁵/20k
   (global arm measured 85.4%). Arithmetic behind it: the hot set is ~350 locals re-hit
   every ~9 ms of wall; belt mints ≈ demotions/flight ≈ 131k over ~20 s ≈ 6.5k/s; ring
   residency at cap 4096 ≈ 0.6 s ≫ 9 ms, headroom ~70×.
4. **Promotions stay at the kick floor.** Hot promotions ≤ demotions × 1.5 at 10⁵/20k
   (global measured exactly 1.0× = 131,053; hot pays extra only for evicted-then-reread
   locals; the belt's mints are the kick bill itself and are identical under both).
5. **Memory win restored.** rss(hot) within +10% of rss(seam) at 10⁵/20k (≈ 386 MB; the
   cache itself is ≤ 4096 × ~1.5 kB ≈ 6 MB + allocator slack) and below rss(ctl) 538 MB;
   clearly below rss(retain) 548 MB.
6. **Wall.** Hot wall within +15% of ctl at 10⁵/20k (global retain measured +6.5%): the hit
   path is unchanged and compile time stays ~1.4 s (vs seam 12.4 s). At 10⁵/48k hot wall ≤
   global retain's 27.5 s (its residue grew with waves: +0.7/+2.8/+8.8 s at 20k/48k/100k;
   hot pays the same per-read machinery, so this may tie, not beat).
7. **Cap cliff exists (falsification arm).** At cap 512 (≈ 1.5× the ~350-local hot set but
   only ~80 ms of ring residency at the 6.5k/s mint rate) hits fall materially below the
   cap-4096 arm (prediction: < 70%, promotions > 2× demotions): the policy needs headroom in
   *time*, not just in *count*, because the belt's one-per-interval mints are the eviction
   pressure. At cap 65536 hits ≈ the global arm's (763,888 ± re-mints).
8. **Burn arm.** On burn 10⁴/20k (the checker's case 1 flown under hot): digest identical,
   promotions ≤ 1.5 × demotions (global measured exactly 40,187), hits ≥ 88% (global 93.6%
   at higher mint density — residency shrinks with mint rate; 10⁴ belt mints ≈ 2k/s, so
   residency at 4096 ≈ 2 s, even safer).

Kill rule (frozen): if at cap 4096 on coast 10⁵/20k hits < 60% of demoted reads or rss(hot)
> rss(retain), the bounded rule as named (per-slot caches + FIFO eviction) is wrong — the
hot set does not survive eviction — and the adoptable form must key the cache by orbit key
(a shared map), not by slot. Report as KILL of the slot-FIFO variant, not of bounded
retention.

Not measured here: the 10⁹ residency arithmetic beyond the composition argument (locals hit
every frame ≈ 16 ms ≪ 0.1 s at the 10⁹ mint rate — extrapolated, not flown), the M1 compile
price, contacts-rich scenes (the `same()` experiment stays open).
