Working...
Check complete. `check2.md` written to the run folder; the author's proposed page corrected in place; working tree left clean (patch reverted, real wiki pages md5-verified untouched).

**Grade: gold.**

**Reproduced bit-identically** from a clean tree + `work/patch.diff` (`regen.sh`, <1 s): the three damaged pages heal to 0 markers of all three kinds with 0 content lines lost, Runs lists byte-identical, index leak 3→0; two concurrent publishes on the healed page stay at 0 markers; the live arming control (real 1637 window through shipped `apply`) deepens 19→46; the skip turns re-apply into a no-op vs +50 lines/14 banners without.

**Predictions**: written 23:31, before every instrument (23:33/23:36) and the decisive run (23:38); P3–P6 held; held-out counts matched; one honest miss disclosed.

**Attack** (5 cases, 2 outside the author's range): pathological depth-4 interleaves all heal clean — backed by a structural invariant verified in the code (`defuse` output cannot contain a marker line at any depth). Two new edges found, both latent/conservative, both added to the page's Open directions:
- **A5**: a conflict block containing the `## Runs` header heals fine but the version rendering introduces a second `^## Runs` that truncates `split_runs`' parse — the next publish duplicated a runs line and deleted a prose line. Not reachable from today's corpus or from a clean patched pipeline.
- **A3**: a run re-presented under the same id with corrected content is silently skipped (undisclosed mirror of the renamed-id case).

Also noted: the census instrument is blind to the disclosed setext loss (marker lines excluded from its content multiset).

**Novelty**: closes the prior silver's checker-named residual; no `defuse`/`heal` exists on main. **Fit**: infrastructure gold (the lab's mandated memory, board topics #1 and #3 were unreadable), not engine gold — flagged for the integrator's weighting.
