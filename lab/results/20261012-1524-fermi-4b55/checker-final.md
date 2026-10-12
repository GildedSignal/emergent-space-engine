Working...
Check complete. **Grade: silver** — written to `lab/results/20261012-1524-fermi-4b55/check.md`, nothing else in the run folder touched.

**What I did:**
- **Reproduced bit-for-bit** in a scratch copy: `h_live_fermi.py` (139 s) and `crosscheck.py` (75 s) — every stored number, including the superseded first-version P3 (54.4/body/orbit) and the adjudicated SOI count (1197).
- **Ran four adversarial cases** (brute-force dense-time truth, sign-fixed Newton, 60/200-orbit windows, headline regeneration).

**Findings:**
1. **Headline off by 460×.** The dossier's own inputs give 0.0365 rebinds/s at 10⁹, not 36.5/s (a 10³ slip), and that rate is itself 2.2× low: `crosscheck.py` §2's planet Newton is sign-flipped (`dn = npp − nb` against residual `λ_body − λ_planet`, so `t −= dth/dn` diverges). Brute-force truth: **1.30×10⁻² SOI transits/body/orbit**, window-stable to 200 orbits — which lands *inside* the author's pre-registered P3 range; the prediction held, the instrument didn't.
2. True H_live ≈ 20 bits/s (rebinds ≈ player ≈ 10 bits/s, so "player nil" flips), saturation ≈ 77 orbits not 167; the stored JSON still carries the first bug's 331.7/s table, never regenerated.
3. The structure survives correction and is strengthened: mutual encounters informationally inert at ship mass (12-order margin, P4 reproduced), contacts nil, the only 8 GB-scale term is post-repopulation mixed entropy. Novel (HANDOFF: "not measured yet"), on a named board bottleneck.

Not gold by the lab's own rule — a headline the log contradicts — but one hour of work (fix the sign, regenerate the table) from it.
