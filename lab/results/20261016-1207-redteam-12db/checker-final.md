Working...
Check complete. **Grade: silver** — written to `lab/results/20261016-1207-redteam-12db/check.md`, page corrected in place.

**What was verified:**

- **Reproduction.** Clean tree at base `cab6188`, empty patch (pure measurement on shipped code). regen.sh exit 0; medians match to 0.1 µs (made 34.8 µs = 695× the doc's 50 ns; leavers 203.2), memo 2262/2262 distinct exact keys, quantized 98.0%, digest-stable. Only drift: p99s 50.7/394.8 vs the dossier's 53–63/399–408 — timing noise, recorded.
- **Adversarial arms (3+ outside the author's seed-1/rtf-600 domain).** Seeds 7 and 42, rtf 100 and 3000: 14,219 rebinds total, **zero exact reuse everywhere**, made median 34.6–35.4 µs, refused 0. The refutation is robust; the leaver median is pace-dependent (162–365 µs), now scoped on the page.
- **Citations.** Every doc/code/wiki citation stands — representation.md L32/L57/L67/L113/L114, law.md L20/L36/L39/~L90, ENVELOPE/QUADRATURE, rung inventory (no r5, no r6, no kick-cost rung), B8–B11/B19, all cited runs present on their wiki pages.

**Why silver, not gold:** the decisive refutation is the record's own at gold grade — `b063` (11 Oct, frame-cost page): "kick 75.6 µs vs 42–56 ns floor (~1,800×); exact memo 0%" — the closest prior, uncited by the author; a repetition is not gold however well done. What is genuinely new: the six-premise census, the guard-gap map (r5/r6 never created, no kick-cost falsifier), and the both-sides memo squeeze in one instrument — real, reproduced, adoptable in one editing pass. Also flagged: prediction 2's made≈leavers equality failed by 6× unacknowledged, and "the §6 cost table has no rung or gate at all" is overbroad (B9/B10/r7 touch other rows; the kick row is the unguarded one).

**Gold path named:** freeze the missing kick-cost rung on the shipped bench, so §6's row is guarded by a frozen criterion instead of by three golds the doc ignores.
