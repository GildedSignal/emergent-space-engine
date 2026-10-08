# Predictions — redteam cc34 (written before the decisive run)

**Attack:** the law's resonance gate (law.md #29: kicks orbit-averaged away from resonance, resonance detected from compiled frequencies p·Ω₁ − q·Ω₂ ≈ 0) is a state-selected switch at a fixed frequency tolerance. r4 v3's cases sit at fixed detunings inside or far outside the resonance; nothing ever crosses the boundary. The true first-order libration island width scales as (μ·e)^(1/2) while the representative tolerance W = 2.5·μ^(2/3) (r4 v3) is fixed in e. So one fixed tolerance cannot track the island.

**Setup (float, planar circular restricted 3-body, 2:1 interior resonance, μ = 3×10⁻⁴):** truth = full unaveraged RK4; "switched" = the design's shape: secular-averaged elements outside tolerance W, exact integration inside (giving the design its best inside law). A slow chirp carries the particle across the resonance.

**Pre-registered predictions (held-out cases not tuned on: e₀ = 0.05, and the second phase λ_p0 = 180° for every e₀):**

1. **Width sweep.** Measured libration half-width / W ≈ 0.5 at e₀ = 0.005, ≈ 1.5 at e₀ = 0.05, ≈ 3 at e₀ = 0.2 (island ∝ e^(1/2), W fixed).
2. **Outcome at e₀ = 0.2** (island ⊃ W): truth and switched diverge in the irreversible outcome — capture label differs, or e_final differs by more than 1.5×.
3. **Outcome at e₀ = 0.005** (island ⊂ W): labels match (both see the island late or not at all), but more than half of the switched model's time inside W is spent outside the true island: over-trigger into the dense order with no dynamical reason (cost, not behaviour).
4. **Held-out e₀ = 0.05:** marginal — I expect at least 1 of 2 phases to diverge in e_final by more than 25%, but I hold this weakly (island ≈ 1.5 W, phase luck matters).
5. **Convergence:** halving the truth step changes no outcome label.

**Kill criterion for the premise (frozen before the run):** if the switched model matches truth's capture label and e_final within 25% at every e₀ and phase, the fixed-tolerance switch survives this probe and the attack is dead.

**Cheapest falsifier budget:** < 60 s total runtime, Linux x86, orders of magnitude only.
