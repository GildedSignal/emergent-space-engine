# Predictions — 20261008-0458-dynamics-7166 (written before the decisive run)

Question: on the frozen contact law `es-lattice-relativistic-v1` (event core `EventCore`,
the plane's battle path), does per-chronon work stay thin-tailed as N and packing grow, or
is there a packing phase where one indivisible connected batch scales with N?

Cases below were **not** tuned on: the sweep values were fixed from geometry before any run
(only the instrument control `instrument_control_lone_body` may be run first).

- **P1 (walled gas, steady state).** For fill ≤ 0.2: Fano factor of contacts per chronon
  < 3, `max_batch` ≤ 10, and neither grows with n (1024 → 16384). For fill 0.6–0.7 (cage
  regime, mean free path ~ a diameter): Fano > 10 or `max_batch` ≥ 30, and contacts per
  body per chronon grow ≥ 5× over fill 0.4. The boundary sits in (0.4, 0.7).
- **P2 (stock battle, spacing 5q, mixed responses).** `max_batch` ≤ 12 at every n (the
  interpenetration front is a rate spread over chronons, not a simultaneous percolation
  cluster). Fired contacts per body over the crossing grow ≈ √n (optical depth: my
  geometric estimate is ~5 at n=400 and ~34 at n=25600). p99/p50 of per-chronon ops stays
  < 8 at all n; the *median* per-chronon ops at the front peak scales ~ n.
- **P3 (mono-disperse battle packing sweep, n=6400).** Even spacing 3q (fleet fill π/36 ≈
  0.09, front fill ≈ 0.17) stays thin: `max_batch` < 30, Fano < 10. The gas carries the
  phase boundary, not the battle; if 3q already avalanches, co-orbital concentration
  (taleb-09b5) extends to contacts.
- **What kills what.** P1 high-fill fat tails or `max_batch` ≥ 30 growing with n: the
  "law is smooth at every reachable packing" premise is dead — a missing p99 gate on batch
  size. All fills thin with `max_batch` ≤ 10: my phase-boundary hypothesis is dead; the
  law is smooth everywhere reachable (confirmation, reported as held).
- **VOID conditions:** the lone-body control spikes; any config exceeds 60 s; a law
  refusal (genesis out of ranges).
