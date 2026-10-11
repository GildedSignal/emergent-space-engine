Working...
**Grade: gold** — written to `lab/results/20261011-0517-second-20261011-0324-fermi-c211-b3e7/check2.md`; nothing else in the run folder changed (author's data restored byte-for-byte after my reproduction).

**What I verified:**

- **Reproduction** (clean tree, empty patch, 31 s): every deterministic number regenerates bit-identically — S by rung 61.2→172.5 b (165.7 family jump), saturation 4096 scars at every rung, reabsorption ≈ −S, m-stability, zero round-trip mismatches; `budget-output.txt` regenerated **identical**. Only ns timings jitter. k0 confirmed bit-identical to shipped `Pop::kick` (`pop.rs:276–279`), and the `orbit` mirror matches the private `pop::orbit` draw order.
- **Held-out predictions** (predictions.md timestamped before the data): P1 predicted S from the representation within 4% at every rung; P2–P8 within tolerance.
- **My adversarial cases:** asymmetric magnitudes outside the author's ladder — `34,10,10,10` → S = 79.3 vs formula's 79; `16,10,10,40` → 81.7 vs 82 (ω wraparound saturation confirmed); m-stability extended to k5 (1.7% spread); probe reproduced exactly (|ΔE| med 2³⁵ p99 2⁴⁰). The formula generalizes; no exception cascade.
- **The headline correction is genuine arithmetic** from the original's own table: over ×23.9 ⇒ 4.2% of 10⁹ sustainable, not 0.5% (= 1/191, a division by core count); f* is 0.19–0.55 and the packed ceiling 53.5→160.8 b, so the original's constants were magnitude artifacts while the rule's structure survives.
- **Novelty:** nothing in HISTORY.md (through H0215) or the docs measures scar cost vs kick magnitude.

**Noted misses:** P4's "dH/kick ≈ 0.91·S" was a real unreported calibration miss (actual 0.373·S — 0.91 is the members-with-scars fraction); the family-jump redraw also jumps t, so it's a stress corner wider than a real orbit change (~128 b t-coherent); correlated encounter deltas and the inherited 29 µs/kick compute row remain unmeasured.
