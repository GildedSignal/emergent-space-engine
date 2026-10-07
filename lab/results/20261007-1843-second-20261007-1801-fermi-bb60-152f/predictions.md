# Predictions — second author on 20261007-1801-fermi-bb60

Written 2026-10-07 before the decisive runs (the xtask build was still running).
The checker's named experiment: (a) the plane's real per-kick fold cost — cycle-memo
hit rate and recompile cost on **distinct** kicks; (b) the frontier republished
intersected with the 2.5×10⁸ tube-memory cap.

Held-out cases (not tuned on): the exact/quantized memo hit rates on distinct kicks
at seeds I have not run before (2, 3), and the per-kick cost at RTF 100 vs RTF 1.

- **P1 (memo, exact key):** on distinct kicks the exact-key memo hit rate is < 1%
  (the 5 October correction: distinct kicks ask distinct exact cycles; the 95–98%
  of earlier runs was one re-timed pending kick per frame).
- **P2 (memo, quantized key):** the law's 12+12-bit memo key hits 90–96% on
  distinct kicks — but re-rounding the orbit at every kick is a law change
  (law.md "Not adopted"), so this number is a bound, not a design.
- **P3 (per-kick cost):** the plane's distinct-kick cost on this box has median
  15–60 µs (29 µs on the M1 [H0210], x86 transfer within 2×), p99 ≤ 3× median.
- **P4 (decomposition):** `Orbit::compile` alone is > 50% of that kick cost
  ("recompile-dominated"), so the designed cold fold (0.05 compiles/kick, law.md)
  is ≤ 0.05 × compile < 1.45 µs — the dossier's 1.45 µs cold anchor is an upper
  bound, not a floor.
- **P5 (frontier robustness):** replacing the synthetic 64 ns hot fold and the
  1.45 µs cold anchor with the measured numbers moves every frontier row by less
  than one order of magnitude; the ~50,000× swing and the realistic-scene margins
  survive.
- **P6 (memory cap):** the resident-tube wall (16 B × strong-tide population ≤
  4 GiB) caps N* at 2.68×10⁸ ≈ 2.5×10⁸; it binds before compute in the two
  optimistic rows (K1+hot, K2+hot), and the S1c headline "all-10⁹ strong-tide
  fits compute at 15× margin" is machine-false (16 GB of tubes); the operative
  conclusion (realistic scene, compute reordering) survives.
- **P7 (realistic scene):** the galaxy scene (10⁹ belt at ≤1% live + 10⁷ fleet)
  stays under both walls by ≥ 10× (0.16 GB tubes, ≤ 9 cores worst cold).

**Kill criteria for the original claim:** if the exact-memo hit rate on distinct
kicks is > 10%, the hot-memo corner is real and *cheaper* than the dossier said
(claim strengthened, numbers corrected); if the measured distinct-kick cost is
≥ 10× 29 µs here, or compile is < 10% of the kick, the recompile-dominated
premise and the 0.05×29 µs cold anchor both break and the frontier must be
republished with different orders — that would be a refutation, not a repair.
