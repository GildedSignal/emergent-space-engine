Working...
Check complete. `check2.md` written; tree restored (author's patch reverted, my probe example removed); nothing else in the run folder touched; no commits.

**Grade: gold.**

**What I did:**
- **Reproduced bit-for-bit**: applied `work/patch.diff` to the clean tree, built, ran — binary output identical to `hlive.log`; independently measured 0.20 s wall / 10.6 MiB maxrss. Every dossier number confirmed, including the attribution gap (85 steady bodies → 0.46 MiB engine-attributed of 2.91 MiB live, matching the disclosed ~0.43 MiB) and the drop control (+1,400 B).
- **Prediction order verified** (mtime 04:08:19 vs log 04:13:39). The claim-bearing predictions P2–P5 held, P4 exceeded (175× vs ≥10×). P1 (event mix) was falsified — kicks 20%, slices 61% — and honestly disclosed as the run's surprise; my independent runs confirm the corrected reading. I did not let this block gold: the apparatus did its job (no tuning detectable), and the falsified expectation is auxiliary to the memory claim.
- **Five adversarial cases**: seeds 7/100 (median ship 1,552–1,648 B, reabsorption holds), members 256 (per-ship bytes insensitive), 2× horizon (live falls to 2.52 MiB, created ≈ reclaimed; steady state is real), Dense order (killed at 300 s — the lockstep reference, not the plane's engine path; Sparse scoping is honest since every plane test uses it).
- **Novelty**: H0158 measured ~2.7 KB/ship in the *old* engine; H0209's shipmem designed the program representation. Neither measured the flying plane's H_live, which HANDOFF line 70 listed as "not measured yet". This run measures it and inverts the premise: the rate is harmless, the standing bytes (1,456 B median vs the 16-byte tube) decide — redirecting the queued `b-h-live` build in one step.

**What I found that the author missed** (recorded in check2.md): worst-ship history depth creeps 11→14 over the doubled horizon (retention not proven bounded — strengthens the claim); the trait's default `history_depth() → 0` silently under-reports for future stores; the "2.91–3.29 MiB" flat claim mixes pruned and unpruned values; shape sharing is asserted, not measured — that plus a belt scene is the natural next run.
