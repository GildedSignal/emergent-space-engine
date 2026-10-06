Working...
`check2.md` written. Verdict: **silver**.

What I did (blind, ~25 min):

- **Reproduced**: rebuilt `bench.c`, re-ran the decisive cells on a busier box (load 2.0 vs author's 1.5) — gather-L4 8T 38.6e6 vs 47.4e6 ev/s, chase-L4 14.8e6 vs 17.4e6, gather/chase 2.61× vs 2.72×, stream L1 8T 22.5 vs 21.8 GB/s. Every budget verdict unchanged; `budget.py` regenerates `budget.json` byte-identically. All imported inputs verified in-repo: 29 µs/kick (HANDOFF:42), 190-core Fermi (HANDOFF:99), 83% view gather (HANDOFF:41), 64/orbit (`step.rs:6,66`), 0.3/orbit (H0190).
- **Adversarial**: (1) 1 GiB footprint — all-core rates hold within 5%, no TLB cliff; (2) found a real artifact: raw stream rows L≥2 imply 25–41 GB/s, above the ~22 GB/s DDR3 ceiling their own L1 rows pin (cross-thread LLC co-travel on the shared buffer); the model's self-cap at 21.8 GB/s contains it, but "confirms the counting is honest" overstates; (3) the dossier's "8.2×" resident/DRAM ratio isn't derivable from raw.jsonl (it gives 10.7×; my rerun 8.6×) — conclusion unchanged, number wrong.
- **Predictions**: pre-dated the decisive matrix (mtimes); 6/8 held, failures honestly reported; noted that prediction 8 is true by formula construction, and prediction 3 was graded on the 8T cell (single-core is 0.70×, not half).
- **Novelty**: direction already in HISTORY ("random gathers of body data cost more than the arithmetic", ladder v6); new is the controlled quantification and the compute/memory/cadence factorization with the ~15 µs crossover.

Silver, not gold: it prices the levers (a zero-cost rule and table) but moves no bottleneck 10×, deletes nothing, and the L=4 cold-lines-per-kick assumption is unmeasured on the real path. The gold experiment: instrument the real kick path to count cold lines per kick — it either grounds the rule or re-prices the layout lever.
