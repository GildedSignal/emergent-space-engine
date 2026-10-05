# Predictions (written before the decisive run; 2026-10-05)

Oracle: equatorial Kerr derived from the metric only (Boyer–Lindquist, M = 1, χ = a):
g_tt = −(1−2/r), g_tφ = −2a/r, g_φφ = r²+a²+2a²/r, Δ = r²−2r+a².
Independent of the branch's kerr.rs: no BPT polynomial, no closed form, is trusted until it is
checked against the metric machinery (circular orbits from Ω = ±1/(r^{3/2}±a), constants by
lowering, u^t by 2×2 solve AND by normalization, future = u^t > 0 = E − ωL > 0, ω = −g_tφ/g_φφ).

P1 Anchors. My machinery reproduces BPT's ISCO closed form, r_ph± = 2{1+cos[(2/3)arccos(∓a)]},
the horizon r_± = 1±√(1−a²), ω_ZAMO = 2ar/A and α = √(Δr²/A), at χ ∈ {0.5, 0.9, 0.998}, both
senses, to < 1e-12 relative (40-digit mpmath).

P2 Timelike existence. At r = (r₊+2)/2, ZAMO-frame v_φ = −0.9995 (counter-rotating): E < 0,
L < 0, future-directed (u^t > 0 computed two ways), at every χ. Every future-directed E < 0 state
found anywhere lies at r < 2, has P = E(r²+a²)−aL > 0, and its allowed arc reaches the horizon
(it plunges).

P3 Null existence (the Penrose process). Split of a v_φ = 0.6 parent at the same r: the backward
photon has E < 0, L < 0 and ε_ZAMO > 0 (future-directed), E_forward > E₀, E_f+E_b = E₀; at r = 3
the same split has E_back > 0. So future-directed negative-energy null geodesics exist inside the
ergosphere — the Penrose process is real in the equatorial plane.

P4 The disputed claim. No BOUND (two turning points, periapsis outside the horizon) fully
future-directed equatorial orbit with E < 0 exists, timelike or null, for any χ ∈ [0.01, 0.9998]
(scan: |E| ∈ [1e−3, 1), |L| ∈ [1e−3, 1e3], all cubic root patterns). The builder's conclusion
stands; their justification ("dt/dτ has the sign of P") is wrong as a statement about the metric
(sign(u^t) = sign(E−ωL) = sign(αε_ZAMO), not sign(P)), but on the allowed set R ≥ 0 the two signs
agree, so the scan's verdicts are correct. The doc's phrasing "the solutions with E < 0 are all
time-reversed" overstates: only the BOUND ones are past-directed; the tubes are future-directed.

P5 Equivalence check. On ≥ 10⁶ sampled states with R ≥ 0 and r > r₊: sign(u^t) = sign(P) with
zero exceptions; u^t from the 2×2 solve and from A(E−ωL)/(r²Δ) agree to ~1e-14; every state with
E < 0 and r ≥ 2 is either forbidden (R < 0) or past-directed (u^t < 0).

P6 Planted laws (against the row's six criteria).
 (a) No frame dragging (ω := 0): answers dφ/dt < 0 for counter-rotating tubes inside the
     ergosphere → fails criterion 3; answers E = αγ > 0 for them → fails criterion 4(a).
 (b) Schwarzschild fudged to the ISCO (a := 0, ISCO restored): b₊ = b− = 3√3 in both senses,
     against Kerr's split b± at χ = 0.998 → misclassifies captures at x ∈ {0.97, 1.03} of b_c
     → fails criterion 2(d); ω = 0 against Kerr's ω → fails criterion 3's 1e-6 rates.
 (c) Split that does not conserve (fragments rounded, or E_back := |E_back|): fails 4(c)'s
     8-ulp conservation or its E_back < 0.

P7 Criterion 4(b) under my independent test: the (E, L) of P2 re-asked at r' ∈ (2.2, 30) are
refused for the true reason (E − ωL < 0 or R < 0), so "nowhere else" holds.
