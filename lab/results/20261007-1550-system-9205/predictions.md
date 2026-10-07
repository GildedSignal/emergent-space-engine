# Predictions (written before the decisive run)

Scene (float replica, heliocentric WH, planet on an exact circular orbit, μ = 0.01, a_P = 4, belt body at e₀ = 0.05, 6 phase seeds each, 120 body orbits, truth = fixed dt at 4096 kicks per body orbit):
- A_off: a = 2.35 (far from 2:1);
- A_res: a = 2.52 (exact 2:1);
- A_det: a = 2.44 (detuned toward resonance).

Variants: fixed cadence 8/16/32/64 per body orbit; v2-style adaptive dt = Δs·f′(U_P + c) (composite f′, b = 30c) at far-field 16/orbit; window-only (kicks only when d = |r − r_P| < 1.9, exact Kepler jump between window entries, 64/orbit inside); window + 1 kick/orbit outside.

Bars (B14/B17-shaped): pump ratio (e_max − e₀) ∈ [0.8, 1.25] of truth; Δϖ error < 10% of truth's total; final |Δe| < 0.01.

1. **Fixed ladder off resonance (A_off):** 16/orbit passes all bars; 8/orbit fails Δϖ or Δe. (Explains the lab's scattered "8 for a belt" vs "16 for smooth regimes" as a resonance-distance effect.)
2. **Fixed ladder at exact 2:1 (A_res):** no fixed cadence ≤ 64 keeps pump ratio in [0.8, 1.25] for ≥ 5/6 seeds (the conjunction phase is mis-resolved; consistent with dynamics-a9c2's "inside a resonance band no rate up to 64 matches").
3. **Window-only (zero kicks outside conjunctions):** fails A_off on Δϖ (loses > 50% of the secular drift — the DC part of the perturbation binds even with no conjunction near; extends q-secular-v2's kill from averaging to windows). At A_res it keeps the pump (ratio in [0.7, 1.3]) but still fails Δϖ.
4. **Adaptive v2 cadence at ~16 far kicks/orbit:** passes all bars at A_off AND A_det at ≤ 25% of fixed-64's kick count. At A_res it comes closest of all cheap variants (pump ratio within [0.7, 1.3]) but may still miss [0.8, 1.25] — resonance may need a finer Δs or per-conjunction kicks.
5. **Window + 1 kick/orbit outside:** passes A_off and A_det at ~2–6× fewer kicks than fixed-64; at A_res it is the cheapest passer if any passer exists.

If 4 and 5 both hold: the per-body cadence rule (q-cadence), the encounter skin (b-encounter-skin) and the secular carrier (q-secular/R2) are one mechanism — U_P's spectrum decides, and one smooth f′ (already in the motion law v2) is the scheduler. If 4 holds and 5 fails, the skin is redundant given f′. If both fail at A_res, resonance is the hard special case that breaks the unification (the lens's blind spot named).
