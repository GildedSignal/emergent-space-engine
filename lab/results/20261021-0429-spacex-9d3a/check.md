Grade: silver

**Abstract.** Claim: the live set is sweep-bound, not event-bound, so demotion is dead. Reproduced: every structural number (4 zero-post-birth generations in 100,032/300,032/1,000,032; live 10/20/60% at 1 frame/1 s/5 s; ~8.7 view decodes/body/gather; 2,432–2,447 B/body; misses = 0; seed-stable at seed 7). But the checker's view=none control kills the causal story: 99.78–99.93% of belt bodies get **zero post-birth engine reads** over 20–50 s; the "engine observe path sweeps ~1%/frame ∝N" is the build's frame-0 birth decodes (~8 a body) divided by frames (1e6: 8,055,419 ≈ 8 × 1,000,032). The engine is event-bound; the O(N) oracle gather is the sole population-wide reader — a wall already owned by the view row's golds. Nothing to adopt; page corrected.

## Reasons

**1. Reproduction.** The runner's `regen.sh` exited 0 and regenerated the table (1e6 truncated at 600 frames, disclosed). My own re-run of the 1e5 sparse arm reproduced every structural number exactly (gens 103,783; build_born 100,032; zero_post_build 4; live 0.09996/0.20236/0.60314; readout_engine 897,278; in-flight engine reads 87,264; misses 0), and the engine-side counts are bit-identical across view modes and reruns — the engine work is deterministic. The kept 1e6 log and the fresh rerun agree (8,055,419/8,055,417 engine reads, 4/1,000,032). Minor drift only in the volatile raw rate (dossier 787 vs regen 748 reads/frame), a disclosed class.

**2. Pre-registration.** `predictions.md` (04:41) precedes the decisive 1e6 arm (04:49:43) and the dossier (04:51:18). Note: the author's own 1e5/3e5 logs were overwritten by the checker-time regen, so their original timestamps are gone — not the author's doing. P2 held; P1/P4/P5 are falsified and reported as falsified (the honest premise-kill form); P3 half-held and reported.

**3. Adversarial cases (the grade-limiter).** I added a per-generation engine/view probe and flew controls the author never flew at scale:
- **view=none, N=1e5, 20 s:** zero_post_build = **99,813/100,032 (99.78%)** — without gathers, almost no belt body is ever read after its birth frame. Only **219** build-born bodies get any post-birth engine read; in-flight rebind generations take 87,264 engine reads (~21 each, event-local).
- **view=none, N=3e5:** 299,813/300,032 (99.93%); in-flight engine reads **identical (87,264)** — the steady engine read load is *not* ∝N.
- **view=none, N=1e5, 50 s** (outside the author's 20 s horizon): 99,792/100,032 still zero post-birth; live@20 s = 40.5% — the engine alone leaves most of the belt cold for >20 s.
- **seed 7, N=1e5, sparse:** 4/100,032 zero-post-birth, 99,854 view-read, same live curve — the census is seed-stable (this part of the run is solid).
- **The artifact, closed arithmetically:** the engine read bucket is dominated by frame-0 build decodes, ~8 a body: bb_birth_reads = 799,901 (1e5), 2,399,901 (3e5), and ~8.0M ≈ the whole 8,055,419 at 1e6. "Engine reads/frame 748→2,081→13,426, ∝N" is births ÷ frames; the steady rate is ~95/frame at 1e5 *and* 3e5.

So the dossier's central sentence — "the engine's observe path sweeps ~1% of the population per frame (∝N, not ∝events)" and "the live set is bounded by the sweep" — is wrong. The board's premise ("a body is live only around its events") **survives for the engine**; what pins every body is the harness's oracle gather (`gather_cached`, one per 10 s, 8.7 decodes/body). The "returns/gen ~2.0" and the 440-core demotion bill are that gather's bill, and they collapse under the row-set gather the view row has already adopted (flyable-frame gold: row-set deletion 220×; skyserve: 351–374 readouts/frame flat in K). The redirection "kill the sweep (the running wt/cadence per-body-clock job)" aims at a sweep that does not exist.

**4. Novelty.** Already known: 4ea0 (gold, kick-jet) killed eviction on the plane's rebind loop (×98 builds; 68–77 reads a generation; readers 99% engine, view 1%) and named interning as the lever; efd4 (gold) measured the catalogue's duplication and the intern; memory-h-live names the view gather as the crowd's first wall; view.md owns the O(N) gather wall and its cure. Genuinely new here: the belt-scale build-born residency census (4 zero-read in 10⁵–10⁶), the live-slack curve at population scale, the per-gather decode law, and the 2,424–2,447 B/body anchors. That is a real addition, not the premise kill it is sold as.

**5. The page.** Corrected in place: the headline and "readers" bullet now separate the two readers and carry the artifact note; the Refuted section no longer claims the board's premise is refuted for the engine; the demotion bill is qualified as the oracle-gather bill; open direction 1 is replaced by the row-set-gather demotion experiment, and direction 3 now cites the view row's adopted golds. Budgets kept (current best 7 lines, page well under 300).

**6. Goal fit.** The instrument is sound (misses = 0; identity-by-address; my probe confirms its per-generation bookkeeping) and the author's PRINCIPLES quotes (#3, #6) are apt for the corrected claim. But the funnel+phase attribution was never split by the one variable the instrument already had (view on/off at scale) — the 5 October lesson again: the reads counted were not the reads the claim described.

## The one experiment to gold

Fly the census under the **adopted row-set gather** (with view=none as the control already in hand): if the live set is event-bound there and the demotion return rate falls by the ~10² the gather's read share (66%) plus horizon implies, the memory row's closure is "demote once the view stops walking N" — the premise restored with a number, adoptable in one step.

## What the author missed

The view=none control at scale (one flag, already meaningful to their PHASE instrument); the birth-read contamination of the engine bucket (births are frame-0, not per-frame); the shipping status of the row-set gather (their "shipped read path" is the oracle gather the view row is deleting); attribution of the 219 ever-engine-read build-born bodies (plane/player neighbourhood, presumably); and the 1e6 arm's "13,426 engine reads/frame" being ~99% build decodes.
