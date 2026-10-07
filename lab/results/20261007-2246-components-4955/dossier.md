# Dossier — the event queue's idiot index (components lens)
**Claim.** The plane's event queue (a 4-ary indexed heap, `crates/space` `events::Calendar`)
sits ~4–8× off the floor of its own workload at 10⁶–10⁷ bodies; a monotone bucket wheel
with batch-sorted drains reproduces its exact pop sequence at 2.1–4.4× lower cost per
event (4–9× under co-orbital concentration) and lower p99, with one honest tradeoff:
rare O(n) rebuild spikes (24 ms at 10⁶, 1.2 s at 10⁷) that the frame-budget law must
chunk anyway.

**Bottleneck.** Not on the board's ranked list, but load-bearing for board item 3
(cost at a billion: the queue is per-event overhead on every kick) and the top scaling
risk (co-orbital concentration: the wheel is 4–9× there). Expected gain at the engine's
own cadence: the queue's share of a 32-kick orbit drops ~3×; what it deletes is the
log(n) term in per-event cost, which is the only term that must survive to 10⁹ bodies.

## Component and its owner

- Plane foundation 2: "One clock, one queue. Every entity holds the time of its next
  certified event. The queue is a min over the dolls, with deterministic ties."
- PRINCIPLES #12: "the algorithm that allocates the work to prevent those heavy tails,
  it's the most important one". #14: "no ticks… we only care about changes" — the queue
  IS the no-tick discipline's only index.
- law.md ties (5 October): same-epoch events sharing a body are one batch; the queue's
  key is (time, smallest body id, kind).

## The floor

Two structural facts of the law's own workload, both already written down by the engine:

1. **Re-predictions move monotonically later.** One slot per body; resolving a body's
   event re-sets only that body, later than now (the Calendar's own header says so).
   A monotone min-queue needs no heap: bucket by time, drain forward. This is the
   timing wheel / calendar queue (Varghese–Lauck 1987; Brown 1988) — routers, kernels
   and discrete-event simulators paid to learn it (PRINCIPLES #26).
2. **The full distribution of next-times is known at all times** ("the simulation tells
   us what's next, not us"): the window and bucket width are derivable from the state,
   so the queue is re-derived, not tuned.

Floor per event = deliver one record in order + touch the popped body's state line:
~2 ns/event streamed (measured floor control) + one cold line touch (~100 ns at 10⁶,
DRAM) that the engine pays regardless (the replan reads the body's record). The heap
pays that same touch plus a sift path of log₄(n) cold lines, and the shipped interface
pays Scalar (16-byte normalized fixed-point) compares on top.

## Design

`Wheel` (in `qbench/src/main.rs`, ~150 lines): b = n power-of-two buckets over a window
derived at rebuild (base = min, width = span/b); inserts at/behind the drain cursor go
to a value-ordered side heap, so **correctness never depends on the workload** — only
speed does (width ≤ min inter-event delta keeps the monotone path in buckets). Buckets
drain as batches, sorted once by the (tick, id) key — exactly the tie rule's order.
Cancels are lazy (dead entries purged on surfacing; the dead-count guards the per-pop
state read to zero when nothing was cancelled). The far list is re-binned at window
exhaustion. Verified: identical pop sequences vs the shipped Calendar on all four
workloads, 5 seeds, sizes 999–4096, including cancels and earlier re-sets.

## Evidence (reproduce with `run_decisive.sh`; raw cells in `metrics.jsonl`)

Reproduce: `lab/results/20261007-2246-components-4955/run_decisive.sh` (each cell ≤ 60 s;
full grid ~180 s; `cargo build --release` in `qbench/` first). Verification (exact pop
sequence vs the shipped Calendar) must print `verify ok` for all four workloads first:
`$BIN belt 4096 32768 7 verify` (and formation/averaged/perturbed; done for 5 seeds and
n ∈ {999, 30000, 4096}). Machine state before/after in `machine-state.log` — note the box
rose from loadavg 0.19 to 2.05 during the run (other windows); medians over 3 seeds are
used, and the belt-10⁷ cell ran under load 2.0. Raw cells: `metrics.jsonl`.

Medians over seeds, ns/event (p99 in parentheses):

| cell | calendar_scalar (shipped) | calendar_u64 | binaryheap | wheel | floor |
|---|---|---|---|---|---|
| belt 10⁵ | 554 (884) | 317 (606) | 278 | **108** (363) | 1.5 |
| belt 10⁶ | 831 (1315) | 553 (934) | 582 | **188** (430) | 1.4 |
| belt 10⁷ | 862 (1307) | 710 (1268) | 900 | **343** (394) | 1.3 |
| formation 10⁶ | 622 (1068) | 279 (654) | 376 | **69** (277) | 1.3 |
| averaged 10⁶ | 601 (930) | 414 (742) | 511 | **224** (1450) | 1.4 |
| perturbed 10⁶ | 584 (1387) | 403 (1065) | 536 | **187** (781) | 1.3 |

- **Idiot index at game scales (10⁶–10⁷, the real Scalar interface): 2.5–4.4×** per
  event against the wheel, and the wheel sits at ~1.3–2× the discipline's floor (one
  cold line touch per event, ~100–150 ns at 10⁶ on this box, plus O(1) work; the pure
  streamed-delivery control measures 1.4 ns). So the shipped queue is ~4–8× off the floor.
- **Co-orbital concentration (the board's top scaling risk case) is where the gap is
  largest: 4–9×**, because the tie rule's same-tick batches amortize into one sort
  (max batch 15,959 at 10⁶) instead of 16k full-depth heap pops.
- **The Scalar key interface alone costs 1.2–1.7×** on the heap path (u64 keys are the
  law's own ticks); the biggest single cheap win if the queue keyed on raw ticks.
- **Tails:** the wheel's p99 is below the calendars' everywhere except `averaged`
  (1450 vs 742: bucket-collision sorts; mean still 1.85× better). The wheel's honest
  cost-shape: rare O(n) rebuild spikes — 24 ms at 10⁶, **1.2 s at 10⁷**, once per
  window (~2×10⁹ events between rebuilds on belt; amortized < 1 ns/event, but the
  stall must be chunked — pure scheduling, outcomes unchanged; plane foundation 7
  already forbids unbounded synchronous claims). The heap is uniform by construction;
  that is the trade this design makes.
- **Predictions (`predictions.md`, written before the grid):** held on the wheel's
  dominance and every p99 direction, on the batch amortization (69 ≤ 188 ns), on
  formation max-sample (24 ms, predicted 10–200), on binaryheap losing at 10⁶–10⁷.
  Missed: belt-10⁷ calendar_scalar landed just under the predicted band (862 vs
  900–1700); the u64/wheel ratio at 10⁷ is 2.1× (predicted ≥ 2.5×) — the wheel's own
  cold bucket headers (b capped at 2²² = 100 MB of Vec headers) grow with n; the
  10⁷ rebuild spike hit 1.2 s (predicted ≤ 400 ms); Scalar/u64 at 10⁷ is 1.21×
  (predicted ≥ 1.4×: cold misses dominate both equally). Seed spread reached ±30%
  (predicted ±25%) — the box was shared; recorded, medians used.
## What would make it wrong
- Handoff storms (many earlier re-sets) fall to the side heap; measured under
  `perturbed` at 187 ns/event (equal to belt's monotone 188: at one re-set per 64
  events the side heap is nearly free). If a real scene's re-set rate makes the side
  heap dominate, the fix is the queue's caller (batch re-keys already exist:
  `rekey()`), not the heap.
- Linux/Haswell timings; orders of magnitude only; the M1 (4P+4E, 12/4 MB L2,
  no L3) re-measures differently but the structural argument (footprint vs cache)
  is stronger on it, not weaker.

## Fit with PRINCIPLES

- #12: p95/99 per event measured, both improved; the spike is named, bounded and
  chunkable.
- #19 (one law at every scale): the wheel's cost is per-event + window-rebuild, with
  no log(n) term — it keeps the queue's share flat as bodies grow to 10⁹.
- #16 (cheapest arithmetic): keys are plain u64 ticks (the law's own integers); the
  Scalar key interface costs 1.4× on the heap path alone.

## The lens's blind spot

A local optimum can move cost to neighbours: the wheel moves per-op cost into rare
rebuild spikes (measured), and its `live_t` line touch is only free if the next-time
lives in the body's own record (a storage-layout note, not a queue change). The
neighbours measured: build/bulk-load, cancels (perturbed), burst (formation).
