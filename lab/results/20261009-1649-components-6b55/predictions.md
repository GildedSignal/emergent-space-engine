# Predictions — H_live for a belt population (run 20261009-1649-components-6b55)

Written before the decisive sweep. All are cases I have not tuned on: the
Monte-Carlo (`hlive.py`) has not been run beyond a syntax check; the numbers below
come from paper estimates only.

- **P1 (calibration, belt-0).** The shear conjunction formula reproduces r8 v2's
  belt-0 count (427 encounters, N=1e4, 20 orbits) within a factor of 2 at the
  low-draw corner (σ_e≈2e-3, ρ≈1.5e-5) and over-predicts by 5–10× at the median
  draw (5.5e-3, 5.5e-5) — i.e. belt-0 drew low.
- **P2 (diffusion control).** MC walk σ / analytic diffusive σ ∈ [0.7, 1.4] at
  N=1e4, M_belt=1e-3, over 1e3 orbits.
- **P3 (heavy control).** N=1e6, M_belt=1e-3 M_star, Q_e=1e-9: scarred fraction
  ≥ 0.5 within the simulated window (the instrument can see scarring).
- **P4 (scale invariance, held out).** At fixed M_belt in the ρ∝1/N regime,
  the analytic walk σ after 1e4 orbits is N-independent within ±30% (Γ const,
  per-event δv const); in the fixed-ρ regime σ(1e9) ≈ σ(1e4)·√(1e4/1e9).
- **P5 (the claim).** Kuiper-like mass M_belt=1e-7 M_star, Q_e=1e-7, N=1e9:
  no quantum crossing within a 1e4-orbit session; margin τ_cross/T > 100;
  measured bits/body ≤ 1e-3.
- **P6 (the boundary).** The lightest M_belt crossing Q_e=1e-7 within 1e4 orbits
  lies in [1e-5, 1e-3] M_star; Q_e=1e-9 is crossed already at M_belt=1e-7
  (the finest quantum is where the premise gets tight).
- **P7 (player cone).** Bodies inside a light-second cone at belt density ≈
  3–5×10³ per game-second; at 32 bits each that is 0.5–1.6×10⁵ bits/s against
  a 4 GiB/hour budget of 1.2×10⁶ bits/s — small but not zero (5–15%).

What would kill the claim: if P5 fails (crossing at Kuiper mass with a
behaviour-plausible quantum), the billion-belt premise needs re-inference
machinery from day one, and the dossier must say the premise is at risk.
