# Predictions (written before the decisive run)

Component: the binet cell's in-band frequency. The frozen r1 law sets ω² = 1 − 6u_k with
u_k the band's geometric centre — the memory grid's geometry sets the dynamics. The page's
open direction 2: refit the centre to the orbit's own mean. Arms (all float64, G = c = M = 1,
oracle = Python ports of the shipped `periapsis_elliptic` + `bound_period_quad`, validated
against an independent RK4 of the exact Binet ODE):

- `frozen-m{8,16,32}`: shipped r1 law verbatim (control; must reproduce the prior run's pattern).
- `mid-m16`: ω² = 1 − 6ū, ū = (u_peri+u_apo)/2 — the page's literal proposal.
- `invL-m16`: ω² = 1 − 6/L² — the invariant-only centre.
- `agm-m{2,8,16}`: ω = 2π/Δφ_exact, Δφ_exact = 4√(p/d)·K(4e/d) − 2π compiled from the
  cycle's own two turning points by AGM (~30 flops, once per compiled cycle). The centre
  leaves the dynamics entirely; the bands keep crossings/plunge/ISCO.

## P1 (control — frozen arms)
Reproduces the prior run (20261015-1450-redteam-fe85) without reading its code:
- eccentric sampler advance error second order in band width: median ≈ 1.8e-4 at m=16,
  ÷4 per m-doubling;
- e=0 worst-offset circles carry a first-order error → fail the 0.1% period bar at
  p ≲ 60 (m=16) and p ≲ 35 (m=32);
- m=8 fails precession (< 0.99).

## P2 (the literal refit `mid` kills one family, buys another)
- e=0 family: error drops to ~1e-15 at every p (the rotation runs at the circle's own
  exact epicyclic frequency).
- Eccentric corner degrades: the rotation at ω(ū) is not the exact eccentric frequency;
  predicted relative advance error ≈ (2e − 0.92e²)/p (1PN e-expansion of Darwin's formula).
  At e = 0.7 that crosses the 1% bar at p ≈ 95 → predicted `mid-m16` precession_pass_fraction
  ≈ 0.70–0.90 (a regression vs frozen's 0.996). The refit as worded trades the near-circular
  family for the strong-eccentric one.
- `invL-m16` fails the e=0 family outright (centre off by 3u² → error ~3/p ≥ 1% for p ≲ 300).

## P3 (the compiled-frequency law `agm`)
- Advance error < 1e-12 at every sampler seed, every m (the advance is the exact closed
  form of the orbit's own turning points; m leaves the dynamics).
- precession_pass_fraction = 1.0 at m ∈ {2, 8, 16}; e=0 family machine-level; separatrix
  neighbour (p = 8.5, e = 0.9) exact (K diverges as d → 0, precession diverges — emerges).
- Period: NOT constructed — read through the rung's dt/dφ rule on the law's own shape
  (a cosine in u). Residual is pure shape error. Held-out prediction: median < 1e-5,
  worst at the strong-eccentric corner ∈ [1e-4, 3e-2] — may fail the 0.1% bar there.
  This is the row's honest uncertainty: if the cosine shape cannot hold 0.1%, the cycle
  needs the Darwin χ-shape as a third compiled word.
- Plunge/capture/ISCO unchanged (the bands' channel; scoping stated in the dossier).

## P4 (cost)
Crossings per radial cycle track m alone: median ≈ 57 (m=16) / 28 (m=8) / 7–14 (m=2–4).
With agm the error is m-free, so m becomes a pure cost dial: the frozen record needs m=32
to pass clean; agm passes at m=2 → ~8–15× fewer band-crossing events at equal or better
behaviour.

## Kill criteria
- If `agm` advance error > 1e-9 anywhere on the sampler, the compile is not exact — kill P3.
- If `mid` does not delete the e=0 first-order family, the prior run's mechanism
  (band-centre frequency) is misattributed — kill the page's open direction 2 as stated.
- If frozen does not reproduce P1's pattern, my port of the prior law is wrong — VOID
  everything until fixed.
