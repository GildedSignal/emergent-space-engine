# predictions.md — 20261007-2057-library-26cb

Written before the decisive probe (`probe_hlive.py`). Bottleneck: H_live, distinctions per game-second, "not measured yet" (HANDOFF risks, 6 Oct). It decides whether 10⁹ bodies fit 8 GB: memory binds either on static programs (belts, 0.126 bits/body) or on the rate of canonical distinctions (quantized (E, L) key changes, the tube's 16-byte logical view re-keying, law.md §Tube).

## Setup (fixed before running)

- Belt: N = 20,000, a ∈ [2.2, 3.2] AU, e Rayleigh(0.07), star 1 M☉, Jupiter μ_J = 9.55e-4 at 5.2 AU, e_J = 0.
- Physics per orbit: Laplace–Lagrange secular quadrupole of Jupiter (forced eccentricity; E untouched at first order), synodic scattering impulse Δv = 2 G m_J/(b v_rel) at conjunction (b = a_J − a_aph, v_rel = |v_K(a) − v_K(a_J)|), mapped to Δa, Δe.
- Canonical key: quantized (E, L) on 16+16 bits over the belt's range (law.md memo key is 32 bits). Sensitivity: 8+8.
- Hot contrast population: P = 5,400 s (LEO-like), 32 kicks/orbit (H0190 unaveraged) with kick Δv set by the parent's tide.
- Controls: μ_J = 0 must give exactly zero key changes (leak test); the quadrupole forced-e must match the analytic Laplace–Lagrange value within 1% (truth check). Either control failing ⇒ VOID, not a finding.

## Predictions (held out: not tuned on)

- P1 (belt): E-key changes ≈ 0 per orbit (the quadrupole conserves E); L-key changes only when the secular e-cycle crosses a bin: I expect O(0.01–0.1) bits/orbit at 16+16. Belts ≈ memory-static: programs, not distinctions, carry the billion.
- P2 (hot tail): ≥ 1 key change per orbit ⇒ ≳ 1.5×10⁻⁴ bits/s/body; a fraction 10⁻³ of 10⁹ in short-period orbits writes GBs per simulated hour — the tail, not the count, owns H_live.
- P3 (quantum): at 8+8 the belt's distinctions fall to ≈ 0 — H_live is set by the key quantum (a law parameter), not by the physics; same moral as r8 v4's dip quantum.

## Kill criteria

- If the belt at 16+16 produces ≥ 1.5 bits/orbit sustained, the "store the generator" premise fails at that floor for live universes (scars grow without bound): the bijective-belt gold priced only a static program.
- If μ_J = 0 gives nonzero key changes, the pipeline leaks: VOID.
