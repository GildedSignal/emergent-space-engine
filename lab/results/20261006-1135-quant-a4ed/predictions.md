# Predictions — 20261006-1135-quant-a4ed (quant lens)

Written before the decisive matrix. Tuned set (smoke runs, single core, 512 MiB,
declared): chase L1 10.2 M ev/s (98.5 ns/line), gather L4 10.6 M ev/s (4 lines =
23.6 ns/line), chase L4 2.30 M ev/s (109 ns/line), stream L8 30.7 M ev/s,
L2-resident stream 189 M ev/s. Everything below is **not** tuned on.

## Held-out cases (this box, i7-4790, DDR3, orders of magnitude only)

1. **All-core gather scaling.** gather L=4 at 4 threads (physical cores) ≥ 3.5× the
   1-thread rate (~170 M lines/s, under the ~25 GB/s dual-channel ceiling), and
   8 threads (hyperthreads) ≤ 1.3× the 4-thread rate.
2. **All-core chase scaling.** chase L=1 at 4 threads scales near-linearly (≥ 3.5×):
   latency-bound loads don't contend bandwidth.
3. **gather L=8.** ns/line ≤ gather L=4's ns/line (more memory-level parallelism per
   event), events/s about half of gather L=4.
4. **Cache-resident control.** chase L=4 in a 1 MiB set ≥ 20× its DRAM rate —
   confirming the DRAM runs are memory-bound, not loop-bound.
5. **perf corroboration.** On gather L=4 (1 thread), LLC-load-misses ≈ lines touched
   (within 20%): the counted lines are the cold lines.

## The budget grid (M1 translation, prediction of the shape)

6. With the measured all-core gather rate G and the law's 64 kicks/orbit
   (step.rs: a kick is 1/64 of the radial period), a **pointer-chasing** kick path
   (chase-L4 rate) caps N below 10⁹ for battle-scale orbits (P ≈ 90 min) at 1× real
   time, while a **gathered** path (G) passes 10⁹ at 1× but not at 10× real time.
7. For belt-scale orbits (P ≈ 1 year), even today's cadence passes 10⁹ at 10× real
   time: the wall is only at short-period, dense-population scenes.
8. Averaging (0.3 kicks/orbit, H0190) multiplies N_max by ~200 at the same layout:
   cadence and layout are independent multipliers on the same budget.

Machine state: load 0.28 at start; recorded per run in metrics.json.
