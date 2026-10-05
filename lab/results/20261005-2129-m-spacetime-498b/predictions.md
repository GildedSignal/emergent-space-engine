# Predictions (written before the decisive probes, 2026-10-05)

Cases below were **not** tuned on. Each probe has a positive control that must pass
and a negative control that must fail, or the run is VOID.

## Probe A — multi-Kerr-Schild superposition (`probe_mks.py`)

Held-out cases (first tuned only on the one-mass control):

1. **Two equal masses, wide test orbit** (p/d = 10 and 30, e = 0.1): the multi-KS
   metric's perihelion excess over the Newtonian quadrupole precession will match
   the 1PN oracle (isotropic 1PN superposed metric, geodesics integrated the same
   way) to **better than 2% relative** on the GR excess. The GR excess itself is
   ≈ 6π·M_tot/p, so this is a statement about cross terms of order (M/p)².
2. **Light past two masses** (b₁ = b₂ = 40 M, masses on either side of the ray):
   multi-KS deflection within **0.1%** of Σ 4M_i/b_i (cross terms are 2PN,
   ~ (M/b)² ≈ 6×10⁻⁴ — I predict marginal pass, 0.05–0.3%).
3. **Negative control (naive river sum β = Σβ_i):** for equal masses the
   effective flow overshoots by √2, so the precession excess will be off by
   **roughly 2× (100 ± 40%)** — a clear fail, confirming the board's premise.
4. **Determinism:** integer rank-1 accumulation of the contravariant field
   h^{μν} = −Σ f_i k_i^μ k_i^ν in random deposit orders is bit-identical (I
   predict identical digests in 20/20 permutations — this is exact by
   associativity of integer addition; it must hold or the harness is wrong).
7. **Added before any run (still pre-registration):** a second light case at
   b₁ = b₂ = 4000 M, where the single-mass 2PN content (15π/16)(M/b) ≈ 7×10⁻⁴
   no longer dominates: MKS deflection within **0.15%** of Σ 4M_i/b_i, and the
   *difference* between the MKS two-mass deflection and the MKS single-mass
   (equal total mass) deflection within 3×10⁻⁴ of the 1PN cross prediction 0
   (cross terms are 2PN). At b = 40 M I now expect the Σ 4M/b comparison to
   miss by several percent — the single-mass 2PN term — and I record that here
   as the likely cause rather than tuning it away.
5. **Cone slide (held-out):** adding one source changes the local null cone of
   g^{μν} = η^{μν} − f k k^T only along the k direction: for η-null covectors ξ
   with k·ξ = 0, g^{μν}ξ_μξ_ν = 0 stays exactly 0. I predict the numerical
   cone-eigenvalue test shows the characteristic variety shifts only along k
   (residual < 10⁻¹² for machine-precision check), i.e. "a source slides the
   light cone along its principal null direction" — the light cone as a rank-1
   updated data structure.

If (1) fails above ~5% at p/d ≥ 10, multi-KS is killed for bottleneck 1.

## Probe B — Farey/PSL(2,ℝ) velocity sheets (`probe_farey.py`)

1. **Exact integer composition:** for rational velocities u = s/r, v = q/p,
   Einstein addition is the bilinear form (qr+sp)/(pr+qs): a symmetric integer
7. **Added before any run (still pre-registration): the carry arm.** Pure
   snapping may random-walk (round-to-nearest after each boost is a martingale
   in the error): I predict the *measured* envelope grows like √K quanta
   (std ≈ q·√(K/12)), i.e. prediction 3 as written FAILS for naive snapping —
   and that adding the law's sigma-delta carry (Inose–Yasuda, already in
   representation.md §4) bounds the total error to **≤ 1 quantum forever**
   (represented value = snapped + carry is exact by construction; the question
   is only the carry's own width, predicted ≤ 1 quantum). This arm tests
   whether fixed-bit velocity sheets need their carry bit-for-bit, as r2 found
   for the plane's increments.
   matrix [[r,s],[s,r]] acting on (q,p). Composition of K = 100 random rational
   boosts equals the float Einstein formula **exactly (0 ULP difference in
   rational↔float round-trip, mismatch rate 0)**.
2. **Height growth (why sheets must snap):** exact composition multiplies
   denominators; after 100 boosts with ≤ 3-digit rationals, the exact rational
   needs **> 1000 bits**. Prediction: bit length grows linearly in K (~+60
   bits/boost at 3-digit inputs) — unbounded storage per body without snapping.
3. **No compounding after snapping:** with log₂D² snapped to the level-ℓ grid
   (ℓ = 8, 12, 16; D² = (1+v)/(1−v)), after K = 10⁴ random boosts the
   |log₂D² − exact| error stays **≤ half a quantum + 10⁻⁹** with **no secular
   drift** (fitted drift < 10⁻⁶ quanta/boost). This is the load-bearing
   prediction: errors do not compound (principle 13) because snapping is a
   monotone retraction onto a multiplicative lattice.
4. **Order/causality:** for 10⁵ random pairs with v₁ < v₂, snapped order is
   never inverted (monotonicity); collisions (equal snaps) < 0.5% at ℓ = 12.
5. **Nothing past c:** |v| < 1 holds by construction for every level-ℓ sheet;
   I predict zero violations in 10⁶ random boosts, with the *closest approach
   to c* bounded by the largest representable node at each level
   (1 − 2·4^(-ℓ)... i.e. the top node of level ℓ), reported.
6. **Mediant is not the group law (self-kill of the cuter idea):** the Farey
   mediant of two velocities *underestimates* their Einstein sum
   (v ⊕ u > max(v,u) > mediant for 0<v,u<1). The Stern-Brocot tree's role is
   precision levels, not composition. Prediction: mediant-vs-Einstein mismatch
   ~1–10% for typical pairs — confirming the tree indexes the sheet, the
   bilinear form moves within it.
