Working...
**Check complete: `Grade: gold`** — written to `check2.md`, with two page corrections in the run's `wiki/nladder.md`.

**What I verified independently (not from check.md):**

1. **Reproduction** — runner's regen matches the dossier arm-for-arm (global staircase 2.503/5.395 body, 285/389 MB, 595 over; reader arms at control 1.016/157 MB/0 over; burn arms identical to the digit). I re-ran a third control execution myself (211,468 kicks, 79,162.2 game-s = regen's) and re-verified digest off/on md5 identity.
2. **Off = shipped, proven stronger than claimed** — I rebuilt the pristine tree: **pristine** `ladder_digest` md5 `d8593cc4…` = patched-off = patched-on. (Pristine `nladder` can't build on Linux — main's `proc_pid_rusage` is macOS-only; the patch's `/proc` port is necessary harness, and the rule lives in the crate the digest covers.)
3. **Predictions** — `predictions.md` (04:53:09) predates `flights.sh` (05:01:30) and the grid; P1–P7 all held.
4. **Four adversarial cases** — K=10⁵ (deletion holds: 1.007 vs control 1.033/body, `seen` 100,046 both); D=10¹² (immune, gap 4,925,490.9 s exact); burn at 5 ms + stuck-dump (`doll_min_behind_s` all-zero through the SOI handoff — stale-slot fix verified in flight); **vacuity probe** — mode 4 (oldest term deleted *entirely*) passes the digest with the same md5 and the flown rung at control's census/counts, so the soundness battery cannot discriminate reader-relation choices at all.
5. **Page corrections** — "counts BIT-IDENTICAL" overstated (same-arm executions spread 211,442–211,468; rates equal to 3 digits); corrected in the claim block and the Runs line. The "soundness hole closed by measurement" framing is bounded in my reasons: it's closed by construction + read-path audit (all six `Refused("history pruned")` tells verified in code), open for real far dolls (E9) — which the dossier's own wrong-making section admits.

Gold rationale: 9147's checker-named experiment flown end-to-end, the priced 9.2 MB/body far-item term deleted for nil frame cost, adoptable in one step, plus the run's own stale-slot hazard found and fixed. Both checkers' corrections converge on the same two wording overstatements; the measured content stands.
