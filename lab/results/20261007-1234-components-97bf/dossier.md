# Dossier — 20261007-1234-components-97bf

**Lens:** first principles, one component at a time. **Component:** the event calendar (the
sparse order's queue; plane.md foundation 2: "One clock, one queue… a min over the dolls").

## Claim

The engine's event calendar does not need a comparison structure at all: because event
times are canonical integer ticks, a bitmapped timing wheel with one 24-byte packet per
body delivers the **identical** (tick, body-id) stream at **2.2–4.5× lower cost** than the
shipped indexed 4-ary heap, with a **flat p999/p50 (2.1 vs 6.3)** — and the measured floor
analysis says the heap is ~16× over the memory floor at 16.7 M bodies while the wheel sits
~3.5× over it. The calendar's cost is memory-line count per event, not algorithm: at
10⁹ bodies every one-slot-per-body structure is DRAM-latency-bound, and the wheel touches
~6 lines where the heap touches ~25.

## Bottleneck

PRINCIPLES #12 (OC#36: "the algorithm that allocates the work to prevent those heavy
tails, it's the most important one"; "i care about the p95/99"), #14 (no ticks: the queue
*is* what replaces ticks), #3 (compute only surprises: the container must not outcost the
surprise), #17 (von Neumann). The shipped `Calendar` (`crates/lattice-event/src/lib.rs`)
already reports "sift-down dominated the calendar's cost at a million bodies" — the queue
is the measured hot spot of the sparse order at today's frontier, and the plane needs the
same min over 10⁹ bodies.

## Floor

An event must be written once and read once: 16 B in+out. Measured on this machine
(`floors` mode): streaming floor **1.33 ns/event**, dependent-chain (L1) floor
**2.0 ns/op**. At DRAM scale the floor is ~2 cache lines per event ≈ **260 ns** (any
structure that stores one slot per body must touch the body's record). "physics loves e
while we love 2" (OC#38): base-2 wheel, bitmap occupancy, CLZ finds the next tick.

## Evidence

Binary: `work/calendar-bench` (Rust, isolated workspace; `cargo build --release`, binary
at `$CARGO_TARGET_DIR/release/calendar-bench`). Incumbent = `Calendar` copied verbatim
(4-ary, `pos` backpointers). Candidate = ring of W = 2²¹ buckets + 2-level occupancy
bitmap + intrusive links in one 24 B per-body packet (`at`,`prev`,`next`,`loc`) + lazy
min-heap overflow for delay ≥ W. Digests of the delivered (tick, id-ascending) stream
must match across structures — the law's tie key (time, smallest body id).

Reproduce (each ≤ 60 s; medians over seeds 1–3; single thread; 8 vCPU cloud box,
load 0.3–0.9, 14 GB free — state in `results/machine.txt`):

```
B=.../calendar-bench
$B A 1 1 1 floors x                                   # -> results/floors.json
for s in 1 2 3; do for lg in 12 14 16 18 20 22 24; do
  for st in heap wheel; do for m in clean tail; do $B A $((1<<lg)) $s 500000 $m $st; done; done; done; done
for c in B C D; do for s in 1 2 3; do for lg in 16 22 24; do
  for st in heap wheel; do $B $c $((1<<lg)) $s 500000 clean $st; done; done; done; done
$B C 16384 1 20000 clean linear; $B C 65536 1 20000 clean linear
for c in A B C D; do $B $c 4096 7 50000 diff x; done   # differential: heap vs wheel, step-by-step
```

Case A engine-shaped churn (85% "later", 15% near-immediate; quantized to 64-tick
epochs), B all-earlier, C clustered ≤1024, D far-horizon (overflow-heavy). All raw rows
in `results/*.jsonl`.

| N (case A) | heap ns/op | wheel ns/op | ratio | wheel p999/p50 | heap p999/p50 |
|---|---|---|---|---|---|
| 4 096 | 88 | 31 | 0.35 | 7.6 | 12.9 |
| 65 536 | 106 | 38 | 0.36 | 9.3 | 15.2 |
| 1 048 576 | 245 | 87 | 0.35 | 4.0 | 3.1 |
| 4 194 304 | 993 | 247 | 0.25 | 2.1 | 5.7 |
| 16 777 216 | 4 243 | 946 | **0.22** | **2.1** | **6.3** |

- **Correctness (P1, held):** 0 digest mismatches in 48 (case,N,seed) groups + 30
  cross-mode groups, including the overflow case D; `diff` mode (step-by-step heap vs
  wheel) reports no divergence on all cases.
- **Heap scaling (P8/P2a, held):** 48× growth 2¹²→2²⁴ (the benchmark exercises depth).
- **Ratio (P3, held):** 0.22 at 2²⁴; B/C/D: 0.22–0.53.
- **Wheel flatness (P2b, failed):** the wheel also grows (31×) — with **footprint**, not
  depth: flat only while resident (31→36 ns from 2¹²→2¹⁴), then DRAM-latency-bound like
  everything at one slot per body. This is the informative failure: at scale the lever is
  *lines per event* (wheel ≈6, heap ≈25 including `pos`).
- **Tails (P4, held at 2²²/2²⁴ as pre-registered):** wheel 2.1 vs heap 5.7/6.3; at 2²⁰
  wheel 4.0 > 3 (partial).
- **Floor distance (P6, mixed):** wheel = 15× the L1 floor in-cache (predicted ≤10),
  ~3.5× the 2-line DRAM floor at 2²⁴; heap ≈ 44× in-cache, ~16× at DRAM scale.
- **Negative control (P5, failed as pre-registered):** no-structure linear scan is only
  11–12× the wheel at belt density (case C: 450 vs 38 ns/op), because events-per-tick
  amortize the scan; at sparse density it would diverge further. The control separates,
  but not by 100×; reason understood, not tuned away.
- **Overflow (P7, failed in the good direction):** even case D (half the events beyond
  the wheel horizon) stays 0.30–0.53 — the lazy overflow heap is small, so its log
  factor barely bites. The wheel's real weak spot is elsewhere: **same-tick storms**.

**Disclosed mid-run findings (all before the final data; every number regenerates):**
case A's delay mixture degenerated after epoch quantization (~96% of bodies in the first
64-tick epoch), so at 2²⁴ case A measures a shared-epoch storm — engine-real (law.md:
"one uniform vector per kick epoch") but named as such; of the wheel's 0.47 s wall at
2²⁴, ~0.1–0.2 s is sorting one 16 M-entry bucket by id (the heap pays the same storm as
16 M × log-depth pops). A radix/counting sort by body id would cap it — next measurement.

## Predictions

`predictions.md` was written before the decisive sweep; the outcomes are marked inline
above (P1 held, P2 split, P3 held, P4 held at the pre-registered sizes, P5 failed with
reason, P6 mixed, P7 failed in the wheel's favour, P8 held).

## What would make it wrong

1. Dense shared-epoch ticks cost the wheel a per-tick sort (k log k) — capped only by
   switching to id-radix; if the engine's real tick density is storm-like, measure that
   first.
2. The wheel assumes integer ticks and a horizon W covering the certificate span
   (2²¹ here); far-horizon events fall to the overflow heap (still fast, but no longer
   O(1)-flat). A cascade level trades memory for horizon.
3. Cloud timings are orders of magnitude only: the M1 (unified memory, 16 KB pages) may
   soften the DRAM cliff — the *line count* argument is what transfers.
4. Measured in isolation; the slack allocator above the queue changes the op mix
   (batching due-tick work would amortize further, in the wheel's favour).

## Cost of adoption, fit with PRINCIPLES

~150 lines replacing `Calendar` in `lattice-event`; the 24 B packet joins the body's
record (the same store `shipmem` lays out); delivery order is the law's tie key by
construction, so B8 determinism is unchanged (digests prove it). PRINCIPLES #16 ("there's
no continuum… physics loves e while we love 2"): the queue becomes base-2 arithmetic —
mask, CLZ, intrusive links — with **no comparisons at all**; #17 ("best part is no
part"): the priority structure degenerates to a bitmap over time itself, which is Julien's
"memory laid out in causal order" (29 September) made literal: the ring *is* the timeline.

## The lens

What this lens may have missed: a local optimum can move cost to neighbours — the wheel
makes the *drain* cheap but pushes ordering work into per-tick sorts, and I measured the
sort only as part of the storm wall time, not separately. The queue was also judged at
fixed workload shapes; the allocator's real op mix (slack-ordered, batched per frame)
remains unmeasured.
