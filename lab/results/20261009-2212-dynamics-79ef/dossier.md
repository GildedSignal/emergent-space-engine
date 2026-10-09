# Dossier — 20261009-2212-dynamics-79ef (dynamics lens)

## Claim

A stirred belt's close-encounter rate is **not** a constant set by orbital geometry: it decays as a smooth power law in belt age (λ ∝ t^-0.25, e_rms ∝ t^0.4, collapse λ = 0.345·e^-0.215 across all stirred runs) because secular stirring thickens the belt; vertical thickness (inclination) is a first-order variable (a pre-thickened belt runs ×15–20 fewer encounters), and the event stream, once heterogeneity is removed, is genuinely but only mildly self-exciting (within-body branching b ≈ 0.35, subcritical) — so the allocator may schedule encounters from a precomputed, slowly-decaying rate with bounded per-body tails, and no avalanche gate is needed.

## Bottleneck

Board #4 (smoothness/allocator: "least-slack scheduling fed by surprise rates") and the top scaling risk #6 (candidate work must track *real* encounters): what the surprise-rate process of a belt actually is. Expected gain: delete reactive rate estimation (the rate is generator-computable from age), and size per-body p99 budgets from measured overdispersion instead of worst-case.

## Evidence (machine: Linux x86, 8 vCPU shared; load 0.8–2.4; all runs single-threaded, <100 MB)

Instrument: `work/belt.c` — direct O(N²) leapfrog, fixed primary M=1, N=600 equal-mass belt bodies, encounter = d < 1 mutual Hill radius (R_H = ((2m)/3)^{1/3}·(r_i+r_j)/2), hysteresis release at 1.5×, one event per approach; per-event Δ(a,e) both bodies; per-orbit e_rms, bound fraction, |dE/E|. Reproduce (each ≤ 2 min):

```
cd lab/results/20261009-2212-dynamics-79ef/work
gcc -O2 -march=native -o belt belt.c -lm
./belt 600 1 1e-7 0.05 1e-4 0.02 150 1 1.5 r1_out.tsv r1_ev.tsv   # baseline cold, seed 1
./belt 600 1 1e-7 0.05 0.15 0.02 150 1 1.5 hot_out.tsv hot_ev.tsv  # hot start e0=0.15 (i0=e0/2)
python3 corrected.py    # corrected statistics (the numbers quoted below: exponents, collapse, within-body b) -> corrected.json
```
Validation: r2b (dt=0.01): 48,459 events vs r2's 48,404 (+0.1%), e_rms within 2% — statistics dt-independent; hotb (dt=0.005): λ 0.032→0.040; w30b (dt=0.005): λ(50–100) 0.675→0.817 — high-e runs under-detect fast crossings by ~20% at dt=0.02, far smaller than the ×15 dilution gap; the collapse constant for high-e bins carries that ≤20% bias.

Primary runs (T=150 orbits, dt=0.02): seeds 1–3 cold (m=1e-7, width 0.05), hot (e0=0.15), width 0.10, m=8e-7, width 0.30 (T=200).

| run | λ per body/orbit (t≈10→150) | λ ∝ t^ | e_rms ∝ t^ | e_rms end |
|---|---|---|---|---|
| r1/r2/r3 (cold, seeds 1–3) | 0.81 → 0.46 | −0.21/−0.26/−0.21 | +0.38/+0.40/+0.43 | 0.095/0.101/0.107 |
| hot (e0=0.15, i0=0.075) | 0.032 → 0.032 flat | ~0 | +0.14 | 0.281 |
| w10 (width×2) | 1.06 → 0.54 | −0.30 | +0.39 | 0.133 |
| m8 (R_H×2) | 0.76 → 0.45 | −0.17 | +0.48 | 0.249 |
| w30 (width×6, T=200) | 1.22 → 0.59 | −0.32 | +0.73 | 0.285 |

- **Collapse**: all non-hot (e_rms, λ) 5-orbit bins, e ∈ [0.03, 0.35], N, width, m varied: λ = 0.345·e^-0.215, residuals within ±0.11 dex (r1–r3, w10, m8, w30). Hot sits −1.19 dex below ⇒ inclination/thickness dilution ≈ ×15. No phase transition, no criticality, no e fixed point in 150–200 orbits.
- **Branching (corrected estimator)**: within-body conditional excess b(τ=1 orbit) = 0.344/0.365/0.355 (seeds 1–3); control (per-body Poisson resample at each body's own rate) = −0.006±0.005. Subcritical. Cluster sizes (gap 0.5 orbit) geometric, ratio 0.26–0.27, max cluster 46–62 in ~50k events.
- **Heterogeneity**: per-body rates p99/median ≈ 2.0, max/median 2.3–2.4.
- **Frame tails (r1, orbits 50–150)**: global events/orbit median 294, p99 362 (+23%); per-body 10-orbit counts mean 9.9, p99 32, max 48 vs Poisson-same-mean p99 18, max 24 ⇒ real tail ≈ 1.8× Poisson.
- **Validity**: |dE/E| ≤ 1.2e-3 cold runs (r2/r3 marginal 1.1–1.2e-3 — validated dt-independent by r2b); hot/m8/w30 drift 4e-3–8e-2 (deep fast encounters unresolved at dt=0.02; hotb at dt=0.005 moves λ by +25%, not ×15; disclosed limitation).

## Predictions (predictions.md written before these runs)

P1 λ_stat 0.68±0.05 → **FAIL** (0.47–0.50; rate is not stationary); e exponent 0.2–0.5 → **held** (0.33–0.49); no e fixed point → **held**. P2 hot → same plateau → **FAIL** (×20 lower; found the missing variable: thickness). P3 width×2 → λ/2 → **FAIL** (0.55 ≈ unchanged). P4 m×8 → λ∈[1.2,2.0] → **FAIL** (0.45; faster stirring self-dilutes). P5 → **FAIL** (0.60 vs 0.11). P6 b<0.2 → **FAIL** (0.35 genuine); the pre-registered shuffle-gap control fired (b_shuf ≈ b), correctly VOIDing the naive estimator, which conflated population heterogeneity (λ_i spread 2×) with temporal clustering. P7 p99/median<3.5 → held numerically (2.9) but the right comparison is 1.8× Poisson.

Five of seven quantitative predictions failed, and the failures are the result: no static geometric rate exists; age and thickness set it.

## What would make it wrong

- N=600 only: relaxation scaling not tested (2-body relaxation negligible here, but the collapse's width exponent is confounded: wider belts stir to higher e, partly self-compensating; a clean test fixes stirring history independently of width).
- f=1 R_H threshold sets the constant 0.345, not (verified) the exponents; one f=0.5 run is the named next experiment.
- Inclination measured only indirectly (hot offset); i(t) not logged — the dilution law λ(i) is inferred, not fitted.
- Fixed primary absorbs momentum; deep encounters under-resolved on hot/w30 (dE up to 8e-2) — event *streams* validated dt-independent where compared, but per-event Δe magnitudes there are approximate.

## Cost of adopting, and fit with PRINCIPLES

Adoption is a cost-model rule, not code: the encounters design's premise "cost follows the candidate set" (r8 v2) is right for *discovery* but the per-candidate *encounter probability* is dilution-weighted: a thick/old belt yields ×10–20 fewer real encounters per candidate pair than a cold flat one at the same (N, m, width). Belt gates (B18b) must pin thickness or their cost predictions do not transfer. Allocator: schedule from precomputed λ(age, thickness); per-body budget ≈ 2× heterogeneity × 1.8× overdispersion; no avalanche gate. Quotes: "Compute only surprises. Cost follows change and entropy" (#3); "the simulation tells us what's next not us" (#22); "i care about the p95/99 results" (#12).

## The lens

Dynamics-lens blind spots faced: the first branching estimator measured population spread, not clustering — caught by my own pre-registered control (same lesson as the 5 October memo artifact: check the estimator measures the claimed event). Remaining blind spot: 150–200 orbits may still be a transient of a slower saturation; and long-run λ(t) at fixed N eventually feels the a-diffusion widening the belt (unmeasured).

## Verdict sought

Silver-to-gold: a measured, dt-validated law (λ·e^0.215 ≈ const, b ≈ 0.35 subcritical, tails 1.8× Poisson) with direct allocator and gate consequences; held-out predictions mostly failed *against* my priors, which is the information. One experiment away from gold: the f=0.5 threshold run plus direct i(t) logging to turn the dilution offset into a fitted λ(e, i) law.
