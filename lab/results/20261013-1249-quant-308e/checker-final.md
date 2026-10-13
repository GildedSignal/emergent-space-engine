Working...
Check complete. **Grade: lead** — written to `lab/results/20261013-1249-quant-308e/check.md`, with the author's proposed page corrected in place.

## What reproduces

- Primitives: cos 43.4 ns (author 41.6), unrolled control equal, cos4 lane 28.9 ns = 1.50× isolated, 2M-lane fuzz bit-identity, suite green, both plane digests exact (`0c306185…`, `d8a1847c…`). Pre-registration verified (predictions 13:02 vs artifacts 13:09–13:10). The 30%-epoch-drift warning is real — I watched identical code move 18.2 → 24.5 µs within minutes.

## What falls — the headline "0% at the compile" is an artifact

A coarse sabotage probe (one cos4 lane += 2⁶⁰) leaves **all 28 grid keys and both plane digests bit-identical**: neither the author's grid (p ≥ 2²⁰) nor the plane ever executes the patched `fast_quad`. `compactness = 1/periapsis` clamps to zero below q = 2⁻¹⁸ and `quad()` dispatches e>0 keys to `weak_quad` — which the patch never touched (`predictions.md` falsely claims it did). Both A/B arms ran identical code; the "OoO already interleaves" mechanism was asserted from a measurement of nothing.

On keys that genuinely run cos4 (p 2⁴–2¹⁶, e 0.5–0.999 — the decades below the grid), a balanced A/B (12 runs/arm) measures **+2.9% (2.3–3.4%) per compile**, every key positive, with the unpatched keys at −0.1% as a clean null. The interleave partially survives the node; the direction stays open, with `weak_quad` — the plane's actual quadrature — untested. The exact lab precedent: "check that the measured events are distinct before counting hits" — zero cos4 executions were counted as a cos4 measurement.

The primitive half stands (chain floor, codegen dead, 77 ns corrected); the page now records it with checker corrections, the false refutation withdrawn, and main's dropped 1a restored. Tree left clean at base; no commits.
