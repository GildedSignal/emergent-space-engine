Grade: lead

# Check — 20261018-1025-spacex-22e8 (spacex lens)

Grade: lead

**Abstract.** Reproduced bit for bit (census counters, anatomy, engine_decoded; recompile
4,651–4,684 ns vs the dossier's 4,711–4,758, ~1.5% high) and extended: seed 2 → belt 0/9,700
decoded; N=3×10⁵ (outside the tested range) → 0/299,700, 66 decodes/game-s, 777 MB peak; past
the wave (15,000 game-s, rtf 1,000) → belt 9,700/9,700 read exactly once, ≈1 decode per body
across 33,614 kicks — "read once at the event that pays a compile" confirmed, not per-frame.
But the deletion this prices is prior art on this page: 0e37 (write-only in flight), 760f
(4.6 µs compile, 672 B knots, bit-identical), b9ae/8b89 (the lazy delete flown
digest-identically, births included, floor 680 B/B vs the 478 predicted). New: the per-class
decode census at the current commit, the byte anatomy, the shipped `bytes_of` undercount.

## Reasons

1. **Reproduction: exact.** Applied `work/patch.diff` to the clean base (487a05b8), built,
   re-ran the coast-10⁴ arm solo: every census counter (63,546/2,846/116,462/267), the
   anatomy lines and `engine_decoded BELT 0/9700` match the stored logs digit for digit.
   The runner's regen (exit 0) matches too. The only number the dossier states that no
   regen run produces is the recompile range 4,711–4,758 ns (regen: 4,651–4,675; mine:
   4,684) — a ~1.5% slip, inside P5's 3–10 µs letter.
2. **Predictions.** `predictions.md` predates the out logs (mtime order at session end);
   P1/P2/P4/P5 hold, P3 half-missed and the dossier reports the miss against itself
   (knots alone 45.6% < 50%; deep sum 59% of process-level, outside ±15%). Good faith.
3. **Adversarial arms (all confirm the physics):**
   - Seed 2 (a different world, `plane_extra` seed arg): belt 0/9,700 decoded, 269
     distinct decoded — the zero-reader belt is not a seed-1 artifact.
   - N=3×10⁵ (3× the author's max): belt 0/299,700, decode rate 66/game-s (O(1) in N),
     peak 777 MB — under the 2 GB budget, no regime change.
   - Past the wave (rtf 1,000, 15,000 game-s, 33,614 kicks): every belt orbit read exactly
     once (9,700 decodes ≈ 1/body, vs 8.7M if per-frame). The dossier's own caveat —
     "read once, at the event that pays a compile anyway" — is the measured truth, and
     P1's kill criterion does not trigger even past the wave.
4. **Novelty: this is the page's own prior art, uncited.** The claim's three parts are all
   on `lab/wiki/nladder.md` before this run:
   - compiled orbits write-only in flight, retired 0 reads, flight reads O(1) in N —
     **20261014-1221-components-0e37 (silver)**;
   - recompile = one 4.6 µs compile, bit-identical 120,083/120,083; knots 672 B/body —
     **20261015-0250-scout-760f (silver)** (same 672, same 4.6–4.7 µs);
   - the delete itself **already built and flown**: b9ae (lazy variant, digest
     bit-identical on 4 arms, standing knots → 0 MB, 1,603 → 1,002 B/B), **8b89**
     (ES_LAZY_ALL demotes births too, digest-identical, standing arcs → the centres,
     **680 B/body at the belt's birth state** — the already-flown floor vs this run's
     predicted 478), e0f9 (committed, rss −28%), 0619 (gold, the re-mint price law).
   The frozen ladder artifact itself (artifacts/runs/nladder/ladder.txt:147, break 4)
   already says the compiled shape is "a cache of the key … the representation's lever,
   not a prune rule", prices 2.6→5.1 kB post-kick, and pre-states "a lazy birth … is bit
   for bit; ladder_digest's 13 cases are the check." memory-h-live adds compile purity
   (bit-identical duplicates) and "58% … a cache, not state" (5465). The dossier and the
   proposed page cite none of these and present the pricing as the wall's first.
5. **Instrument nits (immaterial).** The anatomy's `entry_cur` (304) already contains the
   16 B Arc header that `arc` counts again — true birth deep ≈ 1,456 B, orbit share 67%
   unchanged. "knots 672 = 7.3 × 88 B" mislabels: 672 = 7.3×88 + 3.6 crossings×8. The
   `bytes_of` undercount is real and verified in source (body.rs:189–197 omits Entry+Arc
   and all retired deep bytes) — a genuine, small addition.
6. **Why lead, not silver.** Silver needs one named experiment that would make it gold;
   here that experiment (fly the lazy deletion against the digests) is already recorded
   as done by b9ae/8b89 on this page. No further experiment turns a finer re-measurement
   of a flown result into gold. The honest residue — per-class census at the current
   commit, the anatomy, the `bytes_of` undercount, and my past-wave confirmation — is a
   runs-line entry, not a current-best change.

## What the author missed

- The page's own runs list (the wiki exists exactly so runs stop here): 0e37, 760f, b9ae,
  8b89, e0f9, 0619, and ladder.txt's own pre-stated lazy-birth check. Every author reads
  the topic page first; the dossier's "no one has priced this" framing needed those
  citations and a delta statement against them.
- The already-flown deletion floor (8b89's 680 B/B) sits 42% above the predicted 478 B/B;
  the gain estimate (~1.7× flyable N on the birth term) should have been reconciled with
  it, and with the page's standing wall arithmetic (fermi-1051: every arm buys the same
  1.9–2.6× at the 1.2–1.65×10⁶ wall).
- The wave arm (15 s at rtf 1,000, 4.7 s wall) was cheap and would have completed the
  story; the dossier left the read pattern at the wave unmeasured when it was one flag
  away (I flew it above).

## Goal fit

Real bottleneck (board #1/#4, memory per live body) and PRINCIPLES 6/1 are correctly
invoked — but the principle's measured instance was already the page's; this run re-derives
it. Kept as a lead: the per-class census at the current commit, the `bytes_of` undercount,
and the past-wave confirmation are worth one line each on the page.
