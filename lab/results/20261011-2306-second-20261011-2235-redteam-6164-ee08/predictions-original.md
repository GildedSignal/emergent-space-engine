# Predictions (written before the decisive run)

Target premise: `docs/representation.md` §3 — "A cycle's derivatives are stored with it, so a
kick updates the cycle by a multiply-add" (the jet; law.md's adopted form: exact offset plus
stored derivatives, re-anchored when the accumulated offset reaches sqrt(floor/C), after
red-team 20261006-0346-redteam-df81 measured 730 correlated quantum kicks to the 1e-6 floor).

The df81 measurement was one orbit family. Held out here: the eccentricity axis and the plunge
separatrix. Oracle: float64 Schwarzschild geodesics via Binet ODE (u'' + u = 1/L² + 3u², M = 1),
each cycle's (Δφ, T) by RK4 quadrature; jet = first-order Taylor of (Δφ, T) in (E, L) with
numerical central differences. Floor 1e-6 relative (df81's floor), quantum kick α = 1e-6
relative on E (and, separately, on L).

- **P1 (single kick, belt-like domain):** for p ∈ {20, 100} M, e ∈ {0.1, 0.5, 0.7, 0.9, 0.99},
  one quantum kick (α = 1e-6 on E, and on L) leaves jet error < 1e-6 relative in both Δφ and T.
  Expectation: the premise survives its home domain.
- **P2 (quadratic growth / recompile interval):** jet error grows ∝ (kick size)², so the
  recompile interval N ∝ 1/α; at α = 1e-6 correlated kicks, N is of order a few hundred
  (df81 saw 730), i.e. the exponent of error vs N is 2.
- **P3 (the attack — plunge separatrix):** near the bound/plunge separatrix (periapsis
  approaching the unstable circular orbit between 4M and 6M), ∂T/∂E and ∂Δφ/∂E diverge, so a
  1e-6 quantum kick produces cycle error ≫ 1e-6 — the multiply-add is invalid and the body
  recompiles every kick. Prediction: the (E, L) band where a 1e-6 kick gives > 1% cycle error
  has relative width in L between 1e-4 and 1e-2 around the separatrix value — large enough that
  r1's own ISCO seeds ("L 1% above the circular value at r = 7") sit inside the divergent zone
  once kicked.
- **P4 (no eccentricity blowup away from the separatrix):** at fixed p = 20, sweeping e from
  0.1 to 0.99 changes the single-quantum-kick jet error by less than 10×.

If P1/P2/P4 hold and P3 holds, the finding is: the jet premise is sound on the belt and unsound
in a band around the plunge separatrix, with no rung criterion guarding that band (B5 gates E,L
growth exponents; B9 counts crossings; nothing gates the recompile rate or the jet's validity
domain).

Machine note: shared cloud runner (8 vCPU), no other load observed at start; timings not used
as evidence (floats only decide exploration, never canonical outcomes).
