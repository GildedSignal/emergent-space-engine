# Autoresearch log — artifact `crates/encounters`, metric: setup ns per candidate pair (ns per event)

Machine: Linux 8 vCPU shared runner, load 7.6 during final A/B (another run's 5 × enc3.py);
all final numbers are A/B alternated under the same load, min of 3.

Baseline (committed code, same load): setup 9 452 ns/pair, run(1000 orbits) 10 041 ns/pair,
20.26 f-call evals/pair = 40.5 Kepler solves, n = 10 000 belt.

| # | Hypothesis | Change | Metric (setup ns/pair) | Kept? |
|---|---|---|---|---|
| 0 | where do evals go? | instrument d_of_s / numeric_window | 87% of setup evals in d_of_s's fixed 33-sample arc scan; 66 716 window calls for 1 547 Wide sections; 54% of calls have d < 16 rho (geometric tail of conservative advancement) | — |
| 1 | j's arc states don't depend on s; recomputing them per advancement step is pure waste | build j's 33-state tau-grid once per numeric_window, pass to d_of_s | 8 783 -> 6 627 (instr. build) | kept |
| 1b | the scan never uses the relative acceleration rel_of computes (2 x powf(1.5)) | rel_rv (dr, dv only) in the scan; refine keeps full state (Newton needs acc) | no measurable further gain alone, strictly less work per sample | kept |
| 2 | local Lipschitz constant (i's speed over its actual anomaly range) cuts the advancement tail | not run (time); the d-histogram says the tail (54% of calls below 16 rho) is where it would act | — | open |

Stop condition: not reached by three <10% rounds (1b was the only <10% round); the 60-minute
window ended the loop.

Final (A/B, min of 3, n = 10 000): setup 9 452 -> 6 636 ns/pair (**1.43x**), run(1000 orbits)
10 041 -> 7 392 ns/pair (**1.36x**), Kepler solves/pair 40.5 -> ~21. Kick re-certification:
13 770 -> 8 294 us/kick at eps = 1e-5 (**1.66x**), 14 699 -> 8 303 at 1e-3 (**1.77x**);
unchanged at eps = 1e-9; slack_skippable_fraction bit-identical at every eps.

The one idea that carried most of the gain: **j's arc states are s-invariant — hoist them out
of the s-march.** The advancement walks s (the phase offset); only i moves.
