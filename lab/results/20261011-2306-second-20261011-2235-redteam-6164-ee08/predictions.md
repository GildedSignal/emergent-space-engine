# Predictions (written before the decisive run of this second-author run)

Parent run 20261011-2235-redteam-6164 graded gold by one checker, with named misses:
(1) precession ratios at p = 500/1000 not regenerable from shipped code; (2) the T-channel
Kepler remainder stated as 15/4·α² where the checker says 15/8·α²; (3) "2.8 compiles/kick"
is an unsaturated extrapolation (compiles/kick caps at 1); (4) L-channel errors sit at the
oracle's own h-noise; (5) Kerr (χ ≠ 0) and the integer-law rerun remain open; (6) premise 4
(dense/sparse bit-identity) got a doc-level finding where a probe was owed.

This run does the record fixes and the cheapest decisive named experiment: the Kerr
separatrix (B19 already gates Kerr behaviours at χ ∈ {0.5, 0.9, 0.998} but nothing gates the
jet's validity domain there). Oracle: equatorial Kerr timelike geodesics, M = 1, prograde,
from the exact first-order form (du/dφ)² = u⁴Δ²R/Dφ² differentiated once (u″ = F′(u)/2), RK4
in φ, same cycle/derivative/jet machinery as the parent's Schwarzschild probe. Control: at
a = 0, r_c = 5 the machinery must reproduce the parent's P3 separatrix sweep (dphi, T,
|∂T/∂E|, jet errors) to < 1e-9 relative — it reduces to the same Binet right-hand side.

Held-out predictions:

- **P5 (Kerr separatrix, a = 0.9 prograde, r_c = 2.0, fixed L = L_c, E = E_c(1−ε)).**
  The logarithmic divergence persists: |∂T/∂E| grows about 10× per decade of ε (ε = 1e-3 →
  1e-6), whirl Δφ per cycle growing past 15 rad. A 1e-6 quantum E-kick exceeds the 1e-6
  floor by ε ≈ 1e-4 (as in Schwarzschild: 5.5e-6 there), and errs tens of percent at
  ε = 1e-6. Encounter-grade kicks (α = 1e-3 on E) at ε = 1e-3 err tens of percent, and some
  α in {3e-3, 1e-2} exits the bound family (plunge-after-kick): the multiply-add updates a
  cycle that no longer exists.
- **P6 (spin trend).** High prograde spin does not shrink the failure band; if anything the
  whirl is longer (a = 0.998, r_c = 1.15: Δφ at ε = 1e-3 ≥ the Schwarzschild 15.5 rad), and
  a = 0.5, r_c = 3.5 sits between. All three spins show the same categorical failure at
  encounter kicks.
- **P7 (a = 0 control).** Agreement with the parent's P3 numbers to < 1e-9 relative on
  dphi and T (not bit-identical: the lambdified right-hand side rounds differently).
- **P8 (per-channel decomposition — attacks the parent's own derivation).** The parent
  claims the corruption is the precession phase (4·(α·a)²) and the T-channel Kepler
  remainder is r_apo-free. I predict the parent's decomposition is wrong on both halves:
  the T-channel of an E-kick is the Kepler binding-energy curvature (15/8)·(δE/(1−E))²,
  which scales as (α·a)² — NOT r_apo-free — and at the parent's belt points it dominates
  the max error (e.g. p = 20, e = 0.5: T-channel ≈ 5.1e-9 of the 5.18e-9 total; p = 100,
  e = 0.99: ≈ 1.9e-4 of 1.887e-4). If instead the measured T-channel comes out flat
  ~1.9e-12 across r_apo, the parent (and the checker's 15/8·α²) are right and this
  prediction fails. Either way the headline (err ≈ 2–6·(r_apo·α)², validity condition
  r_apo·α < 4e-4) is unchanged: both channels carry the same (α·a)² scaling.
- **P9 (record regeneration).** Precession ratios (Δφ−2π)/(6π/p) at p = 100/500/1000,
  e = 0.5 regenerate the dossier's 1.0481 / 1.0092 / 1.0046 (checker: 1.00922 / 1.00459);
  the r_apo = 2000 walk at α = 1e-6 measures N_floor = 1 (every kick recompiles; the 2.8
  formula figure caps at 1); the doc-level findings (Minsky named the primary in-cell
  solution in representation.md, r5/r6 named but absent from lab/rungs/, law.md's
  darwin16 replacement, no jet-domain/recompile criterion in B5–B19) regenerate from the
  tree by grep.

Not run here (named, costed): the integer-law rerun of the sweep (needs a rung on
space-darwin16-v1 — the integrator's call, not a lab probe); premise 4's dense/sparse probe
(needs the r5 CW+lattice scene built; no dense-order contact evaluator exists in the crates
today — lattice-event's Grid is a dense/sparse *cell store*, not the r5 evaluation-order
pair, so a bit-identity probe has nothing to run yet). I will verify and document that
absence rather than fake a probe.
