# Dossier — 20261009-1754-quant-f2f7 (quant lens): the plane's per-event price, decomposed and budgeted

## Claim

The plane's event cost is the resolve itself (pure kick 21.7 µs hot ≥ whole-universe mean 19.4–20.1 µs at every N): scaffolding, memory and the calendar are under ~15 % combined (cold/hot 1.07, flat in N to 65 536, 5.9 allocs/event), and inside the resolve the **rebind `Rebinding::from_state` alone is ~12.8 µs ≈ 60 % of every kick** — while the derived budget says 10⁹ bodies at 1 AU-belt cadence and rtf 100 allow exactly ~19.7 µs/event, so the engine sits on the budget line today and moon-scale populations need cadence (kicks/orbit), not per-event polish.

## Bottleneck

Board focus line 1 ("kicks dominate the engine's cost") and 4 (smoothness). The run prices each current lever by its measured share: per-event layout/queue/allocator work is capped at < 1.2×; the rebind is a ~1.7–2.5× whole-engine lever if made incremental; kicks/orbit (averaging, H0190's 114×) is the only lever that reaches 100× regimes. It also hands the integrator the ns/event dashboard the quant lens was asked for.

## Evidence (all commands ≤ 60 s, single-threaded, i7-4790 shared — orders of magnitude only; integrator re-measures on the M1)

`cargo build --release -p emergent-universe --example kick_budget && $CARGO_TARGET_DIR/release/examples/kick_budget` (32 s, 996 MB peak; full log: `work/kick-budget.txt`; harness: `crates/universe/examples/kick_budget.rs`, patch-saved):

- **Sizes (M0):** BodyRec 448 B (7 lines), Binding 176, Entry 224, Segment 192, Item 16, calendar slot 36 B.
- **N-sweep, whole universe, ship class (M2):** per-event mean 20.1 / 17.5 / 19.5 / 19.8 µs at N = 16 / 1 024 / 8 192 / 65 536 — **flat** (65 536/16 = 0.99×; K4 negative). Mix at N=65 536: 583k kicks, 552k boundaries, 66k opens; cadence 7.33e-12 events/body/tick, identical at every N. Allocations **5.94/event, 1 644 B/event** (counting global allocator; K3 positive).
- **Pure resolve (M1):** hot p50 **21.7 µs** (p99 24.0), 2 000/2 000 real kicks; pool-cold (16 384 records ≈ 4× L3) p50 23.1 µs; clflush-cold 23.3 µs → **cold/hot = 1.07** (K2 negative: memory is not the lever at this cost scale). `rec().clone()` alone 84 ns.
- **Stages (M3, hot p50):** readout 2.8 µs, secondaries 3.9 µs, tide 0.02 µs, `root_state` (ramped, per-apply position cache) 10.3 µs.
- **Rebind (existing `cost` example, `$CARGO_TARGET_DIR/release/examples/cost`):** `Rebinding::from_state` **12.8 µs**, `Orbit::compile` 3.8 µs, `signed_state` 3.1 µs, cartesian 0.3 µs.
- **Budget (B1):** tick = GM☉/c³ = 4.925 µs → 203 252 ticks/game-second; allowed ns/event = 4 cores · 1e9 / (N · cadence · 203 252 · rtf 100). Measured scene cadence: 26.9 µs allowed at N=10⁹ (1.35× headroom, N_max ≈ 1.35e9). 1 AU belt (P=6.42e12 ticks, 64 kicks/orbit): 19.7 µs allowed at 10⁹ — **zero headroom** (p99 already 24–35 µs). Low moon (P=6.4e10): 197 ns allowed — **100× over** at any plausible per-event cost.

## Predictions (`predictions.md`, written before the runs)

K1 fired as written: pure/whole ≈ 1.09 ≥ 0.5, the law-dominates premise stands, so this is a **lead by my own frozen rule**, not a premise flip. Held-out outcomes, honestly: P1 wrong (21.7 µs vs 2–8 predicted — the resolve is heavier than I read), P2/P3 wrong (scaffolding ≥ 50 % predicted; it is under ~15 %), P4 wrong (1.07 vs ≥ 1.3), P5 right (5.94 ≥ 1), P6 wrong (flat 0.99× vs ≥ 1.2×), P7 arithmetic confirmed by the measured cadence row. The two independent cold measurements (pool sweep, clflush) agree within 1 %.

## What would make it wrong; cost of adoption; fit

Wrong if: the pure-path harness (`process` on a stripped clone) skips work the real loop does (it is the same `step::process` the universe calls; `apply`'s `root_state_raw` is outside it and bounded above by the mix arithmetic); or if the M1's per-event profile differs structurally, not just in rate (x86→M1 is same-order per lab rules; the M1's 29 µs whole-kick at H0210 brackets my 19–26 µs). Adoption: the dashboard numbers and the rebind-share finding are adoptable in one step (a delta-rebind probe is the named next experiment; `secondaries`' per-kick `Vec` allocation is a one-line reuse fix worth ~4 % and one alloc/event). Nothing here changes the law. PRINCIPLES fit: "the cheapest compute is compute not done" — the 12.8 µs rebind is recomputing an invertible map every event; "Measure before claiming"; "i care about the p95/99" — the budget line is drawn at p99, not the mean.

## The lens

The quant lens bought the decomposition and the budget line, and its blind spot bit exactly as warned: it prices nanoseconds and tails, but the finding is that per-event polish (layout, allocator, queue) is nearly worthless here — the value sits in *how often* events happen and in one 12.8 µs integer inversion. A latency dashboard cannot price a law change; it can only show where the next 10× must come from.
