Working...
Check complete. `check.md` written to the run folder; nothing else touched, no commits, worktrees removed.

## Verdict: gold

**Reproduced from a clean worktree of main `70f27a9` + `work/patch.diff`:**
- **P6** bit-identical: 4447 events per schedule, worst image miss 0.500 tick, key offsets (−8314, 6002), one history under 1/4/8 threads and both make orders, 0.83 s.
- **Control** (identity key forced): fails with the dossier's exact unarchived numbers — member 1 off −110.523964, the pair tied at 16,384. The tests are falsifiable.
- **B13**: detail line identical across author-before, author-after, my clean-main baseline, and my patched run (60/64, worst 2.12e-2, same 9 replaced draws).
- **B17**: timeout 60.0 s after (the box can't exercise it; M1 re-measure per lab rules).
- **B8 suite**: 56 green / 1 known-ignored, 256 s (−4.5% of the 268 s baseline, inside the ±10% prediction).
- **Plane**: Moon key −25, Skimmer +1, rest 0 — byte-identical.

**Predictions genuinely held out**: mtimes put `predictions.md` (23:14:26) after the baselines it quotes (22:59–23:04) and before the decisive runs (00:38–00:40). All five held.

**My adversarial cases**: depth-2 doll chain matches a composed two-edge float oracle to ±0.49 tick (units and second edge verified); β=0.001 slow doll keeps keys exactly at doll ticks; **β=0.9 found a real edge** — 79/300 members' events sit past the state-made passage tube's readout domain and `root_offset`'s silent `break` drops the shear back to the old convention. Deterministic, no regression vs main, bites only passage-centred dolls (bound-orbit centres unaffected), recorded in the check as a boundary on adoption.

**Novelty**: closes law.md:34's exact Open; no prior implementation anywhere in the repo.

**Missed by the author** (in check.md): the silent high-β degradation; `run.log` empty so the control/hang-probe claims weren't archived (I reproduced the control); "22 tests" miscount; B17's "unchanged" is really "times out both ways here".
