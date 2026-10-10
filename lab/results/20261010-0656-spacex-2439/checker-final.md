Working...
**Grade: gold** — written to `lab/results/20261010-0656-spacex-2439/check.md`. Tree restored to pristine; only `check.md` added.

**What I did:**
- **Reproduced from scratch**: applied `work/patch.diff` to a clean tree at a838a28, built release xtask, ran the full matrix. Engine p50 0.054→2.81 ms (71→6,203 bodies) vs author's 0.058→2.67, slope 0.45 vs 0.43 µs/body/frame, events/s constant 453–454 throughout, `walked/frame` = N−60…124 at every size.
- **Bit-identical digests** across four configurations, my build vs the author's stored runs, plus rekey↔norekey neutrality at 859 and 6,203, and patched-vs-pristine-binary equality on the default scene (I built both binaries).
- **Adversarial**: 9,888 quiet bodies → engine p50 4.70 ms ≈ the entire 5 ms engine budget (the claimed ~10⁴ wall is real); rtf 30 independence confirmed; per-band slopes rise with N, so the 0.43 µs extrapolation to 10⁹ is optimistic, not alarmist.
- **Predictions**: mtime order confirms they preceded the held-out matrix; the claim-level predictions held, the rekey-deletion hypothesis failed and the pre-registered kill criterion fired honestly — the acquittal reproduces.
- **Novelty**: no HISTORY entry measures the frame loop's own per-frame O(N) term (H0210/H0213/H0215 own gather, readouts, kicks); the finding kills the premise that the frame budget buys events (P14, plane.md foundation 7).

**Named misses** (in check.md): "p99 does not grow" overstated (1.9→8.2 ms), mid-scale prediction intervals missed low from convexity, the defer-path attribution rests on the counter rather than a built fix, and the gather (24 µs/body, 88% of a 6,203-body frame) is the larger per-frame wall — correctly left to `b-readout-cost`.
