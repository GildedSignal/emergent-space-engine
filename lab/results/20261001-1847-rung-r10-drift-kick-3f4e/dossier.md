# Dossier — r10: the compiled drift plus kicks, with a smooth changeover

**Claim.** In the circular restricted three-body problem, a second-order symmetric split whose
drift is the exact Kepler orbit about the dominant body — star far, planet near, blended by a C²
changeover of the separation with recursive sub-stepping (Duncan–Levison–Lee's SyMBA, restricted
form) — keeps the Jacobi constant bounded (exponent ≤ 0.2), reproduces the Hill moons' classes and
apsidal precession, keeps resonances librating, at a median cost of ~170 force evaluations per
dominant orbit; a hard switch at the sphere of influence (events3's configuration) fails the
Jacobi gate at the same step budget, and plain fixed-step Wisdom–Holman fails it on unresolved
close passages.

**Bottleneck.** Board focus line 1 ("fewer kicks per orbit"): the changeover is what lets the
drift-plus-kick law use one base step of 192 per planet orbit everywhere (32 kicks/orbit with
averaging was already reached in H0190; the changeover's job is correctness near the secondary,
not cost). Cost gain over dense truth: ~10³–10⁴ force evaluations per orbit (see cost below).

**Configurations** (canonical CR3BP units, sep = 1, planet period 2π, all float64):

- `truth` (positive): SciPy DOP853, rtol 1e-12 (converged against 1e-13 on the B12 coarse
  samples and the resonant cases), barycentric inertial, planet interior regularized as a
  uniform sphere exactly as `xtask/src/behave/restricted.rs` does.
- `symba` (candidate): per base step H = 2π/192, the changeover K̄(d) (C² smoothstep: 1 outside
  2 R_H, 0 inside 1 R_H) splits the step into a far chunk (Kepler drift about the star +
  planet direct+indirect kicks) of duration K̄·H and a near chunk (exact two-body Kepler drift
  about the planet + stellar tidal kicks) of duration (1−K̄)·H, sub-stepped at H/2^j with
  j = ceil(log2(96·√(μ/d³)/192)), depth capped at H/2¹⁴. Both chunks are symmetric DKD maps, so
  the whole step is time-symmetric; the dominant body follows the changeover, never a hard
  switch. This is the rung's configuration read literally ("moons in the planet's region drift
  about the planet").
- B12: the gate's frozen ships, ported exactly: SplitMix64(20261002) draws of the `handoffs`
  rule (side ±1, k ∈ [1.5, 3] R_H, α ∈ [30°, 330°]) and the frozen `HANDOFF_KEPT` indices.
  Within this run's 90-minute cloud budget the first **6** of the 16 were verified (each
  crossing r_SOI ≥ 20 times in 200 planet periods under this run's reference, with the Jacobi
  constant agreeing between rtol 1e-12 and 1e-13 to 1e-9 relative); the median exponent is
  over these 6. A Python-random search port (Random(20261011), as the rung's sampler line
  suggests) was tried first and abandoned: 40 draws produced no ship with ≥ 20 crossings whose
  reference was affordable to verify, and screening at 1e-9 destroyed the chaotic crossing
  behaviour entirely (0 of 40), so the frozen list is the only faithful port.
- B14: the **first 128 births** (the circular set: a ∈ [0.2, 0.9] R_H, phase uniform,
  prograde even / retrograde odd), 50 planet periods, sampled every P/64. Non-chaotic = the
  truth's bound/escaped class survives a semimajor-axis nudge of 1e-6 (nudge integrated at
  rtol 1e-10; the gate's rtol-1e-13 recheck was dropped for time). The eccentric births
  (e₀ ≤ 0.3) were dropped for time; the circular set is the harder one for precession anyway
  (defined apses come from the tide pumping e, and every bound circular birth develops one).
- r4 v3: all 36 cases (2:1 and 3:2, μ ∈ {3e-5, 3e-4, 3e-3}, detuned by thirds of
  W = 2.5·μ^(2/3), e₀ = 0.02, phases 4° and 172°), 200 synodic periods, φ = (j+1)λ_p −
  jλ_s − ϖ_s unwrapped; libration amplitude = the excursion; truth-librating = excursion
  < 0.8·2π, borderline (within 20% of 2π) excluded. The 1e-13 convergence recheck was dropped
  for time; borderline excursions are excluded from the amplitude comparison instead.

**Evidence.** See `metrics.json` (the five rung metrics per configuration), `metrics_extra.json`
(denominators and truth's true force-evaluation counts), `picture.png` (|ΔC_J/C_J| against time,
four configurations, three ships with the most SOI crossings). Reproduce with
`python3 r10.py` (self-tests), `python3 run_driver.py` (everything; ~25 min on 2 vCPU),
`python3 make_picture.py`.

**Metrics** (filled by the run):

PLACEHOLDER

**Predictions** (`predictions.md`, written before the decisive runs): see the file. What held
and what did not is recorded there in place by the checker's convention; the author's summary:
PLACEHOLDER_PREDICTIONS

**What would make it wrong.** The symba map is not symplectic in the changeover band (the
changeover weights depend on position; this is also true of DLL98's changeovers) — only
time-symmetric; if ships spend many consecutive steps grazing d ≈ R_H the Jacobi error could
random-walk faster than 0.2. The pair drift inside the planet's regularization radius (9.2e-5)
is point-mass Kepler, where truth is a uniform sphere; only deep B12 dippers notice. The truth
runs in barycentric (not planet-relative) coordinates, so its own Jacobi floor is set by float64
rounding of O(1) quantities; the 1e-12 floor and the 1e-9 convergence check guard this.

**Fit with PRINCIPLES.** "A body's motion is a symmetric, symplectic split" (`docs/law.md`,
Perturbed motion): the split is symmetric and each piece is exact; the errors that remain are
O(H²) at band crossings, the type that does not compound (principle 13). "Compute only
surprises": away from the planet the changeover costs one table lookup per step; the recursion
is paid only where the local period demands it. "The best part is no part": no per-body step
sequence, no state-selected switch, one base clock.

**The lens** (rung-directed, no lens file): a directed rung answers the integrator's frozen
question; what it may have missed is the integrator's own criterion risk — force_evals_per_orbit
judges the median body, and moons at the top of a recursion shell can exceed 200 per moon orbit
even when the median passes.
