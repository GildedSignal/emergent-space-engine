# Predictions (written before the decisive experiment)

Question: can the exact kick's division cost (the named lever after 061f: ~900
i128-division-equivalents at 30.9 ns owning most of a 33 µs kick) be cut by a cheaper
bit-identical division primitive, without relying on divisor repetition?

Cases I did NOT tune on (held out until after the bench):
1. **Primitive landscape (this Haswell-class box, cold divisors):**
   - P1: `u128 / u128` (`__udivti3`) ≥ 25 ns per call; `div_word` (2 dependent native
     64-bit divisions) ≈ 30 ns; a reciprocal (Möller–Granlund-style) division with the
     reciprocal computed cold lands at 12–22 ns — i.e. **at most ~2×, likely ~1.5×,
     over `div_word`**, because two Newton steps cost most of what they save. If it
     lands > 25 ns the primitive lever is dead cold.
   - P2: with the reciprocal amortized over repeated divisors, per-division cost drops
     to < 8 ns (3 multiplies + correction), ~4× over `div_word`.
2. **Divisor repetition in the real compile (instrumented `div_word` + the four
   `fast_quad` `/` sites over a key sweep):**
   - P3: divisors do NOT repeat materially across nodes within one compile (distinct/total
     > ~0.8) — 061f's "where divisors repeat" hedge is not available on this path; the
     reciprocal would have to pay cold. (If they DO repeat ≥ 3× on average, this flips
     to the strongest lever on the page.)
3. **Workload (patched `div_word` + `fast_quad` routed through it, bit-identity):**
   - P4: reciprocal division is bit-identical to `/` over ≥ 10⁷ fuzz cases including
     adversarial near-multiple and high-bit inputs (provable; my implementation is the
     risk — any mismatch kills the whole direction).
   - P5: if P1 holds (~1.5× cold), `Orbit::compile` wall drops ≤ ~25% on key sweeps;
     it takes P3 flipping (repetition) for the hoped 2×+. A compile gain < 10% kills
     the primitive lever.
4. **Kill criteria:** any fuzz mismatch (P4); or cold reciprocal ≥ `div_word` (P1);
   or compile gain < 10% (P5). A KILL here kills the division primitive as the named
   lever, never the exact-recompile direction itself (the count lever — fewer panels,
   fewer divisions per panel — survives untouched).

Controls: native u64/u64 division timed as the floor; `/` on u64 operands (no
libcall) as the no-trick baseline; the shipped `div_word` reimplemented verbatim in
the bench and cross-checked against the crate's own (same bits) before any timing.
