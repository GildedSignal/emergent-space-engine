Working...
**Grade: gold** — written to `check.md` in the run folder. Tree restored to clean; nothing else touched.

**What I did:**

1. **Reproduced every claim** on a fresh build from the disclosed patch (and a pristine no-patch build): `6ce636fa…` at cut 406050894 across paced/unpaced, dt 16.7→500 ms, engine-events 0/1/4/64 (ev0 = defer-everything, beyond the author's sweep), threads 8, prune off, load 5.56 under 6 spinners, shared pinned core; seeds 1/2/3 → one digest per seed (`6ce6…`/`c979…`/`1e05…`); `ES_DIGEST_PARTS`: all 77 per-body lines bit-identical, only the un-hashed `resolved` counter moves (my spread 6721/6781/5117 vs author's 6746/6756 — same conclusion). Stored data: 57 runs, no `56f4…` anywhere.

2. **Resolved the anomaly the author left open.** The prior checker's flip *does* reproduce — on their own surviving binary `/home/glmlab/lab-target-1/release/xtask` (built 08:19:35 mid-session from checkout `lab-1`, per its dep file): same command flips `fbc3…`×5 ↔ `56f4…`×2, at their reported events/s 227. Since a clean a838a284 build is deterministic (proven ~75 runs across three independent builds), that binary is provably not the shipped code — their "clean tree, shipped code" described the run's end state, not the 08:19 build state. The falsification was a stale/dirty-binary harness artifact, exactly the 5-October independence lesson turned on a checker.

3. **Record nits noted:** "70+ runs" counts 7 compile-error logs (57 real); the patch silently removes `--engine-ms`; the author priced the stale-binary hypothesis but never spent the 60 s to test it.

Gold because: fully reproduced, the premise "the digest flip is engine-side" is shown wrong *with mechanism* (this check closing the last gap), the integrator's named prerequisite is discharged, and adoption is a one-step record correction with no code change.
