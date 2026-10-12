# Predictions (pre-registered before the decisive run)

Toy: event-driven belt, N bodies, conjunction rate Γ per body per orbit (anchored to r8's measured 1.1/orbit at belt density, swept), impulse kicks Δv = 2Gm/(b·v_rel) with phase-mixed miss distance b, quantum ε on relative (a, e). "Game-second" = 1 real second at rtf 100; one 2 AU orbit ≈ 8.9e5 game-seconds. Held-out cases: I have NOT run the ε sweep, the stirring-feedback scenario, or the cone accounting before writing this (only the Fermi estimate in requirements.md).

- **P1 (rate, not volume, in the sparse regime).** Distinguished count D(t) is linear in simulated time (fit exponent 1.00 ± 0.06) until D/N > ~5%, and the inflow per body per orbit is independent of N. Wrong if D(t) is superlinear without feedback, or N-dependent at fixed Γ.

- **P2 (cone saturates; H_vol fails).** Live-RAM distinctions follow the light-arrival annulus: inflow grows ~linearly in T until the light-crossing time T_x of the active region, then flat at the system's total rate. At rtf 100 a 2.4 AU belt saturates within tens of game-seconds of play, so a player sees constant inflow almost immediately. H_vol (inflow ∝ T forever) must FAIL after T_x at system scale; it only holds at galaxy scale (T_x ≈ 1.6e11 game-seconds at rtf 100).

- **P3 (the quantum is the lever).** Survival fraction s(ε) = fraction of encounter kicks that move the victim out of its (a, e) quantum cell follows a power law ε^−α with α ∈ [0.5, 1.5] while partial, saturating at 1 for coarse ε (from Δv ∝ 1/b with b ~ uniform: P(ΔE > x) ∝ 1/x). One decade coarser floor ⇒ ~10× fewer live scars in the partial regime. Wrong if s(ε) is flat (then the floor is not a lever) or the exponent is outside the band (then my ΔE model is wrong — report which).

- **P4 (repack pays only late).** With CRAM/git-style shared references per occupied quantum cell, the fraction of distinguished bodies sharing a cell with ≥1 other grows with accumulated scars but stays below ~50% for the first orbit at Γ = 1.1, N ≤ 2e5 (kicks spread bodies across cells faster than they cluster). So the lever is the quantum (P3), not reference sharing, in the first hours.

- **P5 (the real tail risk is self-stirring).** With e-pumping feedback (kicks random-walk e; conjunction reach ∝ e), inflow becomes measurably superlinear (fit exponent ≥ 1.15 within a few orbits). This is planetesimal self-stirring; if it shows, H_live must budget the stirring timescale, not just the encounter rate.

Controls: no-encounter run must give exactly 0 live bits (positive control); the 88 B/body baseline (R0) and the cone-volume model are the negatives that must lose.
