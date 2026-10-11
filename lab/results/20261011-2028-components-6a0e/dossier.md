# Dossier — the event calendar as a container vs. a scan (components lens)

**Claim.** The engine's "one clock, one queue" (docs/plane.md foundation 2) does not need a
container at all: a per-frame counting scan over the per-body next-event array ("store the
generator, not the generated", PRINCIPLES #6) reproduces the shipped 4-ary indexed heap's
pop stream **exactly** — every (tick, id) order, the frozen tie rule, late requeues included —
at **2.7–3.1× lower ns/event** at 10⁶–4×10⁶ bodies, flat in n, and owning **zero container
memory** (8 B/body key vs the heap's 16 B/body + slack); the shipped heap sits ~4–6× above
this component's memory-physical floor, and the "obvious" steal (a two-level bucket wheel)
only reaches 1.9× and degrades as much as the heap when arrays leave cache.

**Bottleneck.** Board #3/#4 (cost at a billion; smoothness). Not a 10× kill: measured 3× at
today's testable scales, but the *gap widens with n* (heap sift depth grows, its arrays stop
fitting anywhere; the scan's cost per event is 8 B × inter-event gap⁻¹, size-invariant at
fixed density) and at 10⁹ the heap's 24 GB working set does not fit the machine at all while
the scan's key array can ride the binding columns the engine already owns. What it deletes:
the `pos[]` side table, the heap array, and the second ordered copy of ordering information
the engine currently maintains (crates/space `Calendar`, lifted into crates/lattice-event).

**Evidence** (median of seeds 1–3; ns/event; every config's pop stream bit-identical to the
heap's, FNV over the full stream; Linux x86 cloud box, 8 vCPU shared, load 1.1–2.7 during
runs, temps 28–52 °C — orders of magnitude only, per lab rules; machine state in
`state-decisive.txt`):

| n | load | heap | heap p99 | wheel | wheel p99 | scan | scan p99 | heap/scan |
|---|---|---|---|---|---|---|---|---|
| 10⁶ | belt | 319 | 336 | 182 | 187 | **117** | 121 | 2.74 |
| 10⁶ | formation | 334 | 372 | 187 | 189 | **120** | 123 | 2.80 |
| 10⁶ | uniform | 111 | 164 | 36 | 88 | **34** | 91 | 3.26 |
| 4×10⁶ | belt | 408 | 409 | 208 | 222 | **133** | 151 | 3.08 |
| 4×10⁶ | formation | 386 | 395 | 211 | 212 | **136** | 139 | 2.85 |
| 4×10⁶ | uniform | 107 | 164 | 37 | 58 | **36** | 63 | 3.00 |

Memory at 4×10⁶: heap 64 MB (12 B entries + 4 B pos), wheel 88 MB (next/prev/key/gen/live/lvl),
scan 33 MB (key + per-frame buffers). The under-floor control (FIFO ring, uniform load) reads
0.3 ns/event: unreachable, because it omits the one random re-time write per event that is
this component's real memory-physical floor (≈ 60–100 ns at these working sets). Against that
floor the scan sits at ~1.3–2×, the heap at ~4–6×, the wheel at ~2–3×.

Reproduce (each ≤ 60 s, from this folder):
```
rustc -O calbench.rs -o calbench
./calbench --n 1000000                 # ~30 s, all loads
./calbench --n 4000000 --load belt     # ~11 s (also: formation, uniform)
```
`calbench.rs` carries: a faithful port of the shipped `Calendar` (4-ary, pos[], pop-by-cancel,
requeue churn 0.5%/frame, 256-tick frames), the two-level intrusive wheel, the `ScanCal`, and
the identity controls. Raw per-seed rows in `n1m.json`, `n4m-*.json`; medians in
`results-medians.json`.

**Design (one step to adopt).** `ScanCal::frame(base, target)`: one sequential pass over
`key[]` counting due ticks in `[base−1, target]` (the `base−1` slot is a requeue at "now",
which the heap's pop loop fires first); a stable scatter by tick gives the batch already in
`(tick, id)` order — the frozen tie rule for free (law.md, 5 October); a small 4-ary heap of
same-frame re-due events (cadence < frame) merges in by `(tick, id)`, matching the heap's
interleaved re-pop semantics exactly. `peek` for the horizon between frames is a byproduct of
pass 1 (min key beyond target). Cancels and re-timings are plain key writes — no unlink, no
sift, no stale entries. Semantics match `pop_through(deadline)` batches (foundation 7: budgets
change when, never what).

**Predictions** (`predictions.md`, written before the 1M/4M runs; tuned only on a 100k smoke):
exactness held everywhere (3) — after the controls caught two real bugs in my candidates: a
stale-pointer splice in the wheel (popped bodies live in `ready`, and `unlink` treated
"not-in-a-list" as "in-level-1"; benign at ≤10⁶, dropped ~23k events at 4×10⁶) and the scan
dropping requeues at the previous frame's tick (10 events at 100k). Both were found by the
pop-stream identity control, not by inspection — the rung lesson that controls on both sides
pay. Heap-cost growth held (2.37× from 100k→4M, ≥1.5 predicted) (2a). **Failed:** the ≥4×/≥5×
speedup (got 2.7–3.1×) — this box's L3 keeps sift touches cheaper than modeled; wheel stays
flat (it degrades 3.8×, predicted ≤1.3×) — bucket lists are id-random pointer chains, so the
wheel chases DRAM too; "uniform weakest" (it is the strongest at 1M); tail flatness mixed
(scan p99 ≤ heap on belt/formation, worse on uniform: 91 vs 64 ns).

**What would make it wrong.** An engine whose per-frame pop horizon is far sparser or denser
than a belt at 32 kicks/orbit (the scan's cost is the key-array pass amortized over the due
batch; at pathological sparsity — every body silent for megaticks — the amortization dies and
a hierarchical variant is needed); multi-doll queues whose keys are not one integer tick
basis; and the measurement being synthetic — the op mix (pop→re-time at t+cadence, 0.5%
churn, 256-tick frames) is taken from `universe.rs`'s `requeue`/`set(e,None)` pattern, not
wired end-to-end. **Adoption cost:** replace `Calendar` behind its three call sites
(`set`/`peek`/pop-through in universe.rs and lattice-event), move `key` next to the binding
columns, keep the tie rule as the scatter's stability — one contained change, no gate edits.
**Fit:** PRINCIPLES #6 ("store the generator, not the generated"), #14 (no ticks: the frame's
deadline batch is the engine's own `pop_through`), #16 (integer ticks, cheapest arithmetic —
counting, no comparisons), #22 (the simulation still decides; the scan is exact, not a
heuristic schedule). The wheel result also settles the prior-art lead
(`docs/reference/original-research-report.md`: "radix heaps or hierarchical bucket queues
deserve benchmarking"): benchmarked — bucket *wheels* are the wrong half of that suggestion;
the radix *scan* is the right one.

**The lens may have made me miss:** end-to-end framing (Amdahl: the queue is ~⅓ of an event's
cost at 4M — the 6 October gold says window setup dominates kicks — so 3× here is ~1.2× on a
frame today, growing with scale); single-threadedness (the scan chunk-parallelizes over
`key[]`, the heap's sift serializes — unmeasured); and I did not measure the doll-level
min-of-mins (`Hierarchy::root_time`) that sits above this queue.
