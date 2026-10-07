# Predictions (written before the decisive re-anchoring run)

Context: the checker of run 20261007-2002-spacex-3b99 confirmed the physics but
blocked gold on (a) the hot rows not regenerable by shipped `hlive.py` and (b) the
time-to-ceiling being anchored on an inadmissible premise (fixed per-body mass
m = 10⁻¹⁰ at N = 10⁹ implies a belt of 0.1 M\*, a disk, where the test-particle
linearization breaks). This run fixes (a) and measures the scaling laws behind (b).

Model being tested (same MC as the original run): per-body element-delta spread
σ² ∝ m² · λ · t with conjunction rate per body λ ∝ n at fixed belt geometry
(surface density). Two channels: mutual (m ∝ belt, λ ∝ n) and embedded perturber
(m = m_p, λ_p = 0.1475, n-independent). σ instrument (Gaussian, from `measure_sig.py`),
cold belt σ_e = 0.01, w = 0.05, a₀ = 2.1, t = 30 orbits, seeds 1–3 (2 at n = 10000),
n ∈ {100, 1000, 10000}, plus the n = 2000 anchors from the original `hlive_sig.json`.
Script: `python3 rescale.py` (< 90 s).

## Held-out predictions

1. **Fixed per-body mass scan** (m = 10⁻¹⁰ at every n): σ_E(30) ∝ √n.
   Fit exponent on (n, σ_E) across the three n plus the n = 2000 anchor:
   0.50 ± 0.05; ratio σ_E(10000)/σ_E(100) ∈ [9.0, 11.0].
2. **Fixed total belt mass scan** (M_belt = 2×10⁻⁷, m = M_belt/n): σ_E(30) ∝ n^(−1/2).
   Fit exponent −0.50 ± 0.05; ratio σ_E(100)/σ_E(10000) ∈ [9.0, 11.0];
   σ_E(30)·√n constant across all four n within 6%.
3. **Perturber channel is N-independent**: with m_p = 10⁻⁷ present, σ_E(30) at
   n = 100, 1000, 10000 all within 3% of each other and of the n = 2000 anchor
   (7.38×10⁻³); the mutual channel contributes < 1% of the perturber variance at
   every n tested.
4. **Re-anchored verdict** (computed from the measured scaling, not the inadmissible
   fixed-m premise): at fixed M_belt the mutual walk needs t_ceiling(10⁹) > 10¹²
   orbits (never inside any game); the embedded-perturber channel carries ≥ 47 of
   the 51.2-bit ceiling by t = 30 orbits ≈ 91 game-years at any N; an embedded body
   of ~Pluto class (m_p ≈ 5×10⁻⁹ M\*) pushes per-body scar bits past the 32-bit
   budget within a 30-game-year session.
5. **Regeneration**: with the thinning moved into `hlive.py` (hot: rate/50, kicks
   ×√50, variance-preserving), `python3 hlive.py` regenerates the whole record in
   ≈ 60–80 s; the four cold/pert cases stay bitwise identical to the original
   `hlive_results.json` (thin = 1 changes no float op); the hot row's flux_check
   (sim × 50 / expected) ∈ [0.9995, 1.0005].

What would falsify the re-anchoring: a fixed-m exponent measurably below 0.5
(saturation or correlated kicks at large n), a fixed-M exponent above −0.5 (same),
or σ_E(30) in the pert scan drifting with n (a hidden n-coupling in the perturber
channel). Any of these would mean the extrapolation to 10⁹ is not supported even
inside the model, and the dossier must report the ceiling claim as unextrapolable.
