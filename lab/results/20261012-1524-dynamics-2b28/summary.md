# Ensemble analysis (dynamics lens)

Control encounter rate per body per orbit: 4.511e-03 (window spread 4.35e-03..4.67e-03)

## A. Feedback scan (belt, N=512, T=1500, mean of 3 seeds)

| mu | R_med | A_early | A_mid | A_end | e2 xgrowth | deaths | repay/enc | repay share |
|---|---|---|---|---|---|---|---|---|
| 3e-8 | 3.4 | 1.44 | 1.20 | 1.34 | 1.12 | 0.0% | 1022 | 0.78 |
| 3e-7 | 1.0 | 0.98 | 0.74 | 0.67 | 2.12 | 0.0% | 1022 | 0.69 |
| 2e-6 | 0.4 | 0.95 | 0.47 | 0.36 | 3.89 | 0.0% | 1022 | 0.62 |

A(t) window means per mu (cascade check: any window >1.1 * first window?):
  mu=3e-8: 1.44 1.34 1.21 1.25 1.26 1.20 1.21 1.21 1.23 1.34
  mu=3e-7: 0.98 0.90 0.86 0.81 0.78 0.74 0.79 0.74 0.68 0.67
  mu=2e-6: 0.95 0.85 0.67 0.62 0.60 0.47 0.50 0.45 0.37 0.36

Stirring check (mu=3e-7, seed 1): measured d<e2>/dt vs Gamma*<de^2> per body:
  d<e2>/dt = 3.224e-07/orbit ; Gamma*mean(de^2) = 6.413e-08 (coherent pumping would give ~2e*de: 5.524e-07)

## B. N scaling at fixed linear density (mu=1e-9, T=300, mean of 2 seeds)

| N | conj/body/orb | enc/body/orb | repay/enc | repay share | work tot (Mops) |
|---|---|---|---|---|---|
| 512 | 1.579 | 8.05e-02 | 1022 | 0.98 | 12.9 |
exponent conj/body vs N: +0.037
exponent enc/body vs N: -0.202

## C. Formation bursts (N=32, T=3000)

| cfg | enc tot | R_med | peak/mean (50-orb) | Fano (1-orb) | first3/last3 peak/mean |
|---|---|---|---|---|---|
| aligned mu=1e-11 | 205 | 43.9 | 55.8 | 140.3 | 187->187 |
| random mu=1e-11 | 155 | 48.0 | 46.3 | 95.7 | 124->124 |
| aligned mu=1e-8 | 5 | 0.8 | 13.0 | 1.0 | 1->1 |
| random mu=1e-8 | 3 | 0.5 | 25.0 | 1.0 | 1->1 |

Belt Fano (per-orbit counts, mu=1e-9, mixed): 75.11
