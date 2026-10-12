# Dossier — 20261006-1101-autoresearch-52e5

## Claim
Replacing SipHash with a multiply-xor hasher in the CPU chronon reference's three maps
makes the reference 1.4× faster (771 → 542 ns per body-chronon at n=200k) with bit-identical
digests; two heavier restructuring attempts (scatter table, Bloom gate) measured *slower*
and were reverted, locating the remaining cost in cache misses, not arithmetic.

## Bottleneck
Board #3, "cheaper events": the CPU chronon reference is the artifact every other mode must
reproduce bit for bit, and its per-chronon cost sets the pace of every verification run
(iteration speed, P10). Gain: 1.4× end-to-end (2.1× where map ops dominate), for a 60-line
patch that deletes nothing but a hasher. What it deletes: SipHash-1-3 on ~2.4M map
operations per chronon at n=200k (1.8M `ranges` probes + 0.2M inserts + 0.39M `consumed`
probes).

## Evidence
Protocol: `taskset -c 4`, median of 5 (tuning) / 3 (held-out); Linux x86 shared runner
(8 vCPU, load 1–3), orders of magnitude only. Reproduce (each ≤ 60 s):
- Build: `cd lab/results/20261006-1101-autoresearch-52e5/bench && cargo build --release`
  (binary lands in `$CARGO_TARGET_DIR/release/chronon-bench`).
- Tuning case: `taskset -c 4 $BIN 200000 32 0.1 256 2718281828 5`
  → baseline 771, final 542 ns/body-chronon (digest `af1ddc8f…|81428e3f…` in both).
- Held-out (baseline → final, digests equal in every case):
  n=50k 652→308 (2.12×); n=400k 819→554 (1.48×); fill .05 567→318 (1.78×); fill .2
  1308→930 (1.41×); vmax 64 517→316 (1.64×); vmax 512 1005→711 (1.41×); RelativisticV1
  627→586 (1.07×); new seed 731→573 (1.28×).
- Behaviour lock, final build: `cargo run --release -p xtask -- lattice-check` → 3/3 EQUAL
  (events, finals, wall momentum vs the independent all-pairs integer reference);
  `lattice-check-rel` → 4/4 EQUAL. Raw outputs in `work/`.
- Section profile at baseline: detect phase 92.7%; after H1: pair loop 77%, sort 13%,
  map build 4%, advance 3.4%, respond 1.8% (instrumented copy, since reverted).

Full loop with kept/reverted verdicts: `log.md`. Patch: `work/chronon-fastkey.patch`
(applied to `crates/lattice/src/chronon.rs`; the tree carries it).

## Predictions
`predictions.md` was written before the decisive runs. What happened:
- H1 ≥ 1.4×: held (1.42×).
- H2 (scatter table) ≥ 2.5× combined: **failed** — 0.79×; reverted. The premise ("sort +
  map dominate") was wrong *in steady state*: bodies barely move between chronons, so
  pdqsort runs near-linearly on nearly-sorted keys, and hashbrown's SSE group iteration is
  cheap; the table's 14 MB random-probe footprint was the regression.
- Held-out P1 (gains hold across n, shrink at fill 0.2 where `hit` dominates): held
  (1.41–2.12×). P2 (vmax 512 holds or improves): held (1.41×).
- P3 (digests identical everywhere): held — all 8 held-out configs plus lattice-check
  and lattice-check-rel.
- P4 (relv1 ratio unchanged within noise): **half-missed** — 1.07× vs Newtonian's 1.42×
  at the same shape; the relativistic `respond` is heavier and dilutes the map savings,
  which I under-counted.

## What would make it wrong
The gain is measured on one Linux box, one gas family (uniform discs, fill 0.05–0.2,
vmax 64–512): a workload with far fewer map operations per body (near-empty cells at
extreme dilution, or one body per cell) shrinks the ratio toward 1. The M1 may differ in
cache behaviour (SipHash speed relative to memory). Wrongness would show as: a digest
mismatch (impossible by construction — iteration order never reaches an output; verified
on 11 configs), or a slower M1 (integrator re-measures).

## Cost of adoption, fit with PRINCIPLES
~60 added lines, no API change, no law change, no new dependency. Fits "the cheapest
compute is compute not done" (P1: the hasher work is deleted, not optimized) and
"iteration speed" (P10: every chronon-mode verification run gets 1.4×). It is not a
10× board move: silver-grade, adoptable in one step.

## The lens
The autoresearch loop found a local optimum fast and the stop rule fired after three
reverted rounds. What it made me miss: the *structural* alternatives named up front in
`predictions.md` — per-body reach tiers (cell size is set by the worst kmax, so every body
pays the densest body's neighbourhood) and the event-sorted frontier (the event mode's
answer, already in the tree). Both would restructure the 77%-pair-loop rather than cheapen
its hashing; both are law changes, out of this run's scope, and they are where the next
10× on this artifact lives.
