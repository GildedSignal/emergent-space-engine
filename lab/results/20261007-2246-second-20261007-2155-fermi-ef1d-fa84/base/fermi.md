# The 10⁹ budget on the M1, decomposed (Fermi lens, run 20261007-2155-fermi-ef1d)

Question, one sentence: **at 10⁹ bodies, which term of the budget (memory stock, distinction flow, kick compute, encounter discovery, fill, gather) breaks first, and by how much?**

Machine (HANDOFF): 8 GB unified (plan budget 4 GiB for the universe), ~10¹⁰ simple ops/s CPU, ~60 GB/s, GPU 7-core. Plan: one hour of play, 30 FPS. Plane target rtf ≥ 100 ("and more"; galaxy view implies 10⁴–10⁶). Belt parameters (fiducial, from the belt gold components-98bc family): N = 10⁹, R = 3 AU, ΔR = 1 AU, h = 0.05 AU (V ≈ 0.94 AU³), peer mass 10¹² kg, v_circ = 17.3 km/s, P = 5.2 yr = 1.64×10⁸ s, v_rel = 2 km/s, velocity quantum q_v = v·2⁻²⁴ ≈ 10⁻³ m/s (32-bit fractional certificate; sensitivity ±4 bits below).

## Terms

**1. Memory stock — the program.** Measured (gold 98bc): 0.126 bits/body → 10⁹ × 0.126 = 15.6 MB. Nothing.

**2. Memory stock — scars (H_live).** Encounter velocity diffusion (Chandrasekhar, exact per body):
D = 2π n (2Gm_p)² lnΛ / v_rel, with n = N/V = 3.4×10⁻²⁵ m⁻³, 2Gm_p = 1.33×10² m³/s², lnΛ = 10:
D ≈ 3.0×10⁻²² m²/s³ (binned integral, verified by the run). The lattice-crossing rate D/q² ≈ 4.9×10⁻⁸/orbit is the **saturated** rate; the early first-crossing rate is 0 until σ(t) ~ q, i.e. t* = q²/4D ≈ 8.3×10¹⁴ s ≈ 2.6×10⁷ yr — **measured: zero scars and zero crossings in 10⁴ yr, also at 100× density** (first distinction then at ~2.6×10⁵ yr sim ≈ 96 days of play at rtf 10⁶).
σ_v after 1 Gyr: √(Dt) ≈ 3.1 quanta → ~11 bits/body, ~1.4 GB at 10⁹ — still inside 4 GiB.

**3. Distinction flow — chaos, not encounters.** Regular (secular, resonant-regular) evolution is compiled into the program by re-parameterization; only exponentially diverging evolution makes irreducible bits. Level (not rate): σ²(t) = (D τ/2)(e^{2t/τ}−1), so the residual crosses quanta at t ≈ 4τ and the 34 bits/body line (4 GiB) at t ≈ 8τ ≈ 8×10⁴ orbits ≈ 4×10⁵ yr sim ≈ **5 months of play at rtf 10⁶** (τ_L = 10⁴ orbits, seeded by encounter noise). Only τ_L ≲ 10³ orbits (planet-crossing Wisdom-gap chaos) breaks the budget within weeks of play — those are a small strip whose members tube out individually.
**3-measured.** τ_L = 300: 6.57 bits/body at 10⁴ yr (97% scarred), re-fit removes 0.01%; a fully chaotic belt reaches 34 bits/body at ~1.5×10⁴ yr sim (5.5 days of play at rtf 10⁶), but real τ_L ≲ 10³ populations are resonant strips whose members tube out at 16 B/body, capped.

**4. Kick compute.** 10⁹ × (0.3–32) kicks / P: 200–2×10⁴ kick-events/s of sim time. At rtf 100: ≤ 2×10⁶/s; at rtf 10⁶: ≤ 2×10¹⁰/s → **breaks the CPU at rtf 10⁶ with raw per-kick WH (32/orbit), fine at 0.3 averaged**. Kicks bound compute before anything else does — consistent with the board's own ranking.

**5. Encounter discovery.** Real encounters: λ(b < b_q)… negligible rate (crossing rate above). But certificate *maintenance* is per body per orbit (phase-neighbour k ≈ 4): 10⁹×4/1.64×10⁸ s = 24 checks/s sim → 2.4×10⁷/s at rtf 10⁶ ≈ 2.4×10⁹ ops/s ≈ 25% of CPU. **Second binding term at galaxy rtfs, invisible at the plane's rtf 100.**
**6. Fill.** One-time 10⁹ program evaluations ≈ 10¹⁰–10¹¹ ops ≈ seconds. Not binding.

**7. Gather (the view).** Reads cells/aggregates on the light cone, not bodies. Not a 10⁹ term unless the view is per-body; flagged, not estimated here.

**Re-fit ≠ reabsorption.** Convoluted entropy H(X+ε) ≥ H(X): re-fitting the program's marginal absorbs the coherent drift (mean shift) but cannot remove the spread of the walk. True reabsorption is (a) sub-quantum aggregation (the accumulator, principle 6), (b) the scar→tube packing cap, or (c) lossy coarsening of never-observed scars (an error-type choice, not made here).

## Verdict (estimates; measured in dossier)

At the plan's budget (rtf ~100, one hour, 4 GiB) **every 10⁹-belt term sits ≥ 3 orders of magnitude inside the machine**. The board's premise "distinctions, not the body count, decide whether 10⁹ fit" is confirmed with the opposite sign for the cold belt: background H_live is a rounding error (≤ 10 bits/body at 1 Gyr); the body count itself never tests 4 GiB because the program is 0.126 bits/body. The terms that do bind, in order: kick cadence (rtf ≥ 10⁶, raw 32/orbit), certificate maintenance (rtf ≥ 10⁶), tracked populations (fleets: small N, huge rates, tube-cap fine). **10⁹ cold-belt bodies fit with ~2 orders of margin; the risk register should move H_live from "decides whether 10⁹ fit" to "decides whether tracked hot populations fit".**
