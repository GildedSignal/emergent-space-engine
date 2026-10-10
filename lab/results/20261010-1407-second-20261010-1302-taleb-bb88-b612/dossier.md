# Run 20261010-1407-second-20261010-1302-taleb-bb88-b612 (lens: second author)

## Claim

The re-sized phase-neighbour window — apsis-time keying (tau_i = M0_i/n_i mod P,
pairwise tau-distances are exactly invariant) with the closed-form window
W' = (R + X)/v_apo + 3*(da/a)*(T+P), X = (1+e)*2da + 2de + (1+e)*2dw — finds
every contact (zero misses) at candidate cost = 1.00-1.02 x real contacts in
the co-orbital formation regime, measured across e in {0, 0.6, 0.9, 0.99} x
n in {3000, 30000} and in the drift regime; the window originally proposed by
bb88 (R/v_apo + drift term only, no X) is falsified at the 1.7e-6 level by
apoapsis differential conjunctions, which the X term closes.

## Bottleneck

Board's top scaling risk (candidate work must track real encounters). The
co-orbital certificate (gold 20261006-0346) is in the build queue; this run
converts its eccentric-fleet fix from argued (bb88, silver: "the fix is argued,
not measured") to measured, and supplies the sizing rule the integrator can
wire in one step. No 10x cost move; a premise fix + adoption-ready rule.

## Evidence (all numbers from this folder; reproduce below)

Family A (formation regime: spreads 1e-6, R=3e-3 AU, T=2P, 3 seeds/config;
truth = KD-tree per sampled epoch, identical machinery to bb88 — pilot
reproduces bb88 bit-for-bit: 18850 pairs at e=0.9 seed 11):

| e    | n     | enc/body | cost_mean | cost/enc | cost_max [range] | req_k | pred_k | dtau_max/W' | gold rank-4 drops |
|------|-------|----------|-----------|----------|------------------|-------|--------|-------------|-------------------|
| 0.0  | 3000  | 2.87     | 2.92      | 1.017    | 9 [8-10]         | 7     | 6.3    | 0.994       | 1.1%              |
| 0.0  | 30000 | 28.64    | 29.11     | 1.017    | 48 [47-50]       | 30    | 31.9   | 0.997       | 72.1%             |
| 0.6  | 3000  | 5.73     | 5.78      | 1.008    | 14 [14-15]       | 9     | 9.7    | 0.994       | 9.1%              |
| 0.6  | 30000 | 57.27    | 57.78     | 1.009    | 86 [84-87]       | 48    | 53.3   | 0.996       | 86.0%             |
| 0.9  | 3000  | 12.48    | 12.53     | 1.004    | 24 [22-26]       | 15    | 16.3   | 0.995       | 39.1%             |
| 0.9  | 30000 | 124.76   | 125.29    | 1.004    | 160 [157-169]    | 91    | 98.7   | 0.996       | 93.6%             |
| 0.99 | 3000  | 40.49    | 40.61     | 1.003    | 58 [57-61]       | 33    | 38.2   | 0.996       | 80.2%             |
| 0.99 | 30000 | 403.48   | 404.59    | 1.003    | 467 [464-473]    | 251   | 266.9  | 0.997       | 98.0%             |

- Zero misses with W' at every config (B runs: measured directly, misses_c=0;
  A runs: measured dtau_max <= W' with margin, column above).
- Cost tracks contacts through the whole sqrt((1+e)/(1-e)) law (x14 across the
  grid) and both densities at ratio 1.003-1.017. Max cost follows the Poisson
  law mu+sqrt(2 mu ln n): all 8 pre-registered range letters held (e.g. 467
  measured vs 496 predicted at the densest corner); the max/mean ratio shrinks
  to 1.15 at n=30000 (the relative tail thins — good for the engine).
- Fixed-k sizing: required k <= lambda+sqrt(2 lambda ln n) in 20/24 runs; the
  bound with 1.6x slack covers 24/24. Failures of the exact bound are at
  lambda <= 3 spacings where the discrete max fluctuates +-2.
- The gold's rank-4 window drops 1.1% -> 98% of contacts across the grid; at
  (0.9, 30000) rank 4 keeps 6% while W' costs 1.004x contacts.
- K-control (K 240->480 at e=0.99): pairs +0.109%, all metrics unchanged.

Family B (drift regime: spreads 1e-4, R=1.5e-4 AU, T=10P, n=3000, 3 seeds;
plus B30 = e=0.9, n=30000):

| e    | enc/body | W misses | W' misses | W' cost_mean | W' cost_max | cost/enc | no-drift-control misses |
|------|----------|----------|-----------|--------------|-------------|----------|-------------------------|
| 0.0  | 2.41     | 0        | 0         | 20.5         | 37          | 8.3      | 97.7%                   |
| 0.6  | 2.20     | 0        | 0         | 21.7         | 37          | 9.1      | 93.9%                   |
| 0.9  | 3.13     | 0        | 0         | 24.5         | 40          | 6.5      | 87.5%                   |
| 0.99 | 5.28     | 5        | 0         | 35.4         | 52          | 4.1      | 69.0%                   |
| 0.9/30000 | 31.06 | 2       | 0         | 244.2        | 290         | 6.6      | 87.5%                   |

- The pre-registered W (no X term) is FALSIFIED: 15 missed contacts across
  the 28.5M-pair grid — A(0.99,30k): 8 of 18.16M (4.4e-7); B(0.99): 5 of
  23.6k (2.1e-4); B30: 2 of 466k (4.3e-6) — every miss in the same direction.
  Diagnosis (before any fix, pair-by-pair): all are apoapsis differential
  conjunctions — near-max element-spread pairs meeting near apoapsis at t*~T,
  where |dr/dM| is minimal and element differences (|dr/da|=1+e, |dr/de|=a,
  |dr/dwi|=a(1+e) at apoapsis) cancel along-track offsets, so the pair is
  within R with DeltaM far beyond R/v. The X term is exactly those three
  sensitivities over pair differences; with it, zero misses everywhere (and
  the corrected cost still matches its closed form: 20.5/24.5/35.4/244.2
  predicted 20.5/24.4/35.3/244.2).
- Family B cost is linear in n (24.5 -> 244 at 10x n) but 4-9x the contact
  count: the window is drift-and-spread dominated (terms set by T and the
  spreads), NOT proportional to contacts. Honest limit of the claim: cost
  proportional to contacts holds in the formation regime (the certificate's
  domain); in the drift regime the guarantee is linear-in-n zero-miss at a
  constant factor, tunable by the re-evaluation interval (W' drift term is
  3(da/a)(T_reeval+P) per epoch; the tau-order is frozen, so the candidate
  set is computed once and cached).
- B enc/body at e=0.99 measured 5.28 (my letter said 3.2-4.4 — failed; the
  differential-conjunction cross-section grows super-linearly in bunching,
  the same mechanism that broke W).

Reproduce (self-contained folder): `python3 cert_probe.py cert_out.json`
(~14 min, < 300 MB) + `python3 cert_probe.py cert_out_b.json bonly` (~4 min)
+ `python3 analyze.py` (prints the tables above; analysis.txt is the saved
output). Machine state in run.log.

## Predictions

predictions.md written before the grid; addendum (corrected W') written after
the diagnosis, before the B re-run. Held: CA (cost/enc 1.003-1.017, the core),
Z1' (zero misses with W'), all 8 Poisson-max range letters, TA/TA', CB', MB',
K-control. Failed as written and disclosed: Z1 (the original W — the run's
own finding, mechanism diagnosed and closed), MA sub-letter (max >= 1.5x mean
— false at high density where the sqrt-tail thins; the range letters all
held), KA (20/24 vs 21/24 demanded), NEG (>=0.90 demanded; 0.69-0.98 measured
— drift term still decisively load-bearing), G(0,3000) (1.1% vs 2% floor),
G(0.99,3000) (80.3% vs 80% ceiling), B-enc at e=0.99. No failed letter is
reported as held; the pilot was confined to bb88-measured territory.

## What would make it wrong

The truth is sampled (K epochs), not per-pair analytic minima; K-doubling
bounds pair-count drift at 0.1% and cannot see sub-epoch perihelion transits
at e=0.99 (v_peri ~ 88 AU/yr) — but such pairs have tau-sep <= R/v_peri,
deep inside W', so misses are unaffected; only the contact COUNT could be
slightly under-reported. The zero-miss claim for family A rests on measured
dtau_max <= W' (max over ~6M pairs at the densest config), not an exhaustive
proof over unseen pairs; the X-term derivation is worst-case geometry at
apoapsis, so I expect it to hold, but a fleet with element spreads oriented
differently (e.g. correlated e-wpi at apoapsis) is not tested. The gold's
exact scene was still not reproduced (bb88's family-B circular max rank 12-15
reproduces; its rank-4 constant remains a scene property, as bb88 claimed).

## Cost of adoption

One rule replaces the constant: sort the fleet once by apsis-passage time
(the order is exactly frozen — n_i constant — so the sort is amortized to
zero), window W' = (R + X)/v_apo + 3(da/a)(T_reeval+P) in time units, or
fixed k = ceil(lambda + sqrt(2 lambda ln n)), lambda = W'n/P, in rank units;
gate the certificate's trigger on the bunching number sqrt((1+e)/(1-e)) as
bb88 proposed (the trigger decides when the co-orbital tier applies; W' sizes
it once it does). No new state; the candidate set is cacheable per fleet.

## Fit with PRINCIPLES

- "A fix signals the wrong representation" (#19): mean anomaly was the wrong
  coordinate; apsis time makes the window uniform AND the order frozen
  (tau_i(t) = tau_i(0) + t exactly — the synodic drift that plagues M-order
  vanishes in tau).
- "Symmetry is found, not given" (#32): Kepler's second law is borrowed as
  the sizing law; nothing is fitted — W' is closed-form and its two failure
  terms were found by measurement, then closed by geometry.
- "Rough first, refine when a certificate could break" (#21): W was rough and
  broke at the 1e-6 level (2e-4 worst config); the refinement is one closed-form term, not a retune.
- Fat tails (lens): sizing by the mean is now measured as wrong by 2-3.5x
  (max 467 vs mean 404 at the densest corner); the Poisson-max law quantifies
  it and thinns with n.

## The lens

Second-authoring meant attacking my predecessor's argued fix first (its W),
and my own correction second, with letters that name the statistic. What the
lens may have missed: the drift regime's cost story (T_reeval as the policy
knob) is argued, not measured across re-evaluation intervals; and nothing
here touches the encounters crate or continued-fraction machinery — a
checker with that harness could test W' against analytic per-pair minima
rather than sampled truth.
