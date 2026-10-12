# Predictions — run 20261011-2306-dynamics-0b04 (dynamics lens)

Written before the decisive run. Decisive config (unless stated, all runs use it):

    python3 belt.py --mu 1e-3 --T 3000 --spf 24 --N 112 --e0 0.05 --amin 0.55 --amax 1.9 --seed 7 --tag m1m

Scene: circular restricted three-body (star + Jupiter-like at a=1), ships as massless
tubes in the star's doll, exact-Kepler drift + planet kicks (the design's own motion
path, in float). One sample per planet orbit; statistics over the second half.

Definitions. `revisit` = fraction of steady-state samples whose quantized (E,L) key was
seen earlier in the same half (the memo's hit rate, lagged). `churn` = distinct keys per
planet orbit (the compile-rate proxy). `lam_hat` = ln(max shadow separation / d0)/T,
unrenormalized: ~0 regular, = λ while unsaturated, = ln(0.5/d0)/T once saturated
(regime classifier only). `d_res` = min_{q≤15} |n_b/n_pl − p/q| from the mean a (the
engine's resonance detector). `msd_slope` = log-log slope of Var(Δa) over lags 8/32/128.

## P1 — instrument control (mu = 0) must pass
Every body: revisit = 1.000 at every q; distinct2 = 1; lam_hat < 1e-4; a_range < 1e-12.
If this fails the instrument is broken and nothing below counts.

## P2 — bimodality of the key process at a coarse quantum (the claim's core)
At q = 1e-4 the steady-state revisit distribution is bimodal: a regular mode
(revisit > 0.8) and a chaotic mode (revisit < 0.05), with fewer than 15% of bodies in
between. The key process is a bounded attractor (returns) in the regular sea and
diffusion (no returns) in the chaotic web.

## P3 — the phase boundary is the resonance web
Bodies with d_res < 0.01 are chaotic (revisit < 0.05 or lam_hat ≥ floor/2) more than
80% of the time; bodies with d_res > 0.03 are regular more than 90% of the time.
Chaos concentrates in |a−1| < 0.12 (co-orbital/Hill zone) and near the strong
first-order resonances (2:1 at 0.63, 2:3 at 1.31, 1:2 at 1.59); the deep interior
(0.55–0.60) is mostly regular.

## P4 — the collapse quantum equals the element range (why the exact memo hits 0%)
As q shrinks 1e-4 → 1e-6, the fraction of bodies with churn ≥ 0.5 rises towards ~1:
at engine-scale quanta every body churns ~1 key/orbit, regular ones included, so the
(E,L) memo cannot pay anywhere; it would pay only at q comparable to the element
oscillation range. Quantitatively: a regular body's revisit at q = 1e-4 drops below
0.5 once its relative element range (a_range/a_mean) exceeds ~3×q; the median collapse
threshold q* across regular bodies is within a factor 3 of the median relative a_range
(order 1e-3 here, i.e. order mu).

## P5 — work concentration flips with the quantum (p99 story)
At q = 1e-4 the top 5% of bodies by distinct2 carry more than 60% of all distinct keys
(work concentrates on the chaotic web). At q = 1e-6 that same top-5% share drops below
30% (everyone churns; the fine quantum destroys the concentration the allocator could
exploit).

## P6 — the engine's own detector orders the work
Spearman rank correlation across bodies: ρ(lam_hat, churn at 1e-4) > 0.7 and
ρ(d_res, churn at 1e-4) < −0.5. The resonance distance computable from the compiled
frequencies alone (no run) orders the compile-rate budget.

## P7 — instruments agree
Bodies classified diffusive (msd_slope > 0.7) have revisit(1e-4) < 0.05 and lam_hat
near the floor; bodies classified bounded (msd_slope < 0.3) have revisit(1e-4) > 0.8.
Cross-agreement ≥ 90%.

## P8 — held out (for the checker to run, I have not run these)
- mu = 3e-4: chaotic fraction less than half of the mu = 1e-3 value; deep interior
  (a < 0.7, away from 2:1) essentially all regular.
- mu = 3e-3: majority of the belt chaotic (resonance overlap); revisit collapse
  quantum q* scales up roughly with mu.
- e0 = 0.2: chaotic fraction grows (wider resonances), same bimodality shape.
- A second seed (e.g. 11): all fractions above move by less than 10 points.

## Kill criterion for the premise
If revisit at q = 1e-4 is not bimodal (no regular returning mode), then the memo pays
nowhere at any engine-relevant quantum, and the claim becomes the negative result:
"the (E,L) key process is diffusive everywhere below q ≈ element range; only the jet
(re-anchored offsets) is regime-independent." Either way the run reports.

## What I tuned on (disclosure)
Smoke runs at T ≤ 300 fixed two instrument bugs (a wrong universal-variable term;
a renormalization bias that faked λ = 0.3 at mu = 0) and chose q values; no statistic
above was tuned. The μ=0 control and T=300 smoke are the only runs before these
predictions.
