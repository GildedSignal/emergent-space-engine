# Predictions — what happened (written after the run; the predictions above were frozen before it)

Scorecard, by the grid in `grid.txt` / `grid-d.txt` (horizon 2^35 ticks = 169,239 game-s each):

1. **Pump unconditional — HELD (6/6 + 2 sub-check).** Every flight whose detector fired crossed and
   pumped: A-L15 (γ₀30), B-γ₀ 10/3/1.5/1.1 — γ_min ≤ 1.0005 at every crossing, then monotone rise
   (end γ = g_max_post on all six: 4.1, 44.0, 58.3, 61.7, 63.1; none captured, none at rest, zero
   refusals). D-L15 crossed sub-check (γ_min 1.0000 within one 2^24 window) and pumped to γ 64.0;
   D-L8/L6/L5 crossed sub-check and drifted out at γ 1.12/1.008/1.002. The cut control never got to
   test its cut (L8 from γ 30 doesn't reach rest in the horizon) — P1's pass stands from its own gate.
2. **The ruler — WRONG in its strong form, corrected by the data.** γ_min does not track Ψ₀ across
   knobs: off45 (Ψ₀ 0.036) crossed at γ 1.723 while B-g3 (Ψ₀ 0.065) crossed at 1.0003. The
   first-order ruler is the **transverse rapidity at hold start, η₀·sinθ**: off45's leftover
   cosh(η₀ sin46.6°) = cosh(1.27) = 1.92 vs measured 1.72 (gravity's rotation, the Ψ term, shaves
   it); all θ=0 rows have η₀ sinθ = 0 → γ_min 1.0000–1.0005 with Ψ₀ spanning 0.0008–0.57 — the Ψ
   term is invisible at 4 decimals in this grid. Measured Δφ_v is NOT the ruler either: it reads
   exactly π on every crossing (the thrust-cancellation flip of v̂, not gravity) and 3.04 on the
   from-orbit rows.
3. **A-row — half wrong, my arithmetic not the physics.** L15 crossed (158,744 s); L12 did NOT cross
   in the horizon (γ_min 25.75 still falling at 169,239 s: root-time braking needs sinh(η₀)/α =
   6.4×10⁵ s ≈ 4× the horizon — I dropped the γ̄ factor when pre-computing). L8/L4/L2 barely brake
   (γ_min 29.74/29.99/30.00). No crash basin exists on this axis: no A flight ever left the start
   radius band (minR/R 1.0990 all).
4. **B-row — FALSIFIED, both counts.** γ₀ 1.1 and 1.5 both crossed cleanly (γ_min 1.0000, Ψ₀
   0.57/0.35) and pumped; no crash, no γ_min ≥ 1.05. The near-Home race I feared is invisible:
   the pump-up to γ ≥ 1.1 ejects the ship through Home's SOI in seconds (doll0 = star on every
   B/A/C hold), so the braking never happens near the planet.
5. **C-row — held where tested; two cells died before the burn.** off90: pumps monotonically from
   the start (γ 3.02 → 5.01, no rest — as predicted; 12,762 refusals, alive). off45: crossed at
   γ 1.72 then pumped (γ 2.42; 13,386 refusals, alive). off135/off180: **lost during the turn
   phase** — `Kick(0): Space(Range)` at 0.9435 c (= γ₀, before any reverse key) — the far-field key
   wall (the baselined `range` red) eats the long turns at escape speed; prediction 5 never got
   its test there.
6. **Refusals/faults — FALSIFIED.** Range refusals in braking phases: A-L2 (γ 30.0, 0.9994 c, 1
   refusal, lost) — braking too weak to bind before the ship crosses the far-field wall; and the
   two turn-phase deaths above. Also unpredicted: off45/off90 accrue 12.7–13.4k refusals yet stay
   alive and keep accelerating (state manifestly not frozen).

**The row the predictions missed entirely (run after seeing the grid): D, held reverse from the
start orbit (no pump-up) — the actual arrival maneuver.** Λ = thrust/local-weight at the start
orbit (8.1 m/s²) orders it: L0 (Λ 0.43), L2 (1.7), L4 (6.8) all **crash into Home** (5.35–8.47
km/s relative, world time 6:03–12:38, minR/R 0.946–0.970); L5 (Λ 13.6) grazes at 1.014 R and
escapes at γ 1.002 — the separatrix specimen; L6 (27) dips to 1.059 R and drifts out at γ 1.008;
L8/L15 escape cleanly (γ 1.12 / 64.0 at horizon). The crash/escape boundary is Λ* ∈ (6.8, 13.6).
Not predicted because I derived the endgame as a thrust-vs-turn race and never asked
thrust-vs-fall at the planet — the D-row was added only after the grid showed no crash basin
anywhere else.
