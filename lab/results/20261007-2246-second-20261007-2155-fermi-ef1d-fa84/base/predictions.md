# Predictions (written before the decisive run of hlive.py)

Cases not tuned on. Fiducial belt from fermi.md: D ≈ 1.9×10⁻²² m²/s³, q_v = 10⁻³ m/s, P = 1.64×10⁸ s, N = 2²⁰ (rates are intensive; extrapolate ×10⁹).

1. **Crossing rate (diffusion):** quantum crossings per body per orbit = D·P/q² ≈ 3×10⁻⁸ (within a factor of 2 from the measured count / orbits; the toy's strong-tail-exact + Gaussian-sea sampler must land there, else the sampler is wrong).
2. **Scarred fraction** grows ∝ t while ≪ 1 (first-crossing process): after T orbits, frac ≈ 3·(2/π)^½·√(DT)/q·… order √(2DT)/q per dim ⇒ ≈ 4×10⁻⁴ after 2000 orbits; ≪ 1 always in the run.
3. **Bits per scarred body ≤ 12** throughout the fiducial run (Elias-gamma of a few-quantum residual + sign), so total bits/body ≪ 0.01 at 2000 orbits.
4. **Re-fit control:** re-fitting the marginal (subtracting the ensemble mean) removes < 10% of the stored bits in the fiducial case — re-fit absorbs drift, not spread (H(X+ε) ≥ H(X)).
5. **No-encounter control:** with D = 0 the scarred fraction stays exactly 0 and zero bits are stored (any nonzero output is a leak in the toy).
6. **Held-out (not tuned):**
   a. Dense belt (n ×100 ⇒ D ×100): crossing rate ×100 exactly (linearity in n), scarred fraction ×10 (∝ √D) — still ≪ budget at 2000 orbits.
   b. Hot chaos (τ_L = 10⁴ orbits, same D): stored bits/body grows ≈ linearly at 1/(τ_L ln 2) ≈ 1.44×10⁻⁴ bits/orbit once saturated, i.e. ≈ 0.3 bits/body after 2000 orbits — two orders above the diffusion case, confirming chaos, not encounters, is the distinction engine.
7. **Extrapolation to 10⁹ at the plan budget:** new bits per game-second ≤ 1 at rtf 10⁶ (diffusion) and ≤ 2×10³ bits/s (hot chaos, before tube-out); neither approaches 4 GiB in one hour.

If 1 or 5 fails, the measurement is VOID (broken instrument). If 6b fails low (< 10× the diffusion case), the "chaos is the engine" claim is wrong and the risk register keeps encounters as a live term.


**Addendum (pre-run correction, before any execution).** Re-deriving the levels (not just rates) before running: pure diffusion at 2000 orbits gives σ ≈ 0.01 quantum, so the diffusion numbers above stand or shrink. The hot-chaos level at 2000 orbits, τ_L = 10⁴: σ² ≈ (D τ/2)(e^{2t/τ}−1) ≈ 1.2×10⁻¹⁰ m²/s² → σ ≈ 0.011 quantum → **revised 6b: ≈ 0.01–0.05 bits/body after 2000 orbits** (my original 0.3 conflated the saturated growth rate 1/(τ ln2) with the level). The two-orders-over-diffusion ordering claim is unchanged. The budget-crossing time in fermi.md term 3 is level-based: t ≈ 8τ ≈ 8×10⁴ orbits ≈ 4×10⁵ yr sim (≈ 5 months of play at rtf 10⁶); corrected in fermi.md.