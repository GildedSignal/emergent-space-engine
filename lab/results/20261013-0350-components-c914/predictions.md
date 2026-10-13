# Predictions — 20261013-0350-components-c914 (written before the decisive runs)

Lens: first principles, one component at a time. Component: the kick's exact recompile
(`Orbit::compile` interior), the board's live question "cheapest exact kick on the shipped
representation". The record's standing attribution (061f: ~900 i128-division-equivalents own
the interior) is a count-based inference; these predictions are what the timing-hack
decomposition and the Newton-reciprocal prototype should show if my measured split is real.

## Held-out cases (not tuned on)

1. **Interior split, second key grid.** Measured on the tuned grid (e ∈ {0.02…0.99},
   radius_exp −4…20): divisions 34.6% (median 45.78 → 29.94 µs), cos 40.2%
   (45.78 → 27.39), isqrt 13.6% (45.78 → 39.54). On a held-out grid (seeded uniform e,
   random radius_exp in −6…24) I predict the same ordering: cos > divisions > isqrt, with
   cos share 35–50% and division share 25–45%. If divisions come out first (> cos share),
   my split is grid-specific and the record's division-first attribution stands.
2. **Hardware division floor.** x86 `divq` (asm, exact) vs the compiler's soft
   `__udivti3`/`__divti3`: I predict |Δ| < 15% on the fast_quad operand shapes
   (dividend < 2^127, divisor ∈ [2^20, 2^62], high limb < divisor). Measured baseline
   22.55 ns (u128) / 26.60 ns (i128) vs asm 22.79 ns — already consistent; the checker's
   rerun should reproduce within shared-box noise (±25%).
3. **Exact Newton-reciprocal division** (f64 seed, 2 integer Newton iterations, exact
   ceil-reciprocal fix, one final correction): I predict it is exactly equal to `/` on all
   random and adversarial operands (0 mismatches; d near 2^62, d = 2^20+1, dividend near
   2^127, high limb = d−1, d a power of two), and lands in 8–18 ns — at best ~2× the soft
   division, i.e. the division share caps any kick win at ≤ ~17%.
4. **Per-node arithmetic floor.** With knot counts printed, per-node cost (total compile
   time / 4·panels) should be roughly flat across e (110–200 ns/node) — if instead it
   grows with e, panel count, not per-node cost, owns the high-e tail and the law's π/4
   quantum is the lever (a law change, not an optimization).
5. **Default-path identity.** With the env-gated hacks off, the compile checksum must be
   identical to the unpatched tree's (133c7636a7f1f4cacd3bf1a43e92b57c on the tuned grid)
   and `cargo test -p emergent-space` must pass — the probe must not change shipped bits.

## What would make the claims wrong

- A division variant materially faster than 2× (then the open direction revives with a
  measured lever);
- cos share < division share on the held-out grid (grid artifact);
- any mismatch in the Newton division or any checksum/test drift (probe is not
  bit-identical; run loses its identity claim).
