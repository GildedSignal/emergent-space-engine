# Predictions (written before the decisive run)

Question: how fast does a belt under the plane's own kind of perturbation (secular,
orbit-averaged — the law's kick layer) create live distinguishing information (H_live),
measured in the law's own quanta (E Q48, L Q32, ϖ u32) and encoded by the shipped
`shipmem` block codec?

Scene (held fixed): belt of m bodies, Darwin p uniform in [2048, 3072) (Q16), e₀ Rayleigh
σ = 0.04, ϖ₀ uniform; birth order = p-sorted (banded, as B18b). One exterior perturber:
a_J = 5120, μ = 9.55e-4, e_J = 0.048, ϖ_J = 1 rad. Times T = 0, 1e2, 1e3, 1e4, 1e5
reference orbits (reference = the inner edge, p = 2048). Columns scarred: δE, δL, δϖ
(δt_p is affine in cycle count under constant a — a program, excluded, stated).
t_p/kind columns are constant programs in this scene.

Arms:
- **A (naive store):** scars = state(T) − birth state, encoded in 256-blocks, birth order.
- **B (generator):** scars = state(T) − RK4-integrated LL at one step per orbit (the
  plane's averaged cadence). Truth = closed-form LL.
- **C (the kick model):** `Pop::kick`-magnitude random walk (±2^10 quanta per orbit on
  E, L, ϖ), the model a memory designer would assume without the law.

## Predictions, falsifiable before I look

- **P1 (A, E column):** δE reaches ≈ log₂(zigzag amplitude in E quanta) ≈ 38–48 bits/body
  by T ≈ 1e4 (a quarter of the secular cycle), then stays flat (±2 bits) to 1e5.
  Differential precession across a 256-block is reabsorbed by DFOR because birth order is
  p-sorted; only the birth-phase-dependent oscillation is incompressible.
- **P2 (A, L and ϖ):** δL ≈ 25–33 bits (16 fewer mantissa bits than E); δϖ grows
  monotonically and saturates ≤ 32 bits (uniform).
- **P3 (B):** total residue ≤ 2 bits/body at all T. If > 4 bits by 1e5, the generator's
  one-step-per-orbit cadence is too coarse and the wall returns — that would falsify
  "the secular bulk is derivable at plane cadence".
- **P4 (C):** bits ≈ log₂(√T·2^10) → 14–20 bits by 1e5 and still rising. So the kick
  model *understates* the immediate secular amplitude (arm A) and *mispredicts the shape*
  (growing vs flat): wrong in both directions. Any H_live number from a synthetic kick
  model is untrustworthy.
- **P5 (the wall):** arm A total (E+L+ϖ) at 1e5 lands 80–110 bits/body → 10–14 GB at 1e9
  bodies, breaking 8 GB **but flat in T**: the wall is set by the quantum/amplitude ratio
  (representation), not by a rate. Arm B total ≤ 2 bits → 1e9 fits with ~zero growth.

Kill criteria: arm A total ≤ 32 bits at T = 1e5 kills P5's wall (1e9 fits even naive);
arm B ≥ 10 bits kills the generator claim; flatness of A beyond ±4 bits from 1e4→1e5
kills P1's shape claim.

Controls: T = 0 must encode to ~0 bits (a scar arithmetic bug shows here); the forced
eccentricity e_F = (b₂/b₁)·e_J must land in [0.03, 0.15] for α ∈ [0.4, 0.6] (else my
Laplace–Lagrange is wrong and the run is VOID).
