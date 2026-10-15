# Predictions — gravity-is-news at strong field (written before the decisive sweep)

Oracle: Kinnersley's photon rocket, exact GR, Carlip's retarded Kerr-Schild form
(gr-qc/9909087 eq. b1/b1a/b2). Instrument controls, already green before this file:
static pull = m/R²(1−2m/R) hand-derived (2.9e-11); metric = Lorentz-boosted static KS
at machine precision (2e-16) for free-fall β ∈ {0.01, 0.1, 0.3}; FD-of-metric vs
Carlip's analytic b1a agree ≤ 2e-10 through β = 0.3 under burn.

Arms (causal data only: the retarded (x, v, a) of the source):
- R1 naive retarded (Laplace), R0 as-if-now tube (thrust-blind, linear extrapolation),
- R2 (x,v,a) quadratic extrapolation, R2b R2 + Carlip's velocity prefactor and the
  nonlinear −2m/R term (his ε₁, ε₂ unimplemented — they are the measured residual).
Scar ρ = |a_arm − a_exact|/|a_exact|, exact = −Γⁱ₀₀ (static probe; the consumer's own
kinematics belongs to the doll, not the news channel). ρ_perp = transverse part.

## Pre-registered predictions (decisive grid: free fall β_s ∈ {0.003,0.03,0.1,0.3} ×
## r0 ∈ {200,50,20,12}; gentle burn 0.10 v_c/0.25 P and hard 0.82 v_c/P at r0 ∈ {50,20,12}, β_s0 = 0.1)

P1 (control, must pass or the instrument is broken): ρ_perp(R1) ≈ β_s within a factor
of 2, at every radius (the Laplace aberration); R1 is the negative control.

P2 (free fall): ρ(R2) is set by the missing velocity prefactor and the nonlinear term:
grows ~β_s² and ~2m/r0; predicted ρ(R2) at (β_s=0.1, r0=200) below 1e-2, rising toward
a few ×1e-2 at (0.3, 12); ρ(R2b) sits 10-100× under ρ(R2) — the b3 resummation, not
the extrapolation, carries the strong-field corrections. Both stay under 1e-1
everywhere in the grid.

P3 (the thrust-blind tube): ρ(R0) − ρ(R2) ≈ ½·a_burn·r0 (the ½aT² lag at perfect
cadence, T = light time r0): for the gentle arm at r0=20 ≈ 1.6e-3, hard ≈ 3.3e-3 —
i.e. the burn channel is the SAME ½aR law at strong field as at weak field (7ab4),
no new strong-field amplification beyond the 2m/r terms already counted in P2.

P4 (decisive): the (x,v,a) payload with the b3 readout stays complete at strong
field: ρ(R2b) < 1e-2 for β_s ≤ 0.1 at every r0 ≥ 12, gentle and hard burn; its
residual is flat in the burn magnitude (R2 carries the total a — the burn channel is
deleted, not attenuated, exactly as d947 measured at weak field).

Kill criteria:
- If ρ(R2b) > 1e-2 at β_s = 0.1, r0 ≥ 12 under gentle burn, the payload verdict
  changes: the version ring needs more than (x,v,a)+b3 at strong field.
- If ρ(R0)−ρ(R2) does not scale ~a·r0, the ½aT² strong-field composition claim dies.

Held-out (not tuned on; the checker runs these): (β_s=0.2, r0=16, free fall and
gentle burn); hard burn at r0=30; a jerk row at r0=20 (a(t) = a0(1 + t/T)); and the
retro-burn (a_burn opposing v0) at r0=20, gentle.

Expected there: P1-P4 continue to hold with the same scalings; the jerk row's ρ(R2b)
stays at the constant-burn level (the a-slot stays exact under jerk; only quartic
programs would move it — d947's weak-field finding transfers).
