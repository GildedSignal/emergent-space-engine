# Predictions (written before the decisive run)

Question: does the rate of live distinguishing information (H_live) that belt encounters
create — scars per body per game-second × bits per scar — grow fast enough to break
10^9 bodies in 8 GB (32 bits/body budget at half the RAM)?

Model (stated so the checker can attack it): impulse-approximation Monte Carlo of a
Keplerian belt (G = 4π², M* = 1, a ≈ 2.1 AU-equivalent, width 0.1), encounter flux from
the local surface density and shear+eccentricity relative speed, deflection δv = 2Gm/(b·v_rel)
with random geometry, accumulated per body as integer deltas (ΔE, ΔL, Δω) against the
population program, quantized at relative widths Q ∈ {2⁻¹⁶, 2⁻²⁰, 2⁻²⁴} for E and L and
2π·2⁻²⁴/2⁻²⁸ for ω. Cross-check: simulated encounter rate must match the analytic flux
Γ = n·π·b²·v_rel·T within 20% (else VOID by my own hand).

Cases: cold belt (σ_e = 10⁻², equal masses 10⁻¹⁰ M\*), hot belt (σ_e = 0.1),
embedded perturber (one body at 10⁻⁷ M\*, i.e. lunar-to-Pluto class), and the
carry/spill accounting at 2⁻²⁰ relative.

Held-out predictions (not tuned on):

1. **Scar rate, cold belt:** first-scar fraction per body per orbit < 10⁻⁴ at Q = 2⁻²⁰
   (sub-quantum kicks accumulate in the carry; spillover is rare). Over a 10-year
   session (≈ 3.5 belt orbits) fewer than 0.05% of bodies carry any scar at all.
2. **Scar rate, embedded perturber:** ≥ 100× the cold rate (close encounters scale with
   the perturber's mass: b_min for a 1-quantum kick ∝ m, so flux ∝ m² — a 10³× mass
   gives ~10⁶× the strong-encounter rate at fixed quantum, softened by the belt's
   geometry; I predict 10²–10⁴×).
3. **Bits per scar:** 25–45 bits at Q = 2⁻²⁰ relative (Δω's angular width dominates at
   coarse quanta; ΔE dominates at fine). At the law's own Q48 the naive integer scar is
   48+32+32 = 112 bits — the idiot index of storing scars at law width instead of
   behaviour width is ≈ 3–4×.
4. **Saturation, not growth:** per-body scar entropy saturates (random walk bounded by
   the belt's own element spread) within ~10³ orbits; bits/body asympotes below 32 in
   the cold case — H_live is NOT the binding constraint for a cold belt; it binds
   through hot regions and massive perturbers.
5. **Reabsorption split:** the coherent (mean-drift) part of the scar information is
   < 1% of the identity-scatter part for a strangers' belt (a program refit absorbs
   almost nothing); reabsorption only matters for families/convoy programs.
6. **Verdict:** cold belt at 10⁹ bodies stays under 32 bits/body for > 10⁵ game-years;
   a belt with one embedded 10⁻⁷ M\* perturber exceeds it within 10–10³ game-years
   unless scars are stored at behaviour width, not law width.

What would make me wrong: if single conjunction kicks at behaviour quantum are already
≥ 1 quantum (my δv/v arithmetic off), prediction 1 flips to "first conjunction scars
the pair" and the belt needs the refit machinery immediately.
