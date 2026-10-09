Working...
**Grade: gold** — written to `check2.md`, blind to the first checker.

**What I did:**
- **Reproduced exactly**: applied `work/patch.diff` (one new example, no library edits — claim holds), ran all three dossier commands; `kink-rtf1.txt` and `kink-rtf100.txt` match byte-for-byte, `run20` identical (244k kicks, 12/12 kinked, 0 drops / 0 cold≠memo / 0 oracle mismatches, reads/em 1.78).
- **Predictions**: `predictions.md` (17:20:24) precedes all decisive outputs (17:21:42+); P1–P5 held exactly; P6's timing miss honestly reported and led to the stronger run20.
- **Four adversarial cases of my own**: (1) a +1-tick corruption of the gather flags 7188 oracle mismatches — the instrument can fail; (2) a 111× heavier source (gm 1/9): 44 kinks, all 44 inside the swept range, still 0/0/0 at reads/em 2.45 — kinks cost readouts only, and this also regenerates sweep.txt's row exactly (kicks 7991, refused 36); (3) a 4× closer flyby: clean; (4) the 0.9-case anomaly diagnosed — its kinks' light arrived ~3 frames *before* the window (the dossier's parenthetical explanation is inverted, though its recorded numbers are right).
- **Novelty**: no prior kinked-tube view measurement (HISTORY's "kink" hits are the unrelated GEM law-lab); r6 is open; this is the original checker's pre-named gold experiment, done in its pre-registered "kicked" form, with the regime limit measured (deflection ≤ 1e-7 relative at any accepted mass), not asserted.

The claim now holds on the shipped record with the named experiment done; nothing broke under attack.
