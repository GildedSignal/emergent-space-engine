# Predictions — written before the decisive run

All numbers below are hand Fermi from Bardeen's closed forms (photon circular
orbit r_ph = 2M{1+cos[(2/3)arccos(∓a/M)]}, b_c = −(r³−3Mr²+a²r+a²M)/(a(r−M))),
done before the instrument ran. The instrument (exact equatorial Kerr null
geodesics, RK4 on Carter's first-order system) decides. Held-out cases for the
checker: **a = 0.5 and a = 0.998 at r_o = 20M and 6M**, and **a = 0.9 at
r_o = 3.2M** (near-side, where |b_c−|·√(1−2/r_o)/r_o may exceed 1 and the
retrograde edge wraps past the tangential direction).

- **P1 (a = 0 controls).** Shadow arc at r_o = 20M ≈ 8.3–8.4% of the sky
  circle (039d measured 7.9% by their pixel criterion); at 6M ≈ 25.0%; edges
  symmetric ±arcsin(3√3·√(1−2M/r_o)/r_o). Deflection at b = 100M ≈
  4/b + (15π/4)/b² = 0.041178 rad; the RK4 must match to < 10⁻⁵ relative.
  Photon spiral: a ray launched with b just outside 3√3M winds > 2 full turns.
- **P2 (a = 0.9M, r_o = 20M).** Edges α⁺ ≈ +0.136 rad, α⁻ ≈ −0.288 rad;
  |α⁻|/|α⁺| ≈ 2.1; arc ≈ 6.7% of the circle vs the χ-blind law's 8.4%
  symmetric; arc centre displaced toward the prograde side by ≈ 0.076 rad
  (≈ 4.4°). This displacement shifts every near-hole star's bearing, not just
  the shadow.
- **P3 (a = 0.9M, r_o = 6M).** α⁺ ≈ +0.47 rad, α⁻ ≈ −0.95 rad; arc ≈ 22.6%
  vs χ-blind 25.0%; displacement ≈ 0.24 rad (≈ 14°).
- **P4 (rim wall).** The prograde edge's log-divergence coefficient is larger
  than Schwarzschild's (photons wind longer near r_ph⁺ = 1.56M than at 3M);
  the relative b-resolution needed for 10⁻³-rad image placement at r_o = 6M,
  a = 0.9 is ≈ 10⁻⁷–10⁻⁶, i.e. 2–10× finer than Schwarzschild's measured
  1.2×10⁻⁶–4.7×10⁻⁶ (039d), and the two sides differ by that same factor.
- **P5 (the shipped law).** `kerr::deflection(χ, b)` is sense-aware (signed b
  enters `Constants::photon`), returns `None` exactly between the two critical
  b's, and matches the float oracle within its quantization for |b| ≳ 3M. If
  so, the lopsided bend *can* be carried by the memo, and the question moves
  to the rim: at what quantized key width does the memo break the sky
  placement. If it instead folds |b| or loses the sense, the lopsided shadow
  cannot emerge from the memo as built — a kill on law.md L32's "none is a
  special case".
