# predictions.md — 20261021-1346-second-20261021-0429-scout-451f-8833

Written BEFORE the decisive grid (flyby rp{18,100} × β{0.5,0.9,0.95} and the
conv ladder).  Disclosed context: the checker's own probes (sign flip ×70/×10⁴,
halving ladder 6.7→3.4→1.7e-3, in-plane excess ~9× z at 3e-2 β0.95 with the OLD
map+IC) and ONE timing cell I ran at β 0.9, rp 18 with all three fixes (z 1e-4:
4.1e-4; z 3e-2: 0.1224; radial 3e-2: 1.064; along 3e-2: 5.404).  Everything
else (β 0.5/0.95, rp 100, angles π/8..3π/8, τ shapes, the convergence ladder,
the repro cell) is held out.  A third fix (the log-map's dual projection) was
adopted on measurement before this file: mapcheck shows it 10–400× closer to
the exact exponential map (along 3e-2 rp18: 7.6e-2 → 3.3e-3).

1. **Quadratic purity (decisive for the checker's open question).** In every
   channel × β × rp, err(u) fits c₂·u² over u ∈ [1e-3, 3e-2] with pointwise
   err/u² within ±25% of the median; no flat component (kill: any channel with
   err(1e-3) > 3× c₂·1e-6, i.e. a floor).  Expected truth-side floor from the
   timing cell: err(z,1e-4) ≈ 4e-4 ∝ 1/u → ≤ 3% of signal at u = 1e-3.
2. **Convergence.** repro451f (old sign, old map, frozen E, 4000 steps)
   reproduces 451f's stored z numbers (6.7e-3 at 1e-4, ~0.123 at 3e-2) within
   5%; the fixed instrument's err(z,1e-4) at 4000 steps is ≥ 10× below frozen;
   refining nsteps 4000→16000 moves c₂ (read at u ∈ {1e-2,3e-2}) by < 5%.
3. **Angle pattern.** c₂(α) ≈ A·cos²α + B·sin²α with B (along-motion) > A
   (radial) > c₂(z) at β 0.9/0.95; at β 0.5 near-isotropic (spread < 2×).
   From the timing cell: A ≈ 1200, B ≈ 6000, c₂(z) ≈ 136 at β 0.9 rp 18.
4. **M/r independence (P4 at second order).** c₂(rp=100)/c₂(rp=18) ∈ [0.9,1.1]
   for every channel and β.  Kill (refute the naive extension): any channel
   outside [0.8,1.25] — then the second-order certificate carries an M/r term.
5. **β scaling.** c₂(0.95)/c₂(0.9) ≈ 2 ± 0.5 (γ²-like) in every channel;
   c₂(0.9)/c₂(0.5) between 1.5 and 8 (z measured 1.65 with the old instrument;
   in-plane channels larger).
6. **Verdict on the sign-fixed in-plane excess.** If 1 holds at both rp and all
   β: the excess is a REAL quadratic channel (the second-order law), not
   instrument prey — and the certificate tightens: the linear law holds 1%
   only for ξ/rp ≲ 1.3e-3 along-motion at β 0.9 (≈8× tighter than z's 1e-2).
   If 1 fails: the in-plane channel is instrument prey; I report which floor.
7. **τ-growth shapes.** ≥ 60% of exit err accumulated by snap 0.1 (r ≈ 2rp)
   in every channel; c₂(τ)/c₂(exit) channel-independent within ±20% (one tidal
   kernel); flat after snap 0.5 (tide ∝ r⁻³ dead by r ≈ 8.5rp).

## Addendum (written before the exact-IC run, after reading the fixed grid)

The fixed grid shows err = k(alpha,beta,rp) * u EXACTLY (z beta0.9 rp18:
k = 4.076 constant to 4 digits over u in [1e-4, 3e-2]) — |delta xi| quadratic
in the separation.  451f's c₂ = k/u_max is exposed as a quadratic-fit artifact
of a linear law (its "resolution robustness" needs no floor cancellation).
Before reading k as the physical second-order law, an O(xi^2) IC-truncation
propagated must be excluded: I add the exact-IC control (member IC = numerical
parallel transport of u0 along the TRUE exponential-map geodesic, all orders).
Predictions for that run:
A. k_exact/k_trunc in [0.7, 1.3] for every channel with k > 3 (the linear
   channel is the physical second-order tide, not IC convention).  My scaling
   estimate for the propagated IC truncation gives err/u^2 ~ gamma^2 M/(rp beta)
   ~ 0.3 at rp18 beta0.9 — 400x below the measured 136, hence A.
B. vrel0_fd with exact ICs scales xi^2 (one order below the truncated IC's xi).
C. If A fails downward (k_exact << k_trunc), the certificate loosens to
   u ~ 1e-1 at the 1% bar and the reading flips to "IC convention owns the
   in-plane error" — refuting the physical reading, not the instrument.
D. The angular nodes (k(alpha) crosses zero: near pi/4 at beta 0.5, near pi/8
   at beta 0.9, min rotating with beta) survive the exact IC unchanged.
E. k_z(rp100)/k_z(rp18) ~ 0.17 (measured M/r scaling) survives; in-plane
   ratios stay within [0.7, 1.3] away from nodes.
