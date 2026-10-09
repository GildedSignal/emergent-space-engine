# Predictions — 20261009-1259-inversion-2360 (inversion lens)

Written **before** any run. Question: does the adopted two-regime encounter design
(pairwise tier + train certificate, trigger ζ) stay sound and sub-ruinous on
**collisionless families** — same a (clump), e-spread ≫ ρ, apsidal (ϖ) spread?
That is the regime the gold 20261006-0346-taleb-09b5 itself flagged ("a formation with
e-spread ≫ ρ could break phase-order = distance-order"), and the certificate build
20261006-1931-b-coorbital-cert-152e died at 429 before running one scene.

Scenes (added to the dead build's own `train_verify`, generator unchanged:
a = 1 ± 1e-5, e ~ Rayleigh(σ_e) cap 0.5, ϖ uniform over ±π, λ uniform or bunched):
- fam-u σ_e ∈ {0.005, 0.02, 0.05}, λ uniform — families.
- fam-b σ_e = 0.02, σ_λ ∈ {0.05, 0.01} — bunched (phalanx) family with e-spread.
- Controls: the build's phalanx set and ring-pom-uniform-34 (σ_e = 1e-3 bridge), ρ = 1e-4.

Held-out predictions:

1. **Controls** (must hold or my harness is VOID): phalanx scenes fire the train
   (ζ < 1), train misses zero encounters — the gold's regime reproduced.
2. **Families fire**: uniform-λ families at all three σ_e have ζ ≈ 2·L̄/2π ≈
   2·K_v·p·1.8σ_e/2π ∈ [0.02, 0.06] < 1 → train fires; watched fraction of clump
   pairs ≈ 2·L̄/(2π) ≈ 2–6%.
3. **The hole — bunched families are declined**: σ_λ = 0.01, σ_e = 0.02 gives
   ζ ≈ 2·0.076/0.01 ≈ 15 > 1 → declined → falls back to the pairwise tier whose
   n_c²/2 setup the gold proved ruinous at 10⁶. Predicted: declined, and no third
   regime catches it.
4. **Train soundness holds**: zero train misses on every family scene (the ϖ-free
   window bound |Δλ̄| ≤ δ(1+L_E) + K_v·p·|(ΔV,ΔW)| is correctly ϖ-blind).
   Any miss is a soundness kill of the certificate bound.
5. **Pairwise tier keeps missing in the family regime** (weak confidence, 60%):
   the gold found 4/233 misses in the coherent phalanx; family crossings (Cross
   sections, e-spread breathing ≫ ρ) extend it: predicted ≥ 1% missed.
6. **Work per real encounter**: train ≤ pairwise on family scenes; both grow with
   σ_e (watch widens with the e-window), and in the bunched-congested corner the
   watch degenerates toward all-pairs (watch fraction → 2L̄/spread ≫ 1 is the
   declining condition).

Kill criteria pre-registered: (a) any train miss in any scene → the certificate's
bound is wrong (adopt-blocking); (b) bunched family declined while pairwise setup
is quadratic → the two-regime design has a hole one hard burn away from its tested
regime (design change needed before adoption); (c) controls fail → VOID, not a result.
