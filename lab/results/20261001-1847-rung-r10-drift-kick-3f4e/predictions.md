# Predictions (written before the decisive runs)

Written after the samplers, the truth reference, and the three split integrators were implemented
and unit-checked (Kepler roundtrip, wh-fixed vs truth on a smooth ship, symba's apsidal rate on one
moon: ratio 1.0002), and **before** any metric was computed on any case. Held-out: everything below
is a prediction about cases I have not run.

Free parameters I chose (not tuned on results): base step H = 2π/192 (planet period), changeover
band [1, 2] R_H with a C² smoothstep, near-region recursion level j = ceil(log2(96·√(μ/d³)/192))
(so every planetocentric orbit gets 96–192 force evaluations), depth cap H/2^14.

## jacobi_exponent (B12, 16 ships, 200 planet periods; floor 1e-12, median, limit 0.2)

- `truth`: 0 (below the floor throughout, or a perfect-law noise fit 0.0–0.3 on one or two ships;
  median 0).
- `soi-switch`: 0.5–1.2, failing. events3 measured 0.83; each hard SOI switch is an O(H) event at
  d ≈ 0.016 where the unresolved planet force is ~4, so I expect a near-linear random walk.
- `wh-fixed`: ≥ 0.5 and up to no-answer: at H = 2π/192 the SOI passages (d down to ~10⁻³) see kick
  accelerations of 10²–10³, so the Jacobi error should blow past 1e-4 within tens of crossings
  (B12 also demands max err 1e-4; I expect the worst ship to break it).
- `symba`: **≤ 0.2, my central claim.** The far and near chunks are each symmetric splits of the
  exact flow, and the changeover is C², so the only Jacobi error comes from O(H²) split error at
  band crossings and the leapfrog's own floor. I predict 0.0–0.25 on the median ship, worst ship
  below 1e-4 relative at the end. Risk: ships that graze d ≈ R_H for many consecutive steps sit
  in the blend and may random-walk faster (0.3–0.5). This is the prediction the rung can kill.

## class_match (B14, 256 moons, 50 planet periods; limit 0.99)

- `truth` = 1 by construction; `symba` = 1.0 (nothing is averaged or switched; moons live wholly
  inside K̄ = 0, where the map is pair-drift + tidal kicks at 96–192 evals/orbit). Prograde moons
  past ~0.5 R_H escape; retrograde last — both classes should follow the truth exactly here.
- `wh-fixed`: 0.9–1.0 (inner moons at 10–30 steps per orbit: some prograde inner moons may flip
  class). `soi-switch`: 0.5–0.9 (inner moons at 5–10 steps per orbit in the near mode).

## precession_match (limit 0.99, within 10% of truth's rate)

- `symba` ≥ 0.99 — r9 showed averaged tides fail above 0.17 R_H; unaveraged tidal kicks at
  96–192 evals/orbit should hold 10% everywhere, including retrograde outer moons (my probe:
  ratio 1.0002 at 0.3 R_H). Held-out risk: outer prograde moons near 0.5 R_H have the slowest
  apsidal rates and escape mid-run; if their ϖ series is short the rate is noisy for law and truth
  alike.
- `wh-fixed`: 0.4–0.8 (inner moons under-resolved). `soi-switch`: ≤ 0.5.

## libration_ratio (36 resonant cases, worst min(r, 1/r); limit 0.8)

- `symba` ≥ 0.9: these cases never enter the band (conjunction distance ≥ 2.3 R_H even at
  μ = 3e-3), so symba is plain Wisdom–Holman there, which is the correct resonant dynamics (r4
  killed *averaged* kicks, not WH). Worst case: μ = 3e-3, exact commensurability, phase 4°.
- `wh-fixed` identical to symba here (same map away from the band): ≥ 0.9.
- `soi-switch` also far-form throughout: ≥ 0.9 (it should pass everything except jacobi).
- I expect 4–12 of the 36 cases to librate under the truth (mostly phase 4°, detune −1/3 and 0).

## force_evals_per_orbit (median over all bodies; limit 200)

- `wh-fixed` and `soi-switch`: 192 (base steps per planet orbit).
- `symba`: 170–195. Ships and resonant bodies: 192; moons: 96–192 per moon orbit (j chosen by the
  local period). Median lands on a moon: below 192 but not far. Truth: 0 by convention (true count
  reported in the dossier: order 10⁵–10⁶ per ship, ~10⁴ per moon at rtol 1e-12).

## What would make me wrong

- If symba's median jacobi exponent exceeds 0.2, the smooth-changeover claim as I built it
  (split-time blend of two symmetric maps) is killed at this step size, and the DLL98 pure form
  (heliocentric drift at every recursion level) is the next configuration, not a bigger changeover
  band.
- If class or precession fail anywhere for symba, the failure will be at inner retrograde moons
  (fast apsidal rates, fewest steps per orbit at the j-shell top edge).
