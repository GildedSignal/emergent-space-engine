Working...
**Grade: gold** — written to `check2.md`, with the page corrected in place and the tree restored clean (patch reverted, 0 modified files).

**What I verified independently:**

1. **Reproduction** — applied `work/patch.diff` to the clean base tree, rebuilt, re-flew A3: clock census **bit-identical** to the author (59,425/59,425 fired, same Σ|dvq|max 8.6585e15 and max 10.6435e13); split differs only at the wall-capped window edge. All five arms' numbers in the dossier check out against regen.log, including the arithmetic (170,897 items; wave 2 − wave 1 = 29,715; 0.2% Σ difference).
2. **Probe soundness** — read `step.rs`: the census sits on every completed `kick`/`kick_clock` item before its fired-check, counters only; the OFF/ON full-log diff shows identical deterministic state (P5).
3. **Four adversarial arms outside the author's domain** — burn mode (a law path never flown: clock non-thrust 29,589/29,589), a 1-ms starved scheduler (0.9999), 101.7k game-s ≈ 4 waves (118,865/118,865), and K=10⁵ (46,143/46,143, split **bit-identical to 3×10⁴** — direct proof nothing scales with belt N). Share 1.0, m≥16 in every fired item, everywhere.
4. **Predictions** — pre-registered with the kill criterion; P1 failed *as written* and the author reported it: that failure is the finding (tide ≈ 1.5×10¹¹ quanta/step vs the carry's 1-quantum margin). P2/P4/P5 held and I re-verified each.
5. **Novelty** — closes budget-1e9's open direction 2; a9d7 measured the rate, never the share; nothing in HISTORY.

**Corrections applied to the page:** the unfired total is 268 (266 A3 + 2 A2 — the dossier's "266, one arm" undercounts), and the earlier "0.16–0.3% on the split" blended denominators (0.16% of all items / 0.26% of split items); appended the second-checker line including the one domain note the author missed — the cadence wave smears with K (0.46 items/body by 14.3k gs at 10⁵ vs 1.00 at 3×10⁴), which doesn't touch the share.

Both checkers independent, both gold: the dial stands closed at p = 1.0.
