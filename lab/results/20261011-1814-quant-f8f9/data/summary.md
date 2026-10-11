# The frame ledger of the shipped plane (xtask universe --bench, threads=1, 900 frames each)

Linux/x86 cloud runner (8 vCPU shared, load ~1), release build, orders of magnitude only.
Readout = view_gather + view_json + wire. CPU = thread CPU ms per frame (work, not waiting).

| run | bodies | cpu p50 | cpu worst | hitch>16.7ms | overflow frames | rtf low 1% | events/s | engine share | gather share | readout share |
|---|---|---|---|---|---|---|---|---|---|---|
| rtf 1 | 28 | 0.76 | 1.16 | 0 | 0/900 | 1.00 | 61 | 7.3% | 69.5% | 92.7% |
| rtf 100 | 71 | 1.58 | 9.72 | 0 | 6/900 | 100 | 367 | 21.6% | 64.5% | 78.3% |
| rtf 1000 | 76 | 7.19 | 13.52 | 0 | 101/900 | 83 | 604 | 24.9% | 68.1% | 75.1% |
| rtf 100, members 200 | 221 | 2.89 | 8.57 | 0 | 38/900 | 9.8 | 1212 | 31.4% | 54.9% | 68.6% |
| rtf 100, members 400 | 417 | 6.10 | 15.21 | 0 | 185/900 | 0.0 | 1669 | 27.3% | 58.0% | 72.7% |
| rtf 1000, engine 1 ms | 76 | 6.58 | 12.00 | 0 | 651/900 | 0 (median 310) | 463 | 19.6% | 71.5% | 80.5% |
| rtf 1000, engine 15 ms | 76 | 4.84 | 23.65 | **5** | 3/900 | 1000 | 627 | 23.5% | 69.7% | 76.6% |
| rtf 100, unpaced | 71 | 0.99 | 6.07 | 0 | 3/900 | 100 | 368 | 21.7% | 66.1% | 78.3% |
| rtf 100, seed 7 | 70 | 0.97 | 6.41 | 0 | 2/900 | 100 | 420 | 24.5% | 63.0% | — |
| rtf 1000, seed 7 | 73 | 1.86 | 6.46 | 0 | 4/900 | 1000 | 1770 | 38.3% | 55.7% | — |

Digests (full 64 hex, sorted unique): rtf 1000 at engine budgets 1/5/15 ms → 1 digest;
rtf 100 paced vs unpaced → 1 digest. presented_tick_at_end vs cut_tick: rtf 1000 seed 1
misses the cut by 5%; members 400 at rtf 100 misses by 17%; all other runs reach the cut.

Per-event engine cost (engine_cost_by_kind, items ≈ resolved events): blended 62 µs/event
(rtf 100) to 151 µs/event (rtf 1000); by kind: ship 105–195 µs, player 579–1213 µs,
fleet 28–58 µs. Largest single event ≈ engine_max − budget ≈ 2–3.4 ms.

Gather cost per body per frame: 8.6 µs, flat from 221 to 417 bodies, rtf-independent (the
frame's floor; the engine is the slope, capped by the budget).

Capacity arithmetic to the goal (single thread, engine budget 5 ms × 60 Hz = 0.3 CPU-s per
wall-s): goal = 1e9 bodies, rtf 100, year-scale orbits (3.15e7 game-s), 32 kicks/orbit →
1.0e5 events/s → needs ≤ 3 µs/event; measured 62–151 µs → 20–50x short single-thread
(~5–13x short on 4 P-cores). At secular cadence 0.3 kicks/orbit → ~1e3 events/s → 300 µs/event
allowed: inside today's measured single-thread ceiling (~2–5k events/s engine-only).
