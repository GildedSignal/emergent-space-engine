# Predictions — run 20261004-2311-quant-fde3 (quant lens)

Written before the decisive run of `kickprice.c` (4 Mi bodies, past the
32 MiB L3; AMD EPYC 7763 cloud vCPU, orders of magnitude only). Nothing
below was tuned on: the binary has not been run yet.

## P1 — the kick stream is memory-bound, not ALU-bound
- `i32_sorted` accounted bandwidth ≥ 60% of the measured `memcpy_ceiling`.
- `f64_sorted` / `i32_sorted` ns-per-kick ratio in [1.6, 2.6] (bytes ratio is
  88/44 = 2). If the ratio comes out ≈ 1, the stream is ALU/issue-bound and
  width does not buy capacity — that would kill my capacity argument.

## P2 — the player's wake (scattered order) costs the tail, not the median
- `i32_shuffled` p50 ≤ 1.5× `i32_sorted` p50.
- `i32_shuffled` p99.9 ≥ 2× `i32_sorted` p99.9 (prefetch defeated).

## P3 — the per-cell sub-quantum accumulator deletes body touches
For the heavy-tail uniform far field (P(|u|>x) ≈ (u_typ/x)³, sign-symmetric):
- q = 0.25·u_typ: touches deleted < 20%
- q = 4·u_typ: touches deleted ≥ 50%
- q = 16·u_typ: touches deleted ≥ 80%
- `always` control touches ≈ 100% of epochs (|u| ≥ u_typ ⇒ d ≥ 1 always,
  since steps are ≥ 2^F: prediction ~100.0%).

## P4 — exactness (the integer identity)
`applied == floor(total/quantum)` prints OK. If it FAILs, the accumulator
representation is wrong as written (this kills the mechanism, not
PRINCIPLES #6).

## P5 — capacity at a billion (derived, from measured GB/s)
At the law's 32 kicks/orbit (H0190) with 44 B/kick and 10⁹ bodies:
1.4 TB of traffic per orbit ⇒ at an M1-class 68 GB/s whole-machine budget,
≥ 15 s per orbit even at perfect bandwidth utilisation, i.e. unaveraged
kicks at 10⁹ cannot fit a ≤ 10 s orbit cadence on bandwidth alone; the
averaged path (0.3 kicks/orbit) fits at < 1 s/orbit. The 32-bit word is
load-bearing: f64 words halve everything again.

## What would make this wrong
- Accounted-bytes model badly off (e.g. write-allocate counted twice):
  then GB/s numbers are relative, and the capacity table must be re-derived
  from the raw ns/kick instead.
- The cloud vCPU is shared: a neighbour run could sink the ceiling. Medians
  over ≥ 8 sweeps; if memcpy ceiling varies > 2× between variants, rerun.
