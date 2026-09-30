# predictions.md — rung r8 v2 (written before the decisive 16-belt run)

Tuned on: belt 0 only (seed 20261008, sigma_e=2.70e-3, rho=4.44e-5), where
candidates = 1.68e6, conjunctions = 1.39e5, truth = 427, element-sort
work/enc = 326, hier-bounds work/enc = 2.4e4, shear-grid detected 427/427,
ring-cells detected 65/427.

Held-out expectations over the remaining 15 belts and the scaling runs:

1. **Controls.** oracle: missed = false = 0, work/enc = 1 (by construction),
   scale_exponent ~ 0 (see 5). ring-cells: missed_fraction in [0.6, 0.95]
   (a pair within rho sits in the same coarse cell, but a check fires only
   at a cell crossing: ~0.2 expected crossings per d<rho interval), and
   work/enc > 1e3. If either control misbehaves the rung is VOID.

2. **element-sort** is exactly the reference's own conjunction enumeration
   (same exact checks), so missed = false = 0 on every belt, no tuning
   possible. Median work/enc over belts in [50, 3000]: conjunctions scale
   ~ N^2 * (a sigma_e)^2 * T while truth grows with rho/sigma_e, so the
   worst belts are small-rho & large-sigma_e. Fails `cheap` (<= 10).
   scale_exponent = 2.0 +/- 0.1 (candidate a-reach is set by e, not rho):
   fails `scales` (<= 1.1).

3. **shear-grid**: complete (missed ~ 0) because rho-cells force an
   epicyclic crossing during most approaches, but events/body/orbit ~
   4 a e / rho + epicyclic azimuth/rho ~ 10^2..10^4, i.e. work/enc in
   [1e4, 1e7] — fails `cheap`; exponent ~ 2 (cells must shrink as
   rho ~ 1/N) — fails `scales`.

4. **hier-bounds**: missed = false = 0 (exact floor examinations).
   Its floor member tests ~ (#candidate pairs)^~1.3 > element-sort's
   conjunctions at T = 20 orbits, so median work/enc in [1e3, 1e6]:
   fails `cheap`; exponent ~ 2: fails `scales`. The certificates only
   separate groups whose radial envelopes are disjoint; within one
   e-reach everything falls to the floor.

5. **The rung's scaling premise will not hold.** Encounters per belt ~
   (#conjunction events) x P(encounter per conjunction), and P ~
   (rho / a sigma_e)^2 up to a passage factor. Under rho = 1e-4 (1e4/N)
   with sigma_e fixed, total truth ~ N^2 rho^2 ~ const, NOT linear in N.
   I expect measured truth counts flat across N (exponent -0.2..0.3), so
   oracle's `scales` passes trivially and the criterion does not test what
   it intended. The candidates still show exponent ~2 against it.

6. **events_per_body_orbit medians**: element-sort 1–30 (a cold belt has
   < 1 synodic cycle per candidate pair per run: swaps amortize);
   shear-grid 10^2–10^4; hier-bounds 30–3000; ring-cells ~20–30.
   The certification floor (the integrator's fear) is a few events per
   body per orbit for the sorted and hierarchical representations, and
   thousands for rho-sized cells.

7. **Mechanism.** The cost is set by the candidate set (a-reach ~ a*e per
   body, ~ N sigma_a a e pairs), not by rho: shrinking rho by 10x shrinks
   truth by ~100x and the work not at all. The ratio work/encounter ~
   (a sigma_e / rho)^2 / (passage gain) is the number the rung calls
   work_per_encounter; it is a property of the belt, not of the algorithm.
