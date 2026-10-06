# Predictions — 20261006-0346-redteam-df81 (written before the decisive runs)

Attacks, ranked by how likely the player is to see the failure (the lens's own rule):

1. **A3 (kicks × cycle derivatives).** representation.md §3: "A cycle's derivatives are stored with it, so a kick updates the cycle by a multiply-add", and §6's cost table (≈50 ns per kick). Falsifier F1 (float, Schwarzschild exact quadrature; `f1_jet.py`).
2. **A5 (view gather at the past light cone).** "Newton's method finds the crossing, starting from the previous frame's" + "≤ 1 sample per pixel per frame". Falsifier F2 (`f2_view_newton.py`).
3. A4 (dense/sparse bit-identity), 4. A1 (two-body doll at 1PN only), 5. A2 (Binet cells), 6. A6 (≈0 cost undisturbed) — reasoned, no falsifier (A2 and A6 already have rung support; see dossier).

## F1 — the jet (cycle updated by first-order derivatives) under correlated kicks

Setup: exact Schwarzschild bound-orbit cycle increments Δφ (apsidal advance) and Δt (radial period) by Darwin-ψ Gauss–Legendre quadrature; anchor cycle at (p₀, e₀); kicks δL/L = ε per cycle, same sign (Peters inspiral, tidal torque — both monotone, both listed in representation.md §3); N = 10⁴ cycles (B5's shape horizon); floor = 10⁻⁶ relative (the compiled cycle's own accuracy, law.md: "about 10⁻⁶ at m = 16").

Held-out predictions, written before running:

- **P1 (instrument control):** my quadrature Δφ matches the closed form 2π(1/√(1−6/p)−1) to < 10⁻¹² relative for every case. If not, the run is VOID.
- **P2 (negative control — frozen increments, no derivative):** crosses the 10⁻⁶ floor within ≤ 10 cycles at ε = 10⁻⁴, and within ≤ 10³ at ε = 10⁻⁶. If it does not fail, the harness cannot detect drift and the run is VOID.
- **P3 (the jet in the interior, e₀ = 0.5, p₀ = 20):** error ≈ C·(nε)² with C = |f_LL L²/2f| of order 1. Crossing of the 10⁻⁶ floor at n* ≈ 10⁶ for ε = 10⁻⁶ (so it *survives* B5's 10⁴-cycle horizon, error ~10⁻⁸), and at n* ≈ 10²–10³ for ε = 10⁻⁴ (*fails* the horizon by 1–2 orders).
- **P4 (the jet near the separatrix, e₀ = 0.995, same p₀):** C is larger (the period's curvature in L grows as e→1 at fixed E), so n* shrinks by ≥ 3× versus e₀ = 0.5 at the same ε.
- **P5 (random-sign kicks, contrast):** error grows ~√N slower than the same-ε systematic sequence (drift ∝ √N·ε, curvature still second order); no floor crossing within 10⁴ cycles at ε = 10⁻⁴. This isolates *correlation*, not size, as the killer.
- **P6:** the implied re-anchor rule (re-anchor when the jet error reaches the floor) costs 38 crossings per n* kicks; at ε = 10⁻⁴ that is ≳ 0.04–0.4 crossings per kick on top of the ≈0 promise, i.e. the cost table's kick row needs a second term that the design does not carry.

## F2 — Newton from the previous frame's crossing at high closing speed

Setup: emitters on circular orbits (β_e ∈ {0, 0.3, 0.6}), observer flying through at β_o ∈ {0, 0.9, 0.99} (the game's 0.9c stream is a designed-for case, B15), flat spacetime (the multiplicity/lensing half is attacked in the dossier by argument), frame cadence resolving the orbit (~1° of emitter orbit per frame); truth by bisection; Newton seed = previous frame's root, max 50 iterations.

- **P7:** at all β_o ≤ 0.99 and β_e ≤ 0.6, ≥ 99.9% of frames converge in ≤ 4 iterations: the gather's *conditioning* survives in flat spacetime (g′ = 1 − β_los > 0 keeps Newton tame). If instead the p99 exceeds ~8 iterations or any Newton leaves the causal window [t_obs − D_max, t_obs], the "≈1 sample per pixel" cost claim fails at the flagship regime.
- **P8:** iteration count grows ≈ like 1/(1 − β_close) only through curvature, so the effect at β_close = 0.996 is a factor ≤ ~3 over rest, not an order of magnitude.

If P7 holds, A5's flat-spacetime half **survives** and the live risk moves to the two halves I argue but cannot falsify in 60 s: the cross-doll time map (relativity of simultaneity, flagged open in law.md) and lensing multiplicity (no memo of image count; composition of two dolls' deflections).
