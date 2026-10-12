# Dossier — run 20261010-0656-autoresearch-cc88 (lens: autoresearch on something that works)

## Claim

Interleaving the four Gauss–Legendre panel cosines of the cycle compiler into one
four-lane Horner evaluation (`num::cos4`, each lane running `cos`'s exact operation
sequence) cuts the plane's kick cost by 16% (median µs per kick, all populations,
four seeds) with the law's bits identical — replay and universe digests unchanged,
both test suites green.

## Bottleneck

Board focus line 1: "fewer kicks per orbit … kicks dominate the engine's cost."
The cost of a kick is the product of kicks per orbit and µs per kick; this run
attacks the second factor at fixed behaviour. Measured on the plane's own kick
bench (`--kick-bench`, the deterministic per-kick replay): `bind` is ≈80% of a
kick, and 84% of `bind` is `Orbit/Passage::compile` (63 µs per compile on this
runner), of which ≈33 µs is `num::cos` (759 calls × 42.9 ns, a 13-step
latency-bound chain) and ≈17 µs is `isqrt`. Exact-key memoization of compiles is
dead (663 distinct shapes in 663 rebinds — the 5 October taste-log entry,
independently reconfirmed). Not an order of magnitude: 1.19× per kick, reported
as such.

## Evidence (log.md has the full table; runner: 8 vCPU i7-4790 @ 3.6 GHz, light load)

- Baselines: 2 reps per seed, spread < 1%. Final: 3 reps seed 1, 1 rep each held-out
  seed (as pre-registered).
- `kick_us_all` median: seed 1 88.45 → 74.6 (−15.6%), seed 2 58.70 → 49.34 (−16.0%),
  seed 3 88.05 → 73.73 (−16.3%), seed 4 71.85 → 60.14 (−16.3%). Leavers (80% of
  kicks): −16.6 to −17.3%. p99 falls too (seed 1: ~376 → ~350 µs).
- Bit-identity: `replay_digest` and `digest` equal the baseline values on every seed
  (seed 1 `59ea9969…`/`13cfe88b…`, seed 2 `d608ef86…`/`44f39a11…`, seed 3
  `84f30efe…`/`cac2c8c7…`, seed 4 `1f8769f7…`/`0b6ceac7…`); `refused` 0 everywhere.
  Per-key knot hashes of 338 compiled orbits were compared against the original code
  during development: identical.
- Exactness pinned in-tree: new test `cos4_returns_cos_exact_bits_per_lane`
  (200 k random quads over [0, π] plus the guarded corners).
- Reverted by measurement (log.md): hoisting the append cut (−0.3%, the weak path's
  q = 0 short-circuits to `PI`), `isqrt` via `div_word` (+1.1%), `atan` via
  `div_word` (+0.7%) — on this core, i128 division is not the cost center; `cos` was.

Commands (build ~40 s once; each run ≤ 60 s; target dir is `$CARGO_TARGET_DIR`):

    cargo build --release -p xtask
    for s in 1 2 3 4; do $CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 10 --rtf 100 --seed $s; done
    cargo test --release -p emergent-space      # 41 passed (incl. the new exactness test)
    cargo test --release -p emergent-universe   # 54 passed (bit identity, replay, ties)

Deliverable: `keep.patch` in this folder (134 lines: `cos4` + `node_at` + the two
panel quadratures + the test). Nothing else changes.

## Predictions

Written before the held-out runs (`predictions.md`). What happened:
1. "Gains within ±5 pp of seed 1" — held (max deviation 1.7 pp).
2. "Digests equal baseline, refused 0" — held on all four seeds.
3. "Plane-made kicks improve ≥ half the leavers' relative gain" — held (−12% vs −17%).
The two losers (isqrt, atan via `div_word`) were predicted −5–15%; they measured as
small regressions and were reverted — the prediction was wrong about the cause
(i128 division cost), and the measurement caught it.

## What would make it wrong, adoption cost, fit

- Wrong if: the digest lock is weaker than it looks. It hashes `Debug` output of the
  resolver's records, so it is format-sensitive (during development, adding a struct
  *field* changed the digest with zero physics change — caught and routed around by
  passing the hoisted value as an argument instead). The final patch changes no
  `Debug` output, and knot-level per-key hashes were checked separately.
- Cloud caveat (lab rule): these are Linux/x86 orders of magnitude; the integrator
  re-measures on the M1. The mechanism (four independent latency chains overlap) is
  architecture-generic, but NEON's 128-bit lanes may prefer a 2×2 interleave.
- Adoption cost: trivial — two files, no API change, no law change, one property
  test added. No migration.
- PRINCIPLES fit: "Simplify, never dumb down" and "Compute only surprises" (1, 3):
  the same compute is done, its latency is overlapped; "cheapest arithmetic … we
  love 2" (16); "Exact means bit-identical on every machine" (law.md) — equality is
  by construction per lane and pinned by test; gates judge behaviour, and behaviour
  (digests, suites) is unchanged.

## The lens

A local search at fixed behaviour found a local optimum: 1.19×, then three rounds
under 10% and stop. What would beat it structurally: (a) the re-anchored jet for
kick rebinds (law.md "Not adopted" note; gold-graded once) deletes most compiles
entirely — a law change, outside this lens by construction; (b) the panel count
itself (~134 knots per compile) is set by the band ladder — fewer knots at identical
bits is impossible, so the remaining compile cost (≈40 µs of div_word, Scalar adds,
knot stores) is the floor for exact recompiles; (c) SIMD: on the M1 the four lanes
are two NEON 2×i64 words — worth one build there before adopting, as the checker
should verify on ARM. This lens also optimized only the compiler's weak path (the
plane's kicks); strong-field scenes (fast_quad) were measured but not tuned.
