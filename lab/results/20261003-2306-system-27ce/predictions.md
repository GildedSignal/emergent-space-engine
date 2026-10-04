# Predictions (written before the decisive runs)

Question: is the plane's kick cadence (1/64 of every forced body's radial period, `step_for`) a
derivable certificate or a magic tick? Probe: float WH drift-kick-drift, exact Kepler drift,
per-body fixed step h = T0/n, behaviour judged against a dense reference (n=512), in the probe
idiom of gravity-v1 (float explores, never decides).

Scenes (2D, units GM_sun = 4π² AU³/yr², c = 63,241 AU/yr):
- **Belt**: circular Jupiter (a=5.2, µ=GM/1047) + 120 test asteroids, a ∈ [2.45,3.35] with a
  dense slice at the 2:1 (3.277), e0 ∈ [0.02,0.2], 6,000 yr (~1,150 orbits at 3 AU).
- **Moon**: Jupiter-like planet (µ=GM/1047) at 5.2, moon as test particle of the planet's doll,
  full differential solar pull (as `force.rs`: never the linear truncation), a_m ∈ {0.15,0.25,
  0.35,0.45} R_H, e0 ∈ {0.05,0.2}, 1,500 moon orbits.

Quantum: velocity quantum q_v = c/Q; at Q = 2^20, q_v = 0.0603 AU/yr. Certificate form probed:
step h such that the kick's midpoint quadrature error (h³/24)·|a″| stays below one q_v.

Derived before running (keyboard arithmetic, conjunction-distance estimates):

1. **Belt n_pred ≈ 2/orbit** (a″ ≈ 3.4e-2 AU/yr³ at conjunction → h ≤ 3.5 yr, T = 5.2 yr).
   Prediction: behaviour (Δa/a, Δe, Jacobi error type) at n = 4 and n = 2 matches the n=64
   control's own agreement with the reference (both ≪ their mutual secular drift); the failure
   below n_pred is a bounded bias (wrong apsidal rate), not a walk.
2. **Moon n_pred ≈ 2/orbit on impulse grounds, but the m=2 harmonic of the solar tide needs
   n ≥ 4/orbit even to average right** (antipodal sampling at n=2 aliases cos2φ to DC).
   Prediction, r9's pattern repeating: a_m, e_m stay fine at n = 4–8 while the apsidal
   precession degrades ~1/n²: within B14's 10% at n = 8, marginal at n = 4, badly wrong at n = 2.
3. **Resonant slice (2:1)**: sparse kicks over-pump e relative to the reference (r4's
   first-order-in-µ lesson re-appearing as sampling error): at n = 4 the slice's e error exceeds
   the non-resonant belt's by ≥ 5×; dense n = 64 does not. The certificate must detect resonance
   and keep density there (law.md already says so).
4. **Error type**: at every fixed n in the belt the Jacobi error stays bounded (growth exponent
   ≤ 0.2); sparsity trades error size, never type, until the bounded bias of (1) appears.
5. **Q scaling** (side observation): n_pred ∝ q_v^{-1/3}, so at the target Q = 2^40 the same
   certificate demands ~2^{20/3} ≈ 100× denser kicks than at Q = 2^20 — i.e. today's fixed 1/64
   is ~30× denser than the quantum needs at Q = 2^20 and slightly sparser than it needs at
   Q = 2^40, for belt-class bodies. A magic constant is unanchored at both ends.

What would kill the claim: if behaviour at n = 4 already differs from the reference by more than
the n=64 control's own secular uncertainty (then the cadence was load-bearing), or if the Jacobi
error walks at sparse fixed n (then sparsity broke the split, probe-1's failure mode).
