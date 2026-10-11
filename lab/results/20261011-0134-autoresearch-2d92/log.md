# Loop log — 20261011-0134-autoresearch-2d92

Artifact: `EventCore` (`crates/lattice-event`), the plane's contact engine (Fermi-frame battles).
Metric: ns per fired event on `worlds::gas` (contact-dense regime), digests bit-identical.
Machine: GitHub Actions Linux, 8 vCPU i7-4790, shared; 3-rep means used for decisions
(single runs bounce ±10% here; the chronon reference, untouched, moved +5% between runs).

| # | Hypothesis | Change | Metric (gas 256/1024/4096, ns/fired) | Kept? |
|---|---|---|---|---|
| 0 | — | baseline (main, instrumented counters) | 3462 / 3629 / 4299 | — |
| 1 | The i128 visit predicates (`first_hit` in predict, `hit` in scan) dominate; an exact i64 path guarded by the GPU's own certificate (|d_c| ≤ 2²⁶, |w_c| ≤ 2¹⁶, reach ≤ 2²⁴) is bit-identical and cheaper | `law::hit64`/`first_hit64` + guarded call sites in predict/scan | 2930 / 3202 / 3822 (−12…−15%) | **kept** |
| 2 | The density probe keeps L₀ for uniform gas; smaller cells (CROWDED 2.0→0.5) cut visits per prediction | `CROWDED = 0.5` | 2900 / 3150 / 3513 — but cell moves identical (10046/41960): the probe never fired; differences are noise | reverted (no effect) |
| 3 | `first_hit`'s binary search is the hot core | profiled first (gprofng): binary search runs only on hitting pairs (~10% of calls); the None path was already single-mul (LLVM folds sext·sext). Remaining wall: visit loop 43%, `Calendar::down` 14%, step 12% | — | not pursued (no cheap exact win left inside 60 min) |

Stop rule: round 2 gained <10% (nothing), round 3's measured share says its ceiling is <10%;
two consecutive sub-10% rounds → stopped, wrote up.
