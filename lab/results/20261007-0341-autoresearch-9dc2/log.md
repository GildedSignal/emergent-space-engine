# log.md — autoresearch 9dc2

Artifact: `xtask universe --kick-bench` (pure kick resolver on the plane's own scene).
Scalar metric: median µs per distinct kick; behaviour lock: `replay_digest` + `digest`.
Tuned-on config: `--rtf 100 --members 400 --seconds 8` (4918 samples, deterministic).
Cloud caveat: Linux/x86 shared runner (loadavg 0.2); orders of magnitude only.

Baseline (pristine, 3 runs): median 83.6–84.7 µs, p99 386–390 µs, digests
`14d14cd4…` / `57c91487…`, samples 4918 every time. Run-to-run spread ~1%.

| # | Hypothesis | Change | Metric (median µs) | Kept/reverted |
|---|---|---|---|---|
| 0 | Where does the kick go? | phase probe: read/ctx/field/quant/rebind/post | rebind 97% of kick time (avg 80.9 µs, max 667) | probe |
| 0b | Inside rebind? | sub-probe: fit_key / compile / at_radius / decoded | compile 66.5 µs = 79% of kick (10437 calls: ~95% Cycles ~52 µs, 492 Passages ~374 µs) | probe |
| 0c | Inside compile? | counters: quad panels, cut calls | quad 776,786 panels × 0.589 µs = 75% of compile; cut 774,516 × 0.197 µs = 25%; ~70 panels + ~70 cuts per bound-orbit compile (EDGE band walk emits ≥1 panel/band; eccentric orbits ⇒ many bands) | probe |
| 1 | u128/u128 software divisions dominate the node | `fast_quad`: 4 divisions → guarded `div_word` (bit-identical by contract) | 91.7–91.9 vs 85–91 baseline: 0% (quad_avg 0.580 vs 0.589 µs); digests identical | **reverted** (falsified: `__udivti3` is not the kernel; a ~30% compile win would have shown as ~70 µs median) |

Stop condition: hit — falsified the only arithmetic hypothesis reachable in the window;
the remaining cost is panel COUNT (structure of `append`/EDGE bands), not per-panel arithmetic.
Three-consecutive-<10% rule: R1 = 0% ⇒ stop (no further rounds fit the window anyway).

Held-out (pristine build, after revert): tuned 84.9 µs / replay `14d14cd4…` (= baseline);
rtf 1000: 49.0 median, p99 390, replay `2007b2b2…`; seed 7: 72.5 median, p99 380, replay `8b1a5c20…`.
p99 ≈ 390 µs on every config = one Passage compile (~374 µs measured), config-independent.

Tree restored to pristine (patch empty); the probe instrument is `evidence/probe-and-hdiv.diff`.
