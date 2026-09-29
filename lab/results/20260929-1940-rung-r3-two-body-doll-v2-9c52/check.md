# check.md — rung r3 v2, run 20260929-1940-rung-r3-two-body-doll-v2-9c52

## Abstract

The author hit the 60-minute wall mid-run: **no `metrics.json`, no `dossier.md`, no picture**; the 5th flyby was killed buffered (4 of 192 done), and `run.log` is empty. What exists reproduces exactly: the 1024-seed binary sweep is bit-identical to my rerun, and the ported oracle (`eih_invariants`, `damour_deruelle`, `schwarzschild_from_invariants`, Darwin quadrature) matches `gr_oracle_extended.rs` verbatim and my two independent integrations to ~1e-8. Outcomes: the v2 truncation exclusion leaves **0 judged precession seeds** (min estimate 0.0079 > 0.005), so `judged` fails for every config; eob-doll passes period (652/652) and misses ν by 7 seeds (690/697 = 0.98996 < 0.99); assists fail by 22–10,000% on every measured seed (criterion requires 64/64). The transfer reference is unconverged (half-step 10.9 vs the frozen 1e-9). Expected verdict: DISPUTED (author metrics missing).

## Reasons

**1. State of the author's run.** `author-final.md` still says "Working...". Files present: sources (`r3.c`, `metrics.py`, `seeds.py`), data (`bin.csv`, `seeds.txt`, `flybys.txt`, `tr_law{0,1,2}.txt`, `fb_law0.txt` = 4 rows), `predictions.md`. Absent: `metrics.json`, `dossier.md`, the picture. `work/patch.diff` is empty (all work stayed in the results folder — legal). The rung's own output contract is therefore unmet; this check reproduces what exists.

**2. Reproduction (no number differed where the author has one).**
- Seeds: `seeds.py` regenerates `seeds.txt` and `flybys.txt` byte-identically (sampler matches the frozen spec).
- Binaries: `./r3 bin < seeds.txt` (current build) reproduces the author's `bin.csv` **identically in all 1024 rows × 17 columns**.
- Flyby law-0 rows 1–4: my rerun matches to ~1e-6 relative (adaptive-step ordering noise).
- Transfer: not re-run to completion (the law-0 reference alone hits the 3e7-step cap; laws 1/2 took ~0.5e6 ref steps). I recomputed all summary metrics from the author's stdout captures with the author's own formulas.

**3. Independent verification of the law and oracle.**
- The four oracle functions are line-by-line ports of `gr_oracle_extended.rs` (checked side by side); `acc_1pn` matches the Rust `eih_ode` acceleration.
- My own 1PN harmonic ODE integration from the author's periastron initial conditions agrees with `damour_deruelle` to 2.2e-2/8.5e-2/5.9e-3 at p = 200/37.5/900 — the O(1/p) structural gap the xtask's own gate encodes (`advance_diff < COEFF/p`), so the DD formula behaves exactly as the reference implementation expects.
- `doll_eob`'s EOB map is the exact inversion of the rung's `E_real = M√(1+2ν(E_eff−1))` (E_test = 1+((1+νε)²−1)/2ν keeps the quadratic term; period scale 1+νε). I verified the Schwarzschild chain (EIH invariants → cubic turning points → geodesic) with two independent quadratures (u-space energy integral; midpoint, n=1e5) agreeing with the C's Darwin-χ `refine` to 3e-8 — my third path (a u(φ) RK4) initially disagreed at 2e-4 and turned out to be my own integrator's bug, outvoted by the other two.
- Truncation-estimate family: measured (Aeob0−Aor)/Aor·p median 7.99 vs claimed 7.5+e² (median 7.59) — the estimate is honest to ~5%, far from the ~35% error needed to un-empty the precession set.

**4. Criterion outcomes (my numbers, `metrics-check.json`).**
- `judged`: **0** — every seed's prec estimate ≥ 0.0079 > 0.005. The v2 exclusion (added to fix r3 v1's contamination) makes the prec criterion unjudgeable on p ∈ [20,1000] M. This is a **rung-design defect, not law evidence**: it fails all three configs identically. The author predicted it (predictions #1) and it reproduces bit-identically.
- `prec`: 0/0 judged → 0.0 for all (vacuous).
- `period`: eob 652/652 = 1.0 (pass); test 4/652; newton 2/652 (negatives behave).
- `nu`: eob **690/697 = 0.98996 < 0.99** — a real, marginal miss of the 10%-of-ν-term tolerance; test/newton 0 (as designed).
- `handoff exponent`: law 0 fit over 425 handoffs = 0.0000 with constant |E_doll−E_ref| = 3.337e-2 (a systematic SOI offset, not growth). Laws 1/2 collapsed to **1 handoff each** (chaotic divergence from law 0 at the 1e-8 law difference), so their 0.0 is the author's <3-points fallback — vacuous, reported as such.
- `assist`: 0.0. The author completed 4/64 law-0 flybys (all NOAIM); all fail by 115%–10,500%. I reproduced law-0 seed 1 (match) and ran the frozen sequence's first seeds for laws 1/2: eob fails seed 1 (b=18.6 R⊕) by 21.9%, seed 3 by 20.6×, seed 4 by ~105×; test-mass fails seeds 1 and 4. Since 0.99 of 64 requires 64/64, **one failing seed of the frozen sequence already determines FAIL**; the exact 64-seed fraction was not measured (each bisection case ran > 4 min; 192 cases exceed both budgets). Denominators: eob 0/3 distinct seeds (+1 half-step check rerun), test 0/2, newton 0/4 (author) + 2 reruns; stragglers (b=14.59, all laws) were still integrating at my wall and were killed.
- `cost`: events/orbit 6.6759 (law 0) and 0.0157 (laws 1/2) — all pass 512, but the metric is degenerate for laws 1/2.

**5. Spec deviations by the author (beyond the missing deliverables).**
- Transfer geometry: the rung freezes a figure-eight transfer with 100 SOI crossings; the author ran a co-orbital (h=−0.006) giving 425 crossings for law 0 and 1 for laws 1/2. A figure-eight branch exists in `r3.c` but was not used in the final runs.
- Reference quality: the rung requires half-step reruns agreeing to 1e-9. Law 0's reference hit the 3×10⁷ step cap and reports halfstep **1.088e+01**; the flyby reference's halfstep_v is 1.16e-4 (0.32% of |Δv_ref|) — coarser than the bar, though two orders below the measured assist failures, which stand.
- Flybys ran NOAIM (realized b within ~4% of nominal) instead of the bisection (promised <1%, unaffordable: one case > 4 min).
- `metrics.py` maps `tr_law0/1/2` to eob/test/newton, but `r3.c`'s LAW is **0 = newton, 1 = eob, 2 = test-mass** — every transfer/flyby metric would have been attributed to the wrong config. The bug never materialized (no metrics.json was written); my metrics-check.json uses the correct mapping.
- Doll final energies: all three laws end at E_helio ≈ +0.4966 from −0.4970 — the SOI doll does not conserve heliocentric energy across handoffs (the constant 3.3e-2 offset, sign-flipped endgame). Consistent with the author's own architecture finding (prediction #9: pre-SOI pull too coarse for R⊕-scale encounters).

**6. Predictions.** Written 4 minutes *after* `bin.csv`'s mtime, so the header's "before reading bin.csv" is unsupported by file times (the author may mean before *analyzing*; unverifiable — `run.log` empty, omp output lost). Content: #1 held exactly (judged 0), #2 held (652 seeds, period 1.0), #3 near-miss (0.98996 vs "≈1.0"), #4/#5 held (negatives fail), #7 half-held (law-0 exponent 0.0; laws 1/2 degenerate — the 425-crossing stability did not survive 1e-8 perturbations, which the prediction did not anticipate), #9 held dramatically (assist ≈ 0 for eob *and* negatives — an architecture finding, not a config difference), #10 held for law 0 (6.68).

**7. Novelty.** First implementation of the EOB two-body doll (board bottleneck 1's open question). No prior H-entry covers it; r3 v1 was voided for criterion contamination before any verdict. The two new rung-level findings — the v2 exclusion empties the precession set at p ≤ 1000 M, and SOI handoffs fail planetary encounters by two orders of magnitude — are new and actionable.

**8. What would decide this rung.** Not a re-run of the same file: (a) the integrator must either widen the p-window (e.g. p up to ~10⁴ M where (7.5+e²)/p < 0.005) or drop the prec criterion, else `judged ≥ 64` is unsatisfiable by construction; (b) the transfer needs a non-chaotic geometry where the 1e-9 reference bar is attainable and all laws produce ~100 crossings; (c) the assist criterion needs either a stitched pre-SOI patch or an explicit admission that SOI-level handoffs cannot serve R⊕-scale encounters.

**9. What the author missed.** No time-boxing of the flyby sweep (the 60-min wall was hit inside case 5 of 192 — the bisection cost was measurable and predictable after case 1); no partial metrics.json/dossier written before the wall; the law-permutation bug in metrics.py went unnoticed; the reference-quality failures (halfstep 10.9, 3e7-step cap) are visible in the author's own SUMMARY lines but were not flagged; the ν near-miss (690/697) was never examined.
