# Predictions — rung r8 (written before the decisive 16-belt + scaling run)

Belt 0 (sigma_e=0.0027, rho=4.4e-5) was used to debug the machinery end-to-end
(brute-validated: 0 classification mismatches on 91 pairs, min-distance
agreement 3e-10 relative vs a 40k-sample brute scan). Predictions below are
for the full frozen run and were written before it.

## oracle (positive control)
- missed_fraction = 0, false_fraction = 0, work_per_encounter = 1.
- scale_exponent ~ 1.0 (truth is linear in N by the rho ~ 1/N design; fitted
  on exact counts at N in {1e3, 3.2e3, 1e4}; exact truth at 1e5/1e6 costs
  more than the whole run window allows).

## element-sort (candidate)
- false_fraction = 0 (its check at each swap is the exact per-conjunction
  minimum, same code as the reference).
- missed_fraction > 0, my estimate 1-10% pooled: encounters need a
  *true*-longitude alignment, but swaps happen at *mean*-longitude
  conjunctions; near-co-orbital pairs (|dn|*T < 2pi) can align in true
  longitude without any mean-longitude crossing in [0,T], and those dips are
  never checked. Belt 0 measured 30/502 = 6%.
- work_per_encounter ~ 1e2-2e3 (belt 0: 1173): every conjunction between
  radial-overlap pairs is a swap+check, and only ~rho/(radial spread) of
  conjunctions dip below rho. Fails cheap (<= 10).
- events_per_body_orbit ~ 1-10.
- scale_exponent ~ 2: conjunctions between overlap pairs grow like N^2 at
  fixed sigma_e while encounters grow like N. Fails scales (<= 1.1).

## shear-grid (candidate)
- missed_fraction ~ 0 (in-window cell changes fire during dips; grazing
  co-orbital pairs drift through many cells). Belt 0: 0/502.
- false_fraction = 0.
- events_per_body_orbit ~ 5e2-5e3: the epicyclic loop (size ~ a*e) must be
  resolved by rho-sized cells, ~8*a*e/rho per orbit; rho down to 1e-5 pushes
  this to ~1e4.
- work_per_encounter ~ 1e4-1e6. Fails cheap.
- scale_exponent ~ 1.0 (per-body cell-change rate does not depend on N at
  fixed sigma_e and rho ~ 1/N). Passes scales.

## ring-cells (negative control)
- Must fail cheap: 128 spoke crossings per body per orbit plus occupant
  checks (occupancy = N/2048) regardless of encounter rate; work_per_encounter
  ~ 1e3-1e5. Belt 0: 151e6/502 = 3e5.
- missed_fraction 0-0.4 (it checks only the entered cell, so fast dips with
  no crossing inside the within-rho window, and straddling partners, slip).
- scale_exponent ~ 2 at large N (occupancy term).

## Verdict I expect
Both candidates are KILLED: neither finds encounters at a cost proportional
to their number. The rung's fear is confirmed — the certification that a
body is undisturbed (the broad phase) costs orders of magnitude more than
the encounters themselves, and the sorted-element representation's cost
grows with density (N^2) rather than with encounters. The controls behave
(oracle passes, ring-cells fails), so the criteria are passable and the KILL
is informative.
