Working...
Second blind check complete — `check2.md` written, nothing else touched in the run folder.

**Grade: silver.**

**Reproduced exactly (timing-free, deterministic):**
- Byte-identical reruns: digests and all 12 integer fields for seeds 1/3/5 (seed 5 twice); kind annotation differs in exactly 1/60 000 frames, as disclosed; flat-vs-item digest control extended to a second seed (3) — holds.
- `analysis.py`/`addendum.py` regenerate both JSONs exactly from the author's data.
- Every decision number on the demand stream: max/p99.9 = 3.69 (A), 4.25 (hour); median-bench-misses-hour 4.5×/6.8×; window lottery 44×; Gaussian 11.1×/25.8×; rtf-16 thinning (2.61, P4 inversion confirmed); m-400 burst (p99.9 = 100, max 328). Held-out seeds 21–23: 4.33/3.36/2.21.
- Cost plateau α̂(1%) ≈ 1.0–1.4 on all 7 of my quiet-box runs.

**Not reproduced (my attack landed):** seed 1 resolves the identical item sequence every run, yet its tail tip swings 6 650→2 248 µs (p99.9 3 064→328) — the "no construction bound" 8× seed spread collapses to 2.1× (below P2's own registered 3× kill) and the ≥3 ms fleet-epoch census vanishes (0 items ≥ 2.25 ms in 360 k frames; player dominates at ≥500 µs). That leg is runner load, not engine work — the same shared-harness lesson as the 5 October memo artifact. Also: the demand stream's own construction bound ≈ members (48→48, 400→328) sits unremarked in the author's data.

**To gold:** one noise-robust tail experiment — thread-CPU time or deterministic work counts per item, controlled load, repeats, plus demand-max vs members — to pin construction ceiling vs engine-real spread. The adoption itself (one tail line + per-item bench logging) already stands on the reproduced demand stream.
