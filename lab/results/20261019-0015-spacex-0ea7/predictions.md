# Predictions (written before the decisive census)

Cases not tuned on: the σ axis and the N axis beyond the plane's 48–192 bodies, the
random-e arm, and the locals' branch. All are computed by the same shipped arithmetic
(`ladder_ship` → `OrbitKey::bound` → `MemoCode::encode`), none was inspected body by body.

1. **The belt's standing shapes saturate, its cells do not.** At the shipped driven
   belt (Rayleigh e, σ = 0.07, cap 0.4, a uniform in [2,3) AU), distinct shape
   identities C_shape(N) ≈ 600–1,500 already at N = 10⁶ and flat from 10⁶ to 10⁷
   (it is set by the e-entropy in 11-bit gap classes, ~2×10³ of them reachable),
   while distinct 44-bit cells C_cell(N) ≈ 0.85–1.0 × N at 10⁶ (the a-axis at 2⁻⁸
   AU plus the gap axis makes cell collisions a birthday event only).
2. **Amortization crosses over between 10³ and 10⁴**: at N = 10³ the belt is near
   one shape per body (like the plane scene's 85 cells / 48 bodies); by 10⁶ it is
   ≥ 500 bodies per standing shape.
3. **The σ axis is the memory dial**: C_shape grows ≈ linearly in σ (the occupied
   relative gap range ≈ 2σ·(1+o(1)) at 2⁻¹¹ relative resolution). A phase-locked
   belt (σ = 0.03) collapses to ≤ 300 shapes; σ = 0.15 ≥ 2× the shipped count;
   uniform-random e makes C_shape ≈ min(N, ~10⁵) — the ladder's random end has no
   sharing, which is the floor's worst case, not the belt's.
4. **The locals (Home/Moon ships) are strong-branch and ~all distinct** (compactness
   above 2⁻¹⁸ near a planet), so their shapes are not shared — a few hundred bodies,
   immaterial at 10⁹, but the census should show the branch split, not hide it.
5. **Weak shapes are cheaper than the plane's ~43 knots** (fewer radial panels at
   small e): mean knots per standing shape ≤ 30, so standing bytes per shape ≤ ~3 KB.
6. **Consequence if 1–3 hold**: a 10⁶-body belt's compiled-shape store is ~10³
   shapes × few KB ≈ single-digit MB, not N × 3.8 KB ≈ 3.8 GB; per-body memory
   becomes the exact key + phase words (~40–60 B). The compiled-orbit share of the
   memory wall is an artifact of unshared shapes, and it deletes at belt scale.

Kill criterion for the premise: if C_shape(N) grows ≈ linearly in N at fixed σ past
10⁴, sharing buys nothing at belt scale and the carried cell is a rebind-time win
only (cell-rebind's silver already stands, no memory claim).
