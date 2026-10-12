# log.md — autoresearch loop (artifact: `crates/space` orbit compile; metric: ns/compile; behaviour held fixed = bit-identical compiled output, judged by a hash of the full Debug dump of every compiled orbit)

Baseline (main corpus, 3×30 reps): mean 36.1 µs/compile, median 29.5, p99 114.4, hash 7932a7d0de3d965919763c10a2a780f2.
(The shared box drifts; all keep/revert verdicts below use interleaved A/B of two saved binaries, not cross-time comparisons.)

| # | hypothesis | change | metric (interleaved A/B) | verdict |
|---|---|---|---|---|
| 0 | where does compile go? | TEMP stage counters in orbit.rs (quad/cut), then removed | quad ≈ 70% (≈225 ns/node), cut ≈ 15% (≈190 ns/call), rest ≈ 15% | attribution only |
| 0b | which kernel? | micro-bench: isqrt 97.5 ns, u128/u128 (`__udivti3`) 24.2 ns, `div_word` 47.0 ns | — | div_word swap REJECTED: the crate's 2-digit division is *slower* than the compiler's software 128/128 division on x86-64 |
| 1 | isqrt's top-64 seed wastes a division | f64 seed + provable at-or-above margin (`est + (est>>40) + 16`, u64 path below 2^40); descent untouched → same bits. Agreement: 2.2e6 adversarial inputs, 0 diffs | main: mean −4.2%, median −3.3%, p99 −6.1%; heldout: mean −5.7%, p99 −5.1%; hash identical | KEPT (real, bit-identical, but < 10%) |
| 2 | the 3 wide divisions per fast_quad node (~72 of 225 ns) can go via div_word or f64+fixup | measured alternatives: div_word 47 ns > 24 ns; f64-two-step + exact fixup ≈ 18 ns vs 24 ns | ≤ 6% best case, high fiddle | REJECTED (no change made) |
| 3 | generic `node()` recomputes cos: `self.x(psi)` re-evaluates `k + product(ONE-k, cos(psi))` already computed as `x` | pure CSE, provably identical bits | no measurable change on either corpus: the generic Scalar path requires delta < 2^30 (within 2^-32 of the separatrix) — unreachable for realistic bound keys; only photon passages can land there | KEPT (weightless-code removal; gain unmeasurable on bound corpora) |

Stop rule: three consecutive rounds under 10% (5%, 0%, ~0%) → STOP, per the lens.

## What the loop did not try (out of time / law changes)

- Extending the u64 `word_root` sqrt below delta ≥ 2^60: the Q31 floor's rounding is not bit-identical → law change.
- Panel count / CAP: quadrature error is law → forbidden by the fixed behaviour.
- SIMD across the 4 GL nodes of a panel: each node's 3 divisions are independent; same integer ops per lane preserve bits. Not attempted in 60 min.
