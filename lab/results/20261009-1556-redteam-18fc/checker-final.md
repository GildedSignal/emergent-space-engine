Working...
Check complete. **Grade: silver**, written to `lab/results/20261009-1556-redteam-18fc/check.md`; tree restored to pristine (only `lab/results/` untracked, as before).

**What I did:**

1. **Reproduced exactly** — applied `work/patch.diff` to a clean tree, ran all three dossier commands; every row of all three tables (rtf 1/100/1000) matches the author's raw outputs byte for byte: zero drops, zero cold-vs-memo disagreements, ≤1.84 reads/emitter, worst frame 163.

2. **Verified the mechanism in code** — the slope clamp ([1e-3, 1e4], `view.rs:136-144`) only degrades Newton's *guess*; the walk's step uses the instantaneous relativistic rate, and `g` is exactly linear for straight tubes, so one bracketed step lands on the root from any lag. P3/P4's predicted failure mode is correctly falsified.

3. **Attacks of my own:**
   - **Independent retarded-time oracle** (the author's admitted gap, ~40 lines, no shared code with `crossing`): apparent positions agree to ≤5e-3 relative at 0.9999c, ≤3e-2 at γ≈707, exactly zero for away — the residual is the retarded tick's 1/(1−β) sensitivity to the ~1e-7 quantization difference, not a gather bug. Cold-vs-memo identity is now corroborated by a path that can't share a bug with either.
   - **Unmeasured geometries** (Away/Across at 0.9999), **beyond-worst-case** β=0.999999, and **40-frame stale-cache jumps** — all clean; memo recovers in exactly 2 readouts/emitter.
   - Found the run's real drama: before first light (~2.6 frames at rtf 100) the 0.9999c emitters show their tick-0 state — the whole approach is invisible until ≈0.4 frames before passage.

4. **Novelty** — shipped `view_rel` stops at 0.99; r6 (view) is open (law.md:88); first data at β≥0.999 and mutual closing speed.

**Not gold:** no bottleneck moved by 10×, nothing deleted, no premise shown wrong (it was defended), and the kinked tube — the game's actual combat content, where the exact-linearity argument fails — is unmeasured. That named experiment (a thrusting emitter at relativistic speed) is the one that would make it gold, and it's the natural pickup for the next run.
