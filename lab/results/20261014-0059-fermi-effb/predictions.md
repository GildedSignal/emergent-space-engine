# Predictions (written before the decisive computation)

Cases I have not tuned on, and what I expect there. All rates per body per game-second;
costs per event; the budget is the M1's 4 performance cores; "cores" = CPU-seconds per
game-second (rtf 1). Constants: `step_log2 = 7` (crates/universe/src/ctx.rs:44),
`MIN_STEP = 128` ticks (step.rs:49), the plane's orbits (scenario.rs:115-256).

1. **The cadence law reproduces the roster endpoints (3071's natives, 0.0484 → 3×10⁻⁵/s)
   from birth constants alone**: rate = κ/P with κ ∈ [128, 256] (the power-of-two rounding
   of P/2⁷). Expect the top native (an Orbiter at ~1.15 Home radii, Home = 2⁻¹⁸ M☉ ≈ 1.28 M⊕)
   to land in [0.023, 0.046]/s (measured 0.0484: within 2×), and the roster floor to be the
   fastest hauler (a = 0.5 AU, P ≈ 0.35 yr → [1.2, 2.3]×10⁻⁵/s; measured 3×10⁻⁵: within 2×).
   A period-independent clock floor would instead make both endpoints independent of P —
   I predict it does NOT (the floor moves with the fastest hauler's period).
2. **7497's measured Orbiters 202–223 kicks/orbit lies inside [128, 256]** (the rounding
   band of 2⁷ per radial period). If it lay outside, the step law is not the cadence.
3. **Composition**: at 10⁹ quiet-belt bodies the encounter cascade (skin on, 0.077 cores per
   10⁴-cell, 90fb) exceeds every other CPU term by ≥ 10³ at Carlson pricing (30 µs/event):
   encounters ≈ 7.7×10³ cores vs kicks ≤ 1.1 cores (a9d7 rate) or ≤ 0.4 cores (code-derived
   κ/P at year periods).
4. **Independent re-derivation of 367f's quiet-belt number**: 10⁹ × 3.55×10⁻⁵ (a9d7) × 231 µs
   (shipped kick) = 8.2 ± 0.5 cores (367f published ~8.3). If my composition differs by > 10×,
   one of us misread a constant.
5. **Held-out, falsifiable only when the tier is wired** (the encounters crate is not in the
   plane yet, H0216): the wired belt's first CPU wall lands at N ≈ 5×10⁵ bodies with the skin
   on (budget 4 cores / 7.7×10⁻⁶ cores per body per game-second), and at N ≈ 4×10⁴ without it.
   The N ladder should meet the promotion-stream wall first (~10³, 367f), then the hot D-slope
   (2.8×10⁴, 790b), then this — an order below the memory wall's 10⁹ (quiet 2.6–5 GB).
6. **The two rails**: the kick-cost gap (10^3.3) is the *hot* rail's gap (battle/member
   events at 0.041/member/s: ceiling 2.8×10⁴ today → ~5×10⁸ at the 42–55 ns floor) and
   contributes ≤ 1.1 cores to the *cold* 10⁹ CPU at Carlson pricing whatever the rate
   constant (a9d7's 3.55×10⁻⁵ or code-derived 6×10⁻⁶–1.2×10⁻⁵ at year periods).
