# predictions.md — rung r3 v2, run 20260929-1940-rung-r3-two-body-doll-v2-9c52

Written before reading `bin.csv`, the flyby sweep, or any transfer `EV`/energy output.
Basis: 6-seed spot checks of the oracle vs the dolls, the 2PN residual family measured
there (advance ≈ (7.5+e²+c·ν)/p relative, period ≈ (3.2–4)/a² relative), and analysis.

## Binaries (1024 seeds, p log-U [20,1000], e U [0,0.6], ν U [0.01,0.25])

1. **Truncation exclusion will empty the precession judging set.** With the honest
   estimate ε_prec = (7.5+e²+5ν)/p, every seed with p ≤ 1000 has ε > 0.005 (half the
   1% tolerance), so `min_judged_seeds` will be ~0–5 for every configuration and the
   `judged ≥ 64` criterion will fail for all. The cause is the criterion window, not
   the law: even the exact Schwarzschild solution (the ν→0 truth) disagrees with the
   1PN oracle by ~0.76% at p = 1000.
2. **eob-doll period:** judged set (ε_period = (4+2ν)/a² > 5e-4 excluded) keeps ~600
   seeds; on those the doll's period is within ~5e-4 of the oracle (2PN residual
   3.2–4/a², and a ≥ ~90 on judged seeds), so `period_pass_fraction ≈ 1.0`.
3. **eob-doll ν-effect:** the energy map reproduces the DD ν-term of the period to
   ~0.3% at p = 500 (spot check −8.467 vs −8.449); expect `nu_effect_pass_fraction ≈ 1.0`
   on a judged set of several hundred (ν ≥ 0.05, 4|E| ≤ 0.05).
4. **test-mass negative:** period scaled by 1/√m₁ → errors 2–40% ≫ 0.1%: pass ≈ 0.
   ν-effect exactly 0 (ν ignored): pass = 0. Precession off by m₂/M: pass ≈ 0 on any
   judged seed.
5. **newton-doll negative:** no precession (advance 0): pass = 0. Period misses the 1PN
   oracle by ~3/a ≥ 0.3%: pass ≈ 0 (perhaps a few large-p seeds). ν-effect 0: pass = 0.
6. Under a lenient γ²-style estimate (if I had chosen one), eob-doll `prec_pass_fraction`
   would be ≈ 0.2 (only p ≳ 770 pass at 1%), i.e. eob-doll fails prec under every
   defensible exclusion. Reported in the dossier either way.

## Handoffs (quasi-satellite transfer, 425 crossings at tmax = 400, law 0 measured)

7. Handoff energy error will be dominated by the missing pre-SOI planet pull just
   outside the boundary; I expect err(k) roughly flat-to-slowly-growing in k, i.e.
   fitted exponent ≤ 0.2 for all three laws (they differ only at 1PN, ~1e-8 of the
   dynamics). If the exponent comes out ~1 for all configs, that is chaotic
   amplification of handoff error, not a law difference.
8. Newton-doll vs Newtonian reference should show the smallest absolute error;
   eob-doll vs 1PN reference similar; test-mass slightly worse (fixed-star frame off
   by 3e-6).

## Gravity assists (64 flybys, b log-U [1.5,50] R⊕, v∞ = 15 km/s)

9. The bisection will realize the reference's b to <1%. The doll will NOT match the
   reference Δv to 1% at small b: the pre-SOI pull the doll drops steers the deep
   encounters, and the doll's realized periastron differs by O(b) (measured in a spot
   check: doll 1.8e-5 AU vs reference 2.13e-4 AU at b = 5 R⊕). I predict
   `assist_pass_fraction` ≈ 0 for eob-doll AND for both negatives at 15 km/s, rising
   toward 1 only at v∞ ≳ 60 km/s (deflection angle → 0). This is an architecture
   finding (handoff at the SOI is too coarse for R_p-scale encounters), not a config
   difference.

## Cost

10. `events_per_orbit` (median of handoffs/crossings/kicks per binary radial period):
    crossings ≈ 425 per 400/(2π) ≈ 63.7 planet orbits ≈ 6.7 per orbit, handoffs the
    same, kicks 0 → median ≈ 6.7 ≤ 512: passes for all configs. Binaries need no kicks
    (one doll, exact generator), quadrature cost reported separately in the dossier.
