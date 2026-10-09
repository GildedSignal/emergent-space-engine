# Predictions — plunge tubes via one-real-root Darwin panels

Written before the decisive experiment. Nothing below is tuned: every number
comes from the derivation only (Schwarzschild, M = 1, u = 1/r, cubic
F(u) = 2L²u³ − L²u² + 2u + E² − 1, one real root u₁ and complex pair a ± ib;
substitution u = u₁ + ρ sin²ψ, ψ ∈ [ψ_a, π/2], ρ = u_h − u₁, u_h = 1/2).

Cases (held out, none tuned):
- A: E = 0.8, L = 3.8 (E < 2√2/3: no critical orbit exists; plunge from apoapsis)
- B: E = 0.97, L = 0.9·L_c (plunge from apoapsis, L_c defined)
- C: E = 1.0, L = 0.9·L_c (direct capture, L_c = 4)
- D: E = 1.2, L = 0.99·L_c (high-speed direct capture)
- E: E = 2000, L = 0.99·L_c (γ ≈ 2000: the refused "flying past γ≈2000" class)
- F: L = 0, E = 1 (pure radial fall, cubic degenerate)
- G: photon, b = 0.9·b_crit (capture; b_crit = 3√3)
- C-scan: E = 1, L = L_c(1 − 10⁻ᵏ), k = 1…7 (no full oracle; divergence scan)

Predictions:

P1 (exactness): for cases A–E, G the ψ-panel tube (fixed 512 panels × GL4,
cumulative sums, one Newton solve per sample) matches a 40-digit mpmath
`odefun` oracle on r(τ), φ(τ), v(τ) at 32 held-out τ per case to better than
1e-9 relative. The identity v'(ψ) = (1 + L²u²)/(E + √F)·dτ/dψ stays smooth at
the horizon, so v(ψ_h) is finite and no log divergence appears in any
non-critical case.

P2 (failure mode): Δφ (turning point or entry → horizon) diverges ~ linearly
in ln(1/(1 − L/L_c)) as L → L_c⁻: Δφ(k+1) − Δφ(k) ≈ constant for k = 1…5,
and the panel machinery needs n ∝ Δφ panels to hold accuracy — cost grows
with winding, not O(1), near critical.

P3 (root precision): u₁ and the pair a ± ib from double-precision np.roots
degrade as the pair coalesces (discriminant → 0 at L_c): error stays < 1e-8
down to 1 − L/L_c = 1e-4 but exceeds ~1e-9 below 1 − L/L_c = 1e-6. The
integer law needs exact Cardano (one real root is the non-degenerate casus:
real cube roots, no trigonometric case) or the asymptotic log form there.

P4 (cost): after compile, one sample (given τ: bracket + Newton in ψ) costs
< 20 µs in Python, independent of winding for |1 − L/L_c| ≥ 1e-3; a DOP853
rtol = 1e-12 integration of the same plunge costs ≥ 1 ms (≥ 50× more per
trajectory, and it must be redone for every sample).

P5 (radial): F degenerates at L = 0; with v' = 1/(E + √F) the same smoothness
holds; the case is handled by the same code with u₁ the single real root of
the linear-in-u remainder (case F checks no special-casing beyond the
root-finder).

Kill criteria: any of A–E, G above 1e-8 vs the oracle, or v(ψ) unbounded at
the horizon, or per-sample cost growing with winding away from critical ⇒ the
one-real-root ψ-tube is the wrong representation for the engine's plunge gap.
