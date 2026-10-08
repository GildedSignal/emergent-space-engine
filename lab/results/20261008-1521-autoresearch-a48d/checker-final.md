Working...
Check complete. `check.md` written; tree restored to HEAD (only untracked `lab/results/`).

**Grade: silver.**

What I did:
- **Reproduced from scratch**: applied `work/patch.diff`, rebuilt, ran `xtask universe --kick-bench --seconds 2` ~30 times across both trees plus the `a48d_bench` stage bench, interleaved A/B on saved binaries. All three test suites green (0 failures).
- **Verified in source**: `bind_in` reads only `trajectory`/`periapsis_time`/`periapsis_angle`/`clockwise` and rebuilds its own residual — the deleted decode was genuinely dead work on the kick path. Digest `dac49af3…` bit-identical in every run, `refused: 0`.
- **Confirmed**: the stage-bench numbers reproduce exactly (process 33.1→29.5 µs, −10.9%; bind 14.9→11.7), as does the whole attribution table.
- **Refuted the headline**: the −38% (72→45 µs) is a contention artifact — my quiet baseline is 46.7 µs with the author's changed numbers matching mine almost digit for digit. Clean interleaved like-for-like: **−7.8%** (46.70→43.07), which is precisely the author's own pre-registered P3 (−6–9%), mis-scored as a "miss". The dossier's explanation (fleet members' `Passage` solves) is contradicted by the bench JSON: `leavers: 0 samples`, `cycle_rebinds: 23/23`.
- **Novelty**: holds — no HISTORY entry deletes this decode; kick cost is a named next step (H0210).

Why silver, not gold: the delete is real, bit-exact, and adoptable in one step, but it moves the dominant event ~1.1×, not 10×, deletes no component, and overturns no premise — and the headline number the dossier leads with does not survive a like-for-like measurement. One experiment to gold: certify the honest gain at the frame level (p95/p99 on `universe --bench`) or take the structural cut this run itself exposes — one shared per-(doll, tick) decode for readout/secondaries/tide, ~30% of the post-change kick.
