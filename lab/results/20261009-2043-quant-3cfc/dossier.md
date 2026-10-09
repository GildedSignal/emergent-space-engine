# Dossier — 20261009-2043-quant-3cfc (Quant lens)

**Claim.** The plane's smoothness contract breaks at ~1,600 fleet members (not somewhere near 10⁵): the frame's first handout slice is indivisible and costs 0.62 s at 3,200–6,400 members, and each member handed out of the frame costs ~6.5 KB resident universe-side, so a 10⁵-member fleet reaches 4.2 GB and a 10⁶-member fleet 8.7 GB — the 8 GB M1 target cannot fly today's plane at B15's 2²⁰-ship rung.

**Bottleneck.** Board: "Cost at a billion" / B15 / fitting 10⁹ in 8 GB; the quant lens's capacity question ("the N at which the edge vanishes"). Expected gain from fixing: the exodus tax is 0.25–0.8 ms per leaver landing in whole-frame spikes (principle 12's spike compute); slicing it is the same rule the lattice crate already applies everywhere else. The 6.5 KB/body is ~400× the law's 16-byte tube and decides B18 for the plane.

**Evidence** (Linux/x86, 1 thread, seed 1, unpaced, rtf 100 unless said; orders of magnitude only, per lab rules; `T=target/release/xtask`, built at this commit):

Requires this run's one-line edit (saved as patch): `--members` clamp 400 → 2,000,000 in `xtask/src/universe/mod.rs:32`. **The shipped harness clamps `--members` at 400 — the plane has never been load-tested above 400 members.**

| members | s | RSS | fleet slices | frame p50 / p99 (ms) | verdict |
|---|---|---|---|---|---|
| 400 (default) | 10 | 48 MB | 9,779 × 31 µs + 163 µs @2 s | 4.8 / 10.1 | holds; view_gather 54 %, engine 32 %; overflow 105/600 |
| 1,600 | 2 | 124 MB | 277 × 2.4 ms (≈ one 0.6 s exodus + cheap ticks) | 15.3 / 25.1 | **broken** (p99 > 16.7 ms; overflow 116/120) |
| 3,200 | 2 | 315 MB | **1 slice = 624 ms**, 1,269 leavers | 24.2 / 30.8 | broken |
| 6,400 | 2 | 842 MB | **1 slice = 645 ms**, 2,573 leavers | 34.1 / 41.9 | broken; ship/star work starved (0 items) |
| 6,400, rtf 1 | 2 | 93 MB | 1 slice = 621 ms, 2,481 leavers | 36.7 / 45.0 | rtf does not save it — the slice is the unit |
| 25,600 | 2 | ~1 GB (est.) | **1 slice = 763 ms**, 3,662 leavers | 37.6 / 61.6 (p99.9 **191.6**) | broken; the spike lands in one frame |
| 100,000 | 5 | 4.25 GB | timeout ≥ 120 s | — | killed |

- The exodus is front-loaded (≈2,500 of 6,400 members leave in the first ~2 s of game time) and lands in one `Fleet::advance` slice that the 5 ms engine budget cannot split: per-leaver cost 0.21–0.8 ms (763 ms/3,662 at 25,600; 299 ms/382 at 400 over 10 s).
- Steady state is cheap and member-count-independent where claimed: at 400 members ticks cost ~31 µs (9,779 slices), and the in-frame battle at rest adds nothing as members idle — the sparse order's "only surprises" held everywhere the exodus was not.
- The universe's own `bytes_per_body` is 6.5 KB at 410 live bodies; the 4.2/8.7 GB peaks at 10⁵/10⁶ members match leavers × 6.5 KB (plus working set), i.e. the handed-out body, not the in-frame member, is the memory carrier.
- At the shipped 400 members the readout, not the engine, is the top cost: view_gather 54 % share, p50 3.0 ms, engine p99 5.6 ms against a 5 ms budget that already overflows 18 % of frames — numbers for the queued `b-readout-cost`.
- Controls: determinism held (two identical 10 s, 400-member runs, same cut tick 203025447, same digest `aadaa1c8…`); rtf 1 control above (slice cost unchanged).

Reproduce (each ≤ 60 s except the marked ones):
```
T universe --bench --unpaced --seconds 2 --rtf 100 --seed 1 --members M    # M = 400,1600,3200,6400
T universe --bench --unpaced --seconds 10 --rtf 100 --seed 1               # readout split (m10000.json)
T universe --bench --unpaced --seconds 2 --rtf 1 --seed 1 --members 6400   # rtf control
T universe --bench --unpaced --seconds 5 --rtf 100 --seed 1 --members 100000  # >2 GB RSS, >120 s: adversarial only
```
Raw JSONs: `m*.json`, `s*.json`, `big*.json` (empty: killed), `extract.py` in this folder.

**Predictions** (`predictions.md`, written after only the 48/400-member calibration): held — the readout dominates at the shipped scale (P4); the tail stays bounded (P3: worst/p50 ≈ 1.9 at 1,600). Failed, informatively — capacity (P1 predicted break at 10⁵, holds to 10⁴): it breaks at ~1,600; linearity (P2): the cost is not steady-state upkeep but one indivisible exodus slice; memory (P5 predicted ≤ ~1 GB at 10⁶): 8.7 GB, because a handed-out body costs 6.5 KB, not a few hundred bytes.

**What would make it wrong.** The exodus is this scene's genesis scatter (battle members born near the frame's edge leaving at t≈0); a fleet born in formation deeper inside its frame might hand out gently and never spike — the per-leaver cost and the 6.5 KB/body would remain, only the burst shape changes. Single seed (1) throughout; leaver counts could vary by seed. Linux/x86 timings, not the M1. I could not profile the slice's internals (perf_event_paranoid=4): the 0.25–0.8 ms/leaver is unattributed between doll-side binding, Leaver bookkeeping and view records.

**Cost of adopting / fit with PRINCIPLES.** The fix candidates follow from the measurement, not a redesign: (a) slice the exodus at the fleet boundary into per-leaver units under the budget (one law, the crate's own bounded-units rule — "no step reallocates or rehashes O(n) data" is currently violated across the `Fleet::advance` boundary); (b) raise `--members`'s clamp so the plane can be load-tested at all (this run's patch). PRINCIPLES: "minimize spike compute and average compute usage so that you get a bigger simulation that runs smoothly" (OC#36) and "why do you need so many bytes per entity?" (OC#34) — both are measured open items on the plane now. Not touched: `main` (this tree is the run's patch), no gate or crate edited except the xtask clamp line.

**Process faults, owned.** My first three "member sweep" runs (1k/10k/1M labels) were silently clamped to 400 — initially misread as scaling data; the clamp itself became finding #1. The 10⁵ and 10⁶ probes exceeded the window's 2 GB process budget (4.25 GB and 8.7 GB RSS, timeout-killed; the machine had ~13 GB free and no other run was seen to fail) — the bounded sweep afterwards stayed under 1 GB.

**The lens.** Quant counted capacity, tail and memory before any bet; what it may have missed: whether the exodus is law-inherent or scene-artifact (no profiler available), the causality structure of the handout (whose light cone wakes whom), and any physics-of-gameplay reason a fleet must be born scattered at its frame's edge.
