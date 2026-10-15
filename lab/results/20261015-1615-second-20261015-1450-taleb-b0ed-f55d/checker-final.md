Working...
`Grade: gold` — written to `check.md`, the author's page corrected in place, tree restored to pristine base `7f8da59e`.

**What I did (45-min budget):**

**Reproduce** — Re-applied `work/patch.diff` on the clean base, rebuilt warm (11.6 s), re-flew 4 arms: all bit-identical to the stored flights (counts + digests; e.g. ratio 7.226/1.000 at 10⁵ burn, the b0ed coast anchor `5e8c9e24`). Every dossier number cross-checks against `flights/table.txt` and the who-files: all seven burn ratios, the extra-promotions = hit-deficit identity on all seven bound arms, plateaus 1.22/1.02/1.01×N, scan-share 26%→71% from the sampled backtraces, the ONCE arms. The crate suite's 2 failures fail identically on the pristine base (the pre-named lazy-tier regression) — the patch adds nothing.

**Attack (18 flights, all outside the author's domain, all identity-clean):**
- **Knee razor:** demotions 130,187 at 10⁵/20k → cap 130,186 gives exactly 1 eviction, 130,187 gives 0. The knee is *exactly* the flight's total mint bill — not the 1.02×N live plateau the dossier's working-set sentence conflates with it.
- **Deep cut (the author left this as inference):** at 48k game-s the bill is 270,979 (2.71×N); the author's 131,072 cap degrades to 1.368 while 273,200 holds 1.000 with zero evictions. "~1.3×N" is the matched-cut constant; the law is the horizon's mint bill — "no constant cap serves burn" holds a fortiori.
- Seed 5 (1.000 at 131,072, 6.84 at 65,536), N=3×10⁵ (bill 330,187 = N + 30,111 exactly, ratio 8.23 at 0.44×N), ONCE at 2×10⁵ (7.61 vs FIFO 7.98), coast demotions 131,053 vs burn 130,187.

**Page** — faithful conflict resolution (both sides kept); I amended the two overstatements in place: the knee constant → the mint-bill law with the 48k measurement, and the wall tax → the regen table's +20–25% (the dossier's +13.7%/+29.5% don't regenerate from its own table — recorded as a defect, direction intact).

Not three agreeing golds yet (0757 is the only other), so the topic stays open. The named gold experiment from b0ed's check is done as named, on the board's furthest bottleneck.
