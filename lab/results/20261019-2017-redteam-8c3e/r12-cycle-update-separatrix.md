# r12 — cycle-update separatrix arm (proposed; NOT run by this run — freeze draft for the integrator)

Prose: docs/representation.md L67's "a kick updates the cycle by a
multiply-add" under L60's budget ("at most one floor unit per event"), on the
Schwarzschild separatrix family p_sep(e) = 6M(1+e)/... in game units:
kappa = p - (6+2e), M=1. Truth = exact geodesic cycle map (periapsis to
periapsis), recomputed at the kicked invariants; candidate = the stored cycle
plus stored derivatives times the kick.

configs:
  taylor-w20 candidate   # kick q = 2^-20 relative on E and L separately, both signs
  exact-refit negative   # the refit itself (must hold the budget everywhere: control)
  farfield-control positive  # kappa=8, e=0.5: must pass (the licensed domain)

criteria:
  rem-taylor behaviour  remainder_taylor_dt   <  1.0    # budget multiples, worst over grid e in {0.1..0.98}, kappa in {0.05..8}
  rem-taylor-phi behaviour  remainder_taylor_dphi  <  1.0
  crossing type  unrepresentable_kicks  ==  0     # a kicked point outside the bound region has NO cycle; the Taylor path returns finite numbers
  scaling type  q2_ratio  in  [8, 32]        # remainder scales q^2: 4x in kick -> 16x in remainder
  control-far cost  farfield_rem  <  1e-3    # positive control must hold strongly
