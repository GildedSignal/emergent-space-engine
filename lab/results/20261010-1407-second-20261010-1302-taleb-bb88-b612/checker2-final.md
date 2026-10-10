Working...
Check complete. `check2.md` written to the run folder; nothing else in `lab/results/…-b612/` was modified, no git operations.

**Grade: gold** — second blind checker, independently.

**What I did**

- **Reproduce**: fresh tree, the dossier's commands — full 38-run grid + 13-run B re-run: **907 stored fields, 0 diffs, bit-for-bit** (n_pairs, misses, cost_mean/max, required_k, tightness…). Pilot matches the predecessor branch `claude/lab-20261010-1302-taleb-bb88` exactly (18850 pairs / enc 12.5667 / rank 15). Recomputed both dossier tables from the stored JSONs with my own code — every number reproduces (√((1+e)/(1−e)) law 14.13 vs √199; Poisson-max 496 vs 464–473; 27.91M A-pairs / 8 W-misses; 523,994 B-pairs / 7 / 0).
- **Predictions**: the corrected-window addendum is provably pre-registered before the B re-run (mtimes 14:47 < 14:49 code < 14:52 output). Pre-grid registration isn't mtime-provable (append overwrote it) but six honestly-failed letters argue it. Held-out B30 held; addendum letters Z1′/CB′/MB′/TA′ held.
- **Attack**: e=0.95, 10× spreads, correlated ±e–w fleets (the author's named gap — W fails 141–184 there, W′ holds zero-miss, X term load-bearing), K=6000 truth — all held, cost matches 2W′n. The 4 real W-miss pairs verify the apoapsis mechanism on their faces. My e=0.995 kill attempt turned out **void**: the shared Kepler Newton solver diverges for e≳0.993 (proven by bisection: fake contacts), and the author's e≤0.99 grid is safely inside the convergence domain.
- **Novelty/goal fit**: no HISTORY or doc precedent for W′/X/sizing law; bb88's apsis keying was argued-only. The rule makes the build-queue co-orbital certificate valid at eccentricity (rank-4 drops up to 98%) at cost 1.003–1.017× contacts — adoptable in one step, no new state.

**Named misses** (in check2.md): the instrument's e-ceiling is unstated in the dossier; run.log phase times off by 5–8 min vs mtimes; B-table cost_max column is a cross-seed median; the "sort amortized to zero" claim holds only between kicks (the unmeasured T_reeval knob).
