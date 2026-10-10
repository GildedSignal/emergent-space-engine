# Predictions (written before the decisive run)

Scene (canonical, from the board's belt): a = 2.2 AU, width 0.5 AU, N = 10^9 real bodies,
belt mass 2×10^21 kg (real-belt mass ⇒ m = 2×10^12 kg each), Rayleigh e ⇒ in-plane
dispersion σ0 = 20 m/s. Star 1 M☉. Player velocity floor q_v (the differentiation
quantum) swept over [10^-6, 10^-2] m/s. Kernel: shearing-sheet encounter flux with exact
hyperbolic deflection (focusing included), impulse form below.

Hand estimates behind these (Fermi, before measuring):

- b_q (impact parameter where the per-body kick Δv = q_v) scales as q_v^-1/2 (shear
  regime) or q_v^-1 (dispersion regime); the above-floor rate λ_+ = (Σ/m)·2 b_q·v_rel(b_q)
  then scales as q_v^-1 in BOTH regimes. Predicted exponent β = d ln λ_+ / d ln q_v = −1.0 ± 0.2
  over q_v ∈ [10^-6, 10^-2].
- λ_+(q_v = 10^-6) ≈ 0.1–0.5 above-floor kicks per body per orbit (hand integral ≈ 0.36).
- Weak (sub-floor) kicks dominate the diffusion coefficient (Coulomb log): D ≈ (2Gm)²(Σ/m)·2∫db/(b·v_rel)
  ≈ 10^-10 m²/s³ for the canonical belt ⇒ σ_residual(t) ≈ √(D t) ≈ 10 m/s at 10^4 orbits,
  while σ0 = 20 m/s keeps v_rel dispersion-dominated (no strong self-limiting yet).
- Therefore live bits per body ≈ n_dof · log2(σ_residual/q_v), growing only as
  n_dof/2 · log2 t: PREDICT measured growth slope ≤ 1.5·n_dof_true bits per time-octave
  (n_dof_true = 2 for my 2-D residual tracking), i.e. ≤ 3 bits/octave, and it must DECLINE
  once σ_residual ~ σ0.
- Store total at 10^4 orbits, q_v = 10^-6: 26–32 bits/body (2 dof) ⇒ 3.3–4 GB at 10^9
  bodies; with 3 dof 5–6.5 GB. Each octave of floor coarseness saves n_dof bits/body
  (0.25–0.375 GB per octave at 10^9).
- Dense scene (Σ ×2500, a concentrated swarm like the taleb-gold formation): rates linear
  in Σ (predict linearity within 25%; super-linearity means my Poisson flux misses
  correlations ⇒ flag), σ_residual ×50 ⇒ +11–12 bits/body ⇒ the concentrated scene, not the
  smooth belt, is what breaks 8 GB.
- Cold swarm (σ0 = 0.01 m/s): focusing matters; the impulse-only kernel must deviate from
  the exact hyperbolic kernel by >2× on kick size (negative control), and the exact kernel
  must match a direct numerical integration of the two-body passage within 1% (positive
  control). If either control fails the whole run is VOID.

Held-out cases (not tuned on, decided before running): q_v = 10^-4 and 10^-2 points,
Σ ×2500 scene, σ0 = 0.01 m/s scene, and the growth slope after the σ0 crossover.
