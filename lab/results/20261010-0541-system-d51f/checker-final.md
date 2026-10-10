Working...
Check complete. Summary of the verdict:

**Grade: silver** (`check.md` written; nothing else in the run folder touched; tree restored to pre-patch state).

**Reproduced** (exact command from the dossier, clean tree + `work/patch.diff`): events 2827, levels 36594, memo hit share 2.9%, gather median 775 µs vs engine median 56.7 µs (13–18× across seeds 7/3/99), sched walk 1123 calls @ 7.1–7.9 µs. The mechanism story verifies in source end to end: `apply`'s `root_state_raw` feeds only `deadline_of`, `ViewCache` already stores `1+n·β`, and news gravity is a queued build (HANDOFF, motion law v2).

**Four adversarial findings:**
1. **The shipped control is vacuous** — `lab::reset()` after the last gather ⇒ `levels 0` for any scene. My corrected control (7680 levels, 0 hits) confirms the author's 0% conclusion was right anyway.
2. **Unit conflation** — 7.1 µs is per *call* (avg chain depth 2.04 ⇒ ~3.9 µs/level); the gather-derived 6.4 µs/level attributes all gather wall to readouts. The "internally consistent" argument is coincidence; the derived news-gravity cost halves to ~60–90 µs/kick — still ≥1 engine frame per kick, so the warning stands.
3. **Bit-identity assert is wall-sensitive** — `Budget::wall(5.0)` is 5 **ms**, not 5 s; on seed 13 both flights overflow at frame 68 with 19 vs 20 events resolved (verified via `Frame.overflow`), so the divergence is budget bites, not memo impurity (purity is provable within a frame; allocation churn alone flips bites). The seed-7 pass was quiet-machine luck.
4. **Median vs mean** — the sched tax is 47% of the *median* engine frame but ~7% of mean engine compute and 9% at rtf 10/1000; the stated framing is honest but reads larger than the total share.

**Why silver, not gold:** no 10× or demonstrated deletion (the ~26 µs/frame deletion is designed, not measured), two instruments defective, one derived number inflated ~2×. **The gold experiment:** build the incremental deadline behind the same lab flag, show the ~26 µs median-frame drop with digests equal at a settle cut (not raw flight cuts), across seeds and rtf including a β→1 flight — one afternoon on this same harness.
