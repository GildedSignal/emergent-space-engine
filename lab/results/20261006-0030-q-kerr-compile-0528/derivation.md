# Equatorial Kerr in Darwin's phase: the derivation

Run 20261006-0030-q-kerr-compile-0528. Units M = c = 1. Equatorial plane θ = π/2,
Boyer–Lindquist. The claim to verify (Opus memo, "Adequate, confirmed: Kerr"):
Darwin's ψ carries over from Schwarzschild and only the integrands change.

## 1. The metric and the constants

Equatorial line element (Σ = r², Δ = r² − 2r + a², a = χM = χ):

    ds² = −(1−2/r) dt² − (4a/r) dt dφ + (r²+a²+2a²/r) dφ² + (r²/Δ) dr²

Conserved E = −u_t, L = u_φ. Radial potential (Chandrasekhar's form):

    r⁴ (dr/dλ)² = R(r) = [E(r²+a²) − aL]² − Δ[r² + (L−aE)²]

## 2. Mino time makes the cubic Schwarzschild's

With **standard Mino time** dσ = dλ/Σ = u²dλ (u = 1/r; λ = proper time for
μ = 1, affine for photons), du/dσ = −(dr/dλ), so (du/dσ)² = R u⁴. Substituting
u = 1/r and expanding:

    (du/dσ)² = (E²−μ²) + 2μ²u − [L² − a²(E²−μ²)] u² + 2(L−aE)² u³

The u⁴ terms cancel identically because (Ea² − aL)² = a²(L−aE)², and the u²
coefficient collapses as −2aE(L−aE) − (L−aE)² − a²μ² = −[L² − a²(E²−μ²)].
This is exactly Schwarzschild's (du/dσ)² = (E²−μ²) + 2μ²u − L²u² + 2L²u³ under

    L² → L² − a²(E²−μ²)      (call it L̃²)
    2L² → 2(L−aE)²           (call L' = L−aE)

— the Opus memo's statement, re-derived and verified independently (the memo's
parenthesis "dτ = r²dλ" has the fraction inverted; standard Mino time dσ = u²dλ
is what makes the statement true).

## 3. Darwin's phase ψ, unchanged

Factor the cubic by its roots u₁ < u_p < u₃ (u_p periastron, u₁ apastron for
e < 1, u₁ < 0 for e > 1, u₃ the inner barrier) and scale the clock, s, by
dσ = ds/|L'|:

    (du/ds)² = 2(u−u₁)(u_p−u)(u₃−u),   u = (1 + e cos ψ)/p,
    e = (u_p−u₁)/(u_p+u₁),  p = (1+e)/u_p = R(1+e)  (R = periapsis radius)

Then (u−u₁)(u_p−u) = (e²/p²) sin²ψ = (du/dψ)², so

    (dψ/ds)² = 2(u₃−u)              — universal, bound or unbound.

In crate variables x = R/r = k + (1−k)cos ψ, k = 1/(1+e), q = M/R: at a = 0,
2(u₃−u) = 1 − qA with A = 6k + 2(1−k)cos ψ, exactly ENVELOPE.md's g².

## 4. The integrands (what changes relative to Schwarzschild)

With P = E(r²+a²) − aL, the first-order equations are Σ dφ/dλ = (L−aE) + aP/Δ
and Σ dt/dλ = a(L−aE) + (r²+a²)P/Δ; dividing by dσ/dλ = r⁻² and ds/dψ:

    dφ/dψ = [(L−aE) + a(E − a(L−aE)u²)/(1−2u+a²u²)] / (|L−aE| √(2(u₃−u)))
    dt/dψ = [a(L−aE) + (1+a²u²)(E − a(L−aE)u²)/(u²(1−2u+a²u²))]
              / (|L−aE| √(2(u₃−u)))
    dτ/dψ = 1/(u² |L−aE| √(2(u₃−u)))                     (μ = 1 only)

All three are [rational function of u] × g(u), g = 1/√(2(u₃−u)) — the same
structure the crate compiles today. Checks:
- a = 0: dφ/dψ = g = 1/√(1−qA); dτ/dψ·R^{−3/2} = √D g/x² with D = k−q(3k²+(1−k)²),
  L² = μ²/(qD); dt/dψ·R^{−3/2} = √(k(1−2q)(1+2q(1−2k))) g/((1−2qx)x²),
  E²R/L²·... = k(1−2q)(1+2q(1−2k)). These are ENVELOPE.md's three integrands
  verbatim (selftest: agreement to 4×10⁻⁴⁰ at 40 dps, i.e. to rounding).
- Photons μ = 0: (du/dσ)² = E²[1 − (b²−a²)u² + 2(b−a)²u³], b = L/E: the same
  cubic with e = 1 (u₁ = 0); only b and χ enter. The double-root condition
  reproduces Bardeen's r_ph = 2(1+cos(⅔ arccos(∓a))) and b± (selftest: ISCO
  and b± match the closed forms to all printed digits).

## 5. Families covered by the one parametrization

- **Bound** (e < 1, 0 < u₁): ψ ∈ [0, π], mirrored: the compiled cycle
  increments Δφ, Δt, Δτ.
- **Unbound** (E > μ): u₁ < 0 < u_p < u₃; the pass runs ψ ∈ [−ψ∞, ψ∞],
  cos ψ∞ = (p·0−1)/e = −1/e. Δφ converges at x → 0 (finite deflection); Δt and
  Δτ diverge as x⁻¹ (infinity has no finite arrival clock — ENVELOPE's rule),
  so passages quote windowed Δt, Δτ between finite radii.
- **Photons**: e = 1 exactly; Δφ finite (the bend), Δt windowed, Δτ none.
- **Plunging** (one outer turning point u_a, then u grows past u₃ to u₊):
  ψ stops being monotonic at u₃, so the plunge is integrated in u:
  Δφ = ∫ Φ(u) du/√R(u), Δτ likewise, from u_a to u₊; both finite.
  Boyer–Lindquist Δt diverges logarithmically at u₊ with dφ/dt → Ω_H — a
  coordinate fact, not a compiler failure; the crate already keeps "horizon
  arrival times outside this compiler".
- **Negative energy (ergosphere)**: no algebraic change — E < 0 simply makes
  c₀ = E²−μ² ∈ (−1, 0). Such orbits are confined (u = 0 forbidden), exist only
  for r < 2 (verified numerically), and plunge (B19's claim; verified).

## 6. Shape variables and the memo question

At fixed χ the bound family is 2-dimensional. The map (E, L) ↔ (k, q) is
locally bijective per sense (prograde/retrograde branch), because the two
turning-point equations cubic(u_p) = cubic(u_a) = 0 determine (E, L) from
(u_p, u_a) = (q, q(2k−1)) up to branch. Root identities (M = 1):

    u₁+u_p+u₃ = L̃²/(2L'²),  Σpairs = u₁u_p+u₁u₃+u_pu₃ = μ²/L'²,
    u₁u_pu₃ = −(E²−μ²)/(2L'²)

so L'² = μ²/Σpairs, E² = μ² − 2L'²u₁u_pu₃ — the same root-to-constants map the
crate runs in integers (law.md "Motion" 2), with u₁ u_p u₃ now Kerr's.

Consequences for the memo: one memo per (k, χ) **per sense** — sense is one
extra bit in the key, χ is one constant per doll (law.md line 31), and q
remains the series variable. The times still scale as R^{3/2}·f(k,q,χ).

## 7. Weak field: how χ enters the q series

Measured (series_study.py): at fixed k,
    Δφ(k,q,χ) − 2π = 6πkq·[1 + O(q)] + χ·C_odd(k)·q^{3/2}·[1+O(q)] + O(χ²q², q²)
The odd-in-χ piece first appears at q^{3/2}: Lense–Thirring. Even powers of χ
and the χ⁰ corrections both live at q² and beyond. One memo per (k,χ) per sense
carries the q-series coefficients exactly as the Schwarzschild memo does per k.
