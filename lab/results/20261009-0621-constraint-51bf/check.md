Grade: silver

At the player's setting (rtf 100) the plane's frame constraint is the view gather — 67% of frame CPU against the engine's 21%, 95% of the gather in the per-body crossing loop, 81% of readouts in field evaluations re-read per emitter per Newton step. Reproduced: universe digest `6ce636fa…` bit-identical on the pre-edit binary, the instrumented binary and raw-crossing mode; gather share 0.65–0.67 (author 0.67); bodies 0.950–0.951, field 0.81–0.82; kick-bench identical (0% exact memo, 926 fresh shapes, 94.49% quantized); the raw-search exploit loses as reported (field 234→58 ms, bodies loop +50%). Holds at rtf 1, rtf 1000 and seed 7. But the headline is known (H0210: "the view gather is 83% of a light frame"); new is the anatomy and the N-scaling term. Gain ~3× projected, not measured; cost: one lever to build, no code landed.

## Reproduction

Applied `work/patch.diff` to a clean tree, built release, ran every dossier command plus controls. Linux runner, load 0.5–1.0.

- Paced bench: digest `6ce636fa…` ✓; gather 0.653 / engine 0.219 / json 0.091 / wire 0.037 (author 0.668/0.205/0.090/0.037). My p50 frame 1.32 ms vs the author's 4.61 ms (lighter co-tenant load) — shares agree, confirming the dossier's own point that shares are the robust statistic.
- Unpaced: gather 0.674 (author 0.675); 20 s of game in <2 s wall.
- Instrumented split (`ES_VIEW_SPLIT=1`), paced and unpaced: bodies 0.950/0.951 (author 0.950–0.951), observer 0.032–0.033 (3.2%), fleets 0.017–0.018 (1.7–1.8%), field share of partial readouts 0.813/0.815 (author 0.814–0.820). The unpaced view digest matches the author's `exploit-base.txt` bit for bit (`cb69811f…`) — the instrumentation observes only.
- Kick-bench: 949 distinct kicks, made median 37 µs / leavers 101 µs (author 35/92, load noise), exact memo 0.0 with 926 fresh shapes, quantized 94.4924…% identical, digest `c8ab26da…` identical.
- Raw-crossing exploit: field evals 234→58 ms ✓, bodies loop 854→1,280 ms (+50%; author +36%); universe digest unchanged ✓. The cheapening loses as reported.
- Pre-edit binary control: reverted the patch, rebuilt, ran the bench — digest `6ce636fa…` identical, gather share 0.674 uninstrumented. Re-applied and rebuilt afterwards.

## Predictions

`predictions.md` (13 m before the instrumented outputs at listing time) postdates only the dashboard runs it explicitly cites and predates the decisive split runs; its text is consistent with that order. All four held-out bounds held: crossings ≥50% → 95%; field ≥40% → 81%; fleets ≤25% → 1.8%; paced/unpaced split within 15 pp → 0.1–0.9 pp. The bounds were loose, but they were pre-registered and could have failed.

## Adversarial cases

1. rtf 1 (real time): gather 0.72, engine 0.04 — the gather dominates even harder.
2. rtf 1000: gather 0.64, engine 0.29 — the engine's share rises with rtf but does not overtake; bodies 0.975, field 0.816.
3. Seed 7: gather 0.62, engine 0.26, bodies 0.948, field 0.816.

No inversion anywhere in the range; the anatomy is stable. The author's caveat (an encounter-storm scene could flip it) stands untested — the CLI exposes no such scene.

## Novelty — why silver, not gold

The headline "the constraint is the view's gather, not the engine's kicks" is already on the record: H0210's limitations say "the view gather is 83% of a light frame", with "Next: … the gather cache (Sonnet)"; H0211 landed the cache; H0213 made it relativistic (3.6 → 1.2 readouts per emitter at 0.9c); plane.md foundation 7 already lists "a gather" among the unbounded synchronous claims on the frame. The board's line is scoped to "the engine's cost", so the "premise inversion" attacks a reading the record does not quite make, and the dossier cites no H entry for it. What is genuinely new: the post-cache level (67%, i.e. what the cache bought is visible only as 83→67), the anatomy (95% crossings; 81% in `force::field` over `ctx.secondaries`, one tube read per source per emitter per Newton step), the coupling lesson from the failed exploit (search and memo must share one readout), the per-body per-frame term as the piece that grows with N while the engine tracks surprises, and the honest negative. No lever is built or measured: the ~3× median-frame gain and the belt Fermi (60 Hz × 10⁶ × 10 µs ≈ 600 s/s) are projections from a 70-body scene. Gold's "adopted within one step" is not met by a diagnosis alone.

## The one experiment to gold

Build the cheapest named lever — one shared field evaluation per doll per frame instead of per emitter per Newton step (or staggered emitters on the slack skin) — and re-measure `where_the_time_goes_ms`: gold if the gather's share falls materially (frame median ~3× lower, or gather below the engine's share) with the universe digest at the cut unchanged and B16's view behaviour intact.

## What the author missed

- **H0210/H0213 uncited.** The 83%→67% series across the gather cache is exactly the interesting measurement and it is absent; without it the run presents a known fact as a premise inversion.
- **The per-frame view digest is not canonical.** Under `ES_RAW_CROSSING` my view digest (`c002…`) differs from the author's (`b658…`) while base unpaced matched bit for bit: wall load enters the view sequence through the engine budget's overflow (62/1200 frames change which tick each frame presents). Fine as a change indicator; unsafe as an equality control. Only the cut digest is.
- **One rtf, one seed.** The claim survives rtf 1–1000 and other seeds (above), but the author measured neither; at rtf 1000 the engine's share is already 29%, so the ranking is rtf-dependent in the direction the author only guessed at.
- **The belt Fermi extrapolates per-emitter cost from 70 bodies**; the ViewCache's readout amortisation at 10⁶ bodies is unmeasured, and B18b's memory floor is a second blocker at that scale.
- **"~13× more readout work" compares crossing searches (each several readouts) with engine events** — the ratio understates the view's work; the honest number is larger, so the direction survives.
