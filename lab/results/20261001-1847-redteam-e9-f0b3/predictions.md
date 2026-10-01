# Predictions (written before the decisive experiment)

Decisive experiment: `control.py` — an independent absolute-coordinate Schwarzschild
integrator (textbook Christoffels from the diagonal metric, my own code) plus an
independent Fermi-simultaneity construction, compared against a faithful Python mirror
of the judge's difference-ODE oracle (`xtask/src/engine_judge/schwarzschild.rs` on
wt/judge2). Cases not tuned on: α = 0.1 (r/M=10) and α = 1e-6 (r/M=1e6), e ∈ {0, 0.6},
scales s ∈ {1, 1/16, 1/32, 1/64} of the 1e-5·r_p offset, ten proper periods.

1. **Killing constants.** My independent turning-point derivation
   (L̄² = (f(r_a)−f(1))/(f(1)−f(r_a)/r_a²), r_a=(1+e)/(1−e)) matches the judge's Darwin
   formulas to < 1e-12 at α ∈ {0.1, 1e-6}, e ∈ {0.3, 0.6}.
2. **Mirror fidelity.** My Python mirror of their oracle reproduces their printed
   separation-control values (r=10: e=0 → 3.05e-8, e=0.6 → 1.61e-6) within ~30%.
3. **Pairs are true geodesics (core premise).** Member trajectories from my absolute
   integrator vs their difference oracle, identically initialized: position error
   normalized by the offset < 1e-9 at α=0.1, e=0.6 over ten periods. A value > 1e-5
   would break the oracle.
4. **Fermi simultaneity.** Equal-proper-time projection vs orthogonality-solved Fermi
   projection (centered differences, s=1/16): residual < 1e-7 relative at α=0.1, e=0.6,
   scaling ≈ ×4 per halving (even part cancels in the odd difference; residual is O(s²)).
5. **Full-extent gap.** Their linearized truth (s=1/16) vs my full-extent (s=1)
   Fermi-simultaneous truth: < 5e-4 of the offset — i.e. 256× their worst measured
   separation control (1.6e-6) with margin, and far inside the 1% band, so the
   linearization cannot fail a perfect engine.
6. **Circular analytics.** My independent Riemann-projected tidal matrix at λ=0 matches
   the initial d²ξ/dλ² of the oracle pairs to < 1e-6; radial epicycle = √((1−6α)/(1−3α))
   and geodetic rate 1/√(1−3α)−1 to < 1e-6 at α=0.1.
7. **Weak control is wiring-only (premise, already measured).** The Newtonian trace at
   r/M=1e6 misses the GR oracle by 7.0e-6 — *below* the oracle's own 1e-5 validity
   tolerance — so the large-radius rung cannot distinguish GR from Newtonian; it
   certifies harness wiring only. Discrimination lives at r/M ≤ 1e4 (phase accumulation
   over ten periods ~ 10·2π·α).
8. **Runtime.** Release oracle for 21 cases × 3 refinements < 15 s (debug measured
   110 s ≈ 1.75 s per oracle call, 63 calls); the engine's 21×401 samples must fit the
   remaining ~40 s of the 55 s watchdog — unverifiable here, E9 fails closed pre-freeze.

Held expectations that would change the grade if violated: 3 (oracle broken), 5 (false
failure for a perfect engine), 6 (wrong tide in the oracle).
