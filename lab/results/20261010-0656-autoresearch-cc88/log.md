# Autoresearch log — run 20261010-0656 (artifact: `xtask universe --kick-bench`, metric: `kick_us_all` median µs, behaviour lock: `replay_digest` + `digest` per seed)

Machine: GitHub Actions Linux runner, 8 vCPU i7-4790 @ 3.6 GHz (Haswell), shared, load light.
All runs `--seconds 10 --rtf 100`. Baselines are two reps per seed (spread < 1%); tuned runs three reps.

| # | Hypothesis | Change | Metric (seed 1, all-median) | Verdict |
|---|---|---|---|---|
| 0 | — | baseline (instrumented-off build) | 88.33 / 88.57 µs (clean build 88.3/88.6; instrumented bits identical, replay 59ea9969…) | — |
| P | profile (env-gated phase timers + op counters) | no behaviour change | bind ≈ 80% of kick; compile 84% of bind (63 µs); 134 panels/compile (123 weak), 759 cos, 181 isqrt; cos 42.9 ns, isqrt 93.6 ns measured | evidence |
| A | per-append recompute of the shape-constant cut (`√δ/√qa·2⁻²`) wastes 2 isqrt + 1 div × 73 appends | hoist to a field / arg, computed once per compile | 88.05–88.20 µs (−0.3%) | REVERTED (noise; the weak path's q = 0 short-circuits to `PI`, no sqrt in it at all) |
| B1 | cos is latency-bound (13-step dependency chain); 4 independent panel nodes can interleave | `num::cos4` (4 lanes, exact per-lane op sequence), used by both panel quadratures; duplicate `cos` in `node` removed via `node_at` | 73.62–73.77 µs (−16.5%) | KEPT (equality: cos4 == cos on 8,000,016 values incl. corners; digests identical) |
| B2 | isqrt's u128/u128 Newton division → exact `div_word` when quotient is word-sized | fast path in `isqrt` | 74.45–74.81 µs (+1.1 µs vs B1 alone) | REVERTED (LLVM's i128 division is already efficient here; branch+call overhead dominates) |
| C | `atan`'s i128 division (≈73+/compile) → exact `div_word` with sign handling | swapped division | 74.11–74.68 µs (+0.7 µs vs B1 alone) | REVERTED (same lesson) |

Three consecutive rounds (A, B2, C) gained < 10% → loop stopped (lens rule). B1 kept.

## Final configuration (clean build, instrumentation stripped)

| seed | kick_us all median (baseline → final) | gain | kick_us made | kick_us leavers | replay_digest / digest |
|---|---|---|---|---|---|
| 1 (tuned) | 88.45 → 74.6 (73.0–76.1, 3 reps) | −15.6% (−14.6 to −16.7) | 35.75 → 32.3 | 91.55 → 76.9 | identical |
| 2 (held out) | 58.70 → 49.34 | −16.0% | 35.47 → 31.06 | 84.62 → 69.97 | identical |
| 3 (held out) | 88.05 → 73.73 | −16.3% | 35.70 → 31.41 | 91.26 → 75.80 | identical |
| 4 (held out) | 71.85 → 60.14 | −16.3% | 35.75 → 31.49 | 74.27 → 61.91 | identical |

p99 also falls: seed 1 all-p99 375–376 → 346–360 µs. `refused` 0 everywhere (bench exit 0).

## Commands (each ≤ 60 s; build ~40 s once)

    cargo build --release -p xtask
    for s in 1 2 3 4; do target-dir/release/xtask universe --kick-bench --seconds 10 --rtf 100 --seed $s; done
    # target dir is $CARGO_TARGET_DIR (~/lab-target-1 here)
    cargo test --release -p emergent-space        # 41 tests incl. new cos4 exactness test
    cargo test --release -p emergent-universe     # plane bit-identity, replay, ties

## The idea that carried the gain

cos is a 13-step latency-bound Horner chain (42.9 ns each, ~759 calls per kick compile);
the four Gauss–Legendre panel nodes are independent, so interleaving the four chains
(`cos4`) overlaps their latencies without touching any lane's operation sequence — the
compiler's bits are identical by construction, and the exactness is pinned by a property
test. One function, −16% on the engine's dominant per-kick cost, zero law change.
