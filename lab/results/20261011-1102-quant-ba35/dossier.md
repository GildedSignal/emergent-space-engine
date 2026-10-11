# Dossier — 20261011-1102-quant-ba35 (lens: Quant)

**Claim.** The plane's kick path is compute-bound — every kick is a fresh cycle compile (exact-memo hit rate 0.0 at every scale) costing 36–38 µs for made ships and 92–102 µs for handed-out fleet members, flat as the store grows past L3, with the record round-trip at 0.14% of a kick — but the plane stops flying between 400 and 4,000 fleet members on two other walls: one unsplittable fleet battle slice of 0.95 s, and a view gather of 14.9 ms p50 at 2,132 bodies.

**Bottleneck.** Board item "fewer kicks per orbit" and the smoothness/allocator item. The measurement redirects: at fleet scale the kick resolver is *not* the frame's problem; the fleet slice and the gather are. Deleting the wrong target (record layout, cache-line packing of `BodyRec`) buys ≤ 0.14% per kick; making the fleet slice splittable and the gather sublinear buys the flight back. Numbers are x86 orders of magnitude (the integrator re-measures on the M1).

**Evidence** (i7-4790, 4C/8T, L1d 32 KiB, L2 256 KiB/core, L3 8 MiB shared, perf blocked by `perf_event_paranoid`; machine state recorded inside every JSON by the harness; commit a838a284, tree patched by this run — clone-timing in the kick bench, a sizes test, and the `--members` clamp raised from 400 to 500,000):

Layout audit (`cargo test --release -p emergent-universe quant_layout_sizes -- --nocapture`):
`BodyRec=448 Item=16 Binding=176 Kick=48 Ext=96 Segment=192 BodyInfo=72 Tube=16 Trajectory=176 Knot=88` — the plain store's record is 28× the law's 16-byte tube before heap; the plane reports 6.9–9.0 KB per body at rest (432–562×).

Kick sweep — `xtask universe --kick-bench --members M --rtf 100 --seconds 3` (JSON: `kick-m*.json`):

| members | bodies | store | made med/p99 µs | leavers n / med / p99 µs | clone med µs | exact hit | quantized hit |
|---|---|---|---|---|---|---|---|
| 48 | 71 | 0.4 MB | 41.8 / 78.1 | 236 / 120.1 / 523.8 | 0.056 | 0.0 | 0.83 |
| 400 | 393 | 2.8 MB (in L3) | 36.2 / 65.9 | 2,596 / 92.7 / 392.5 | 0.048 | 0.0 | 0.91 |
| 4,000 | 3,842 | 34.5 MB (4.3× L3) | 38.2 / 65.8 | 39,143 / 102.2 / 386.0 | 0.054 | 0.0 | 0.945 |

- Resolver cost is flat across the L3 boundary (made 1.06×, leavers 1.10× from 2.8 MB to 34.5 MB): kicks are compute-bound, not memory-bound, at these scales. The bench's index-ordered scan warms each record first, so this is the warm-path floor; the real path's overhead is measured next.
- The record round-trip (`BodyStore::rec` clone: 448 B + plan Vec + malloc/free) is 0.13–0.15% of a kick. Packing `BodyRec` into cache lines is not a lever.
- Exact-memo hit rate 0.0 at every scale (37,490 rebinds at 4,000 members); quantized 12+12-bit cell hits 94.5% but the engine rightly does not use it (it changes orbits — 5 October finding, re-measured here from a different lens and machine). The compile *is* the kick.
- Members ≥ 40,000: the run dies on the kick bench's own 55 s watchdog (its per-frame O(N) check-clone scan plus the fleet battle's cost), and the scenario build's memory is superlinear: maxrss 40 MB (400) → 587 MB (4,000) → 1.55 GB (40,000) → 3.5 GB (200,000, killed by the outer 90 s timeout). The 200k run breached the window's 2 GB budget before dying; my mistake, noted for the record.

Real frame path — `xtask universe --bench --members M --rtf 100 --seconds 3 --unpaced --threads 1` (JSON: `bench-m*.json`):

| members | events/s | ship µs/item | fleet µs/item | frame p50 / p99.9 ms | hitches/h > 16.7 ms | rtf median |
|---|---|---|---|---|---|---|
| 400 | 2,120 | 73.9 (n=3,267) | 88.8 (n=2,672) | 7.8 / 13.4 | 0 | 100 |
| 4,000 | 702 | 0 (no kick resolved) | 951,681 (n=1) | 28.9 / 38.6 | 198,000 | 0 |

At 4,000 members the whole 300 s of game time is spent inside **one fleet battle slice: 0.95 s single-threaded, one event, unsplittable by the 5 ms engine budget** (`slices: 1, leavers: 2104, kicks: 0`; all 180 frames overflow). The budget counts events, and one fleet event is 57 frames' worth of budget. Independently, the view gather alone is 14.9 ms p50 at 2,132 bodies — nearly the whole 16.7 ms frame. Real-path ship cost is 2.04× the pure resolver (73.9 vs 36.2 µs): the residual ~38 µs is rekey, queue, apply/put and wave coordination, not memory.

**Predictions** (`predictions.md`, written before the sweep): P1 held (flat past L3), P2 held (clone ≤ 0.15%), P5 held (7–9 KB/body), P6 held (leavers 2.6–2.7× made). P3 failed low: real-path overhead is 2.04×, not 3–10×. P4 failed: resolver p99/median is 1.7 (made) and 3.8 (leavers), not ≥ 5 — the true tail is not in the resolver at all; it is the fleet slice (0.95 s), which the kick bench cannot see. Two findings were not predicted: the fleet-slice wall and the gather wall.

**What would make it wrong.** The flatness is the warm-path floor measured on a scan-warmed bench; a cold, scattered-order workload (waves keyed far apart in index space, or the store paged out) could still show a memory step — my sweep only reaches 34 MB because the bench and the scenario die beyond it, so the DRAM regime above ~10⁴ bodies is unmeasured, not exonerated. The 0.95 s slice is one seed at one anchoring; a different `Order` (Sparse vs Dense) or thread count could move it, though not the unsplittability. Adoption cost: nothing to adopt — this run deletes targets (record packing, clone elimination as kick levers) and names two (the slice's granularity, the gather's per-body cost). Fit with PRINCIPLES: "the cheapest compute is compute not done" (the recompile per kick at 0% reuse is the compute being done 39,193 times); "make expensive work bounded, movable, predictable, or avoidable" (plane.md foundation 7 — the fleet slice is none of these today); "measure before claiming".

**The lens.** The Quant lens priced the kick path and the frame tail, and nearly missed what its own instrument hid: the bench times only the resolver, so the thing that actually kills the flight at scale (the fleet slice, the gather) was invisible until I ran the real path. It also tends to treat the 2× real-path overhead as noise; at 2,120 events/s that residual is half the engine's throughput and worth someone's run.
