# Predictions — 20261010-0100-inversion-b063 (written before the decisive run)

Inverted claim under test (gold 20261006-0346, adopted into the encounters design, being built as
`b-coorbital-cert`): *under co-orbital concentration every real encounter lies within partner rank 4
along the orbit, so a phase-neighbour certificate at O(n·k), k≈4, triggered by a dimensionless
concentration number, replaces the quadratic pairwise tier for concentrated workloads.*

Hypothesis being falsified: concentration implies single-stream. All scenes below are co-orbital
(Δa/a ≤ ρ/2, so every pair is inside the Binet cone: the pairwise tier is quadratic on all of them,
i.e. the concentration signature fires on all of them).

Scenes (units μ=1, a=1, P=2π; encounter radius ρ=1e−4, r8's mid-range):
- S0 control (the gold's scene class): ONE stream. n=2000, shared e=0.01, ϖ=0, Δa/a ~ U(±ρ/4),
  phases uniform. Truth: analytic conjunction timing (same mean-motion drift).
- S0b scaling probe: S0 at n ∈ {500,1000,2000,4000} × ρ ∈ {1e−4,1e−3}.
- S1 KILL SCENE: TWO streams. Same a (Δa=0), same e=0.2, ϖ_A=0, ϖ_B=π/2, n_A=n_B=1000, phases
  uniform. Orbit curves cross transversally (angle ≈ 0.25 rad) at two fixed longitudes λ*=π/4, 5π/4.
  Truth: exact pass-time matching at λ* + Kepler-refined closest approach.
- S2 (optional, time-boxed): one stream, σ_e=0.05 with ϖ spread 0.3 (a hot debris torus): a
  continuum of weak crossings. Truth: min-curve-gap filter then time-stepping of survivors.

Predictions, held out (not tuned — the numbers below are derived on paper, the runs decide):

- P1 (S0, positive control / instrument check): ≥ 99% of truth encounters have partner rank ≤ 4 in
  the mean-anomaly ordering, at per-orbit refresh. If this fails my instrument contradicts the gold:
  VOID and diagnose, do not publish a kill.
- P2 (S1): at k=4 the phase certificate catches 0% of truth encounters (rounded to nearest %);
  median partner rank in the M-ordering is > n/8 (paper: |ΔM| ≈ 1.06 rad ≈ 0.17·n at e=0.2,
  ϖ-offset π/2). This holds at ANY refresh cadence, including rank evaluated at encounter time.
- P3 (S1, λ-ordering): sorting by true longitude instead of M rescues nothing at per-orbit refresh
  (< 10% caught); the k needed at refresh lead Δt scales as k ≈ n·v_rel·Δt/2π, i.e. refreshes per
  orbit must grow ∝ n to keep k=4 — the O(n·k) certificate quietly becomes O(n²/log n) per orbit
  unless the lead shrinks as 1/n.
- P4 (S0b): the maximal partner rank is not a constant 4 but ≈ 1.5·n·ρ·(lead/P)·(1/2π-normalized):
  it grows linearly with n and with ρ. k=4 fails somewhere inside n ≤ 4000 at ρ=1e−3 (paper:
  1.5·4000·1e−3 ≈ 6 slots at lead=P). Rank-4 is an artifact of the measured n and ρ, not a law.
- P5 (S2, if run): the rank distribution grows a tail toward Θ(n) as the ϖ spread makes curve
  crossings transverse; median rank ≫ 4 at n=2000, σ_ϖ=0.3.
- P6 (trigger, the design hole): the concentration signature (candidate pairs per real encounter)
  is ≥ 10³ in BOTH S0 and S1 — indistinguishable. No concentration-only dimensionless number can
  route S0 to the phase certificate and S1 away from it. The missing certifiable property is
  single-streamness (no transverse Binet-cone crossings inside the group), not density.

Instrument guards (fail ⇒ VOID): S0 truth must find conjunctions within 2× of the paper rate
(~37/orbit at n=2000, ρ=1e−4); S1 truth must find encounters within 2× of ~2×10²/orbit; S1
same-fleet encounters must be exactly 0 (Δa=0 ⇒ phase difference constant).
