# Predictions (written before any measurement output was observed)

Written 04:2x UTC, before running the shipped `encounters kick` anchor, the at-scale bench,
or the heap bench. Nothing below was tuned on a run. Working point carried over from the
fermi run: N = 10⁹, rtf 100, P = 4 yr, kicks 222/s at k = 0.28/orbit.

The checker's named experiment: anchor the kick→pair-certificate cascade on the current code
at N ≥ 10⁶, and wire in the event-queue cost of the chosen keying (program-level). The
falsifiable structure behind it, stated before measuring:

**The pairs-per-kick law (my central held-out bet).** Candidate partners are crossing orbits in
Binet space; their count per body scales as (bodies per octave of a). So:
1. **Extent-invariance:** mean pairs/kick is set by n per octave, not by the belt's width —
   n = 10⁵ spread over [1, 15] gives within 2× the same mean pairs/kick as n = 10⁵ over [1, 1.5].
2. **n-law:** mean pairs/kick ≈ (0.04 ± 0.015) × (n per octave): ≈ 810 at 10⁴ (the frozen
   anchor), ≈ 8,100 at 10⁵ fixed extent, ≈ 9,000–13,000 at 10⁶ (either extent), i.e. the
   budget's constant 812.8 pairs/kick is NOT a density convention — at a single belt it is
   unreachable at 10⁹; holding it requires cells of ≲ 2×10⁴ bodies per octave (or σ_e ∝ 1/n).
3. **Shipped anchor reproduces** (`cargo run --release -p emergent-encounters -- kick`):
   pairs_per_kick 750–900, us_per_kick 2–10 ms (x86 vs the M1's 4.3 ms — orders only),
   changed_fraction at eps 1e-9 ≈ 0.002–0.003, slack_skippable ≈ 0.94.
4. **Global range bound degrades with belt width:** the shipped `Sorted` uses a global eps_max
   (κ from the belt-wide rmax), so scanned-per-kick grows with extent: ≤ 5× pairs at [1, 15],
   ≈ 10–100× pairs at [1, 150] (scanned ≈ half the belt), ≈ full n at [1, 1500]. A cell-local
   index (per-block Sorted with block-union bounds) restores scanned ≤ 3× pairs.
5. **Cell-local pairs/kick at 10⁶ in geometric 10⁴-body blocks:** 400–1,000 (≈ the 10⁴ anchor).
6. **us_per_pair** (setup + horizon run, shipped path): 3–15 µs at 10⁴ (x86); 5–40 µs at 10⁶
   (88 MB working set, random partner reads); 10–80 µs at 10⁷. It may drift with scale through
   cache effects only — no algorithmic growth inside the pair work itself.
7. **Heap churn (Rust BinaryHeap, packed (u64 time, u32 id), steady pop+push):**
   100–600 ns per op at 7.8×10⁶ depth (the 10⁹ program-level key count).
8. **Queue terms at the working point** (kicks 222/s, cell pairs/kick ≈ 475–950,
   changed_fraction ≈ 0.0024):
   - cell-level keys: ≈ 1–5×10⁻⁴ cores — ≥ 3 orders below the cascade+skin term (0.077);
   - window-level keys (every re-derived pair window queued, the checker's corner):
     ≈ 0.02–0.08 cores — within one order of the cascade+skin term, so "every other term
     ≥ 3 orders below" is FALSE in that corner even at Rust queue speeds; the keying rule is
     load-bearing, now with numbers.
9. **Encounter-rate fix:** the budget's 0.00586/body/orbit (steady.jsonl, n = 3,000) should be
   ≈ 0.04 at the belt's own local density (scale.jsonl at 10⁴); the encounter term stays
   ≥ 3 orders below the cascade either way.

What would kill the run's claim: extent-invariance failing (pairs/kick drops toward 812 when
the belt widens — then the original budget stands as written), or us_per_pair blowing up ≥ 10×
per decade of n (then the cascade anchor itself moves and the table's ceiling rows fall).
