# Dossier — run 20261010-0920-quant-30e1 (lens: Quant)

**Claim.** On the shipped plane, one kick event is one full orbit compile — and the
compile's memory churn (allocation, key search, i128 panels outside `Scalar`), not its
counted arithmetic, holds ~80% of the event's wall time; so the per-event 10× is the
re-anchored jet (fewer compiles per kick), not layout or arithmetic.

**Bottleneck.** Board focus 1 ("kicks dominate the engine's cost") one level down: what
is inside a kick. Pricing the per-event floor decides whether the slack skin (fewer
events) is the only lever or whether the event itself shrinks 10×.

## Evidence (all commands in `repro.sh`, each ≤ 15 s; Linux x86 cloud, 8 vCPU — orders
of magnitude only, the integrator re-measures on the M1)

Instrument: dynamic counters (never a value; replay digests on seeds 1/2/7 are
bit-identical to the unmodified build) on `Scalar` ops, `OrbitShape::bound`/`quad`/
`weak_quad`/`fast_quad`/tail-Newton/cbrt, plus wall-time stage splits of the kick's
five stages. Perf hardware counters and valgrind are unavailable in this container
(`perf_event_paranoid=4`, no sudo); counter+digest instrumentation is the fallback.

`xtask universe --kick-bench --rtf 100 --members 400 --seconds 10`, five seeds
(1, 2, 7 baselines; 11, 23 held out), JSONs in this folder:

- Per-kick wall: fleet members ("leavers", 97% of samples) 85–94 µs median, p99
  ~420 µs (5× median: compile volume varies with orbit shape). Star-system bodies
  ("made"): 39.8 µs median.
- **Every kick compiles one orbit: `bound` = 1.00 per kick on both paths** (5 seeds),
  exact memo reuse 0 of 5,438 rebinds (seed 1; the shipped bench's own metric). The
  quantized 12+12-bit key would serve 246 shapes for those 5,438 rebinds (22:1) — the
  reuse door exists and is a law change (re-rounds the orbit; law.md "Not adopted").
- Op mix per leaver kick: ~1,000 add + ~1,000 mul + ~250 div + ~46 sqrt ≈ **2,300
  `Scalar` ops**, ~180 panel quadratures (93 quad + 86 weak + ≤16 fast), tail-Newton 0,
  cbrt 0. At ~1–2 ns/op the counted arithmetic is ≈ 3–5 µs of the ~86 µs event: the
  majority of the event is the compile's uncounted part (band/knot building, `Vec`
  allocations per compile, key search in `fit_key`, i128 panel math outside `Scalar`).
- Stage split of the clock-stepped path (`kick_clock`, made bodies): fit (rebind) 60%,
  forces 31%, readout 8%, sigma-delta + plan ~2% (seed 1: 3.7/1.9/0.5/0.05 µs of
  6.2 µs staged; stable across seeds 2/7/11/23 within ±5 pp).
- Whole-plane cross-check (`--bench --unpaced --rtf 100`): engine 32% of the frame,
  view_gather 54% (the readout build, already queued), ships 67 µs/item, fleet
  38 µs/item, **player 2.07 ms/item — the player's events cost ~30× a ship's** (the
  "market order" priced), ~2,062 events/s at rtf 100.

## Predictions (`predictions.md`, written before the instrumented runs)

- P1 fit > 40% time: **held** (60% on the clock path; compile dominance on the leaver
  path shown by bound=1/kick + 180 panels/kick, not directly timed — flagged).
- P2 mul > 45% of ops: **missed by a hair** — mul 43.7%, add 43.2%, div 11%, sqrt 2%
  (mul is top class but under the threshold I wrote).
- P3 iteration tail: **wrong in mechanism** — tail-Newton and cbrt never fire inside
  kicks (0 iterations); the 5× p99/median tail is compile volume (panel count varies
  with orbit shape), not solver loops.
- P4 no microarchitectural 10×, the door is fewer compiles (jet) multiplying with the
  slack skin: **held and sharpened** — counted arithmetic is < 20% of the event, so no
  arithmetic/layout fix reaches 10×; law.md's re-anchored jet at ~0.05 compiles/kick
  prices ~20× on the compile share.
- P5 held-out seeds 11/23 within ±5 pp of seed 1: **held** (stage shares 3.0–3.7 µs
  fit etc.; op mixes within a few percent).

## What would make it wrong

The 60% fit share is measured on the clock-stepped (made) path only; if the leaver
path's compile is a different mix, the residual claim (~80% uncounted churn) shifts —
it is derived from ops-vs-wall (2,300 ops ≈ 3–5 µs against 86 µs) and holds unless the
`Scalar` ops are far more expensive than ~2 ns each on the M1. The counters exclude
early-exit paths of add/mul (zero operands), which undercounts cheap ops — direction
favors the claim. Cloud x86 timing; the M1 re-measure may move every absolute number.

## Cost of adopting, fit with PRINCIPLES

Nothing to adopt in code; the patch is measurement-only and reverts with the tree.
Decision input: per-kick floor = one compile; the jet (law.md, graded-gold by one
checker, second never ran) is the per-event lever and multiplies with cadence and the
slack skin — "the cheapest compute is compute not done" (§1); "cost follows change"
(§3). The compile's allocation churn is a candidate for the next build's budget
("we need to be deeply aware of von-neumann bottleneck and memory", §17).

## Grade self-assessment: silver

Real, reproduced on five seeds with digest identity, predictions pre-registered and
adjudicated honestly (one miss, one mechanism correction). One named experiment from
gold: time the leaver path's stages and split the compile's residual (allocation +
key-search counters), which the window's remaining minutes could not fit, and the M1
re-measure the integrator owns.

## The lens (what Quant may have missed)

An HFT lens prices events and tails but underweights law exactness: the 22:1 quantized
reuse is tempting exactly the way a stale quote is — it re-rounds every orbit it touches
(principle 13), and no p99 number prices that. Also: one machine, one harness; the
digest control checks work identity, not the M1's cost structure.
