# Dossier — 20261006-1436-components-ed09 (components lens): the event queue

## Claim

The engine's one queue (`Calendar`, an indexed 4-ary heap copied verbatim into this bench) sits 30–100× above its information floor at a million-plus slots; a lazy-deletion bucket wheel (hashed timing wheel) with per-slot version numbers is order-identical bit for bit on every workload tried, runs 1.9–5.2× faster (146–451 ns vs 585–1045 ns per pop+set at 3×10⁶ slots), and lands within ~10× of the floor — but it only clears its own kill criterion marginally under churn (2.06× at 10⁶), so it is a design answer, not an adoption-grade 10× win.

## Bottleneck

Board focus item "kicks dominate the engine's cost" and the top scaling risk (work that grows faster than real encounters). The queue is the no-tick mechanism itself (P14): every kick and every certificate re-prediction pays one `pop` + one `set`. The crate's own comment concedes "sift-down dominated the calendar's cost at a million bodies" (crates/space/src/events/calendar.rs, lifted from crates/lattice-event). Expected gain: ~4× on the queue's share (1.5–3% of a plane kick today at 10⁶ slots; ~7 vs ~1.7 cores of pure queue traffic at 10⁹ bodies, rtf 1, Fermi-priced), and it deletes the log-n/cache-depth term from the scaling risk. Not a 10× board move at plane scale — stated plainly.

## The component, its owner and its floor

- **Owner (PRINCIPLES):** P14 "No work for no reason, so no ticks" — the queue is what replaces ticks; P22 "the simulation tells us what's next not us"; P16 "physics loves e while we love 2" (bucket width is a power of two); P26 steal from skin in the game (hashed timing wheels: Varghese & Lauck 1987, Linux kernel timers, calendar queues in network simulators — practitioners who paid for slow timers).
- **Floor:** each event must be written once and read once in time order: ~2–4 dependent memory accesses + branches ≈ 10–20 ns per pop+set; ordering information itself is free because time is already quantized (integer ticks; the engine's `Scalar` → `fixed_ceil` deadline conversion exists for exactly this).
- **Idiot index:** heap 585–1045 ns at 3×10⁶ slots ≈ 30–100× above floor (log₄ n sift levels, each a cache miss on a 24 B/entry array that overflows L2 beyond ~5×10⁵ entries). Wheel 125–153 ns (belt/burst) ≈ 6–15× above floor. The lens goal — a design within 10× of floor — is met on the spread workloads; the heap is not.

## Evidence

All numbers: Linux x86 cloud (orders of magnitude only; integrator re-measures on the M1). Reproduce:

```
cd lab/results/20261006-1436-components-ed09/work
rustc -O --edition 2021 queue_floor.rs -o qf && ./qf all 2000000   # ~55 s, prints the matrix
./qf debug4    # brute-force oracle: every wheel pop vs min over cur[] (churn, ~220 s)
```

Final matrix (ns per pop+set cycle, min of 2 reps; `heap/wheel`, order check):

| workload | n=10⁵ | n=10⁶ | n=3×10⁶ |
|---|---|---|---|
| belt (tuned) | 253/70 | 495/126 | 585/146 |
| churn (lateral ±128, 10% cancel) | 375/198 | 819/397 | 1027/451 |
| burst (formation, one interval) | 250/48 | 487/110 | 559/126 |
| tail (5% re-sets 16–64× out) | 255/78 | 507/143 | 600/153 |

Every cell ORDER-MATCH: the wheel's pop stream (tick, slot) is bit-identical to the heap's over 2×10⁶ pops (rolling-hash chain compared entry-wise). Controls on both sides, every workload: the heap itself is the positive reference; a wheel variant that serves buckets unsorted FAILS the order check (`negative(wheel-nosort): fails as expected` — after the bench window was extended past the minimum re-set interval, because short windows only ever saw the slot-ordered initial fill; the first version of this control could not fail and was fixed before any decisive number was kept). `debug4` additionally cross-checks every wheel pop against a brute-force minimum over all slots: consistent through the full churn run.

Scaling (belt): heap 253→495→585 ns (2.3× from 10⁵ to 3×10⁶); wheel 70→126→146 ns (2.1×). The wheel is NOT flat: with fixed bucket width w=1 tick, occupancy per bucket grows with density (∝ n at fixed spread), so the snapshot sort costs ~log(density). A density-adaptive width (w ≈ n/(B·4), still a power of two, correctness independent of w) is the named experiment to flatten it; the heap has no comparable lever.

## Predictions (see predictions.md)

Written after tuning only on belt. Held: churn/burst/tail order-match; burst ratio ≥ 2.5× (4.45×); tail ≥ 2× (3.53×); heap scaling ≥ 1.5× (2.3×). Missed: churn ratio ≥ 3× (measured 2.06× at 10⁶ — versioned lazy deletion plus frontier traffic is costlier than predicted); wheel flat within ±25% (it grows 2.1× with density); idiot index ≥ 5× at 3×10⁶ (3.97–4.45×, just under). The first wheel design also FAILED order twice before the final one: (1) entries snapshotted into the open bucket were served without re-validating against the slot's current time, so a re-set landing on a due-now slot was served at its old tick (caught by churn and tail); (2) duplicate live entries after cancel+re-add to the same tick served a slot twice — fixed with per-slot version numbers; (3) refill was a no-op while unexamined snapshot entries remained, so a churn-killed snapshot tail could return "empty queue" with live entries in buckets. All three were found by held-out workloads and the brute oracle, not by the tuning workload — the ladder's argument for held-out cases, demonstrated on my own work.

## What would make it wrong

- A battle hand-out (every slot re-set to the SAME tick) is not in the matrix: burst spreads over one interval. One bucket would then hold n entries; the snapshot sort pays n log n once, on contiguous memory — probably still ahead of the heap's per-insert sift, but unmeasured.
- The engine's real re-prediction distribution: if most re-sets move events EARLIER (the bench's moves are ±128 ticks around the current time), stale traffic rises and the churn column (weakest, 2.06×) is the honest preview.
- Extreme far-tail fractions (>30% of live events beyond the horizon) would fill the overflow heap and erase the win; tail at 5% still gives 3.5×.
- `pop_through(deadline)` peeks before popping; the wheel's peek is O(bucket-scan) not O(1) — the bench measures pop, not peek-heavy patterns.
- Adoption cost: replace `Calendar` (same API: set/cancel/pop/peek), add a `ver` word per slot (12 MB at 3×10⁶ slots; heap already spends 36 MB on heap+pos), choose w from local density. Determinism is untouched: integer ticks, exact (tick, slot) order, no floats deciding anything.

## Fit with PRINCIPLES

"there's no continuum, physics may be quantitized but appear continous at the right scale… no it's about what's cheapest to compute" (OC#38): the wheel only exists because time is already quantized — the floor argument dies in float time. "we need to keep doing those smarter math and old tricks when people used to be compute deprived" (CL 09-29): the wheel is the compute-starved OS/networking world's queue. And the discipline the lens asked for: measure the neighbours — the queue is 1.5–3% of a plane kick today, so this is a floor-mapping result for the scaling risk, not the next engine lever (cadence still is).

## The lens (what it may have made me miss)

A component-at-a-time view prices the queue in ns/op but not in allocator interaction: the wheel's per-bucket Vecs allocate under churn where the heap is one pre-allocated block (the engine's "allocated once" invariant — lattice-event lib.rs — is a real constraint the bench's steady-state does not test). I also did not measure the neighbours' response to the change in pop-side cache pressure on the rest of the frame, and I took the crate's own workload description (pop earliest, re-set later, mostly-lateral moves) rather than instrumenting the plane's actual op mix.
