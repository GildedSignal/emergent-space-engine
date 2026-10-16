Working...
Check complete. **Grade: silver** — written to `lab/results/20261016-1835-fermi-4093/check.md`, with the author's page corrected in place.

**What reproduced** (regen + my independent flights of the patched shipped binary):
- The core table: A1≡B1 and A2≡B2 *exactly* (11,115/37,935 events at both N — the belt fires zero events below 11.4 k game-s), the clamp (p50 pinned at 11.9 ms, ~230 events/frame ≈ 0.72 s/s ÷ 52 µs, delivered 11.1–13.2k events/s against the 14.4k ceiling), cost 50–52 µs N-flat, memory step 2,340→3,700 B/B. My B3 repeat under load 8.8: 182,363 kicks (−2.1%), same p50/lag. The patch touches only the Linux `footprint()` fallback — all numbers are shipped law.
- The a4ed correction's arithmetic checks: 0.6 cores at 64/orbit-1 AU vs 18.4/184 cores under the shipped 28,141.5-s doll grid; the sentence is still taught on two pages.

**What failed my attack:** the freeze law's printed validation. `frame_to` sets `target = presented + want` per frame (universe.rs:1077), so worst lag is bounded by rtf/60. My rtf-3600 arm reads **exactly 60.000 s** with the crest unchanged, and 10⁵ at rtf 1800 reads 29.3 despite a 3× smaller freeze — "29.8 s measured vs 20.8 predicted" is ceiling saturation, not a duration. The freeze survives on the correct evidence (clamp + delivered rate + count), and I corrected the page accordingly. Two predictions also mis-held (P1's per-body rate invariance failed and was relabeled "hit"; P4 missed), and the prior art (HISTORY's wave entry, cf45's 24×/148×, birth-stagger's crest-vs-budget pricing) is under-cited — that bars gold.

**Named experiment for gold:** measure the crest drain directly (presented-time deficit integral, clean box, full drain) to pin the freeze constant; plus the burn arm.

The run's real nugget stands: a zero-code record correction (a4ed's "belts pass 10⁹ at 10×" is false under the shipped clock), the N1 gate's 20-s window proven pre-crest at every rung, and de-phase ranked before the kick-cost floor.
