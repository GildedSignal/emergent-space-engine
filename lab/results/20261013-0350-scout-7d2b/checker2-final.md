Working...
Check complete. **Grade: gold** — written to `lab/results/20261013-0350-scout-7d2b/check2.md`.

**What I did:**

1. **Reproduced** the full dossier via `regen.sh` (exit 0): every deterministic number bit-for-bit (census 1,274/196/0.846 and 32,384/31,776/0.019, min 89/max 1,752, checksum `34cc8009…`, 0/48 arm mismatches); timings within the disclosed noise (reciprocal cold 40.6 vs libcall 23.4 ns). Verified `Scalar::div`→`div_word` routing and that the four censused sites are the real `fast_quad` u128 `/` sites.

2. **Predictions**: `predictions.md` (03:56) predates the bench code (03:59) and instrumentation (04:06). The decisive ones (P3 no-repetition, P4 bit-identity, P5 gain bound) held; P1/P2 point estimates missed *in the kill's favor* and are disclosed — though calling them "held" is generous wording, which I flagged.

3. **Five adversarial cases**, including one outside the author's range (160-key grid, p 4–8192, e to 0.99):
   - Per-key repeat is **exactly 0.000** for every e>0 key, through e 0.99 and 2,080 divisions/compile — the kill is stronger than the 0.019 aggregate.
   - Found an unnamed corner: **e=0 circular keys repeat 95%** — but at 80 divisions vs ~2,000, immaterial.
   - Found an unmeasured counter-move: **23% of division instances share divisors across compiles** (far-field convergence); bounded even a *free* global reciprocal cache at ~4% of the compile (100% sharing caps at 18%) — caching can't revive the lever either.
   - Independent 2×10⁶-case fuzz of the reciprocal (different PRNG, exact multiples, boundary divisors): 0 mismatches; bit-identity also provable by construction (q̂ never overestimates).
   - Regime timing 379→285 ns/gauss-node (compact→far); the 94 ns delta is exactly the u128-isqrt ingredient, validating Table 4's structure.

4. **Novelty** confirmed (the page's own open direction 1, never measured before), **page faithful** — I corrected it in place with the check2 facts (per-key 0.000, the e=0 corner, the cross-compile bounds).

5. Tree restored to as-found (patch reversed, scratch example removed, verified clean); nothing else in the run folder touched.
