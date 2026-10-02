# Predictions — 20261002-1618-system-dc92 (system lens)

Written before any orbit measurement ran. Floats explore; nothing here is canonical.

**Candidate rule (the thing under test):** the river flow for N static sources is
β = −∇χ with χ the Jacobi/Maupertuis action of free fall from rest at infinity,
i.e. the eikonal |∇χ|² = −2Φ, where Φ = Σᵢ −Mᵢ/rᵢ is the additive multipole
potential the cells already hold. For one mass χ = 2√(2Mr), which is exactly
the Doran river (verified algebraically, not a prediction).

Cases below were not tuned on. Config unless stated: M₁ = M₂ = 0.015 at
(±0.75, 0) static, test body at a = 4.5, e = 0.2 (circumbinary, pericenter
start). References: Newtonian float integration, one-mass river with the same
M_tot and same orbit (the "spherical equivalent").

1. **One-mass pipeline control.** The ray-based evaluation of β (fall-from-far
   congruence) versus the analytic Doran β gives the same periastron advance to
   < 3×10⁻⁴ rad/orbit, and both match 6πM/p to within the 2PN-scale residual
   (a few×10⁻³ relative here).
2. **Eikonal consistency on the fly.** Along every integrated orbit,
   |β|² + 2Φ ≈ 0 to < 10⁻⁶ (machine-level check that the congruence really
   solves the eikonal, not something else).
3. **Newtonian exactness of composition (the theorem).** The two-mass eikonal
   orbit's advance differs from the Newtonian two-mass advance by ≈ the
   one-mass GR term 6πM_tot/p (0.128 rad/orbit here) plus a **cross-term
   correction S** that is small relative to 6πM_tot/p. I predict
   |S| < 0.5 × 6πM_tot/p. (If instead the composition were wrong at Newtonian
   order, S would be comparable to or larger than the Newtonian quadrupole
   precession itself.)
4. **Cross-term structure.** S scales linearly in M₁M₂ at fixed M_tot and a:
   going from equal masses to M₂ = M₁/4 (M₁M₂ down 4×, M_tot fixed) divides S
   by ≈ 4 (within measurement noise). A composition wrong at 1PN would show
   O(1)-relative changes, not this scaling.
5. **Negative control (χ additive, i.e. β = −Σᵢβᵢ).** Its two-mass "potential"
   −½|Σβᵢ|² carries cross terms ~ √(Φ₁Φ₂) — order 50% of Φ here — so its orbit
   must deviate from Newtonian grossly: advance off by ≫ the GR term, or the
   orbit visibly non-Keplerian. If it *didn't* fail, the experiment can't see
   composition errors and the run is void.
6. **What would kill the rule here:** S at the scale of the Newtonian
   quadrupole precession (composition wrong at Newtonian order), or S not
   scaling with M₁M₂, or the one-mass pipeline control failing (then the
   measurement machinery is broken, not the rule).

Known limitation, stated up front: this run measures structure and controls,
not a full 1PN two-mass verdict — that needs the frozen EIH oracle (H0178) on
the same scenes; it is the named next experiment.
