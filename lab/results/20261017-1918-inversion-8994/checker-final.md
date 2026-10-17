Working...
**Grade: lead** — written to `lab/results/20261017-1918-inversion-8994/check.md`, with the author's proposed `wiki/nladder.md` corrected in place where it overstated.

**What reproduced** (runner's regen, exit 0; deterministic anchors exact): the belt first-item band 13,051/14,072/14,542; event counts 23,461/173,696/443,696/1,043,696 at N=0/10⁴/10⁵/3×10⁵; the budget-free crest at game-s 14,137–14,333 crossing 12 ms between 10⁴ (3.1 ms) and 10⁵ (18.0 author / 36.30 regen — load); and the genuinely new result — the **budgeted path holds at 3×10⁵ through both combs** (worst60 ~12 ms, lag ≤ 2 game-s, zero refusals, work complete to 0.035%).

**Why lead, not silver:**
1. **The headline was already on record**: ladder.txt's NEXT BREAKS 1 (merged 14 Oct) measured this exact wave — 13,051–14,534 game-s, lag 0.45 s at 5×10⁵, "10⁶: twice that", frames within 12 ms; the cadence prompt (13 Oct) already scoped "200-s score ~3×10⁵ (the wave breaks 5×10⁵)"; fermi 4093 (16 Oct) held the window fact, the ~52 µs cost, and 69 s of clamped delivery per interval at 10⁶; 917c's ≈6×10⁵ letter is on the page itself. None of the strongest three cited.
2. **The run's distinctive 10⁶ verdict is a 10× arithmetic slip**: 28,141 game-s at rtf 100 is 16,885 frames × 12 ms ≈ **202.6 s** of inter-comb capacity, not "1,690 frames / 20.3 s". The crest at 10⁶ (15–35 s M1-class, 27–80 s x86 on the author's own inputs) drains with 2.5–13× margin — no stacking, no unbounded lag; matches fermi 4093's measured freeze law.
3. **Adversarials** (fresh arms at 4×10⁵, outside the author's range; tree restored, scratch removed, numbers verbatim in check.md): budget-free crest 76.06 ms — *below* 3×10⁵'s 84–86 ms, so the "5.0× super-linear" exponent is not stable; budgeted 4×10⁵ holds with lag still 2 game-s; belt band fixed in N at 3×10⁵ (13,037–14,542, p50 14,072).

**Keepable**: the first end-to-end budgeted confirmation through two combs at 3×10⁵, and the band's N-invariance. The named next experiment: a memory-lean flown 10⁶ (or 5–6×10⁵) budgeted arm measuring peak lag — corrected arithmetic plus fermi's freeze law predict bounded transient lag (10²–10³ game-s), not stacking.
