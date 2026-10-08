# Autoresearch log — artifact: `xtask galaxy --bench` (the billion-ship readout), metric: ns per sample

Machine: shared GitHub Actions runner, 8 vCPU i7-4790 (4 cores/8 threads), 15 GB, Linux 6.8.0.
perf blocked (perf_event_paranoid=4) ⇒ attribution by differential timing. Unpaced 60–100-frame runs drift ±15% with co-tenants, so all keep/revert calls below use paired medians where marked (P), single-shot otherwise.

| # | Hypothesis | Change | Metric (far, ns/sample) | Verdict |
|---|---|---|---|---|
| 0 | baseline | — | 17.4–18.8 (5 reps, median 18.5) | reference |
| diag | cost is cache-bound on the plane (2 MB/thread) | render 480×270 / 960×540 / 1920×1080 | 22.4 / 17.4 / 16.5 | flat ⇒ **not** plane-cache-bound; compute/overhead-bound |
| diag2 | splat dominates the frame | split plan/splat/tone in bench JSON | far: 0.35 / 29.75 / 1.16 ms | splat = 94% of frame; loop targets splat |
| 1 | u64 div+mod in `locate` is the hot op (~30 c) | exact reciprocal division (round-down magic, 1 correction) | first build **wrong** (magic numerator bug: `p<<l/p = 2^l`), gates caught it; fixed + differential test over real periods (610k Python cases, 0 bad; Rust test 0 bad); re-measured 18.5 median (P) | **kept** (exact, no slower; removes a 30-cycle op that will matter once memory stalls shrink) |
| 2 | f64 projection with 2 upcasts per splat costs | f32 projection (error 2e-3 M ≪ 0.81 M/px deepest zoom) | 20.2 median single-window (looked worse; machine noisier) | **undecided — decided by paired A/B** |
| 3 | ln over all pixels dominates tone | (not run: tone is 4% of frame) | — | skipped, off-bottleneck |

Stop rule: after rounds 1–2 the tuned-case metric moved < 10% for two consecutive rounds ⇒ stop, run held-out set (predictions.md), write dossier.

## Held-out result (after predictions.md)
Paired medians, candidate/base: far 0.888, seed7 0.991, mid 0.942, deep 0.866, far-40f 0.932, threads1 0.933, deep-40f 1.014 → median 0.932. Round 2 (f32) verdict flips to **kept** (paired, no regression, part of the ~7%). Round 1 (reciprocal division) **kept**: exact (differential test), free, deletes a 30-cycle op.
