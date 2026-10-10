# Dossier — 20261010-1152-constraint-c575 (lens: the constraint)

## Claim

On the plane as it flies, the frame's binding constraint is the **view gather**, not the engine: it is the only unbudgeted, synchronous, O(N) cost per frame (≈70% of the frame at player rtf, 2–3× the whole engine's cost per body per second), and 63–77% of it is spent re-reading emitters whose presented appearance changed less than half a pixel or one 8-bit colour step — a rate-bounded refresh skin on the existing view memo cuts it 3–4× and re-binds it to the player's channel instead of N.

## Bottleneck

Not on the board's list: the board ranks kicks first ("fewer kicks per orbit … kicks dominate the engine's cost"), which is true *inside* the engine (17.7% of the frame at rtf 100) — but the engine is budgeted (5 ms, defers on overflow) while the gather is neither budgeted nor deferred: every alive emitter is Newton-crossed against the past light cone every frame (`crates/universe/src/view.rs`, `gather_with`: `for i in 0..u.n_bodies()`, no floor). Expected gain: 3–4× on the median frame at player rtf (63–77% invisible), and it deletes the view's N-scaling (10.5 µs/emitter/frame ⇒ a 16.7 ms frame saturates near 1.5 M emitters on this 8-core x86; ~350 k effective with 77% invisible — the goal's 10⁹ needs aggregates, not crossings). Where the constraint moves next: once the view is rate-bounded, the tail constraint is the engine's event bursts at the 5 ms budget (measured below).

## Evidence

All runs on the shared Linux runner (8 vCPU, load 0.25–0.96; orders of magnitude only). Reproduce with the run's patch applied (adds `universe --view-probe`, `xtask/src/universe/view_probe.rs`); each command ≤ 60 s.

1. **The frame, as the player runs it** (`./target/release/xtask universe --bench --seconds 30`, seed 1, members 48; `bench-rtf1.json`; `--rtf 100 --unpaced` in `bench-rtf100.json`):
   - rtf 1: `where_the_time_goes_ms` shares — view_gather **73.5%**, view_json 14.9%, wire 6.4%, engine **5.2%** (engine p50 0.147 ms of a 5 ms budget).
   - rtf 100: view_gather **69.8%**, engine 17.7%.
   - Kicks (`universe --kick-bench --rtf 100 --seconds 30`, `kickbench.json`): 1158 kicks, median 75.8 µs (leavers 91.9), quantized memo hit 95.5%, exact 0% — the memo artifact correction holds.
2. **The gather is O(emitters) with no floor** (`universe --view-probe …`, `probe-*.json`; probe = per-frame engine advance + the page's own `gather_cached`, scripted like the benchmark; digests reproduced across repeated runs, e.g. `09e40859…` twice at m48):
   - p50 per frame: 0.49 ms @ 28 bodies → 0.82 ms @ 71 → 3.36 ms @ 409 (≈10.5 µs/emitter/frame at rtf 100; readouts/emitter 0.95–1.14, warm cache).
   - Sub-pixel emitters (angular radius < one 1080p pixel at 90° FOV = 8.2e-4 rad), median per frame: **84%** (m48), **76–78%** (m400, seeds 1/7); all 23 catalogue ships sub-pixel on 100% of frames; fleet members 53–64%; one of three planets 67% of appearances.
   - **Invisible refresh** (direction moved < half a pixel AND colour shift < 1/255 since the previous presented frame; re-gathered at full cost anyway): median **63%** (m48), **70–77%** (m400) at rtf 100; 49% at rtf 1; **14% at rtf 1000** — the waste is largest exactly at the rtf the player views.
   - Per body per wall-second at rtf 100: view 634 µs (m400) / 816 µs (m48) vs the whole engine 264–283 µs — the view costs 2.2–3.1× the entire engine per body, and its *invisible* part alone (≈444 µs at m400) exceeds the whole engine.
3. **The engine's tail is budgeted and defers; the view never does**: engine p99 hits the 5 ms budget at 400 members (p99 5.66 ms, **136–169 of 600 frames overflow** = 23–28% at rtf 100; 45% at rtf 1000 m400; 22% at rtf 10⁴ m48; 0–3 of 600 at m48 rtf ≤ 100). Outcomes stay canonical (digest at cut, deferral changes *when*, never *what* — `plane.md` §7); the gather has no such bound.
4. **Gate instrument artifact** (`behave-plane.txt`): `behave --law plane` reports G1–G7/B9–B12 as FAIL with "worst inf"/"unanswered" — those gates judge the compiler law, not the plane: `behave --law space --gates G1,G2,B7` → PASS (256/256, 64/64, 64/64, ≤0.06 s). B13 judged 60/64 (matches HANDOFF); B14 timed out marginally (60.1 s / 60 s).

Files: `bench-rtf1.json`, `bench-rtf100.json`, `kickbench.json`, `probe-{rtf1,m48,m48-s7,m400b,m400-s7,m400-rtf1000,rtf1000,rtf10000,m4,m400,m400-s2,m400-s3,m48-s2,m48-s3}.json`, `behave-plane.txt`.

## Predictions

`predictions.md` was written before the probe runs (tuned only on the two 30 s benches). What happened:
- **P1 (rtf ladder) held**: view > engine share through rtf 1000 (engine 32% of engine+gather at rtf 1000); engine takes over at rtf 10⁴ (67%, 131/600 overflow).
- **P2 half-held**: gather linear in emitters ✓ (6.8× cost for 10.5× emitters); "engine grows much less than 8×" ✗ — engine p50 grew ~11× from 71→409 bodies (events 4.8–5.8 per body per game-second in both scenes; bursts, not rate, drive it).
- **P3 held**: ≥50% sub-pixel ✓ (76–84% at rtf 100), seeds 2/3/7 within 1.5× ✓; "nearly all fleet members" ✗ — only 53–64% (battle members near the player are resolvable; the skin must be distance-aware).
- **P4 number missed, conclusion strengthened**: 10.5–13.5 µs/emitter/frame measured vs 30–150 predicted; the view-vs-engine ratio per body (2.2–3.1×) exceeds the 2–9-kick equivalence I allowed.
- **P5 held at m48, broke at m400**: p50 0.05 < 0.2 ms ✓, p99 = 36× p50 ✓; but "budget not exceeded at p99.9 for rtf ≤ 1000" is false at 400 members (p99 5.66 ms > 5 ms at rtf 100) — the tail constraint bites at hundreds of bodies, thousands of times below the goal.

## What would make it wrong, cost, fit

- The half-pixel/1-per-255 floor is a *display* assumption; a zoom, a hover that names ships, or instruments that read fleet internals still need per-emitter answers. Adoption does not delete the gather: the crossing stays a pure function of state (the probe's repeated digests prove observation never changes outcomes), so skipped emitters are recomputed on demand — the skin changes only *when* the debug view refreshes, never any canonical bit. Cost: one angular-motion bound per cached emitter (`|v_⊥|·(1+n·β)/dist`; the arrival-rate slope is already in `ViewCache`) plus an aggregate path for sub-pixel clusters (star-clusters as one luminosity dot) — the same shape as the engine's slack skin (12.6×, taste log 6 Oct), applied to the view.
- Wrong if: the real visual layer replaces the gather entirely (then the finding transfers to it: any per-emitter light-cone readout inherits the same O(N)-per-frame without a channel floor); or if the M1's gather share differs by an order of magnitude from x86 (shares, not absolutes, carry the claim).
- PRINCIPLES fit: #3 "Compute only surprises" — the view re-derives unchanged appearances 60×/s; #5 "the zoom level is the minimap"; #28 "The view is an instrument … your dials are made up and hold no informations"; #33 "a body resolves only the influences that are significant at its own scale"; #1 "The cheapest compute is compute not done."

## The lens

The constraint lens measured the frame as built and may mistake the debug view for the permanent view; the *gather physics* (light-cone crossings, redshift) survives into any visual layer, but its presentation cost may not. It also took the plane's frame as "the system": at galaxy scale the engine's asymptotics (candidate pairs, H_live) may re-dominate, and nothing here measures memory or the GPU path. Finally, Goldratt's "exploit before elevate" biases toward the refresh skin; the representation answer (principle 18) may instead be to gather the *screen*, not the catalogue — pixels hold the emitters, emitters don't hold pixels.
