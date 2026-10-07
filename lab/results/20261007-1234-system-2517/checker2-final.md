Working...
Check complete. `lab/results/20261007-1234-system-2517/check2.md` written: **Grade: gold**.

**What I did (independent of the author and of `check.md`, which I did not read — one grep accidentally echoed two of its quoting lines, disclosed in the file):**

- **Pre-registration**: `predictions.md` (12:39:35) predates every `out/` artifact (first 12:40:09).
- **Reproduction from shipped code**, clean tree: digests `a0096d59e1…`, `bfacdfc5bb…`, `00f39765…` all bit-identical to the author's. Invariance holds **beyond** their grid — engine-ms 0.25 (20× cut), fresh seed 7, all knobs changed at once.
- **The cliff**: applied `work/patch.diff` myself, re-traced at engine 5 vs 2 — median per-frame horizon advance 1,044,936 → 101 ticks (~10⁴×). The author's "~600×" *understates* it. Mechanism verified in code: `advance` takes the global min of unresolved deadlines; `frame_to` clamps `now` to it.
- **Attack**: deeper cut, fresh seed, independent trace pair — all pass. Hitch claim slightly overstated (my 18.04 ms frame; their own 17.3 ms disclosure), noted.
- **Novelty**: budget-invariance-under-overload, the cliff, and the wave pessimization have no prior H entry; the "allocator unused" fact was already in the integrator's same-day method.md deletion pass — corroboration only.
- Tree restored and clean rebuild done; nothing else in the run folder touched; no git commit/push.
