# Predictions (written before any seam run; the code is untested at writing time)

Question: the adopted encounters design (lab gold 20261006-0346-taleb-09b5, build `b-coorbital-cert`)
routes between a pairwise Binet-cone tier and a phase-neighbour certificate via "a dimensionless
concentration number". Its evidence is fleet-only scenes. I probe the **seam**: a fleet embedded in a
belt whose inner bodies cross the fleet's orbit, and graded concentration at fixed N.

Scenes (this run's generator, `make_fleet`): m bodies, a ∈ [1, 1.005], Rayleigh σ_e = 2e-3 with
**aligned periapses** (a convoy), mean longitude uniform in an arc; belt: n bodies, a ∈ [1.02, 1.5],
σ_e = 5e-2, random angles; ρ = 5e-3 (large, so fleet-internal encounters exist inside 20 orbits —
synodic argument: conjunction needs Δa ≳ 2π/(1.5·T) ≈ 3.3e-3 at T = 126, contact needs Δa ≲ ρ).

## P1 — cost seam (kill criterion for my premise)

Mean candidate **degree** of a fleet body grows ≈ linearly with m (m internal + n_cross cross-family),
while a belt body's degree stays constant at fixed belt size. At m = 300, n = 1000: fleet degree
300–500 vs belt degree 100–300. Cross-family candidate pairs ≈ m·(100–250) **regardless of ρ or arc**.
Consequence: after the phase certificate absorbs fleet-internal pairs, a fleet body's kick still
re-sets up ~n_cross pairs against real cross-encounters ≈ 0.01–0.1 per body per orbit → ≥ 10²–10³
setup pairs per real encounter, growing ∝ n at fixed m. The O(N²) risk re-enters through the seam.

## P2 — completeness seam

On mixed scenes the shipped tier misses fleet-internal contacts at the percent scale (reproducing the
gold's 4–6% qualitatively; any nonzero is the point), cross-family misses = 0, belt-internal = 0.
Graded concentration (fleet only, N = 400, arc from 2π down to 0.03): miss fraction rises from 0 at
full-circle to percent-scale at tight arcs; candidates stay ≈ C(N,2) at every arc (cost does not
decide the trigger — misses do).

## P3 — the rank-4 law is really a density law

Fleet-internal rank-at-encounter median ≈ ρ·m/arc: ≈ 15 at arc 0.1, ≈ 5 at arc 0.3, ≈ 1.5 at arc 1.0
(ρ = 5e-3, m = 300). The gold's "partner rank 4" is ρ × linear phase density, not a universal
constant: a certificate with fixed k = 4 is incomplete at denser arcs (or larger ρ); k must be sized
by the dimensionless number ρ·n_arc/arc (still O(1) at game ρ).
Cross-family rank-at-setup: median ≈ N/4 (uniform order) — no O(n·k) phase certificate evaluated at
setup can cover cross-family pairs.

## Controls (must behave, else VOID)

- Belt-only (m = 0, same belt): zero misses, degree constant — the tier's home turf.
- Uniform-arc fleet (arc = 2π, no belt): the dense ring; zero misses, candidates ≈ C(N,2) —
  cost-only failure (the gold's quadratic setup), no silent wrongness.

## Kill criterion for my premise

If fleet degree < 2× belt degree for all m ≤ 3000, AND cross candidates per real cross-encounter
≤ 20, AND fleet-internal rank-at-encounter ≤ 4 at every arc with zero misses: the seam is cheap and
the contracted design stands as written; this run reports a negative result (lead).

## What would make the work wrong

Truth and method share the `rel` solver path only in `refine` (truth is Halley elsewhere) — the
memo-artifact lesson: I check `dup` and distinctness of counted events, and the truth's superset is
radial overlap, independent of the cone. Misses are only counted inside (0.05, t_end−0.05) with
matchup tol 1e-3, same as the crate's verify. Slow-dip encounters (v_rel ~ 1e-3) stress the matchup
time tolerance; if misses cluster at broad dips I will re-check with the dip-quantum reading before
claiming a miss.
