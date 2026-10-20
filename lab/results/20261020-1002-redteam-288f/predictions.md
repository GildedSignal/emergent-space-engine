# Predictions (written before the decisive run)

Target: the fleet doll's interior tide law — representation.md L23 ("Inside it, tides
are linear to first order, with the Clohessy–Wiltshire closed form"), law.md L50
("Members feel only the tide x″ = −E(τ)·x, where E is the Schwarzschild tidal tensor
projected along the tube"), as shipped in `crates/engine/src/frame.rs` (Newtonian
tensor `E = (GM/r³)(I − 3r̂r̂ᵀ)`, phase-2 relativistic tide unwritten).

Truth: exact Schwarzschild geodesics (float64, DOP853/RK4, conserved E and L checked),
central + member born-rigid at ξ = 10⁻³·r₀, separation read in the parallel-transported
(Fermi) frame — the letter's own frame. The analytic truth for the instantaneous tide
is the Riemann contraction E(u)_ij = R_{iαjβ}u^αu^β, cross-checked by finite differences
of the integrated member geodesics (independent path).

- **P1 (control, instrument works):** circular origin at r₀ = 1000 M (local v_circ =
  0.0326 c): the Newtonian-tide law reproduces the truth's member separation over one
  radial period to better than 1% in norm (residue = static 1PN + boost at β² ≈ 0.001).
- **P2 (the shipped cap):** circular origin at r₀ = 18 M, where v_circ = 0.2500 c =
  the weak-field rule's boundary n·R = c/4 exactly: the radial tide coefficient is
  wrong by +10.0% (closed form (2r−3M)/(2(r−3M)) = 33/30 = 1.100 — the same
  eigenvalue E9 froze as w(3γ²−1)); the frame's own budget line says O((nR/c)²) = 6.25%.
- **P3 (flyby coefficients, the player-speed domain):** at a tangential (closest
  approach) launch, r₀ = 100 M, β ∈ {0.5, 0.9, 0.99, 0.999}: the truth's instantaneous
  tidal coefficient exceeds the Newtonian one by γ²(2+β²)/2 radially (predict 1.500,
  7.395, 74.25, 748.9) and by γ² along-track (1.333, 5.263, 50.25, 500.2); the
  finite-difference check agrees with the contraction to < 0.5%.
- **P4 (integrated, player-visible):** same flybys, member at ξ = 10⁻³ r₀: the
  Newtonian-law member offset at flyby exit errs by more than 100% at β 0.9 (the
  coefficient error feeds a stretching exponent, so it compounds; magnitude guess 2–10×,
  wide).
- **P5 (the cure is cheap and total):** replacing the Newtonian coefficients with the
  contracted E(u) (closed form, same kick structure, O(1) coefficients — no new
  mechanism) brings the exit error at every β above within 3× the P1 control level.
- **P6 (instrument):** conserved E and L drift < 10⁻⁹ on every geodesic; halving the
  offset to 10⁻⁴ r₀ changes relative errors by < 0.3% (linearity).
- **P7 (radial-infall geometry, held-out arm):** origin falling radially inward at
  β = 0.5 from 100 M (α = 0): the longitudinal (along-motion) tidal coefficient is
  wrong by exactly γ² = 1.333, the transverse-radial by γ²·(2+0)/2 = 2.667… wait —
  for α = 0 the *radial* (along-motion) channel is γ²·(2+β²·0)/2 → γ²(1)… pre-register
  the clean statement: along-motion ratio γ² = 1.333, cross-track (in-plane
  perpendicular) ratio 1.000 (the (1−β²)γ² cancellation).

Cases I have NOT tuned on (the checker's space): β 0.999 arms, r₀ = 20 M strong-field
flyby, offset 10⁻⁴, negative offsets, and the α = 0 arm.
