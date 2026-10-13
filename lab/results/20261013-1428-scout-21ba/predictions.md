# Predictions — 20261013-1428-scout-21ba

Written before the decisive experiment. The question: is the shipped kick compile's
panel walk (GL4 on ≤π/4 panels plus the near-separatrix dyadic ladder) computing three
half-cycle integrals that are complete elliptic integrals — closed forms a constant
handful of Carlson duplication iterations can evaluate?

Grid (not tuned on): (p, e) pairs chosen to span the branch selector, the plane's
median kicked eccentricity and the separatrix edge. q = 1/p (mass 1), k = 1/(1+e).

| p | e | branch expected |
|---|---|---|
| 2^20 | 0, 0.5, 0.9 | weak (q = 2^-20 ≤ 2^-18) |
| 2^10 | 0, 0.5, 0.9 | strong |
| 2^6 | 0, 0.5 | strong |
| 2^4 | 0, 0.2 | strong |
| 2^10 | 0.94, 0.99, 0.999 | strong, near-separatrix ladder |

Held-out predictions:

1. **The φ channel is one Carlson RF call, exact.** advance() (the half-orbit azimuth
   excess) equals 2K(m)/√A − π with A = 1−q(8k−2), m = 4q(1−k)/A, K the complete
   elliptic integral of the first kind, to within the shipped compile's own quantum
   (I predict rel err ≤ 1e-5 on the excess, and the f64 closed form agrees with a
   4096-panel GL4 f64 truth to ≤ 1e-13). First-order check: excess → 3πqk as q→0.
2. **Panel count grows with e and is unbounded at the separatrix; Carlson cost is
   constant.** I predict knots()/panel counts of ~8–16 at e=0 (circular/weak) rising
   to ≥ 40 at e = 0.99 and ≥ 100 at e = 0.999 on the strong branch (the λ-ladder),
   while my instrumented Carlson RF converges in 3–5 duplication iterations at every
   point of the grid, including the most separatrix-like key that still compiles.
3. **The τ/t channels need at most ~2× the Carlson work of φ** (RJ/RD family, the
   Π-with-derivative identity); as a bound I predict a tanh-sinh (double-exponential)
   evaluation of the same integrands reaches 1e-12 relative in ≤ 40 nodes at every
   grid point, against the shipped walk's 4×(panel count) node evaluations — so even
   the best generic quadrature, not just the closed form, beats the panel walk's node
   count by ≥ 5× at e ≥ 0.9.
4. **The weak branch is already closed-form-able** (first-order integrands are trig
   polynomials — the Opus memo's R1): at q ≤ 2^-18 the excess will match 3πqk +
   O(q²) to ≤ 1e-3 relative of the excess itself.

What would make it wrong: if advance() is not the integral of 1/√(1−q·a(ψ)) − 1
over ψ ∈ [0, π] (scaling/branch mismatch), or if the closed form disagrees with the
shipped compile well beyond its certified quantum anywhere on the grid — then the
"compile = elliptic integrals" mapping is wrong and the scout claim dies.
