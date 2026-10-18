# Predictions (written before the decisive run)

Component (lens): the compile's per-node arithmetic — `fast_quad` in `crates/space/src/orbit.rs`,
the quadrature every compactness≠0 compile walks. Read-stream od 7 micro-measured its four
wide `u128/u128` divisions (4 × 22.4 ns → 4 × 2.8 ns if `div_word`) but never flew them.

The patch: replace the four per-node wide divisions at `orbit.rs:429-433` with
`crate::num::div_word` (the primitive `weak_quad` already uses at `orbit.rs:382`). Exactness
argument: at every site the shipped code casts the quotient `as u64`; a truncating cast would
already be a shipped bug, and for integer `n,d` (d < 2^64) "quotient fits u64" ⟺ `n>>64 < d`
= div_word's precondition — so the patch is exact wherever the shipped bits are.

## P1 — exactness (the certificate)
- `div_word(n,d) == (n/d) as u64` on ≥10^7 random+biased pairs with quotient < 2^64: 0 mismatches.
- Patched vs shipped: space crate test suite identical (all pass), certified-bank rungs
  unchanged in pass counts, `ladder_digest` digests bit-identical on the N=3000 cases.
- Held-out/adversarial (not tuned on): near-separatrix rows (p → 6+2e), e = 0.99999,
  p = 10^5–10^6, the `word_root` boundary delta ≈ 2^62/4, small-k hyperbolic passages
  (a = 6k+2·ac stays > 0 on the walked domain because x > 0 is enforced), debug-build
  div_word asserts on a subset (they fire only if the shipped cast ever truncated).
- Kill: any differing bit, test, bank row or digest → the precondition is not covered by
  the shipped cast domain; the corner found is itself the result.

## P2 — site cost
On this shared x86 box: one wide u128/u128 division ~15–30 ns, one `div_word` ~2–5 ns;
per-node Δ ≈ 40–90 ns (the prior run's micro: 22.4 → 2.8).

## P3 — compile cost (decisive)
Fast-path `Orbit::compile` per key falls **15–40%**, roughly flat in p and e (a constant
per-panel Δ): the four divisions are a fixed per-node tax, so ns/panel falls by the same
fraction as ns/compile. My point estimate before running: **20–30%**.

## P4 — engine level
Digest bit-identity is the certificate; wall on the belt-crossing digest case drops by a
few percent at most (compile is 49% of the fit stage, the fit ~45% of the kick item, and
the frame holds more than kicks — d399/5eb2 numbers), inside shared-box noise; orders only.
