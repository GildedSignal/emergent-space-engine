# Dossier — the constraint is the view's gather, not the engine's kicks

**Claim.** On main, at the player's setting (rtf 100, 60 Hz), the plane's frame constraint is the
view gather — 67% of frame CPU, 95% of it in the per-body crossing loop, and inside those readouts
81% in field evaluations that re-read the same sources' tubes per emitter per Newton step — while
the engine (the board's #1, kicks) holds 21% and is already budgeted; the gather is the one
unbounded synchronous claim on the frame, exactly what plane.md foundation 7 forbids.

## Bottleneck

Not a board line: a premise inversion. The board's focus order (1 October) puts "fewer kicks per
orbit" first because "kicks dominate the engine's cost". Measured on the whole frame loop, the
engine is 21% of the frame; the gather is 67%. The engine already sits under the 5 ms budget in
causal-deadline order (plane.md foundation 7); the gather has no budget, no staggering, no culling —
it loops over **every** body, every frame, visible or not.

Expected gain if the gather is brought under the same discipline (staggered emitters, shared field
per doll, culled by what the player can differentiate): the frame's median cost drops ~3× at today's
scene, and — the order-of-magnitude argument — at belt scale (10⁶ bodies, B18b) the gather's
per-emitter cost (measured ~10 µs unpaced, ~42 µs paced, per body per frame) is 60 Hz × 10⁶ × 10 µs
≈ 600 s per wall second: four orders of magnitude over the frame budget, while the engine's event
rate tracks surprises, not bodies. The gather is the term that grows with N; deleting it as a
per-body per-frame loop is what lets N grow.

## Evidence

Machine: GitHub Actions Linux runner, 8 vCPU, load 1.0–1.3 (shared with the window's other runs);
Linux/x86, so orders of magnitude only. Each command ≤ 60 s. `X` = `$CARGO_TARGET_DIR/release/xtask`
after `cargo build --release -p xtask`.

1. The whole, at the player's setting (20 s, paced, rtf 100 — `X universe --bench --rtf 100
   --seconds 20`, saved as `bench-paced-r100.json`): frame p50 4.6 ms / p99 10.9 ms, zero hitches
   above 16.7 ms; `where_the_time_goes_ms`: view_gather share **0.668**, engine 0.205, view_json
   0.090, wire 0.037. Engine budget bites on 62/1200 frames (rtf lowest 1% = 6.5).
2. Unpaced ceiling (`--unpaced`, `bench-unpaced-r100.json`): 20 s of game in 1.34 s wall (rtf
   ≈ 1,500); gather share still **0.675**.
3. The gather's split (patch in this run's tree: env-gated counters in `view.rs`/`observe.rs`;
   `ES_VIEW_SPLIT=1 X universe --bench --rtf 100 --seconds 20 [--unpaced]`): bodies' crossings
   **95.0–95.1%** of the gather, observer setup 3.2%, fleets 1.7–1.8% — same shares paced and
   unpaced (three runs each). Inside the partial-step readouts (`observe::partial`), the field
   evaluation (`force::field` over `ctx.secondaries`, one tube read per source) is **81.4–82.0%**.
4. Kicks, for contrast (`X universe --kick-bench --rtf 100 --seconds 20`, `kickbench-r100.json`):
   949 distinct kicks, median 35 µs (made) / 92 µs (leavers); exact-shape memo hit rate **0%**
   (926 fresh compiles), quantized key hits 94.5% (known: changes orbits). Engine events ≈ 330/s
   against ≈ 4,200 crossing searches/s (70 emitters × 60 Hz): the view does ~13× more readout work
   than the engine does events.
5. Controls: the universe digest at the canonical cut is bit-identical across the pre-edit binary,
   the instrumented binary, and the instrumented binary with the raw-crossing mode on
   (`6ce636fa…`, cut 406050894) — the instrumentation observes, and the display-side change never
   touches outcomes.

Absolute nanoseconds swing up to 3× with the co-tenant load (two paced instrumented runs: 1,134 ms
vs 3,559 ms in the bodies loop, shares identical to 0.1 pp); the shares are the robust statistic.
That swing is itself the lens's point: the gather is what the machine's noise multiplies, because
it is the largest synchronous claim in the frame.

## Predictions

`predictions.md` was written before the instrumented run. Held: (1) crossings ≥ 50% of the gather —
measured 95%; (2) field ≥ 40% of readout time — measured 81%; (3) fleets ≤ 25% — measured 1.8%;
(4) paced/unpaced shares within 15 pp — identical to 0.1 pp.

Miss (found by trying the cheapest exploit): searching crossings on raw tubes (`state_rate_raw`,
one stepped read at the found tick; `ES_RAW_CROSSING=1`) **loses**: field evals fall 232→56 ms but
the bodies loop rises 842→1,146 ms (+36%), because the ViewCache guess extrapolates the *stepped*
crossing root and is systematically biased for a raw search, so Newton walks more. The view digest
also changes (the crossing tick can move by one tick of light when the root sits within the partial
step's Δx of a boundary); the universe digest does not. Lesson: the constraint is not "field evals
alone" but readout count × per-readout cost, coupled through the guess memo — any cheapening must
keep the search and the memo on the same readout.

## What would make it wrong

A scene where emitters are few and the engine is hot (a dense encounter storm) would put the
engine back on top; the plane's default scene is the player's setting, so it is the right whole to
measure, but the split should be re-measured on a battle-heavy scene before freezing any budget
rule. If `where_the_time_goes_ms` mislabels parts (it does not: `session.step` wraps exactly
`gather_cached`), the shares would be artifacts — the in-function split independently agrees (95%
of in-gather ns in the bodies loop). And the paced/unpaced absolute gap is cache heat, not work:
shares match.

## Cost of adopting, and fit

Adoption is a design rule, not code: the gather joins the budgeted order (foundation 7 already
names "a gather" among the claims that must be bounded), with (a) staggering emitters across frames
on the slack skin (components-4643's surviving lever, 12.6×), (b) one shared field evaluation per
doll per frame instead of per emitter per Newton step (the sources' tubes barely move in 1/60 s),
(c) culling by what the player can differentiate (angular radius and brightness are already
computed per emitter per frame — `angular_radius` — and then every body is pushed anyway). Cost:
the view becomes eventually-consistent across frames, which plane.md already allows ("the visual
layer comes later"; "real vs displayed is not the same thing").

PRINCIPLES: "Compute only surprises. Cost follows change and entropy. Nothing is evolved that can
be derived when looked at (clocks, redshift, views)" — the gather re-derives every emitter's
crossing from scratch 60×/s while the engine resolves ~5 events/s; "an hour lost at the bottleneck
is an hour lost for the whole system" — the kick work, however improved, buys 21% of the frame
until the gather is bounded.

## Where the constraint moves next

Once the gather is budgeted and staggered, the frame's tail is the engine's overflow frames (62/1200
at rtf 100, engine p99 5.5 ms at its 5 ms cap) — i.e. the board's kick question (0% exact-memo
hits, 926 fresh shape compiles per 20 s) becomes the constraint again, now with a measured ceiling:
no kick-side win can show in the frame until the gather's 67% is out of the way. The next run
starts there: a budgeted gather, then re-measure `where_the_time_goes_ms`.

## The lens

Goldratt's reading is only as good as the whole it measures, and I measured the plane's default
scene at one rtf. What it may have missed: the gather's cost per emitter is dominated by the
partial step's field walk, which exists to make reads second-order — a representation question
(the field could be a cell-held quantity per PRINCIPLES 7, not a per-read recomputation), and a
lens that looks only at scheduling would stop at "stagger it" without naming that. I did not
measure the browser/HTTP side (out of the bench's scope by design), nor the M1's cache behaviour
(the integrator re-measures).
