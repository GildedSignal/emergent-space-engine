# Predictions (written before the decisive run)

Model: the repo's own belt (`crates/encounters/src/belt.rs`: a in [1, 1.5] AU, Rayleigh
e, sigma_e = 0.01), perturbed by a Jupiter at a_J = 5.2 AU, m_J = 9.55e-4 M_sun.
Kicks: hyperbolic impulse 2*G*m_J/(v_rel*d) at each synodic conjunction (radial,
v_rel = |v_circ(a) - v_circ(a_J)|, d = a_J - r). Quanta from the tube spec
(law.md line 12): E and L 32-bit over the belt's range, periapsis angle 32-bit over
2*pi, periapsis time 64-bit per radial cycle.

- **P1 (scarring rate).** Every body gets at least one above-quantum conjunction
  kick within <= 3 orbits (synodic rate ~0.85/orbit). f_kicked(2 orbits) > 0.8.
- **P2 (first-scar size).** The e-degrees of freedom (L, omega together) cost
  40–55 bits per scarred body at the tube quanta; the a-degree (E) costs 15–30 bits.
  So a fully scarred belt already carries ~60–85 field bits/body.
- **P3 (t_p dominates).** The periapsis-time divergence crosses one full cycle
  (and thus its scar saturates the 64-bit field) within ~100 orbits; before that it
  grows near-linearly, ~+1 bit per doubling of time. t_p is the largest scar field.
- **P4 (growth type).** After full scarring, field bits grow only logarithmically:
  slope in [1.5, 4] bits per doubling of t (random walk in E, L, e; linear drift in t_p).
- **P5 (smooth field removes little).** Conditioning the kick deltas on 64 bins of a
  (subtracting the smooth-in-a field) removes < 25% of the e-dof entropy: the surprise
  is per-body (phases quasi-random), not shared.
- **P6 (the wall is generic).** Extrapolated to N = 10^9 against the 8 GB budget
  (64 bits/body): a raw 4-field scar + 30-bit ordinal crosses the budget by ~2–4
  orbits; even the sorted-microstate floor of the heated belt (any exact encoding)
  is >= 60 bits/body (>= 7.5 GB). The budget is crossed by the *first scarring pass*,
  not by accumulation. If any of P2/P6 comes out a factor 4 below, the wall claim dies.

Kill criterion for my own claim: if measured steady-state bits/body (best encoding
among scar and sorted-floor) come out < 40 bits/body, then 10^9 fits with margin and
the "wall" verdict is wrong; report that instead.
