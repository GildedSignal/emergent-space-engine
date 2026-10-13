Working...
Check complete. **Grade: gold** — written to `lab/results/20261013-0350-scout-7d2b/check.md`, with one page correction applied.

**What I did:**

1. **Reproduced** the full dossier from `regen.sh` in a clean tree (exit 0): census bit-for-bit identical (1,274/196/0.846 div_word; 32,384/31,776/0.019 u128 sites; 0/48 arm mismatches; identical fuzz checksum `34cc8009c0e3244e3f0b06`), timings within 4% and same orderings (cold reciprocal 42.0 vs 40.4 ns; libcall 24.1 vs 23.6). Three re-invocations confirmed the census is deterministic and the schoolbook-vs-libcall arm difference is invisible under the box's noise (54–57 µs both arms), verifying the dossier's ~0.1 µs census bound.

2. **Predictions**: file times consistent with pre-registration (03:56 → 03:58 → 04:06 → 04:11). P1's point interval was missed by ~2× (predicted 12–22 ns, measured 40.4) — in the kill direction, and the miss is the best evidence of genuine pre-registration. Even under the author's wrong estimate, the pre-registered criteria still kill the lever: no repetition caps it at ~7% of the compile, below P5's own 10% line.

3. **Adversarial cases**: (a) near-separatrix compact keys at e ≤ 0.99, outside the author's tested range — repeat fraction **0.0000** (every divisor distinct, up to 2,080/compile; 2,210 total divisions), so the structural kill holds where the author didn't look and the count lever grows with e; (b) noise-spread re-runs; (c) code-level verification that all four censused divisors are functions of the node's ψ (`root`, `1+root`, `x(ψ)`, `horizon(ψ)` — recomputed per node).

4. **Novelty**: no prior reciprocal/Möller–Granlund work in HISTORY, the wiki, or git log; the killed lever is the standing page's named attack in open direction 1.

5. **Page**: faithful pure additions; I corrected one overstatement in place — the census covers only the four `fast_quad` sites plus `div_word`, with `isqrt`'s internal Newton divisions uncensused (the gap between ~700 and 061f's ~900, and part of the 30% isqrt share).

Tree restored to the state I received (author patch reversed, my probe removed); nothing in the run folder touched except `check.md` and the page correction; no git operations.
