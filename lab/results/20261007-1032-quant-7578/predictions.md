# Predictions — run 20261007-1032-quant-7578 (Quant lens)

Dev seed: 777 (all numbers below were tuned on it, plus one cross-check on the shipped
`scale n 10000`, seed 20261040). Held-out seeds for the decisive run: **888 and 999**
(never run before this file was written). Uniform belt: sigma_e = 1e-2, a in [1, 1.5],
rho = 1/n (the crate's own `scale n` scaling). Single-threaded setup timing, Linux/x86
i7-4790 (orders of magnitude only; the integrator re-measures on the M1).

Instrument: `encounters tail <n> <seed> <sample>` and `encounters tailc <set> <seed> <sample>`
(added to `crates/encounters/src/main.rs` in this run's patch). JSON per line.

## Held-out predictions

- **P1 — degree grows with N despite the rho = 1/N compensation** (the cone's R-term
  dominates eps at sigma_e = 1e-2, so tier-1 candidates track orbit crossings, not rho):
  deg_mean(1e5) / deg_mean(1e4) in **[8.5, 11.5]** on both held-out seeds.
  Dev: 89 → 861 from n=1e3 to 1e4 (9.7x for 10x).
- **P2 — the uniform belt's degree tail is thin**: deg_max/deg_mean in **[2.0, 3.2]**
  at n = 1e4 and 1e5 on both seeds. Dev: 2.54 (1e3), 2.60 (1e4).
- **P3 — the numeric window cost is a burst, not a load**: evals_per_pair p50 = 0 and
  p90 = 0, p999 in **[700, 3000]**, max **< 12000** at n = 1e4, both seeds.
  Dev: p50 0, p90 0, p999 1521, max 6968.
- **P4 — one body's synchronous re-setup (a kick's re-pay) is ms-scale here, with a mild
  tail**: setup_ns_per_body max/mean in **[1.5, 3.2]** and p99 in **[8 ms, 25 ms]** at
  n = 1e4, both seeds. Dev: max/mean 2.49, p99 14.6 ms.
- **P5 — the instrument fails where concentration exists** (control): on the `coorbital`
  set (300 bodies, a in [1, 1.0001]) deg_max = deg_mean = **299** on both seeds — the
  degenerate all-pairs signature, not a thin tail.
- **P6 — the Diophantine step is never the burst**: qsteps_per_pair p999 **< 100** at
  n = 1e4 uniform, both seeds. Dev: 23.
- **P7 — means of bursty quantities are unstable across seeds** (the multiple-testing
  trap made visible): setup_ns_per_pair means of seeds 888 and 999 differ by **>= 1.25x**
  at n = 1e4. Context: the shipped `scale n 10000` (seed 20261040) reported 9.1 us/pair
  against dev seed 777's 2.4 us/pair — a 3.7x swing in a reported *mean* while the
  quantiles (p50 = 0 evals) are pinned.

## Kill criteria for the certificate's tail behaviour (frozen before the run)

- If P2 fails upward (deg_max/deg_mean > 3.2 at n = 1e5): the per-body unit is itself
  fat-tailed and per-body chunking does not bound a frame; the allocator needs a
  per-pair quantum plus priority.
- If P3 fails upward (p999 > 3000 or max > 12000): the window numerics are an unbounded
  burst and the skin must cap per-pair window work, not just defer it.
- If P4 fails upward (p99 > 25 ms at 1e4 bodies on this box): synchronous re-setup after
  one kick cannot fit any frame budget at belt scale; deferral is mandatory, confirming
  the skin as the lever (components-4643) with numbers.
