Working...
Check complete. Summary of the verification:

**Grade: silver** (`lab/results/20261008-0234-quant-2300/check.md` written; tree restored to clean, no commits).

**Reproduced from a clean tree:**
- All three replay digests match bit-for-bit (`72e9fda7…`/`8ee18ba4…`/`b981be81…`); applying `work/patch.diff` reproduces stage shares within 0.5 pp — rebind 79.3/86.1/88.2 % at 4/48/400 members, force 1.0–1.8 % — and instrumentation is digest-neutral, verified directly (patched vs unpatched digests identical).
- Capacity medians flat (leavers 82–92 µs across 100× members), mean grows 59→101 µs (tail lengthens, median doesn't), p99/median ≈ 4.1–5.3× — all as claimed. Struct sizes exact.

**Adversarial:** seed 42 holds (rebind 85.9 %); 1600 members × 20 s holds at 10,092 kicks (92.8 µs, 57 MB). Found one real gap: at the author's 6 s window, `--members 1600` silently replays the m400 kick set (identical digest) — the bench saturates, so the curve's 400 endpoint was a bench artifact, not a tested extreme.

**Predictions:** written 02:37:40, runs from 02:38:02 — precedence verified. P1/P2/P5 held, P3 half-held and honestly reported, P4 withdrawn (no PMU here either).

**Why not gold:** fully reproduced measurement that *locates* the 10× lever (refit timing, not the force law) but doesn't move it; the deferred refit is a certificate-guarded law change, not one-step adoptable, and the adjacent quick fix (kick memo) was already killed. Gold experiment: a deferred-refit bench variant — exact Δv accumulation across k kicks, one refit per k — measured against B13/B17.

**Author's misses:** bench saturation, "cadence <2% of the bill" conflating a multiplier with a share, v2 clock path at n=12 with a merged stage, unexplained p99 tail, and `1932f6c`'s 8% fit-arithmetic gain left uncited despite being supporting evidence.
