# Predictions (written before the decisive run, 2026-10-08)

Question: does H_live (bits of scar per body per unit game time, at the law's own storage grids)
let 10⁹ bodies fit in 8 GB, in the two regimes the board names — a smooth belt and a co-orbital
fleet — without reabsorption beyond periodic program refits?

Model (stated before running): Kepler conjunction Monte-Carlo per neighbour pair; impulses
Δv ≈ 2Gm/(b·v_rel) with b uniform in area within ρ; contacts below R_c change v by ~v_rel;
scar = integer offsets from the program, Elias-delta coded, F = 2 fields (sensitivity 1–4).

Grids: q_cert = ρ/a (the encounter certificate needs elements to ρ); q_doll = 20·2⁻³² ≈ 4.7e-9
(the 32-bit (E,L) memo-key grid over a doll with a_min = 0.05·a_belt).

## Held-out predictions (not tuned on)

1. **Belt rate anchor.** My conjunction MC on r8 v2's belt 0 geometry (N=10⁴, a∈[1,1.5],
   Rayleigh σ_e=1e-2, ρ=1e-4) gives 0.5–5×10⁻³ encounters per body per orbit (r8's truth
   measured ≈2.1×10⁻³ = 427/(10⁴·20)). If my MC is off by more than 10×, the geometry model
   is wrong and everything below is VOID.

2. **Belts scar; ships do not (gravitationally).** Asteroid-mass bodies (μ = 10⁻¹⁰) take
   Δa/a ≈ 10⁻⁴–10⁻³ per encounter (r8 v4's kick scale), i.e. ≥1 quantum on q_cert per
   encounter. Ship-mass bodies (μ ≈ 5×10⁻²⁵) take Δa/a ≈ 10⁻¹⁸–10⁻²¹: sub-quantum on both
   grids, needing ≫10⁶ encounters to land one quantum (principle 6 accumulation, never
   reached in a session). Gravity-driven H_live is therefore a belt phenomenon.

3. **The knife edge is the doll grid, not the certificate grid.** On q_cert the steady-state
   scar after 100 orbits stays ≤ 8 bits/body in every scene, so 10⁹ bodies fit with ≥8× slack.
   On q_doll a single asteroid-belt kick is ~10⁻³/4.7×10⁻⁹ ≈ 2×10⁵ quanta ≈ 36+ bits for one
   field: if scars are stored on the memo-key grid, the belt alone at 10⁹ needs ≥ 2× the
   8 GB budget once every body has been touched once.

4. **Contacts set the fleet's H_live**, at rate = conjunction rate × (R_c/ρ)²·(geometry),
   each costing ~2·v_rel/v_k quanta. I predict ≤10⁻⁴ contacts/body/orbit for dispersions
   ≤10⁻⁴, negligible for memory but the trigger for the co-orbital certificate (gold
   20261006-0346).

5. **Program refits hold the steady state.** Refitting the program's (mean, σ) every 10–100
   orbits absorbs the collective walk (heating), leaving residuals that grow only as
   √n·σ_kick; bits/body stay flat-or-log after the first refit in all scenes on q_cert.

6. **Creation rate.** H_live creation at 10⁹ bodies, rtf 100 (1 AU orbit = 87.6 game-hours):
   ≤ 1 MB per game-hour in belt scenes on q_cert (premise holds), and I predict the number
   to sit within one order of 10 kB/game-hour — small enough that H_live, not body count,
   indeed decides, confirming the outside review's premise for belts.

If 3 or 5 fails on q_cert, the finding is: "programs + scars at 10⁹ need a reabsorption
mechanism beyond periodic refits, at a measured rate" — a premise-level result.
