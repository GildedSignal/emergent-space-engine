Grade: gold

**Abstract.** Claim: the plane's frame loop already is the engine's allocator — bit-identical digests across budget/threads/pace under overload, no hitch tails — but sustained overload collapses presented time via the global horizon, so the missing work is one rung (per-region staleness), not a scheduler. I reproduced every headline number from shipped code in a clean tree: digests `a0096d59e1…`, `bfacdfc5bb…`, `00f39765…` bit-identical to the author's, and the invariance holds beyond the author's grid (engine-ms 0.25, 20× cut; fresh seed 7; all knobs at once). The cliff is worse than claimed: my traced median per-frame advance falls 1,044,936 → 101 ticks (~10⁴×). Adoption: take the design decision now (one rung in `frame_to`/`advance`; wave needs an M1 re-measure before deletion). Cost ≈ zero; no code changed on main.

## Reproduction (clean tree, `CARGO_TARGET_DIR=/home/glmlab/lab-target-2`, shipped binary + `work/patch.diff` applied by me for the trace)

- P1 digests: `--members 48 --rtf 100` engine 5/t4/paced vs engine 1/t1/unpaced → both `a0096d59e104153b…` (author: 4 runs, same digest). `--members 400 --rtf 1000` engine 2/t4 and **engine 0.25**/t4 → both `bfacdfc5bbd2b432…` (matches author's 7 runs; 0.25 ms is 2× deeper than their grid). Fresh **seed 7**, engine 5/paced vs 1/unpaced → both `b507432c2cc40827…`, distinct from seed 1 as it must be. The digest changes *when*, never *what*: confirmed on cases the author never ran.
- Hitch tails: my six bench runs all `hitch_counts=[0,0,0]`, worst 15.3 ms — but two 8 s trace runs caught 18.04 ms and (author's own rerun) 17.3 ms single frames. "No hitches anywhere" holds as h16=0 in 12/13 runs; the absolute wording is slightly overstated, and the author disclosed the 17.3.
- The cliff: my trace runs (patch applied, `UNIVERSE_TRACE=1`, 8 s, members 400, rtf 1000, e5 vs e2, t4) give digest `00f39765ce9bb5cb…` — exactly the author's trace pair — and median per-frame horizon advance 1,044,936 → 101 ticks (~10⁴×). Author's rtf_median 309 → 0.03 is also ~10⁴×; their headline "~600×" **understates** the collapse. Mechanism verified in code: `advance` (universe.rs 822–833) takes the global min of unresolved deadlines over the whole queue plus deferred items, and `frame_to` (867) clamps `now` to it — one group that cannot clear freezes the player's presented time. Engine.md rule 8's rung 2 (off-screen regions lag) is indeed absent.
- Wave (claim 5): author's JSONs show events/s 2963 (t4) vs 3528 (t1) at e5 and 934 vs 1490 at e2; code line 815 fires `resolve_wave` for every ship whenever `threads > 1`, kind-triggered — verified as written. I did not re-measure the p99 pair; shared-runner caveat stands (M1 before deleting).
- Allocator unused (claim 6): my grep matches theirs — `emergent_allocator` only in its own examples/tests and `xtask/src/regions.rs`; `crates/universe` has its own queue.

## Predictions

`predictions.md` (12:39:35) predates every `out/` artifact (first 12:40:09) — pre-registration verified by file times. P1 held everywhere, including my extensions. P2 half-held (h16=0 everywhere; the cliff broke the ">25% of previous rung" criterion — honestly reported, and the failure is the finding). P3 inverted, P4 wrong — both falsified as disclosed, neither tuned on. Per H0183, these are expectation failures that diagnosed real mechanisms, not method failures.

## Attack

1. Deeper cut than any author run: engine-ms 0.25 at members 400 — digest still invariant, cliff deeper (rtf_median 0.001), no tail.
2. Fresh seed (7) with all knobs changed at once — invariance is not a seed-1 artifact.
3. Reproduced the trace pair independently; digests match the author's bit for bit.

## Novelty

Plane.md foundation 2 already promises order/thread-independence (B8 gates it), so digest invariance per se is a contract, now first *measured under overload and budget cuts at the plane*. The cliff, the wave pessimization, and the budget-invariance-under-100%-overflow measurement have no prior HISTORY entry (H0158's 28.7 ms max frames were the old engine's ladder). Claim 6 was already in the integrator's same-day method.md deletion pass (HANDOFF, 7 October) — corroboration, not novelty; the dossier's grep is more precise.

## Goal fit

Board bottleneck 4, ranked, with Julien's "the algorithm that allocates the work… it's the most important one" — adopted, not built, and absent from the 14 queued builds. This run replaces that open design question with measurements and a deletion: the queue exists and holds under bursts; one rung is missing; the second allocator is unused. PRINCIPLES 12 ("p95/99… the allocator"), 1 ("the best part is no part"), 22 ("the simulation decides" — the horizon reads the queue, not a forecast).

## What the author missed

- The sharpest statistic is the disproportion: events/s fell 3.2× (2963→934) while RTF fell ~10⁴× (309→0.03). Compute shrank proportionally; presented time froze. That separates "less compute" from "frozen player" better than the per-frame tick deltas, whose absolute scale is scene-dependent and made "~600×" look tuned when ~10⁴× was available from their own rtf_medians.
- No measured attribution of *which* group holds the horizon min (one log of the argmin entity's kind at overflow would turn the code-read mechanism into a measured one).
- "Worst frame 16.64 ms across every overload run" is contradicted by their own 17.3 ms disclosure and my 18.04 ms; report h16 counts, not a worst-frame bound.
- Claim 6 could have cited the integrator's same-day deletion pass rather than presenting reachability as new.

**Notes.** One grep of mine accidentally matched two quoting lines of `check.md` (it quotes the dossier); I have not read it, and this grade rests only on my own reproduction above. Tree restored after the trace runs (`git checkout -- crates/universe/src/universe.rs`); nothing else in the run folder touched.
