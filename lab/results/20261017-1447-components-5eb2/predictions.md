# predictions.md — 20261017-1447-components-5eb2

Written before the decisive flights (the prof-instrumented `refit_probe` runs and the
real-state bind bench). The instrument itself (nested stages READOUT/SECONDARIES + the
(doll, tick) census) is print-only; `ladder_digest` must come out bit-identical with the
patch applied and `prof` off.

## P1 — the kick's wall-clock owner
The belt clock kick's ns/call (P_KICK_CLOCK, ~40-50 µs on this x86 class) decomposes with
SECONDARIES (the 3-source field rebuild) as the largest single term: I predict
secondaries ≥ 35% of the kick item's own ns, and FIT (bind_surface) ≤ 40%. If FIT instead
holds ≥ 60%, b063's 84-89% refit share is confirmed and the census is the anomaly to explain.

## P2 — the (doll, tick) multiplicity
Steady flight: most secondaries calls are alone at their tick (share of calls at
multiplicity ≥ 2 below ~25%), but crest windows concentrate: I predict the ≥ 8 buckets hold
a measurable tail (≥ 5% of calls) at N = 3×10⁴ within the first interval, because the belt's
two-comb train puts many per-body kicks on shared ticks at the crest. If multiplicity ≥ 2
is < 5% everywhere, a per-tick shared field read buys < 1.05× and read-stream's open
direction 1 dies in its per-tick form (it must batch per drain instead).

## P3 — the refit at true inputs
`bind` (Rebinding::from_state, edge None) on 512 real flown belt states: I predict
8-15 µs/call, above my synthetic-key Orbit::compile median (4.4 µs — the quadrature alone)
because the fit adds fit_key, at_radius, decode and the residual, and real belt keys carry
more knots than my e ≤ 0.33 sweep (the handoff's ~43 knots/body). If real-state bind is
≤ 6 µs, then the whole refit is under ~15% of the kick and the kick's cost is reads and
field algebra, not compiling.

## P4 — held-out
Checker holds out: N = 10⁴ (a decade below my main arm), rtf 1800 (faster delivery, deeper
into the first crest), and coast vs the census (no burn anywhere here). Predictions above
should hold at both N and both rtf (order of magnitude).
