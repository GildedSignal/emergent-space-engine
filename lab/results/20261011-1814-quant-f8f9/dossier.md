# Dossier — 20261011-1814-quant-f8f9 (Quant lens)

**Claim.** On the shipped plane, the readout — not the kick — owns the presented frame (55–72 %
of frame CPU across 10 runs, 2 seeds, rtf 1–1000, 28–417 bodies; the gather alone is 8.6 µs per
body per frame, rtf-independent), the budget allocator holds both the SLA and exact schedule
independence under squeeze (identical digests at engine budgets 1/5/15 ms and paced/unpaced;
zero frames above 16.7 ms whenever the budget stays ≤ 5 ms, even at 72 % overflow), and the
measured µs/event arithmetic says secular cadence, not per-event cost, spans the gap to 10⁹
bodies (32 kicks/orbit needs ~3 µs/event, 20–50× beyond today's 62–151 µs; 0.3/orbit allows
~300 µs and already fits one thread).

**Bottleneck.** Board #4 (smoothness and the allocator) plus the queue's `b-readout-cost`.
Gain: the frame's first lever is measured to be the gather (unbudgeted, synchronous, max
8.5–10.1 ms — twice the whole engine budget), so budgeting/lazing the readout is worth ~3× the
frame before any kick work; and the queue's lever order (cadence before per-event cost) gets
its measured target (3 µs/event at 32/orbit vs 300 µs allowed at 0.3/orbit). Deletes nothing
by itself; it reorders.

**Evidence** (all numbers: `data/summary.md`; raw reports: `data/*.json`; full digests verified
with `jq -r .digest | sort -u | wc -l`):
- Readout share of summed frame time 73–93 % at rtf ≤ 100, 72–77 % at rtf 1000; engine ≤ 38 %.
  Gather p50 0.53→1.1→5.0 ms at rtf 1/100/1000 (it grows with game-time per frame, and 8.6 µs
  per body per frame at fixed rtf, flat 221→417 bodies).
- Allocator: engine budget 1 ms → 651/900 overflow, delivered median rtf 310, worst CPU 12.0 ms,
  0 hitches; 15 ms → 3 overflow, full rtf, but 5 frames above 16.7 ms (deferred work becomes
  hitches past the knee). Deferral granularity = one event: engine max − budget ≈ 2–3.4 ms
  (the player's own item costs 0.6–1.2 ms; the largest single event is the floor under any
  budget).
- Digest invariance: `xtask universe --bench --seed 1 --rtf 1000 --seconds 15` with
  `--engine-ms 1|5(default)|15` → one digest (`6293ce7d…`); `--rtf 100` paced vs `--unpaced` →
  one digest (`01c9be77…`). Foundation 7's "budget changes when, never what" verified at the
  frame level, not asserted.
- Capacity (single thread, default 5 ms): chronic saturation at 417 bodies, rtf 100 (185/900
  overflow, delivered rtf worst-1 % = 0, misses the canonical cut by 17 %); none at 221 bodies
  (38/900). Workload-dependent: seed 7 at rtf 1000 runs clean (4 overflows, 1770 events/s)
  where seed 1 saturates (101 overflows, 604 events/s) — judge capacity by ensembles, not one
  seed.

Reproduce (each ≤ 20 s, from the repo root; binary at `$CARGO_TARGET_DIR/release/xtask`,
here `/home/glmlab/lab-target-1/release/xtask`):
```
for r in 1 100 1000; do xtask universe --bench --seed 1 --rtf $r --seconds 15 > data/rtf$r.json; done
for m in 200 400; do xtask universe --bench --seed 1 --rtf 100 --seconds 15 --members $m > data/mem$m.json; done
for e in 1 15;    do xtask universe --bench --seed 1 --rtf 1000 --seconds 15 --engine-ms $e > data/rtf1000-e$e.json; done
xtask universe --bench --seed 1 --rtf 100 --seconds 15 --unpaced > data/rtf100-unpaced.json
xtask universe --bench --seed 7 --rtf 100 --seconds 15 > data/seed7.json   # fresh-seed control
```

**Predictions** (`predictions.md`, written before any run): P1 readout > 50 % — held (72–93 %).
P2 worst/p50 ≥ 5× — held (6.1× at rtf 100); hitch count nonzero — **missed**: no frame exceeds
16.7 ms at budget ≤ 5 ms (the tail peaks at 9.7–15.2 ms); the first hitches appear only at the
15 ms budget. P3 saturation at rtf 1000 — held at seed 1 (cut missed 5 %), refuted at seed 7
(seed-dependence reported above). P4 per-event flat in N (≤ 2×) — held (1.8×; events/s per body
5.2→5.5→4.0). P5 digest invariance — held exactly. P6 events/s band 1e4–1e5 — **missed low**:
measured ceiling 6e2–1.8e3 events/s whole-thread, so the gap to the goal is larger (~60× at
32/orbit single-thread), strengthening the cadence conclusion.

**What would make it wrong.** Linux/x86 cloud at load ~1, single thread, 15 s runs, one scene,
two seeds, the bench's scripted player: orders of magnitude only, and the integrator re-measures
on the M1 (PRINCIPLES #10). The gather's 8.6 µs/body is this scene's light-cone solve, not a
universal constant; the 10⁹ arithmetic assumes year-scale orbits and kick-dominated events (the
plane's mix carries contacts and decisions), and the readout floor scales with *live catalogue*
bodies, not with 10⁹ stored bodies (shipmem's population programs never enter the gather).
`items ≈ events` in `engine_cost_by_kind` is the engine's own accounting, not an independent
count.

**Cost of adoption, fit.** Zero code: measurement plus arithmetic; it lifts `b-readout-cost`
from "cheaper readout between kicks" to "the frame's floor, unbudgeted" and hands it these
gates (`frame_cpu_ms`, `view_gather`, `overflow_frames` are already in the bench). PRINCIPLES
#12: "the algorithm that allocates the work to prevent those heavy tails, it's the most
important one" — measured verdict: it holds the tail and the digest; its knee is
budget ≈ frame minus one event. #3 "compute only surprises": the gather re-derives every
body's light-cone crossing every frame — the readout is now the largest non-surprise compute
in the frame. #28: the view is an instrument — this instruments the instrument.

**The lens.** Quant frames everything as cost per event and tail risk, and may undervalue that
the gather's 8.6 µs buys the exact GR readout the player sees; cutting it to a memo must not
strawman into "draw less" (the ViewCache memo already exists and the cost stays linear). It
also prices single-thread capacity where the design intends 4 P-cores plus the slack queue.

**Grade asked: silver.** Real, reproduced by exact commands, held-out predictions scored with
two honest misses; one named experiment from gold: budget or lazily memo the gather and re-run
this bench to show the frame floor drops ≥ 3× with digest unchanged.
