# Predictions (written before the probe)

Probe: circular restricted 3-body toy (star 1, Jupiter 1e-3 at 5.2 AU, 240 massless belt bodies, a ∈ [2.0, 3.6], e0 = 0.05, planar), leapfrog dt = P_p/300, horizon 200 P_p. Per body, at its own orbit boundaries: osculating a; residue r = a − linear fit (fit = the ideal secular subtraction; the engine would use an analytic envelope, so this measures the deferral **ceiling**); S = cumsum(r). Growth exponent γ of windowed max|S| on the second half. Deferral D(Q) = first time |S| crosses Q·a0, in orbits.

Held-out cases (not tuned on; adversarial picks of my own):
1. **Off-resonance belt (δa from every p:q resonance > 0.05 AU):** γ ≤ 0.3 (bounded, the short-period tide cancels), so D(1e-4) = full horizon (skip everything; pay secular part only). Median D(1e-4) ≥ 10 orbits.
2. **Near 2:1 and 3:1 (|a − a_res| < 0.05 AU):** γ ≥ 0.75 (pumping; averaging dead there — H0203), D(1e-4) ≤ 2 orbits regardless of Q. Predicted fraction of belt < 20%.
3. **Adversarial e0 = 0.2 off-resonance subset:** still bounded (γ ≤ 0.35), amplitude grows with e but D(1e-4) ≥ 5 orbits.
4. **Q sweep:** for bounded bodies D rises steeply once Q > C·amplitude (cliff), for near-resonance bodies D stays ~1 at every Q (no cliff). If instead off-resonance D stays ~1–2 at Q = 1e-4, the deferral rule is dead and q-cadence must keep fixed cadence — that falsifies the lesson.

Kill criterion for the lesson: median off-resonance D(1e-4) < 3 orbits ⇒ pay-on-crossing buys < 3× on most of the belt ⇒ report lead, not a change to q-cadence.

Decision at stake: q-cadence (queued, 120 min) should be built as a per-body deferral certificate with a resonance dimensionless trigger, not a swept fixed cadence.
