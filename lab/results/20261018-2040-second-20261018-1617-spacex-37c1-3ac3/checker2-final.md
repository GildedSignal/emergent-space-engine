Working...
**Grade: gold** — written to `check2.md`.

**Reproduction (clean worktree at base f8056f86 + patch, private target dir):** shipped tests pass flag-off; probe output byte-identical (part A worst recovery 100.000%, part B 8,311 fires / 0 disagreements / w·P=0 exact on 20,000, part C 144/150 pure-ghost chronons → 0/0); all 8 flight censuses byte-identical; ship400 digests off/on both `4fb49739…10ed`; `cens/ref/` byte-identical to 37c1's branch; sd2on matches 37c1 exactly up to the first fire. `predictions.md` (20:58) predates the decisive artifacts; P1/P2 beaten, P4/P5 held, P3's wording failure honestly diagnosed.

**Adversarial (all outside the author's tested ranges):**
1. 1,200 extreme arms (β 0.9999, masses 10⁶:1, reach 2¹⁴–2²⁴, grazing 999/1000): 0 classification disagreements, 0 bit-flips.
2. The unproven absorption, attacked where it's weakest: 150,000 grazing-biased states (|d*| within ±0.1% of reach, the untested reach gap, |w| to 1.9Q): **0 flips at k = 8, 12, 16, 20** — the margin is ≥ 2¹², not 2⁰.
3. 6362's consumed-root warning: closed structurally (detection requires `hit` = approaching; consumed map; no duplicate fired pair) — a fire cannot occur on a never-touched pair; the dossier's caveat 3 is over-cautious.
4. Multi-seed residue: seeds 2/3 give 59/59 and 76/76 fires bit-identical; ship400 seed 2: 1,532 contacts, 0 fires.

**What the author missed:** the never-touched-fire guarantee was already in the machinery; the contaminated class (gate c) is heavier than reported — 7/76 fires at τ*<−1 on seed 3, min τ* −72.9 (vs −1.99); the k-margin sweep was one line away from turning "absorbed, not proven" into "absorbed with 2¹² slack".

**Page corrections (in place):** "absorbed everywhere" → "everywhere measured" with the checker2 evidence and margin; the no-fire-without-`hit` guarantee added to the firing-rule sentence; seed-2/3 flight data and the deeper gate-(c) numbers folded into Current best and Open directions.

Worktree and temp files removed; nothing else in the run folder touched.
