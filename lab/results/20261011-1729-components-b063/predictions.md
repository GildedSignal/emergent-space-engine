# Predictions (written before the decisive runs)

Component: **the kick resolver** (the engine's atom; "kicks dominate the engine's cost", board 1 October).
Runs that decide: (1) `cargo run --release -p xtask -- universe --kick-bench --seconds 20` on this
machine, (2) the floor microbench `work/floor.c` / `work/floor.rs` below, (3) `perf` sampling of (1).

None of these numbers was tuned on: the last kick-bench entry in the record is the M1's 29 µs
(H0210, 1 October, before motion law v2). This machine is Linux/x86 (cloud: orders of magnitude only).

- **P1 — current cost.** The pure kick resolver's median on this machine lies in **[5, 60] µs** per
  kick, and the p99/median ratio is **< 4** (the fit is the same work every kick; no data-dependent
  catastrophe expected).
- **P2 — the gap's location.** By `perf` sampling (if available) or by construction, **more than
  half the resolver's time is in the refit/rebind path** (fit to catalogue, remainder, history
  segment, Arc traffic), **not** in the field evaluation of the perturbing sources.
- **P3 — the floor.** A batched, body-ordered integer kick applier on 16-byte state records runs at
  **< 10 ns/kick** at a 64 MB working set (DRAM streaming) and **< 3 ns/kick** L2-resident; in
  causal-queue (random body) order **< 150 ns/kick**. The field-evaluation share of the floor
  (3 sources, u32 fixed point, table reciprocal) is **< 40 ns**.
- **P4 — idiot index.** The ratio current/floor is **≥ 100×** for the resolver as a whole.
- **P5 — shapes.** On the replayed kicks, the exact-shape hit rate stays **< 5%** (the 5 October
  finding holds on this snapshot too), so memoization cannot close the gap; only the representation
  of the state between kicks can.

What would make this wrong: the motion law v2 already removed the per-kick refit for clock-stepped
ships (then P2/P4 fail and the gap must be re-located); or the resolver median is below 5 µs
(then the plane is already within ~100× of the floor and the bottleneck has moved).
