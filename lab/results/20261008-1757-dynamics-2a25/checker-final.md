Working...
Check complete. **Grade: silver** — written to `lab/results/20261008-1757-dynamics-2a25/check.md`; tree restored (only `check.md` added to the run folder).

**What I did:**

- **Reproduced everything** from the patch in a clean tree (13 runs, 19 s total): 8/8 identical digests `9b9a5183…` at unlimited×2 and budgets 4–64; b2/b3 diverge at slope 0.64–0.79; b4 max lag 351 frames, rtf 103.6; attractor 3.40/p99 27/max 51; spectrum 33% vs shuffled 5%; burst 10→13.5→30 with N, 1.6 at rtf 1000. `analyze.py` output matches `evidence.txt` except ±1–5 events in burn windows — exactly the disclosed input-clamp difference, digest unchanged. `predictions.md` (18:04:13) precedes all decisive CSVs.
- **Adversarial cases** (seed 3, 220 s horizon, N=192 with budget near its mean): the *law* (bifurcation at the sustained mean, bursts need no coverage, burns displace) survived everywhere — seed-3 budgets 6/8 are bit-identical to unlimited. But the *operating point* is single-seed: seed 3's late mean is 4.42 and rising; seed 7 drifts +3% at 2× horizon; and N=192 with budget 3 (1.3× its late mean) **diverges at frame 466** — killed by the 16-events/frame startup transient the dossier treats as scenery.
- **Novelty:** the digest-invariance half is prior art (H0210, H0213, and the shipped test `the_same_digest_at_every_budget_and_thread_count`); the demand-stream characterization and bifurcation point are new and on bottleneck #4.
- **Gold experiment named:** a tracking-mean bifurcation map (≥3 seeds × 2 member counts × 2 horizons, budget = α·running mean) — a fixed 1.2×-current-mean reading of this dossier fails within 8 s of game time at N=192.
