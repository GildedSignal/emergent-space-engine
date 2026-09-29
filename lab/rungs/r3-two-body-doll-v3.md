# Rung r3 v3: two bodies as one doll, handoffs, and a gravity assist

Frozen by the integrator on 29 September 2026, after r3 v2 (claude/lab-20260929-1940-rung-r3-two-body-doll-v2-9c52). v2's precession exclusion left 0 judged seeds, because the 1PN oracle's next term is about 8·M/p, already 0.8% at p = 1000. So the criterion could not be passed, which was the integrator's error. v2's assist reference was also unconverged. v3 fixes both and adds a positive control. The ν criterion is unchanged: v2 missed it by 7 seeds, and it will not be weakened after that was seen.

**Question.** At first post-Newtonian (1PN) order, the effective-one-body map says the relative motion of two masses m₁ and m₂ is a test body in Schwarzschild with M = m₁ + m₂. The symmetric mass ratio ν = m₁m₂/M² enters only through the energy map. Does that give the right two-body behaviours? And do handoffs between nested dolls, and a gravity assist from a moving doll, behave?

**Configurations.**
- `eob-doll`: relative motion as a test body around M, computed with the exact Schwarzschild geodesic, a float oracle-quality quadrature. The real energy is E_real = M·√(1 + 2ν·(E_eff − 1)) per unit reduced mass (the effective-one-body energy map). Handoffs go through a sphere-of-influence boundary, with the bodies' invariants re-expressed in the new doll's frame at the crossing.
- `oracle` (positive): it returns the 1PN oracle's own precession, period and ν values, and the reference's own handoffs and assists. It must pass, or the criteria are unpassable.
- `test-mass` (negative): ν is ignored, so the lighter body orbits a fixed M = m₁. It must fail the ν-dependent period.
- `newton-doll` (negative): Kepler motion, no GR. It must fail precession.

**Cases** (sampler: Python `random.Random(20261002)`).
- **Binaries:** 1024 seeds with p log-uniform in [20, 1000] (in units of M), e uniform in [0, 0.6], ν uniform in [0.01, 0.25].
- **Truncation rule** (period and ν only; precession uses the band below): for each seed and metric, the author computes the oracle's own truncation estimate, i.e. the relative size of the next post-Newtonian term. A seed whose estimate exceeds half the metric's tolerance is excluded from that metric and counted. Each metric must judge at least 64 seeds.
- **Handoffs:** a ship on a figure-eight transfer between a planet (mass 3×10⁻⁶ of its star, 1 AU circular orbit) and the star. The transfer crosses the planet's sphere-of-influence boundary 100 times. Its reference is a float64 N-body integration (RK4, adaptive, half-step reruns agreeing to 10⁻⁹).
- **Gravity assists:** 64 flybys of that moving planet, with impact parameters log-uniform in [1.5, 50] planet radii. The reference is the same N-body integration.

**Oracle:** the 1PN two-body periastron advance and radial period from `damour_deruelle` and `eih_invariants` (`xtask/src/gr_oracle_extended.rs`), ported. The checker verifies each value.

**Metrics,** one set per configuration:
- `precession_pass_fraction`: over all seeds, the fraction with |Δφ_law − Δφ_1PN| ≤ (0.01 + 2τ)·Δφ_1PN, where τ = 8·M/p is the oracle's own truncation estimate. This is the behaviour "precesses at the rate the oracle can vouch for".
- `period_pass_fraction`: over judged seeds, the fraction with a radial period within 0.1% of the 1PN oracle.
- `nu_effect_pass_fraction`: over judged seeds with ν ≥ 0.05, the fraction whose relative period change due to ν (the same p and e at ν = 0 as baseline) has the oracle's sign and is within 10% of the 1PN oracle's ν term. This is the behaviour "a heavier partner changes the period the right way".
- `min_judged_seeds`: the smallest number of judged seeds across the period and ν metrics.
- `reference_converged`: 1 if the N-body reference for handoffs and assists agrees with its half-step rerun to 10⁻⁹ relative in heliocentric position at the end, else 0. It is the same for every configuration.
- `handoff_energy_growth_exponent`: the fitted growth exponent of the heliocentric energy error across the 100 handoffs.
- `assist_pass_fraction`: the fraction of flybys whose heliocentric Δv (magnitude and direction) is within 1% of the reference.
- `events_per_orbit`: the median of handoffs, crossings and kicks per binary radial period.

**Output.** `metrics.json`, plus one picture: the transfer path with its handoff points marked, and the Δv of flybys against impact parameter, law against reference.

```configs
eob-doll candidate
oracle positive
test-mass negative
newton-doll negative
```

```criteria
ref type reference_converged >= 1
judged behaviour min_judged_seeds >= 64
prec behaviour precession_pass_fraction >= 0.99
period behaviour period_pass_fraction >= 0.99
nu behaviour nu_effect_pass_fraction >= 0.99
handoff type handoff_energy_growth_exponent <= 0.2
assist behaviour assist_pass_fraction >= 0.99
cost cost events_per_orbit <= 512
```
