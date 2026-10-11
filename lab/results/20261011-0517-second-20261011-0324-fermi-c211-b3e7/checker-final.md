Working...
Check complete. Verdict written to `lab/results/20261011-0517-second-20261011-0324-fermi-c211-b3e7/check.md`: **Grade: gold**.

**What I did:**

1. **Reproduction — exact.** Fresh build of the shipped `emergent-shipmem` examples (17 s), full `reproduce.sh` in an isolated copy (28 s, 249 MB peak). Every deterministic field of all 70 JSONL lines matches bit-identically — checksums, scar counts, `inferred` flags, zero mismatches — across measure, ladder and kickmag. Timings within shared-machine noise. The probe's cited orbit ranges reproduce exactly.

2. **Predictions — held.** `predictions.md` (05:28:14Z) precedes all data files (05:31:14Z+). All eight recomputed and held: P1 within 4% at every rung, P2 linearity −7.8%…+4.3% for f ≤ 0.5 at every magnitude, P5 reabsorption −S within 1% everywhere, P7's restated 4.2%/4.5%/0.04% verified from the table (the original's 0.5% was indeed 1/191).

3. **Nine adversarial cases of my own, all confirming the rule:** ω wraparound saturation exact (b=31 ≡ b=46 → S = 81.7 both, formula 82); per-field additivity across three asymmetric patterns (91.4 all, formula 91); off-ladder magnitude (97.5 vs 97); beyond-field-width wrap bounded at 95.5; saturation at a magnitude they never ran (exactly 4096 scars); small-end additivity. **One falsification:** perfect E/L correlation does *not* lower S (111.5 vs 111.6) — the "shared widths" mechanism in their "what would make it wrong" is wrong; the scar store has no cross-column model. The conservative-side conclusion survives via marginal widths, and adoption gets simpler (price S from issued per-field delta widths, correlation irrelevant).

4. **Novelty** — HISTORY ends at H0215; this is the first checker's named experiment on the record's own gap; nothing prior measures scar cost vs kick magnitude.

The gold condition for a second-author run ("the claim now holds on the shipped record with the named experiment done") is met: the constant is replaced by the magnitude-dependent rule `bits/body ≈ 1 + S·f_cum`, the headline is corrected, the record regenerates, and it's adoptable in one step. Misses documented in check.md: the false correlation mechanism, timing figures that don't exactly match the stored final JSONL (119→154 vs 125–158 ns; 349 vs ~280 ns draw), P4's mislabeled 0.91·S ratio, and "every rung" saturation claimed from 3 of 7 modes.
