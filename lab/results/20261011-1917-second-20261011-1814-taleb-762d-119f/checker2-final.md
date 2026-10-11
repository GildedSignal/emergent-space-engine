Working...
Check complete. `check2.md` written; tree reverted to clean main.

## Verdict: silver

**The physics is gold-grade.** Everything reproduces from `work/patch.diff` — after I added one missing line — with bit-exact digests on a fresh build:

- **Prologue kill confirmed:** 14.7 µs at 428 bodies (author: 15.0), 99% rekey. The original run's 0.2–1 ms floor is dead by direct measurement.
- **Cliff factorization confirmed:** 834× = 11.8× throughput × 71× density (author: 792 = 11.3 × 70); "delivers 0.00" is indeed a median artifact (28.8× run-average; paced 5.2× exact; 39 jump frames of 1.28–1.29 game-s carrying 100% of game time).
- **Record corrections exact:** the original's "2.9→8.8 ms engine p50" was view/frame columns (`orig/C-m400.json`); all four R1 digests match the original artifacts bit-for-bit.
- **My four adversarial cells all confirm the model:** a 0.01 ms budget *below* the prologue itself still buys events (no knee, e = 0.058/frame, delivered 20.7×); seed 2 reproduces the cliff (366× = 8.9× T × 41× D); delivered is rtf-independent (28.6× at rtf 30,000 vs 27.6× at 3,000 — the shed-the-target gate's sharpest justification); the unmeasured paced-1ms cell fits exactly (27.9× = T/D).
- I also verified the author's `E = events_per_second × nominal` arithmetic is correct (dash records the fake `dt = 1/60` for unpaced runs — `session.rs:100`), and that `predictions.md` (19:27:16) precedes all data (19:27:28+).

**Why not gold:** the shipped `work/patch.diff` is missing the `"--coast"` parse arm — the author's own final binary rejects `--coast`, so the grid (20 of 27 cells, the decomposition itself) does not regenerate as shipped. With the one-line fix it regenerates bit-exact. This is precisely the record-regeneration failure that has kept runs at silver before ("the record, corrected and regenerating" is this run's own standard). Secondary: the demand line's "293×" is an arithmetic slip (correct: ~19.5× at the 5 ms/60 Hz budget; the dip-is-unavoidable conclusion survives).

**Path to gold:** re-save the complete patch, regenerate the full grid from it in a clean tree, fix the two numbers. One rung, no new physics needed.
