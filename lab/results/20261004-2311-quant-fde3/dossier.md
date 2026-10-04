# Dossier — 20261004-2311-quant-fde3 (quant lens)

## Claim
One kick costs its bytes, not its arithmetic: the body-sorted 32-bit kick
stream saturates the memory bus (0.98 ns/kick, 45 GB/s accounted = the
measured memcpy ceiling; 64-bit words are 1.94× slower, exactly their byte
ratio), so at 10⁹ bodies the unaveraged path (32 kicks/orbit, H0190) is
bandwidth-infeasible on an M1 (≥ 21 s/orbit at a perfect 68 GB/s) while the
averaged path (0.3/orbit) fits at 0.2 s; a player-ordered wake must be
coalesced to body order or it pays 6-11×; and a per-cell sub-quantum
accumulator — exact by integer identity — deletes 63-90% of far-field body
touches when the typical far-field step is ≲ q/5, with a measured kill
region near step ≈ 0.75q (−22%).

## Bottleneck
Focus items 1 (kicks dominate cost), 3 (cost at a billion) and 4
(smoothness/allocator) of the board, from the memory side the board has not
measured (HANDOFF still lists "memory bandwidth" as a *pending* M1 probe).
Gain: the capacity equation for the kick stream (what width, what order,
what cadence 10⁹ bodies permit), plus a mechanism (cell accumulator) that
deletes body touches rather than making kicks cheaper. What it lets us
delete: any per-kick bookkeeping beyond one 12-16 B record and one 16 B
body touch (a pointer chase, a hash indirection: 6-11×), and 64-bit words
on the kick path (2×).

## Evidence
Machine: cloud AMD EPYC 7763, 2 vCPU, 7 GB, L3 32 MiB, load 0.5-1.0;
orders of magnitude only (lab rule). 4 Mi bodies (64 MB i32 working set,
past L3). Commands (each ≤ 60 s):

```
cc -O3 -march=native -o kickprice kickprice.c -lm   # ~1 s
./kickprice 16                                       # ~13 s
```

Numbers (median sweep of 16; tail over all 64 Ki-event chunks):

| variant | ns/kick | accounted GB/s | tail p99.9/max |
|---|---|---|---|
| memcpy ceiling (256 MB, median of 5) | — | 44.2 | — |
| i32 sorted (16 B body, 12 B kick) | **0.98** | **45.1 (= 102% ceiling)** | 1.12 / 1.12 |
| i32w sorted (16 B kick record) | 1.06 | 45.2 | — |
| f64 sorted (32 B body, 24 B kick) | **1.90** | 46.2 | 2.14 / 2.14 |
| i32 shuffled (wake order) | **6.4-11.1** (two runs) | 4.0-6.9 | 12.9 / 12.9 (flat) |

- Width is capacity: f64/i32 = 1.94 ≈ byte ratio 88/44 = 2.0, and both
  variants sit at the memcpy ceiling → the stream is bandwidth-bound, ALU
  cost invisible (two adds per kick either way). Packing the kick record
  to 12 B buys only ~8% over a line-friendly 16 B.
- Order is 6-11×: the scattered wake loses it in the **median**, not
  mainly the tail (p50 10.7 → p99.9 12.9, flat), i.e. prefetch/TLB defeat
  makes every event uniformly slow. Sorted sweeps keep p99.9 within ~15%
  of p50.
- Cell sub-quantum accumulator (K = 128 bodies/cell, 512×32768 epochs,
  heavy-tail far field P(|u|>x) ≈ (u_typ/x)³, sign-symmetric, F = 20):

| typical step | always ns/epoch | skip ns/epoch | body touches deleted |
|---|---|---|---|
| 1.50 q | 95.3 | 95.1 | 0.0% (control) |
| 0.75 q | 88.7 | 102.2 | **−22.2% (kill region)** |
| 0.19 q | 74.6 | 29.4 | **62.6%** |
| 0.05 q | 74.8 | 6.7 | **89.7%** |

- Exactness: incremental application with remainder ≡ one-shot
  floor(total/quantum): `OK (v=53 ref=53)` — integer-identity proof that
  the accumulator is exact by construction (r2's rule: increments and
  kicks are integers of the law; nothing is lost below the quantum).
- Capacity (derived, assumption flagged): at 10⁹ bodies and 32
  kicks/orbit, 3.2×10¹⁰ kicks × 44 B = 1.41 TB per orbit → ≥ 20.7 s/orbit
  at M1-class 68 GB/s with perfect utilisation (f64: 41 s). Averaged
  0.3/orbit: 0.19 s/orbit. Raw files: `run2.txt`, `run3.txt`
  (`run1.txt` keeps the broken first cell control as the audit trail).

## Predictions
Written before the decisive run (`predictions.md`).
- P1 (bandwidth-bound, ratio 1.6-2.6, i32 ≥ 60% ceiling): **held** (1.94,
  102%).
- P2 (wake: p50 ≤ 1.5× sorted, p99.9 ≥ 2×): **half-failed** — p99.9 was
  6×, but p50 also moved 6-11×. The wake costs the median, not just the
  tail; reported as held against me.
- P3 (deletion ≥ 50% at 4 u_typ, ≥ 80% at 16): **held** (62.6%, 89.7%),
  and the unpredated region between (typ ≈ 0.75q) is a **loss** of 22% —
  the honest boundary of the mechanism.
- P4 (exactness OK): **held**.
- P5 (≥ 15 s/orbit unaveraged at 10⁹): **held** (20.7 s).

## What would make it wrong
- The kick arithmetic here is the touch floor (two adds), not the
  engine's compiled kick cost (E/L fit, tube rebind — B9/B10 own that).
  If the compiled kick needs extra touches (a catalogue lookup per kick),
  the floor rises and the capacity table is optimistic.
- Cloud single-core bandwidth (45 GB/s) is not an M1 P-core (~15-20 GB/s
  each, 68 GB/s whole machine): the *ratios* (width, order, skip) are
  portable, the absolute rates are not; the pending M1 bandwidth probe
  should redo `run3`'s table natively.
- The far-field step distribution is synthetic; the real one comes from
  the neighbours' moments. If its typical step sits near one quantum, the
  accumulator is a 22% loss, not a win — measure the real distribution
  before adopting (one rung on the engine's own galaxy scene).
- Adoption cost: one 16 B cell record (remainder + base), one branch per
  scheduled epoch, and the rule that wake batches are sorted to body
  order before touching bodies. No change to outcomes (exactness by
  integer identity), so B8 determinism is untouched.

Fit with PRINCIPLES: "the best part is no part" (#17: the cheapest body
touch is the one not done); "influences below one quantum accumulate"
(#6, made mechanical and exact); "minimize spike compute" (#12: sorted
sweeps hold p99.9 within 15% of p50); "i just care at about how fast it
runs compared to real time" (#27: the 20.7 s/orbit wall at 10⁹ is a
real-time budget line, not a benchmark).

## The lens
The HFT eye prices everything per event and can miss that this is one
exact law, not many small bets: the 6-11× "market impact" of the wake is
not a cost to shave but a representation demand (coalesced sweeps), and
the 22% kill region shows a latency habit (add a fast path) would be a
bandaid where the law's own quanta already decide. It also prices the
M1's thermal/swap reality only by proxy here — the cloud box is quiet;
the player's is not.
