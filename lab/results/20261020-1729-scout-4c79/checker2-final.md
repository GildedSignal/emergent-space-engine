Working...
Check complete. **Grade: gold** — written to `lab/results/20261020-1729-scout-4c79/check2.md`.

**What I did:**

1. **Reproduced** both dossier commands bit-for-bit: `grid` (0.2 s, all 49 points ≤ 7×10⁻¹⁵ vs the closed forms, along-channel exactly 1.000000, vacuum control 2.8×10⁻¹⁷) and `nonlin` (17 s, second-instrument Fermi eigenvalues and P5 rows identical). Empty patch confirmed — no engine/doc/gate file touched.

2. **Held-out verified**: `predictions.md` (17:37:12) predates `instrument.py` (17:43:42) and both outputs (17:44). P1–P4 and P6 held beyond their bars; P5 honestly reported as not cleanly measured (the one aligned case bounds the second-order term at ≤ 0.3 % through r_p/32, below the 3–10 % prediction letter).

3. **Attacked outside the author's range** — all confirm:
   - Speed decade β = 0.9999/0.99999: exactness holds (along-channel float floor ~6×10⁻⁷ = instrument, not law).
   - Compactness floor: r_p = 3M, 2.5M, **2.1M** (inside the photon sphere, vs the author's 6M edge).
   - A fully independent Riemann (finite differences **of the metric**, no shared analytic dΓ) agrees at FD-noise level, plus my own hand wedge-algebra derivation.
   - The rival γ²|1−2β²| dies **by sign alone** at its degenerate point: signed E_zz = +4.00000000 M/r³ at β = 1/√2 where the rival gives exactly 0.
   - Oblique boosts (off the author's transverse axes): middle eigenvalue ≡ 1 to 10⁻¹⁰, out-of-plane γ²(1+β²(2cos²α−sin²α)) to 10⁻¹⁴; α = 90° recovers the classic unamplified radial-infall tide.

4. **Novelty**: page's od 3 (β ≥ 0.99 instrument hole) and od 4 (out-of-plane quoted-never-measured) were open before this run; it closes both and settles the "degrade together" premise as instrument error. HISTORY.md has no prior entry.

5. **Page corrections** (two overstatements): header claimed "od 2/3/4 closed" — od 2's exit-within-5 % half is still 288f's integrated measurement (16 % [θ] at β 0.95), now qualified; and the author's Runs line pre-empted "(gold)" before grading — now "(awaiting grade)".

**Noted author misses** (in check2.md): the sign argument beats the magnitude exclusion; P6's decorative series has a wrong β⁴ coefficient (1.875 = γ³'s; correct 1.5); ψ-swing prose overstates the low end (2.86 vs "2.9"). None material — the claim, its numbers, and its scope limits are sound, and the gain (legal doll domain β 0.25 → 0.999 at zero cost, speed axis deleted from the legality rule) is adoptable in one step.
