# Dossier — 20261008-2349-constraint-70b0 (the constraint lens)

## Claim

At the plane's service level (60 Hz, rtf 100) the one constraint on the frame is the **view's
light-cone crossing**, not the engine: the gather holds 66–74% of frame time at every rtf
measured (1, 100, 1000), it is an **O(bodies) synchronous claim on every presented frame** with
no budget (against plane.md §7's own rule), and inside it **97% is the ramped readout** — 60%
tube decode + ramp credit, 39% the motion-law-v2 partial step with its force evaluation — while
the `Binding` clone and history search are noise (0.7%). Newton already converges in ~1.0
readouts per emitter per frame (the cache works): the per-emitter floor is the readout itself,
12–42 µs on this box.

## Bottleneck

The board's live list is engine-side (kicks, encounters, memory). Measured on the whole, the
frame is view-bound: `where_the_time_goes_ms` gives view_gather share 0.74 (rtf 1), 0.70 (rtf
100), 0.69 (rtf 1000) vs engine 0.05→0.18→0.24. The engine is budgeted (5 ms, bursts there);
the gather is not, and unlike engine work it does **not** compress with rtf: it is paid per
presented frame per body, so at rtf 1000 the view costs ~50× more than the engine per unit of
game time advanced. Deleting the gather's unbounded claim is the plane's own promised design
("nothing takes an unbounded synchronous claim on the frame, whether … or a gather"). Expected
gain of exploiting it: the frame's p99 is currently set by gather+engine bursts (10.5 ms at
rtf 100 contended); amortizing the gather across the slack queue is the 10× class lever at
plane scale, and at billions it is mandatory (per-body-per-frame cannot scale; aggregates must).

## Evidence

Commands (each ≤ 60 s, Linux x86 shared box, orders of magnitude only):

```
B=/home/glmlab/lab-target-3/release/xtask   # main + this run's instrumentation (patch.diff)
$B universe --bench --seconds 30            > bench-paced-30s.json        # rtf 1
$B universe --bench --seconds 30 --rtf 100  > bench-paced-30s-rtf100.json
$B universe --bench --seconds 12 --rtf 1000 > bench-paced-12s-rtf1000.json
$B universe --kick-bench --seconds 8 --rtf 100 > kick-bench-8s-rtf100.json
$B universe --bench --seconds 15 --rtf 100  > bench-rtf100-prof.json      # phase-instrumented
$B universe --bench --seconds 15 --rtf 100  > bench-rtf100-ramp.json      # ramp-instrumented
```

- Frame shares (p50, paced 60 Hz): view_gather 0.737/0.695/0.689 at rtf 1/100/1000; engine
  0.050/0.176/0.243 (its 5 ms budget caps bursts; overflow_frames 4/47/55; rtf lowest-1% falls
  to 10.1 at rtf 100). Hitches > 16.7 ms: 0 everywhere; frame p99 5.0→10.5→12.7 ms.
- Gather decomposition (900 frames, 62,650 emitter-crossings, rtf 100): crossing 2657.8 ms =
  95% of gather (observer 90.7, fleet members 49.8); newton_steps 61,207 ≈ emitters 62,650
  (**1.0 readouts per emitter per frame**); readouts 61,207 → ramps 98,612 (1.6 doll-chain
  levels + nested secondary reads); fields 10,796.
- Inside the ramps (second instrumented run): binding_ms 5.8, cartesian_ms 463.4, partial_ms
  297.2 — sums to 97% of crossing. The partial step (11% of ramps) costs ~27 µs each (its force
  evaluation reads the sources again, recursively); a plain decode ramp ~5 µs.
- Engine per event (same runs): fleet slice 43–51 µs, ship kick 171–286 µs, player 799–1263 µs;
  kick-bench resolver median 88 µs (p99 396 µs) — comparable per event to **one emitter's
  per-frame** gather cost, but kicks are per orbit-fraction and gather is per frame.
- Machine swing, reported honestly: two identical instrumented runs (same seed, rtf, bodies)
  gave gather p50 3.66 then 0.88 ms — this shared box moves absolutes ~4×; the phase ratios
  above are stable across both. Absolutes are order-of-magnitude only; the integrator
  re-measures on the M1.
- Determinism under instrumentation: the two instrumented builds (phase timers, then ramp
  timers) at the same seed, rtf and cut (tick 304,538,170, 900 frames) give the **same digest**
  `01c9be772aa19b0a` — the counters are pure reads and change no outcome.

## Predictions

`predictions.md` was written before the decisive (ramp-instrumented) run. What happened:
- (1) **wrong in one part**: the `Binding` clone is 0.7% (I predicted 10–40%) — negligible;
  cartesian is 60% (>50% predicted, held); **partial is 39%, not <10%** — the miss: the
  motion-law-v2 partial step's force evaluation re-reads the sources recursively, and I
  underweighted it.
- (2) held: no growth with history/game time — per-emitter crossing cost stays in a 45–71 µs
  band across rtf 1/100/1000 at 39–76 bodies (prune keeps the deque short; `binding_at` is a
  partition point). No unbounded read cost found.
- (3) held: view_gather ≥ 60% at every rtf; engine ≤ 24% at its budget.

## What would make it wrong

A different machine state (the 4× swing above) changing the *share* ranking, not just
absolutes — unlikely, the gap is 3–14×. A law-level objection: amortizing or approximating the
crossing changes what the player sees (arrival times, colours) — that is a representation
decision (the view is an instrument; "the zoom level is the minimap"), not mine to make alone.
If the integrator judges the debug view's cost irrelevant (a "physics, not visuals" view to be
replaced), the finding downgrades to: the readout's per-emitter cost (decode + partial) is the
number any future view inherits, because every read of a body pays it.

## Cost of adopting, and fit

Adoption is a scheduler change (gather work into the per-frame budget's causal-deadline order,
crossings re-found only when their arrival quantum moves — the cache's `inst` rate already
predicts the next crossing), not a law change: outcomes stay digest-identical (observation is
pure). It fits PRINCIPLES #3 ("compute only surprises … clocks, redshift, views" are derived),
#12 (smoothness is the p95/99), and #17 (idle time computes ahead). The queue already names
this item ("the readout's cost"); this run pins its measured shape.

## Where the constraint moves next

Once the gather is bounded and amortized, the frame's constraint returns to the engine's kick
path — engine share already grows 5%→24% with rtf, and at rtf ≥ 1000 the budget bursts
(overflow 55 frames/720). At billions of bodies the constraint is candidate encounters and
H_live memory, as the board ranks them. Next run should start at the gather's budgeted
amortization (this run's numbers are its acceptance baseline), or at the partial step's
re-read of the sources (39% of the readout, an exactness-preserving memo candidate — distinct
from the killed kick memo: same inputs, pure function, no orbit change).

## The lens

The constraint lens measured the whole before touching anything, and it profiled inside the
measured phase rather than guessing — but it may have missed that the debug view is scaffolding
(the visual layer comes later), making part of this cost disposable by deletion rather than
optimization; and it could not use `perf` (blocked in the container), so the finest split is
function-level timers, not instruction-level hot spots. The 60-minute window also left the
rtf-growth control confounded by machine contention (order-of-magnitude only).
