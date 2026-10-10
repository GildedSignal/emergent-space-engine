# log.md — autoresearch loop on crates/encounters

Metric: setup_ns_per_pair (`scale n 10000` = σ 0.01 and `scale sigma 0.001`),
medians of 3, interleaved A/B when the shared box drifted (load 1.5 → 4.8).
Gates: verify a|b|c|long (and held-out d at the end) missed:0 false:0.

| # | hypothesis | change | metric (σ0.01 / σ1e-3 ns per pair) | verdict |
|---|---|---|---|---|
| 0 | baseline | — | 9165.8 / 35592.9 (evals 20.26 / 120.73); kick 7188.6 µs | — |
| 1 | powf(1.5) is a slow libm call in the eval path (2/eval) | r³ = r²·√r in rel_of, cross_window, rel | 7894.0 / 30692.9 (−13.9% / −13.8%), evals unchanged, gates green | **kept** |
| 2 | Kepler Newton polishes 3 ulps below any window margin | tolerance 1e-15 → 1e-12 | interleaved A/B: 8431–8842 → 7375–8443 (−8%) | **kept** |
| 3 | the inner arc scan (k=32) oversamples a ~2-extremum function | k=32 → 12 in d_of_s | 4987 / 16701 (**1.84× / 2.13×** cumulative), evals 9.59 / 59.29, all 11 verify belts missed:0 | **kept** |
| 4 | arc-local Lipschitz (helps e ≥ 0.1 belts only) | not run (time); predicted ~1× on tuned specs | — | skipped |
| 5 | the slack skin: skip re-certification of silent pairs whose stored budget covers the kick's drift | kick(): skip iff proposals==0 ∧ budget > 2·rel_dt ∧ Binet shift < 0.5·cone margin; build the skip set only if some budget covers the drift | µs/kick vs same binary without skin: ε1e-9 4583.8→914.8 (**5.0×**), ε1e-7 4644.8→2416.9 (1.9×), ε1e-5 1.06×, ε1e-3 1.006×; **skin_violations 0 on the whole ladder** (the pure phase rule at 1.5× had 5 at ε1e-3) | **kept** |

Stop: not three sub-10% rounds (13.9, 8, 37, 500/90%); stopped for the window,
with the ladder measured. Held-out (run once): verify d 3/3 belts missed:0
false:0 dup:0 (e up to 0.2, a 0.5–3, n=3000); setup σ0.003 13779.0→7719.5
(1.79×), n30000 6102.9→4363.2 (1.40×); gains track the eval ratio (no overfit).

The one idea that carried most of the gain: the Wide windows' cost is samples ×
cost-per-sample; halving an oversampled inner scan (R3) and making each sample
cheap (R1+R2) compound with skipping whole certificates (R5).
