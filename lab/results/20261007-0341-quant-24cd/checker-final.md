Working...
Check complete. `check.md` written; tree restored to clean main; my repro artifacts left in `/tmp/check-repro` (outside the repo; nothing else in the run folder touched).

**Grade: silver.**

What I did:
- **Reproduced** from clean `origin/main` + `work/patch.diff`, rebuilt: the 49,152 row (fp99 10.13, engine p99 5.62 ms, overflow 96/360, ev/s 2.26e3, digest bit-identical `4ec59efc…`), the 393,216 row, player 1,881 µs vs ship 64 µs, burn/coast 0.90, floor 309.7 at seed 2.
- **Adversarial:** (1) capped ≡ uncapped digest at the same cut, plus the horizon-clamp code read — deferral is game-clock lag only, never wrong light (closes the author's open question); (2) rtf_median's pin is by construction (`want = rtf × wall_dt`), not an empirical surprise; (3) a 20 s paced run shows the "27–30% silent deferral" is front-loaded warm-up debt — coverage 91.6%, amortizing, so the headline overstates steady state ~3×.
- **Record defects:** "p99.9 ≤ 13 ms everywhere" contradicted by the author's own m3072x runs (18.45/18.17); "slices/game-s" mislabeled (per nominal run-second); maxrss is 50 MB, not 120 MB (memory is member-flat too).
- **Novelty/goal fit:** no H entry measures members/rtf/deferral; it corrects plane.md §7's "brief, smooth dip" expectation, deletes members-based capacity work, and hits board #4 and principles 14/28.

Gold is one experiment away: long paced runs reporting `presented_tick_at_end / cut_tick` as the capacity number, the mechanism stated, the resolution-rate line landed in `dash.rs`, and the three defective numbers corrected.
