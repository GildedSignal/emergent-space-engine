# predictions.md — 20261003-0520-dynamics-a9c2

Written before the decisive grid run. Tuned-on: only the far-from-resonance controls
(|Δ| ≥ 2·W, W = 2.5·μ^{2/3}) that define the numerical floor of λ_ref, and code
smoke checks (init roundtrip, one-orbit Kepler roundtrip 1.6e-15, VV stability).
The grid itself (5 μ × 15 detunings × 2 phases = 150 configs, 256 orbits, e₂ = 0.05,
gate = e-pump ratio in [0.8, 1.25] + resonant-angle regime match) has not been run.

**P1 — λ map.** λ_ref (per orbit, twin at 1e-12) sits at a numerical floor
(≤ 3e-4/orbit) for |Δ| ≥ 2W at every μ, and exceeds 10× floor somewhere inside ±W.
At μ = 3e-3 the unstable set is wider than ±W (resonance overlap); at μ = 3e-5 it
is empty or one config wide.

**P2 — cost phase transition.** With K* = cheapest kicks per orbit whose behaviour
gate passes (K ≤ 64 else "unmeetable"): K* ≤ 8 for ≥ 90% of configs with λ_ref at
floor; K* ≥ 32 or unmeetable for ≥ 50% of configs with λ_ref ≥ 10× floor. The
boundary tracks instability, not static detuning: at least 3 configs inside ±W
pass at K ≤ 8 (quiet libration centres), and at μ ≥ 1e-3 at least 3 configs outside
±W are unmeetable (overlap tails). If the K* boundary equals the static band
exactly, λ adds nothing and the static rule stands.

**P3 — the layer knows itself.** λ_layer (K = 16, twin at 1e-9, free byproduct)
rank-correlates with λ_ref: Spearman ≥ 0.7 among configs with λ_ref above floor,
and a threshold on λ_layer separates "unmeetable at K ≤ 64" with AUC ≥ 0.85.
If AUC ≈ 0.5, self-measurement fails as a changeover trigger and doll-entry needs
an oracle — a gate we currently lack.

**P4 — transients thrash (lens blind spot).** Among configs with run-mean λ_ref
≥ 10× floor, the 32-orbit windowed λ crosses that threshold ≥ 3 times within 256
orbits for ≥ 1/3 of them (a bare threshold rule toggles the changeover; hysteresis
is required), while no config with run-mean λ_ref at floor ever crosses it.

**P5 — control.** At μ = 3e-5 every config passes at K ≤ 8 with λ_ref at floor.

Kill criterion for the premise: P3's AUC near 0.5, or P2 showing K* independent
of λ (either uniformly cheap or uniformly unmeetable in-band).
