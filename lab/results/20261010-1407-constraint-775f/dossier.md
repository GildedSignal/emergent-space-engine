# Run 20261010-1407-constraint-775f — the constraint lens

## Claim

In the delivered frame loop (the plane at the player's settings, rtf 100, 60 Hz), the constraint is the **view gather's bodies loop** — an O(N) light-cone crossing per body per frame at ~12 µs per tube readout, unbudgeted, unculled and ungated — not the engine, which is already subordinated by its 5 ms budget; the frame ceiling today is ~2,200 bodies, five orders of magnitude below the goal.

## Bottleneck

Board focus item "the readout's cost" (B15, queued but ungated) and plane.md §7 ("bounded work per presented frame… or a gather"). Expected gain of fixing it: the gather is 55–63% of every frame today and scales linearly with universe size; a visibility cut + budget + amortized crossings deletes the whole O(N) term at the frame level (the readout becomes O(visible × surprise rate)). This is not the engine's kick cost (the board's #1 engine item) — that is real but budgeted: the engine trades rtf for frame smoothness by design, and the gather has no such mechanism at all.

## Evidence (Linux x86, 8 vCPU shared, load 0.66–1.8; orders of magnitude only)

All commands ≤ 60 s except `behave` (99 s, noted). Binary instrumented by this run (see Patch): `GATHER_NS` section timers + `gather` block in the bench report.

```
/home/glmlab/lab-target-3/release/xtask universe --bench --rtf 100 --seconds 12 --members 48
/home/glmlab/lab-target-3/release/xtask universe --bench --rtf 100 --seconds 12 --members 400
/home/glmlab/lab-target-3/release/xtask universe --kick-bench --rtf 100 --seconds 10
/home/glmlab/lab-target-3/release/xtask galaxy --bench --frames 60
/home/glmlab/lab-target-3/release/xtask behave --law plane        # 99 s
```

**Frame shares (rtf 100, paced 60 Hz):**

| members | bodies | reads/frame | gather p50 | of which bodies loop | per readout | engine p50/p99 | frame p50/p99 |
|---|---|---|---|---|---|---|---|
| 48 | 71 | 69.2 | 0.87 ms | 0.84 ms (97%) | 12.2 µs | 0.08 / 1.84 ms | 1.2 / 2.9 ms |
| 400 | 415 | 289.3 | 3.27 ms | 3.39 ms | 11.7 µs | 0.61 / 5.53 ms | 5.5 / 10.9 ms |

- Gather share of frame: 63% (m48), 55% (m400); engine 23–30%; json+wire the rest. Uninstrumented run corroborates: 20 s at rtf 100 gave view_gather 68%, engine 20% (`bench-rtf100x.json`; ambient load ~1.5 inflates absolutes, shares agree).
- **Linearity:** gather grows 0.84 → 3.39 ms for 71 → 415 bodies ⇒ **~7.4 µs per body per frame**, no cull, no budget. Ceiling at the 16.7 ms deadline ≈ 2,200 bodies, single-threaded — vs 10⁹ in the goal.
- **The search is already cheap:** readouts/frame ≈ 1.0 per live body (the Newton guess cache works). The cost is the readout itself: one `state_rate` = `ramped` → `decode` (integer Kepler readout of the tube) + doll-chain walk + lapse/composition rates ≈ 12 µs, constant in N. Fleet member pushes and the star are noise (0.02–0.03 ms).
- **Engine is subordinated, not the frame constraint:** p99 pinned at its 5 ms budget; at 415 bodies it overflows 153/720 frames and rtf lowest-1% falls to 0 — it trades throughput for frame time exactly as plane.md §7 demands. Its unit costs: kick median 88 µs (p99 400 µs, exact memo hit 0%, quantized 93% = law change — the known board item), ship events 274 µs, player events 1.4 ms each, fleet slices 60 µs.
- **At goal scale the readout is the over-budget part too:** galaxy bench (10⁹ ships, 4 threads, render only): median 27–39 ms/frame, 60/60 frames over 16.7 ms in all three views.
- **Gates:** `behave --law plane` → B13 60/64 (known marginal), B12 fail (known miscalibrated statistic), B14 timeout at 60 s on this box (machine speed; B12–B14+B17 are the plane's gates per docs); G1–G7/B9–B11 unanswered for the plane law (not wired, not new failures).

## Predictions (predictions.md, written before the runs)

- Held: readouts ≈ 1–1.2 per emitter (measured 1.0) — the cost is the readout, not the Newton search; the bodies loop is ≥ 60% of gather (measured 97%); linearity in emitters with no cull (measured 7.4 µs/body/frame).
- **Miss:** predicted slope 40–60 µs per emitter; measured 7.4 µs (12 µs per readout at ~0.6 readouts per body incl. dead/skipped). The first probe's 47 µs was ambient-load inflation (concurrent galaxy/behave); clean reruns cross-validate at 12.2 vs 11.7 µs. Magnitude wrong by ~5×, direction right.
- Held: engine p99 pinned at budget, share grows with N but the gather still owns the frame.

## What would make it wrong

- If the shipped page already culls or budgets the gather (it does not: `view::gather_with` walks `0..n_bodies()` every frame; the bench is the same loop the HTTP server runs via `Session::step`).
- If the player-facing view were always tiny (a minimap of a few dozen emitters) the O(N) term would never bite — but the goal is billions with a view "inferred based on intelligence for the territories" (OC#16), and the galaxy readout is already 2× over budget at 10⁹ today.
- If the 12 µs readout were irreducible: it is one integer Kepler decode + a two-level chain walk; nothing in it is inherently µs-scale on the M1 (untested here — no M1 in the lab; x86 order of magnitude only).

## Cost of adoption, and fit with PRINCIPLES

No physics changes: the gather is a pure read (plane.md §5), so budgeting, culling or amortizing it cannot move a digest. Adoption is a view.rs/session.rs change: (1) **subordinate** — give the gather the same per-frame budget the engine has (plane.md §7 names "a gather" explicitly; B15 should gate it); (2) **exploit** — amortize crossings over frames at each emitter's arrival rate (`dt_e/dT` is already computed for the guess: an emitter is re-read when its apparent state moved enough — "compute only surprises", PRINCIPLES #3); (3) **elevate** — a light-cone index that returns the bodies whose cones can cross the observer's this frame, the same partition c already gives the engine ("it allows to cheaply partition compute", OCC#10), replacing the O(N) scan with O(visible). Fits "The view is an instrument" (#28) and smoothness p95/99 (#12); contradicts nothing.

## Where the constraint moves next

Once the gather is bounded and O(visible), the frame's constraint moves into the engine's throughput at scale, in this order: (1) kick cost and cadence (88 µs median, 0% exact-memo hits — the board's #1, lever already identified: cadence); (2) the player event at 1.4 ms each (why is one player event 16× a fleet slice?); (3) at 10⁹, encounters candidate work and H_live memory. The next run should start at (1) with (2) as a cheap side-question.

## The lens (what it may have missed)

Goldratt's lens sees one system at a time; I measured the plane's frame and the galaxy's render, not the encounters/shipmem scaling paths (no bench exists that runs them inside a frame). The "one constraint" named is the frame's constraint at today's N; at the goal's N the memory floor (24: information) may bind before any of this. perf was blocked on this box (perf_event_paranoid=4), so the 12 µs readout is not decomposed below `state_rate` — the inner split (decode vs chain vs rates) is one perf-session away on a permissive machine.

## Patch (this run's instrumentation, tree restored by run.sh)

- `crates/universe/src/view.rs`: `GATHER_NS` section timers (player/bodies/fleet), never a result.
- `xtask/src/universe/session.rs` + `mod.rs`: `gather` block in the bench report (readouts/frame, emitters seen, section ms).

## Grade (author's self-grade, for the checker)

Silver: real, reproduced, section-timed, with a falsifiable scaling law and a named gate gap (B15 unbudgeted gather); one experiment away from gold — the gold experiment is the amortized/budgeted gather itself, which is a build, not a measurement.
