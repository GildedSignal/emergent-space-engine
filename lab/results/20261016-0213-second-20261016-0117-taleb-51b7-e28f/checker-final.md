Working...
Check complete. **Grade: silver** — written to `check.md`, with the author's `wiki/nladder.md` corrected in place and the tree restored to pristine.

**What reproduced (my own runs on the re-applied patch, one build):**
- 10⁵ quiet A/B: `c459ac4b…` equal, mints 0 both sides.
- 10⁴ word A/B: `73972744…` equal (= the record's), 324 mints vs **1 + 323 shares**.
- The fence-killer 10⁵ arm: ship re-fenced at 1,913 MB mid-burn; cure completes 720 frames, 307 MB, `mints=1`, flush 116.6 s = 0.384 s/distinct scan, digest `36f8e1a4…` (third independent occurrence). Runner's regen: exit 0, all 14 `ladder_digest` rows identical. Lib+bins tests 10/10.

**Adversarial, both beyond the author's domain:**
1. The author's named unflown "natural next flight" — a 10³ burn across ~18k game-s (past the 13.5k re-key window): A/B digest-equal (`82ab4840…`), **19 cure mints / 931 shares** vs 950 shipped — the mint law holds per candidate-set change, and candidate sets *do* change at depth.
2. N = 3×10⁵ (ship fences at 34 scans per the record's checker): cure `mints=1`, 840 MB, no fence.

**Why not gold:** the derived per-frame ratios are kB-as-B slips, ~10³ off and undisclosed — "(309−237−11.3)/659 ≈ 92 B/frame" is 92 **kB**/frame; the raw tail is 11 kB/frame at 10⁵, flat at 10⁴. Honest multipliers: ~10²–10³× by RSS slope, 971:1 by count — still a decisive win, but the headline contradicted the log. Additionally the page overstated identity (listed the schedule-fragile 10⁵ word pair as an equal) and its conflict resolution deleted two runs' append-only Runs lines (library-cfe5, scout-d86c — restored) while leaving duplicated `## Refuted`/`## Open`/`## Contradictions` sections; the mechanism itself is adoption-ready (~40 lines, `d7bc`'s fence can retire).
