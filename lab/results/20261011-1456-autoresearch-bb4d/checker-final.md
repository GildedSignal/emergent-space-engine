Working...
Check complete. `check.md` written to the run folder; tree restored to clean (patch reverted, temp files removed).

## Grade: silver

**Reproduced in a clean tree** (unpatched baseline → `git apply` patch → rerun):

| Check | Author | Mine | Verdict |
|---|---|---|---|
| Plane digest (seed 1) | `46d63fe0…` | identical pre/post patch | ✓ |
| Replay digest | `f3e04738…` | identical pre/post | ✓ |
| Whole-plane digest | `6ce636fa…` | identical pre/post | ✓ |
| Seed 42 (my adversarial, author never ran) | — | `d02b546f…`/`59c6148f…` identical pre/post | ✓ |
| compile share of a kick | 84% | 84.2% | ✓ |
| quad calls/kick | ~140 | 140.3 | ✓ |
| Tests | 40 green | 50 green, 0 failed | ✓ (undercount) |
| Speedup on x86 | 0% | 0% (prediction honestly failed) | ✓ |

**Adversarial attacks beyond the author's:** a 4M-pair property test of `div_u128_word` vs native division (guard boundary, d=2⁶⁴ edges, all four call-site shapes) — zero mismatches; plus the analytic precondition argument (`floor ≤ x` always holds). Held-out seeds 7/13: refused 0, same orders.

**Main finding the author missed:** the phase µs/kick table conflates bench replays with engine-internal kicks (`lab::enable` is process-wide) and is inflated ~2× by its own instrumentation — proven by a KICK_REPS=1 control (compile 277.7 µs/kick vs 107.3 at reps=9; engine ≈ 20% of the compile slot). The *shares* are robust, so the headline (compile ≈ 84%, panel-count × ~200–270 ns/node, no hotspot, micro-opt dead) stands; the absolute µs do not. Also: `quad` > `compile` because quadrature fires outside the wrapped compile — the panel story is stronger than stated.

**Not gold** because nothing moved 10× and the speedup prediction failed (reported honestly). The named gold experiment: coarser certified band grid (or shape cache keyed by passage edge) at bit-identical digests — a ~10× cheaper kick would directly move board #1.
