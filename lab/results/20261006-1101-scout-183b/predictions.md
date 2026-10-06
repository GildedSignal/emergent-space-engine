# predictions.md — written before the decisive runs (C2–C6)

Calibrated (tuned) on: smoke (N=2k) and C1 (N=5×10⁴, secondary 10⁻³ M☉ at
1.15 AU, σ_e=0.05): 0.160 enc/body/orbit, all encounters distinguishable at
every grid q ∈ {24..36} bit, record entropy ≈ 17.6 bits (4.76+4.81+~8 timing),
lag-1 autocorr +0.32, and the C1 verdict FAILS 64 bits/body before 100 orbits.

## Held-out cases (not tuned)

1. **C2, secondary at 1.30 AU** (belt edge 2.2–2.5 r_H away, only the high-e
   edge crosses): encounter rate per body per orbit drops to 1–5×10⁻³
   (30–150× below C1), concentrated at the outer edge; every encounter still
   distinguishable at all q (scar_frac = 1.0); record entropy 17 ± 3 bits.
2. **C3, secondary at 1.6 AU** (closest conjunction 0.5 AU = 4.5 r_H > bcut):
   **exactly zero encounters** in the whole run; the belt's floor is the
   program alone (0.126 bits/body, components-98bc).
3. **C4, super-Earth 10⁻⁵ M☉ at 1.15 AU** (r_H 4.6× smaller): rate 0.01–0.05
   per body per orbit; scar_frac still 1.0 (impulse at r_H scales as m^{1/3},
   still ≫ quantum).
4. **C5, cold belt σ_e = 0.02, secondary at 1.15**: rate within ±20% of C1
   (conjunction distance is set by Δa, not by e).
5. **C6, N-independence:** C1 at N=10⁴ matches C1's rate within 5%.
6. **Poisson control:** per-body encounter counts in C2 have variance/mean in
   [0.8, 1.3] (events are independent-ish; strong deviation = a broken
   sampler or locked resonances).
7. **Verdicts:** C1 (all-chaotic) fails 64 bits/body by 100 orbits (negative
   control must fail); C2 passes with bits/body < 30 at a 10⁴-orbit horizon.
8. **Ship–ship:** 10⁶ kg ships create no scars at any q ≥ 24 bit (key units
   < 0.02); scars from mutual gravity need ≳ 10⁸ kg aggregates at ≤ few-km
   closest approach.
