# Predictions — written before the probe (lesson test, not a rung)

Probe: `probe.py`. Belt around one star, surface density in `a` fixed (ρ = 5,000 bodies/AU), Rayleigh σ_e, random angles. N grows 10³→10⁶ by widening the belt (dilution testbed, q-candidate-degree's regime). Candidate pair = orbit-crossing band |aᵢ−aⱼ| ≤ aᵢeᵢ+aⱼeⱼ (the cheap necessary condition every tier shares). Calendar entry = one standing prediction "next conjunction at t, miss ≈ local spacing". No tuning on the numbers below.

- **P1 (tuned expectation):** candidate pairs per body at fixed ρ, σ_e = 0.05 are constant in N: log-log slope across 10³→10⁶ within ±0.05 (locality: the band is set by a·e, not belt width).
- **P2 (tuned expectation):** conjunction events per body per orbit (the calendar's pop rate) constant in N, same slope bound — the load never sees N.
- **P3 (HELD OUT):** the danger knob is dynamical temperature, not scale: pairs per body scale ~linearly with σ_e (slope 1.0 ± 0.25 over σ_e 0.05→0.20) while staying flat in N. If it instead grows with N, the calendar needs envelopes, not entries.
- **P4 (HELD OUT):** burstiness: per-body event-count dispersion index (σ²/μ) ≈ 1 (Poisson, Mediocristan) for a uniform belt, but > 2 once 10% of bodies sit on one orbit (co-orbital concentration, Extremistan). If concentration stays ≈ 1, the slack-skin-as-redundancy lesson loses its tail argument and I report it failed.
- **Controls:** sorted-sweep pair count == brute-force count at n = 2,000 (instrument check); total unordered pairs N(N−1)/2 grows quadratically (the thing we are deleting).

Kill criteria: P1 or P2 failing (slope ≳ 0.1) kills the "calendar rate independent of N" lesson-leg; P4 failing kills the redundancy-tail leg.
