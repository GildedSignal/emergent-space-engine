# Predictions — 20261017-0839-inversion-2373 (written before the decisive run)

Pilot: seed 7, same grid, disclosed (work/pilot-seed7.jsonl). The decisive run is seed
20261017 (default), the checker's seeds its own. The law below is fitted on the pilot's
seed only; the numeric bands are the held-out claims.

## The law (derived from shipped phase.rs semantics, pilot-validated)

- `reach = w0 + 0.75·da·TAU·H` with `w0 = angular + 2·centre ≈ 4·e_max` (da = the
  fleet's full a-spread; H in orbits; e_max = the fleet's largest eccentricity;
  angular ≈ rho/a ≈ 1e-4, negligible). n(a=1) = 1 rad/time-unit makes the drift
  coefficient 0.75·da·TAU (pilot slope 0.047/orbit at da = 1e-2, exact).
- Uniform-phase fleets: `pairs ≈ F²·reach/TAU`, `mean_k ≈ 2·F·reach/TAU` (forward
  window); cluster (sigma_l < reach): `pairs ≈ F²/2`.
- Refusal (phase arm dead, tree tier takes over): `reach ≥ π` ⇒ `H* = (π − w0)/(0.75·TAU·da)`
  = 62.6 orbits at da = 1e-2, 626 at 1e-3, 6260 at 1e-4.

## Held-out bands (seed 20261017)

1. keys F=1e5 (da=0, sigma_e=1e-2): pairs ∈ [2.9e8, 3.4e8], mean_k ∈ [5800, 6800],
   max_k ∈ [3000, 3700]. (e_max tail grows with F: reach ∈ [0.185, 0.215].)
2. keys F=1e4: pairs ∈ [2.5e6, 2.9e6], mean_k ∈ [500, 580].
3. train F=1e5, da=1e-4, H=100: reach ∈ [0.24, 0.29], pairs ∈ [3.8e8, 4.6e8], mean_k
   ∈ [7600, 9200].
4. train F=1e3, da=1e-3, H=200: reach ∈ [1.05, 1.20] (alive, no refusal);
   pairs ∈ [1.6e5, 1.9e5].
5. train F=1e3, da=1e-2: refused at H=100 and H=200 (reach 4.8 / 9.5); alive at H=50.
6. clust F=3e4 (sigma_l=0.05): pairs ∈ [4.45e8, 4.50e8] (≥ 0.99·F²/2), quad_frac ≥ 0.99.
7. event (keys F=400, rho=1e-4, H=10): events ∈ [4, 20]; rank_max ≤ 2 (pilot seed 7:
   rank_max = 0 — every contact's partner is the closest body at contact time);
   mean_k_paid ∈ [13, 23]; checked pairs per real event ∈ [250, 450].
8. time: visit_ns_per_pair ∈ [0.03, 1.5] (memory-bound streaming); checked_us_per_pair
   ∈ [2.5, 6.0] on this shared x86 box.
9. tree fallback (F=1e3, da=1e-2, H=100): phase=false; leafpair_tests ≥ 1e4 (the
  quadratic tier); runs in < 10 s.

## Kill criteria for my own claim

- If pred_pairs/pairs leaves [0.97, 1.03] on the uniform arms at seed 20261017, my law
  is wrong and the dossier says so.
- If mean_k at keys F=1e5 comes out ≤ 20 (linear class), the inversion claim dies:
  the certificate would be paying rank-class work for fleets.
- If rank_max at contacts exceeds ~10 while k stays ~F·reach/TAU, the gold rank-4
  property does not transfer to my populations and the "paid vs needed" gap is
  overstated — report as such.

## Checker's own arms (suggested, not run by me)

- Any seed: the law bands above ±10% (except event counts: Poisson, ±100%).
- da = 3e-4, F = 1e4, H = 500: reach ≈ w0 + 0.707 ∈ [0.9, 1.05] — the drift term
  dominating a long-but-legal horizon; mean_k ∈ [2800, 3400].
- rho = 1e-6 vs 1e-3 on keys F=1e4: pairs change < 1% (rho enters only through the
  negligible angular term) — the k dial is radial scatter and horizon, not contact size.
