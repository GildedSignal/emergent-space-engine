# predictions.md — 20261021-0429-scout-451f (written BEFORE the flyby/circular grids)

Controls already passed (not the decisive run): periapsis eigenvalues reproduce 4c79's
certified closed forms (−γ²(2+β²), 1, γ²(1+2β²))·M/r³ to <1e-9 at rp ∈ {6,18,100}M,
β ∈ {0.25,0.5,0.9,0.95}; u·u drift ≤ 3e-15.

Cases below are NOT tuned on (the grid is the first run of each kind).

1. **Quadratic convergence / IC floor.** With exponential-map ICs, the relative error
   err := |ξ_true − ξ_ODE|/ξ₀ divided by (ξ₀/r_p)² is CONSTANT in ξ₀ (within 25%)
   across ξ₀/r_p ∈ {1e-4, 1e-3} at every (r_p, β, angle). If it is not, the instrument
   is VOID (IC floor pollutes the second-order measurement, as it did 288f's naive
   congruences).

2. **288f's aligned case cleaned.** At β 0.9, radial offset, ξ/r_p = 1e-4, the exit
   error drops far below 288f's −0.136% (their reading was "IC floor + slow growth");
   I predict err < 1.5e-4 relative (≥ 10× cleaner), i.e. the second-order coefficient
   c₂ = err/(ξ/r_p)² is O(1)-to-O(10), not O(10⁴).

3. **No M/r term in c₂ (P4 extended to second order).** c₂(rp = 18M, β) ≈ c₂(rp = 100M, β)
   within 30% at every β: the speed amplification of the second-order coefficient is
   purely kinematic, like the first-order one 4c79 certified.

4. **Speed scaling of c₂.** c₂ grows with β roughly as γ^p with p ∈ [2,4] (transverse
   channels compound; along-motion stays ~flat like the linear channel).

5. **Circular duration is LINEAR in orbit count (secular, not bounded).** On a circular
   doll at rp = 18M (β_circ = 0.25) and 100M, err(T)/(ξ/r)² grows ∝ N_orbits with a
   per-orbit rate C = O(1–30) — my Newtonian estimate is C ≈ 2π·(15/8) ≈ 11.8 per orbit
   (the second-order epicyclic phase error). The member certificate then lasts
   N_cert(err<1%) ≈ 0.01/(C·(ξ/r)²) orbits: at ξ/r = 1e-2 that is < 20 orbits (SHORT —
   re-refinement bites within a session); at ξ/r = 1e-3 it is > 500 orbits (free).

6. **Angles.** The oblique-45° c₂ lies between the radial and along-motion values;
   the out-of-plane channel c₂ tracks the square of its linear amplification order.

Kill criteria: (1) failing kills the instrument (VOID); (3) or (5) failing is a real
result (the second-order law has a compactness term / the accumulation is bounded),
reported as such with the numbers.
