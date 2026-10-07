# Dossier — run 20261007-0933-components-2aaa (components lens)

## Claim

The event queue ("one clock, one queue", plane.md foundation 2) sits 2–6× above its
memory floor at the scales the goal demands (10⁵–3×10⁷ live entities): the engine's
4-ary indexed heap costs 160–580 ns per event there, against 23–97 ns median for a
hierarchical timing wheel keyed on the same root-clock integer ticks, with the exact
same `(tick, id)` pop order (verified bit-for-bit and against a linear-scan oracle).
The wheel is a drop-in for `Calendar`'s interface (`set`/`peek`/`pop`, one slot per
body, no stale entries) and its levels mirror the doll clock exponents — but its cost
concentrates into due-tick batches (worst batch 288–2,707× its median), so it is
only adoptable behind the plane's budget slicer, and the honest amortized win is
~1.7–3.9×: **not the 10× the lens hunts for. Silver: real, one experiment away.**

## Bottleneck

Not today's plane (≤ 10⁴ entities: both designs cost 20–130 ns/op, irrelevant next to
the ~µs physics resolve). It is the scale risk on every event's path: 10⁹ bodies at
32 kicks/orbit means the queue is touched per event, serially, pointer-chasing, while
the resolve itself batches and parallelizes. PRINCIPLES #12 names the allocator "the
most important one"; the queue is its substrate. Lens question answered: the component
with the largest measured design-to-floor gap found in this run.

## Floor (the lens's step 2)

Keys are canonical integer ticks (world.md: "a queue of ticks needs no conversion"), so
an event's bucket is a pure function of its key: no comparisons are needed to order it,
only modular arithmetic. A hierarchical wheel over power-of-two levels (PRINCIPLES #16,
"we love 2") realizes that: per event ~2–4 dependent memory touches (unlink, link,
amortized cascade ≤ 3 per firing), ~5–10 ns, 24 B/entity + 1 MB of heads. The measured
wheel sits at 23–97 ns median — within ~10× of that floor (the gap is tick density:
thousands of events share a tick, and id-ordered delivery pays a sort). The heap pays
log₄N sift levels, each swap also writing through a second random-access `pos[]`
array, and grows with N: measured 88–132 ns at 10³ → 433–577 ns at 3×10⁷.

## Evidence

Machine (recorded in `machine.txt`): shared GitHub Actions runner, 8 vCPU Intel
i7-4790 @ 3.60 GHz, load 1.65 during the run, 15 GB RAM. Linux/x86 — orders of
magnitude only; the integrator re-measures on the M1, whose 12 MB L2 (no L3) moves the
crossover earlier, in the wheel's favour.

Structures: `heap4` = a line-for-line mirror of `crates/space/src/events/calendar.rs`
(indexed 4-ary heap, inline `(time, id)` keys, `pos[]` backpointers, one slot per
body); `heap2` = arity-2 control; `wheel` = 4 levels × 2¹⁶ intrusive doubly-linked
buckets, nonempty-bitmap skip-ahead, and each due tick drained as one batch delivered
in id order (insertion sort ≤ 32, LSD radix above). Workload = the universe's
per-event mix: pop the min, re-insert that slot at `t + interval`; intervals fixed per
body, log2-uniform (doll exponents are powers of two); initial phases stationary
(due within one interval). Median of 3 seeds; `p50` is the median 64-op batch, `mean`
is the whole-run amortized cost.

| dist | N | heap4 p50 | wheel p50 | × | heap4 mean | wheel mean | × |
|---|---|---|---|---|---|---|---|
| wide (2⁶–2²⁶) | 10³ | 132 ns | 27 ns | 4.8 | — | — | — |
| wide | 10⁵ | 246 | 23 | 10.6 | 311 | 108 | 2.9 |
| wide | 10⁶ | 402 | 75 | 5.3 | 565 | 334 | 1.7 |
| wide | 10⁷ | 425 | 93 | 4.6 | 414 | 223 | 1.9 |
| wide | 3×10⁷ | 433 | 93 | 4.7 | 428 | 239 | 1.8 |
| narrow (2¹⁰–2¹⁴) | 10⁵ | 164 | 49 | 3.3 | 166 | 43 | 3.9 |
| narrow | 10⁶ | 344 | 67 | 5.1 | 325 | 145 | 2.2 |
| narrow | 3×10⁷ | 577 | 97 | 5.9 | 555 | 242 | 2.3 |

Controls, both sides:
- **Correctness (positive):** all three structures produce bit-identical pop-sequence
  hashes in all 30 (N, dist, seed) configs, and at N ≤ 10⁴ a linear-scan oracle
  verified the first 20k pops are the true `(t, id)` minimum. The wheel keeps the
  frozen tie contract exactly (ties.rs).
- **Known-worse (negative):** `heap2` loses to `heap4` by 1.30–1.49× at N ≥ 10⁷ and is
  at parity when everything fits in cache — as expected for the control.
- Mean vs median diverge because the wheel concentrates cost: a due tick with ~44,742
  events (wide, 3×10⁷; chains: mean 44,742, max 44,943) is drained, radix-sorted and
  delivered as one batch. Wheel worst-batch/p50 = 288–2,707×; heap4's own p99/p50 also
  degrades to ~75–98× at N ≥ 10⁷ in some configs (unexplained here: THP collapse or
  runner sharing; flagged, not diagnosed).

Reproduce (each command ≤ 60 s unless noted):
```
cd lab/results/20261007-0933-components-2aaa
gcc -O3 -march=native -o bench bench.c
./runall.sh            # 90 runs, ~160 s total; writes results.jsonl
python3 summarize.py   # the table above (medians over seeds)
./bench wheel 5000 10 14 29 30000 1   # oracle-checked correctness, ~2 s
```

## Predictions (predictions.md, written before the decisive run)

Held: heap4 grows with N (132→577 ns against the predicted 15–500 band); wheel roughly
flat (27→97 against 10–30 + a density term); heap2 control loses (1.3–1.5× at scale);
wheel tails ≥ 2× median (held, extravagantly: up to 2,707×). Missed, reported as
held-out misses:
- I predicted the ≥ 5× idiot index **at 3×10⁷ on amortized cost**; it holds only on the
  median (4.7–5.9×). Amortized it is 1.8–2.3×: the wheel's batch drains carry a real
  sort cost my estimate ignored.
- I placed the crossover at N ≈ 10⁶; the median crossover is nearer 10⁵ (10.6× already
  at 10⁵ wide) — the `pos[]` backpointer array bites before the heap array does.
- My first run used a non-stationary initial spread (all deadlines uniform over
  2^(hi+1) ticks regardless of interval); those numbers are kept in
  `results-transient.jsonl.bak` and were discarded: they understate tick density. The
  stationary init is the faithful state (a body's next event lies within one interval).

## What would make it wrong

The M1's small fast L2 could pull the heap's mid-N numbers down; the runner's sharing
could inflate the heap's tails. The wheel's advantage also shrinks if events per tick
are huge AND per-event delivery must stay smooth without a budget slicer — then the
heap's spread-out cost is the safer shape. And if the plane stays at ≤ 10⁵ live
entities, the whole component is below the resolve's noise floor and should not be
touched (PRINCIPLES #1: the cheapest compute is compute not done — including this
rewrite).

## Cost of adopting, and fit with PRINCIPLES

Adoption: replace `Calendar`'s body with the wheel behind the same `set`/`peek`/`pop`
interface — the plane's `requeue`/`peek` callsites are unchanged, and `Scalar::integer`
deadlines are already the root-clock ticks the wheel keys on. ~200 lines, one crate,
gated by the digest and tie tests (B8, ties.rs), which the identical pop order already
satisfies. Risk: the burst shape needs the frame budget slicer (plane.md #7) to bound a
due-tick batch per presented frame.

- "the algorithm that allocates the work to prevent those heavy tails, it's the most
  important one" (CL 09-25 14:28) — the queue is that algorithm's substrate.
- "physics loves e while we love 2" (OC#38) — integer ticks + power-of-two levels make
  the ordering free modular arithmetic, no comparisons.
- "Compute only surprises" (#3) — see the next rung: the true floor is per *surprise*,
  not per event.

## The next rung (what would make it gold)

The deeper floor this lens exposed: both heap and wheel pay **per event**, but a
quasi-periodic event's due tick is derivable from `(phase, interval)` — the stored
generator (PRINCIPLES #6). A phase-ring tier (bodies grouped by interval class, one
bucket per phase per class) answers "what is due at tick t" in O(#interval-classes)
per tick, independent of N; only *surprised* bodies (a kick moved the interval,
rebinding, an encounter) enter the wheel. Cost then tracks the surprise rate — the
same story as the plane's exact memo (the plane recompiles ~99% of kicks today; the
memo work in flight drops that). Phase rings + this wheel, measured as ns per event at
fixed surprise rate, is the 10× the lens hunts: one rung away.

## The lens

The components lens prices one part against its floor; a local optimum can move cost
to a neighbour. Measured neighbours: the resolve (~µs/event) still dominates at plane
scale, so this win is invisible end-to-end today — a bet on scale, stated as such, not
an engine speedup. What the lens may have missed: parallelism. The heap is serial
pointer-chasing; the wheel's batch drain (unlink, radix sort, link) is embarrassingly
parallel and GPU-shaped, which a single-threaded benchmark prices at zero — the true
gap at 10⁹ is therefore likely larger than measured here.
