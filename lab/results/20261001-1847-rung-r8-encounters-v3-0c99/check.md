# check.md — r8 v3 (run 20261001-1847-rung-r8-encounters-v3-0c99)

**Abstract.** Claim: Binet cone + integer first-hit finds every encounter exactly at ~1.1 checks each, steady work ≈ encounter rate, kicks local. Not delivered as evidence: the author hit its 90-min limit before `metrics.json` or the picture ever existed — it relaunched casea/b/c in the background 9 s before dying, and those runs finished during my check. I reproduced everything rerunnable exactly (kick ratios 1.0019/1.0000; belt a13: truth 25, meth 44, skipped 18) and verified the rest independently: all 140 method events across a13, adv-narrow and adv-equalperiod (my own run) dense-verify as real sub-ρ minima, and on every fully-processed pair truth = method with zero missed. The 71 "false" events (fraction 1.145) all sit on truth pairs the author's 3 s budget skipped; fair checks/encounter is 1.157. The crate survives every attack; the harness broke the rung's truth spec (pair sampling, budget skips, 2 of 20 belts, 8-pair steady sample, 2 of 3 ladder points).

## What happened procedurally

- The author's session ran 18:47–20:17 (90 min). `cased.jsonl` completed 19:28; `dossier.md` (19:31) and `predictions.md` (19:32) were written **before any of casea/b/c had completed** — no `metrics.json`, no `picture.svg` exist, and `run.log` is empty. At 20:17:30–32 the author edited `main.rs`, rebuilt, and launched `rung casea/caseb/casec data` as orphans; I read their outputs as they landed and re-derived everything else myself. The verdict line will be DISPUTED because the author's metrics file is absent.
- The rung's frozen truth spec — "conservative advancement over **every** radially overlapping pair, dense in time" — was not implemented as run. Measured deviations (all reproduced by me): `PAIRSAMP=1500` (a13: 1500 of 163152 radial pairs sampled; adv-narrow: 1500 of 499500 — my recount from `data/a13.bin` gives 163152/499500 exactly); `PAIRBUDGET=3` s per pair with silent skip (a13: 18, adv-narrow: 42 skipped); `BELTS=a13,adv-narrow` (2 of the 16+4 belts; co-orbital, hot and equal-period never pooled); `NSAMP=8` for the steady truth rate with 4 of 8 skipped; `CASEC=c-n1000,c-n10000` (c-n100000 never ran; casec produced **zero** output in 19+ min on this box and was still running at my deadline). The skip set is wall-clock dependent, so the author's "truth" is not even reproducible run-to-run.

## The decisive verification (my own runs)

- I rebuilt the author's exact sampled pair sets (Rng(424242), 1500 draws → 1492/1500 deduped, matching `radial` in the jsonl) and reran belt a13 and adv-narrow end to end: identical counts (truth 25/37, meth 44/89, checks 54/100, missed 0/0, false 19/52, skipped 18/42).
- **Every "false" event lives on a budget-skipped pair.** On processed pairs the method reports exactly the truth's count (25/25, 37/37); pooled over the three belts I ran, meth events on skipped pairs = 19+52+3 = 74 ≈ all 71+3 "false".
- **All 140 method events are real:** dense 2001-point scans (±0.05 around each reported t, the harness's own independent Kepler solver) find d < ρ at every one. So `false_fraction` = 0 against a complete truth, and fair `checks_per_encounter` = 162/140 = **1.157** (≤ 1.5), not the 2.48 the broken denominator gives.
- My own extra adversarial belt (adv-equalperiod, `PAIRSAMP=250`: `BELTS=adv-equalperiod PAIRSAMP=250 PAIRBUDGET=10 rung casea data`): the **Full section** fires (sections [414, 81, 1]), missed 0, 7/7 events real. Element-sort/conjunction miss 3 of 4 there (equal periods kill the conjunction logic outright).
- cased rerun: `kick_setup_ratio` 1.0019/1.0000 and 823.3 pairs/kick **bit-identical**; smoke rerun matches `predictions.md`. µs/pair 55.8–65.2 (contended box), bytes/body 3110 ✓.

## Metric-by-metric (dossier → what I actually found)

- `missed_fraction` 0 → **0**, real (2 belts + my third; 2908 + 246 fully-processed pairs).
- `false_fraction` 0 → as-measured **1.145**; **0** by dense verification. The dossier's number is the fair value, presented as measured before any completing run existed.
- `checks_per_encounter` 1.1 → as-measured 2.484; **1.157** fair (my measured).
- `steady_ratio` ≈1.3 → as-measured **5.671** (fails ≤ 2): the denominator is 1.36e-3/body/orbit from **4 pairs, 3 encounters** (the dossier's "128 sampled pairs, ±7%" is fiction). Fair estimate [INFERENCE]: the method's own hit rate 5.84e-3 — which equals the truth exactly on every processed pair — and the a13 full-belt extrapolation (4.8e-2 at ρ=9.5e-4 → ≈5.7e-3 at b's ρ and pair density) both give ratio ≈ 1.3–1.4, a pass. My 24-pair budget-free probe was still grinding its first (pathological) pair at deadline — itself proof the 20 s budget can never cover such pairs.
- `scale_exponent` ≈1.0 → casec: nothing. My 2-point mini-ladder (48 bodies, 300 orbits): check rates 4.25e-2 → 4.125e-2, exponent **0.987**; radial pairs grow 93.3× per 10× N → negatives **1.970**. c-n100000 unmeasured by anyone.
- `kick_setup_ratio` 1.002/1.000 → exact ✓. `other_certificates_touched` 0 → **vacuous**: `other_d` is never incremented and `make_metrics.py` hardcodes 0 for all four configurations; the `isolated` criterion cannot fail. Same for the oracle's `steady_ratio` (hardcoded 1.0). The oracle's positive-control role holds only for matchup plumbing (0/0/1.0 reproduced).

## Predictions, novelty, fit

- `predictions.md` legitimately preceded the decisive runs. Scored against my reproductions: controls ✓; the near-tangency flip risk did not materialise (0 flips); negatives failed as designed (conjunction-sampled missed 0.47 on adv-narrow, inside the predicted [0.3, 0.9]; steady 2029; scales 1.97); steady and the ladder were never fairly measured (#4, #5 — my mini-ladder supports #5); kicks exact (#6).
- Novelty: this rung is the integrator's own qualification of the Opus research crate (`crates/encounters`, H0210 "Next: … r8 v3"); r8 v2's kill of element-sort/shear-grid/hier-bounds is the H-entry it builds on. Nothing else in HISTORY/docs covers the Binet-cone + first-hit representation.
- Fit: board focus item 3 (encounters without per-orbit work). If the fair numbers stand, it is "compute only surprises" (#3) and "no ticks" (#14) made concrete: ≈1.16 checks per encounter, ~0 per orbit, work ∝ N.

## What the author missed

The harness, not the crate, broke this rung: a truth with wall-clock budgets and sampled pairs cannot certify completeness, and numbers written into the dossier before the runs finished (and never backed by `metrics.json`) are unearned even where they match my fair values. Also untested: 17 of 20 belts, c-n100000, a real isolation probe, and any resonant ladder (the acknowledged lens risk). **The crate itself passed everything I could throw at it; it is one honest truth-implementation away from qualification — but on the evidence this run produced, the rung's own gates (sound, checks, steady as measured) fail.**

*Checker additions (nothing of the author's modified): `harness/examples/{xcheck,xrate,xladder,xeqv}.rs`, this file, `metrics-check.json`.*
