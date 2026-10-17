Working...
**Grade: gold** — written to `lab/results/20261017-1330-second-20261017-1240-spacex-9c67-d65c/check.md`, with one in-place correction to the author's wiki page.

**What reproduced** (regen exit 0 + my reruns): every deterministic number matches — plane census `(35275, 39, 17643)` and the per-kind split bit-identical to the first checker; belt census 719,845/719,845 boundaries (100%), 283/725,976 kicks; ROOT calls 801,885 in all arms; digest identity with 5ade's anchors reproduced bit-for-bit. Wall-clock differed only within the claimed band (normalized median 9.8% vs 10.5%; stage arithmetic independently brackets 7.4–10.1 µs/kick). Predictions (13:35) precede all decisive artifacts (14:13+); pre-registered kill criteria held.

**My three attacks, all outside the author's range:**
- 3× horizon (70–310 ks, 2.44 M events): digests identical, mechanism intact, normalized drop ≈9.5%.
- N=2×10⁴ over 330 ks (untested N, WH-heavier): digest identical, ROOT calls/kick unchanged, apply −56%.
- Census at 150–230 ks: fallback attribution **verified** (walked = 100,093 — build replans, not handoffs), but boundary |Δx| reaches **1.75×10⁶** root units — the ceiling is window-scoped, not the plane's 6.8×10⁵; corrected the page's "same ceiling" claim.

Also verified structurally: `digest()` never reads `self.pos`; the cache's only consumer is `light_distance` — the §28 blindness claim holds at 1.13 M further divergences in my window.

**Named in check.md as missed:** the two prediction components that failed without being labelled (ROOT calls ≤0.05/kick, apply ≤1.2 µs — the first is the run's own mechanism find), the non-regenerable drift decimals from scratch pairs, and the harness's 2.9 GB footprint at long windows.
