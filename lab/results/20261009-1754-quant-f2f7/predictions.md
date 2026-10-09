# Predictions — run 20261009-1754-quant-f2f7 (quant lens)

Written **before** the decisive measurements. Machine: shared Linux x86, i7-4790 4C, L1d 32K/core, L2 1M/core, L3 8M shared, `perf_event_paranoid=4` (no hardware counters; cold effects measured by working-set sweep + `clflush`, not counters). Orders of magnitude only, per lab rules; the integrator re-measures on the M1.

## Question

Where does the plane's per-event cost live — the motion law's own arithmetic, memory stalls, or the event loop's scaffolding (calendar, read-out/write-back, clones, allocations)? Each share caps one of the board's current levers.

## Kill rules (frozen)

- **K1 (law vs scaffolding):** if pure hot `step::process` ≥ 50 % of the whole-universe per-event cost (ship class), the "law dominates" premise stands and this dossier is a lead, not a finding.
- **K2 (memory):** if cold/hot ratio of the pure resolve < 1.3 (16k-record pool ≈ 2× L3, and a `clflush` variant), memory layout is not a lever at today's cost scale.
- **K3 (allocator):** if whole-path allocations per event < 0.1, the allocator is not a tail lever.
- **K4 (scale flatness):** if whole per-event cost at N = 65 536 is < 1.15× the N = 16 cost, the loop's overhead is flat in N in this range.

## Predictions

- **P1** (hot pure resolve): 2–8 µs per kick on this box. p99 ≤ 2× p50.
- **P2** (whole per event, ship class, hot-cache regime N = 1024): 6–25 µs; law share pure/whole = 0.25–0.5. **This is the run's central unknown**: I genuinely cannot predict which side of K1 it lands on from reading the code; the stage timers in `cost_split.rs` were never summed against the whole-universe number.
- **P3** (scaffolding share): ≥ 50 % (my lean, from `rec()` returning `BodyRec` by value with a `Vec<Item>` plan, `Update.retired: Vec<Segment>`, requeue/apply per event).
- **P4** (cold/hot): ≥ 1.3 at the 16k pool (record + plan buffer + `Arc<Entry>` chase). If the pure path is µs-scale arithmetic, misses may only add ~5 %; I predict the truth is between 1.05 and 1.6 and accept either.
- **P5** (allocations): ≥ 1 alloc per whole-path event (record read-out clone) — predicting ~2–3.
- **P6** (scale): per-event at 65 536 ships ≥ 1.2× the N = 16 value (calendar sift with N-deep heap + record misses).
- **P7** (budget, analytic + measured cadence): with 64 kicks/orbit and rtf 100 on 4 P-cores, a 1 AU belt (P ≈ 6.4e12 ticks) at N = 10⁹ allows ~20 µs/event; a low moon (P ≈ 6.4e10 ticks) allows ~200 ns/event. So at 10⁹ bodies the per-event cost matters only for belts; moon-scale populations are decided by kicks/orbit (cadence, averaging), whatever the per-event cost.

## Held-out cases (not tuned on)

The N-sweep values 8192 and 65 536 were chosen before any run; the clflush variant is a second, independent cold measurement. The budget table's moon-orbit row is held out against P7's arithmetic.

## What would flip the verdicts

If the ship class is not the dominant event mix (opens/boundaries dominate), K1's denominator must switch to the mix-weighted mean — I will report the mix and recompute. If the restricted scene's ships take zero kicks (ships outside the planet's reach), the sweep is void and I fall back to the plane scene with fleet members.
