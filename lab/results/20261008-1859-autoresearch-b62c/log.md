# Autoresearch log — artifact `crates/encounters`, metric `setup_ns_per_pair` (scale n)

Behaviour constraint held fixed: `missed = 0`, `truth_outside_cone = 0` on every verify belt.
Tuned on `scale n 10000` + `verify a` only. Machine: shared 8-vCPU Linux, load 0.1–1.3.

| # | Hypothesis | Change | setup_ns_per_pair | Verdict |
|---|---|---|---|---|
| 0 | baseline | — | 9226 (evals/pair 20.3; wide 4266 ns = 46%, cross 3342 = 36%, q 668 = 7%, scan 118) | — |
| 1 | j's grid states don't depend on the shift s; and the caller only compares D against ρ·1.05 | cache j's 33 grid Kepler solves per numeric window; early-exit the τ-scan once the running min < stop (decision-identical) | 7490 (wide 2825) | **kept** (−19%; wide −34%) |
| 2 | census: 99% of Wide sections are merged arcs (near-identical orbits), not tangencies; merged ⇒ synodic ≥ ~4000 orbits ⇒ conjunctions are rare | merged arcs: window = cap (pre-narrowing superset), no numeric crawl | 2744 (wide 20 ns; evals 0.05) | **kept with a wound**: checks/hit 1.1→21.3, run_ns(1000 orbits) 8219→21003 |
| 2b | the merged check bracket is near-stationary (relative phase drifts 1.6e-3 rad/period) → one slow minimum | Wide check k=64→16 when bracket > 0.5 period | 3242 | kept (checks cheaper but count unchanged — window-driven) |
| 2c | merged encounter needs true longitudes to coincide: superset window from equation-of-centre + chord bounds, closed form, centred at s=0 | merged window = ±(2.1ρ/rmin + 2.2(e_i+e_j) + 2e-3)·1.2/n_i, clamped to cap | 3292 (checks/hit 6.1, run_ns 9041 < baseline 9982) | **kept** (verify a: 4/4 belts missed=0, false=0; method_s ≈ 0.5× baseline) |
| 3 | widen the analytic cross-window regime 0.2→0.5 rad | not built — census killed it first (only 14/1869 wide sections are cross arcs in [0.2, 0.5)) | — | killed by measurement before building |

Stopping: rounds 2b/2c each moved the headline metric < 10% (2b +18% noise-level, 2c −1.5%);
the remaining cross-path (3342→~2000 ns after 2c re-split) is trig/Kepler floor. Loop stopped at
2.8× (9226 → 3292/2744 measured twice; shared-machine noise ±15%).

The one idea that carried most of the gain: **the merged-arc certificate is free** — for
near-identical orbits the expensive numeric hull is replaceable by a closed-form superset because
the encounter's necessary angular condition is computable from the elements alone (equation of
centre bound), and conjunctions are so rare that the exact check pays almost nothing.

What would beat this local optimum (lens blind spot): the cross path (now ~60% of setup) is ~1.7 µs
per section of nearly pure trigonometry (10 `true_to_mean`, secant). The structural move is to
derive the two crossing sections' passage ticks from a per-body precomputed mean-longitude table
(one pass over each body's orbit shared by all its ~870 partners), turning per-pair setup into
per-body setup + O(1) lookups — an ~O(cone_per_body) → O(1) per pair change, not a constant factor.
