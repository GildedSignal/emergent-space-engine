# predictions.md — 20261018-1804-quant-2fd1 (quant lens)

Question: price the encounters page's named, unpriced lever — `first_hit`'s u128
arithmetic (the exact integer conjunction decision) — as a u64 port, with its
soundness domain and its edge on the real section mix.

Frozen before any run of the bench. Kill rule (lens rule 4): if the best sound
u64 variant gains < 1.3x ns/call over shipped on the design-reach cell mix, the
lever is a lead, not a lever (e87d's section cache at 3.4x stays the row's lever).

## Pre-registered predictions (held-out cases; not tuned on)

- P1 (exactness): the u64 port with a u128 return line (V1) and the checked
  u64-return variant (V2) return byte-identical results and identical `steps`
  counts vs shipped V0 on (a) every candidate section of the design-reach cells
  (a-window 1e-4 and 1e-5 AU, 2,000 bodies, rho = 3.34e-6 AU), the wide [2,3) AU
  belt, and a Full-corner formation; (b) >= 2e6 random integer draws at
  m in [2^30, 2^40] with thin/wide windows, near-commensurate d, golden-ratio d;
  (c) brute force at m <= 2^16. Predict: 0 mismatches anywhere.
- P2 (soundness domain, derived): the port is exact for m < 2^63 (all values < m);
  the only wide intermediate is the return line's m*y (<= m^2). Predict the measured
  max m*y over the real belt mixes is < 2^64 in the tight cells (d small => y <= d
  small) but exceeds 2^64 on some wide-belt/formation calls (V2's fallback fires
  there, < 10% of calls).
- P3 (timing): on the design-reach cell mix, shipped V0 runs 300-700 ns/call
  (mean recursion depth ~15-25 levels x ~3 u128 divisions); V2 gains >= 2x
  (Haswell: 64-bit DIV vs __udivti3). Predict V2 in [120, 350] ns/call there;
  >= 1.5x on the wide belt.
- P4 (composition): first_hit is the majority of e87d's 416 ns/pair/kick cached
  decision path; the composed row (cache + port) lands at 1394 -> <= 300 ns/pair/kick
  (>= 4.5x), i.e. the 355-core row -> <= ~160 cores, without touching the decision
  integers.
- P5 (depth): mean recursion depth grows ~ log_phi(m) — predict mean steps/call
  14-26 at m ~ 2^36-2^38, worst > 40 on golden-ratio d.

What would make it wrong: any decision mismatch (V1/V2 vs V0) kills the port's
exactness claim outright; a gain < 1.3x kills the lever (kill rule above); the
fallback firing > 50% on the real mix would cap the gain near V1's.
