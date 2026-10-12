# Predictions (written before the decisive experiments)

Artifact: `crates/space` orbit compiler (`Orbit::compile`), the plane's hot path (it recompiles per kick).
Metric: ns per compile on the tuning corpus (seed 1, 480 keys, p in [2.5, 1.3e6] M, e-biased mix).
Behaviours fixed: bit-identity — FNV hash over every knot, increment, crossing time and readout state must not move; `cargo test -p emergent-space` green.

Baseline (this machine, release, lto=thin): tuning 16409 ns/compile (26.7 knots/orbit), heldout 30004 ns (50.3 knots), readout ~4.1-4.4 µs/state.

Hypothesis chain: the per-node cost (~150 ns) is dominated by 128-bit software divisions (`__udivti3`/`__divti3`: `(1<<104)/root`, `a*g/(1+root)`, `(floor<<62)/x`, `(rtau<<62)/horizon`, isqrt's Newton `x/y`), each replaceable by the exact word-size `div_word` (same floor quotient, quotient provably < 2^64 because the existing code already casts `as u64`).

## Held-out cases (not tuned on)

The heldout corpus (seed 2): near-circular e=0 and e=0.02, extreme e=0.9/0.99/0.999, scales p = 2.2·2^(j/2) M for j=0..23 (compact to far), plus the seed-2 random mix.

1. **P1 (transfer of the division fix):** heldout compile drops by ≥25% (its per-node cost is the same dimensionless arithmetic; its extra knots are near-separatrix panels, same node kernel).
2. **P2 (readout):** the read path (`state` → `at_phase` → partial quadrature + Newton solve, same `quad`/`node` kernels) drops by ≥15%.
3. **P3 (exactness):** hashes identical on both corpora; full crate test suite green after every kept change.
4. **P4 (ceiling):** after the division replacements, the residual compile cost is no longer division-major (cos's 13 nested products and Scalar normalization dominate); a further same-bits change gains <10% per round, triggering the stop rule within ~3 more rounds.
5. **P5 (where the local search cannot go):** the structural win my loop will miss: panel nodes recompute `cos` per node per compile, but knots are per (k, q)-shape and shapes repeat across the fleet; a memoized shape store (already half-built as `ShapeMemo`) removes compile entirely for repeated shapes — my ns/compile optimisation only pays the first-compile price down.

If P1 or P2 fails while hashes hold, the division-attribution hypothesis is wrong and the dossier says so.
