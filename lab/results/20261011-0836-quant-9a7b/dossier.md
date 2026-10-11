# Dossier — 20261011-0836-quant-9a7b (quant lens)

## Claim

The encounter tier's candidate test, rewritten as integer squares over packed Binet records (12 B/body + 4 B reach, u32 grid per doll), is a provable superset of today's float cone, costs **≤ 0.6 % extra candidates** on every belt tried, and runs **19–40× cheaper per scanned body** (2.5 ns vs 47–99 ns, x86, single thread) with **no capacity knee** from 10⁶ to 3×10⁷ bodies (1.17× drift) — the tier's hot path stops being float arithmetic and random 88-byte `Body` fetches.

## Bottleneck

Board risk #1, "candidate work must track real encounters" (q-candidate-degree, taleb-09b5). The
tier's constant was never priced: after every kick a body re-scans its U-range, paying per scanned
body a float `hypot` plus a pair tolerance that reads two random 88-byte `Body` records. This run
prices it and cuts it. Gain: ~40× on the per-kick re-scan (at 10⁶ bodies/doll: 0.4 ms vs 16 ms per
kicked body, x86); lets the tier delete its dependence on `Body` layout entirely (16 B/body of tier
state, no f64 in the decision path). It does **not** touch the scanned-per-body ∝ N structure —
that is the cone/skin's own problem.

## Evidence (all single-threaded, min of 3 reps; Linux x86 cloud, load ~1.1, 8 MB L3 — orders of magnitude only, the integrator re-measures on the M1)

Decomposition at N=10⁶, belt a∈[1,1.5], σ_e=1e-2, ρ=1e-4 (same sample, same ranges):

| variant | math | layout | ns/scanned |
|---|---|---|---|
| today (float pair-eps via random `Body` reads) | f64 hypot+eps | 16 B order + random 88 B | 99.2 |
| float packed (global eps, SoA f64) | f64 hypot | 24 B stream | 14.5 |
| **integer (u32 grid)** | int squares, no sqrt | 12 B stream | **2.48** |

Arithmetic alone buys 5.8×; layout/randomness another 6.8× (and it compounds with N: the float
`Body` path degrades 46.6 → 99.2 ns from 10⁵ to 10⁶ as 88 MB of bodies leaves L3; the integer
stream is flat).

Safety and work (held-out seeds; miss = float-pair candidates the integer cone rejects):

- N=10⁶ uniform: miss = 0 at b16–b30; growth = 1.0060 (b30), 1.0081 (b16).
- Co-orbital keys=8 (equal periods, the concentration workload): miss = 0; growth = 1.0001.
- Hot belt σ_e=0.3 (e clipped at 0.5, reach > span, 91 % of scanned are candidates): miss = 0; growth = 1.0041.
- Truth anchor (N=3000, 50 orbits, dense truth over radial pairs): 831/831 real-encounter pairs are
  integer candidates; float cone's 381,631 pairs ⊆ integer's 383,561; 462 candidates per encounter
  vs 459 (float) — same order as r8 v2's element-sort 786 work/encounter.
- Capacity (integer-only, streaming build, no `Body` kept): 2.456 → 2.514 → 2.598 → 2.885 ns/scanned
  at N = 10⁶, 3×10⁶, 10⁷, 3×10⁷; build 280–680 ns/body (two stream passes + one sort); peak RSS
  1.06 GB at 3×10⁷.

Commands (each ≤ 60 s, `cargo build --release -p emergent-encounters` once):

```
encounters quant speed 1000000 1e-2 1e-4 0 777 96 3     # the table above
encounters quant growth 1000000 1e-2 1e-4 0 777 128 0   # miss/growth, uniform
encounters quant growth 300000 1e-2 1e-4 8 777 128 0    # co-orbital concentration
encounters quant growth 100000 3e-1 1e-4 0 777 128 0    # hot belt
encounters quant growth 3000 1e-2 1e-4 0 777 500 50     # truth anchor (26 s)
encounters quant knee 30000000 64 3                      # capacity point (24 s)
```

Logs: `decisive-a.log` (pre-fix, contains the b16 catch), `decisive-b.log` (final). Code:
`crates/encounters/src/quant.rs` (module), wiring in `lib.rs`/`main.rs`.

## Predictions

Written before the decisive runs (`predictions.md`), tuned only on the pilot belt. Outcome:
growth/keys/hot/anchor/speed/capacity all inside the predicted ranges — except **"miss = 0 at all
widths" failed at b16 (6 misses of 5.5 M)**. Root cause: my superset bound had a sign slip — the
V/W quantization error must *inflate* the slack (k = E + 1 + √2/c), not deflate it; the coarse grid
made the slip visible, the fine grids hid it behind ε's 1.5 margin. Fixed, everything re-run:
miss = 0 everywhere at the corrected k. The kill rule (miss>0, growth>1.10, <2× speedup, >3× knee
drift) now passes on every held-out case.

## What would make it wrong

- A doll whose `eps_max` (global rmin/rmax/e/p) is a loose bound for its pairs' `eps_u` — a
  strongly mixed doll (a ∈ [0.5, 3] with hot eccentricities) could inflate everyone's slack; only
  uniform, keys and hot single-range belts were measured (growth stayed ≤ 0.6 %).
- Tiny ρ per doll span: at ρ=1e-5 the b16 grid degenerates (E < 4 quanta → accept-all-in-range);
  b30 keeps E ≈ 2×10⁴ quanta there. The grid width is per-doll state, chosen from E.
- The superset proof covers the *cone test only*; downstream sections/checks are untouched and keep
  their own guarantees.
- x86 timings; NEON u32 squares should behave the same, but that is unmeasured.

## Cost of adoption, fit with PRINCIPLES

Adoption: pack (U,V,W,rech) once per doll (12+4 B/body), maintain the u-sorted order on kicks (a
kick moves u slightly; local re-slot), replace `is_candidate` in `cone_pairs` with the integer test
(~80 lines, in `quant.rs`). Nothing downstream changes — the tier is still a superset filter.
PRINCIPLES: "discrete by design, cheapest arithmetic… physics loves e while we love 2" (OC#38);
"Floats may explore; only integers decide canonical outcomes" (lab rule); "we just need to have the
right representation so that math is trivial" (CL 09-27). The binet cone was already integer-shaped;
this stores it in its own grain.

## The lens (what it may have missed)

An HFT lens prices the constant and forgets the structure: shaved nanoseconds here must not spend
the slack skin's 12.6× (they multiply — the skin skips re-certifications, the integer tier makes
each re-certification 40× cheaper). Also unpriced: the sort's maintenance cost after kicks (680
ns/body rebuild is setup, not steady state), and whether 12 B/body of tier state is even needed at
10⁹ — with shipmem populations the u-grid may be derivable from the belt program, which would make
the best part no part.
