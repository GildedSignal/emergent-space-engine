# predictions.md — 20261009-1345-scout-9c12

Written BEFORE any run of the decisive configurations. Question: does the
player-caused influence cascade (Julien's "influence of influenced… a series
that converges i bet", OC; the growing-light-cone risk in HANDOFF) stay
bounded, and what decides it?

Model (derived by hand, not fitted): a scar is a body's position-equivalent
error ε (relative units). At an encounter with impact parameter b, the impulse
is I = 2Gm/(b·v_rel), so a partner's position error ε maps to a child error
ε_child = f(b)·ε·|cos θ| with f(b) = 2Gm·τ_drift/(b²·v_rel). Belt numbers:
m = 1e12 kg, v_rel = 5 km/s, τ_drift = 1e7 s ⇒ C_a = 2.67e5 m², b uniform in
b² on [1 km, 2.6e5 m] (mutual Hill), so f ∈ [3.9e-6, 0.267]. Planet flyby
(m = 1e25 kg, b ∈ [1.5, 3.2]·2.5e7 m, v = 15 km/s): f_p ∈ [139, 634]. Quantum
q = certificate floor (base 1e-6 relative). Encounter rate 1.1/orbit (r8's
measured belt rate). n₀ = 8 scarred ships at ε₀ = 8e-4 (a 30 m/s burn drifted
half an orbit), N = 1e6 bodies. Live = ε ≥ q; below q the influence
accumulates on the partner (principle 6) and can cross q later.

Hand-derived consequences (predictions, not tuned):
- Birth probability per encounter for a parent at ε: P = C_a·ε/(2q·b_max²)
  (while < 1). For ε₀ = 8e-4, q = 1e-6: P = 1.6e-3.
- Children are born near the floor (ε_child/q has density ∝ x⁻²), so their
  fertility is ~1e-5/orbit: second generation negligible. Parents never die
  and never shrink: the cascade is a constant linear pump, rate ∝ n_live·ε/q.

Predictions per configuration (T = 100 orbits):

- **P1 base** (pure belt, q=1e-6, no flybys, no chaos): births_cum(100)
  ∈ [0, 4]; n_live(100) ∈ [8, 13]; births/orbit in [0.005, 0.05] and NOT
  growing; n_dusted(100) ∈ [700, 1100] (≈ 8 × 1.1 × 100 minus births).
  Verdict for the bet: subcritical (series converges) at belt scale.
- **P2 crossers** (planet flybys at ν_p = 1e-1 and 1e-2 per orbit): every
  flyby of a live body births (f_p ≥ 139 ≫ q/ε), so n_live grows
  exponentially, n_live(t) ≈ 8·e^{ν_p·t}. Predict n_live(100) ∈ [8e4, 4e5]
  for ν_p = 1e-1; n_live(100) ∈ [15, 35] for ν_p = 1e-2; fitted exponent
  within ±30% of ν_p. Saturation extrapolates to T_sat ≈ ln(N/8)/ν_p orbits.
  Verdict: supercritical — the bet fails wherever any body reaches an
  amplifier, with timescale ln N / ν_p.
- **P3 fine floor** (q = 1e-9, pure belt): P per encounter ≥ 1 ⇒ every
  encounter births; children average ~13q (near-sterile). Predict linear
  growth: n_live(100) ∈ [500, 2000]; births/orbit(90–100) ∈ [6, 12], constant
  (no acceleration). Verdict: unbounded linear, not explosive.
- **P4 chaos** (λ = 0.1/orbit compounding on every error, q = 1e-6): dust
  amplifies as e^{λt} and crosses q (~23 orbits for 1e-7 dust); live ε grows
  toward the 0.5 cap. Predict super-linear: births/orbit(90–100) ≥ 5×
  births/orbit(10–20); n_live(100) ∈ [100, 1e4]. Verdict: supercritical.
- **P5 fleet** (n₀ = 1e4 members at encounter rate 20/orbit, rest belt):
  first-generation pumping ≈ 1e4·20·1.6e-3 ≈ 316 births/orbit into a
  near-sterile halo. Predict n_live(100) ∈ [2e4, 5e4]; births/orbit ≈ 316
  ± 30% constant; T_sat ≈ N/316 ≈ 3e3 orbits. Verdict: the belt saturates.

Kill rule (pre-registered): the bet ("the series converges") is FALSIFIED for
a configuration if n_live grows super-linearly or births/orbit does not decay
to a constant bounded rate; it HOLDS only where total births stay finite and
small relative to N at every horizon. If P1 shows n_live(100) > 100 or
accelerating births, the bet fails at belt scale already.

Confounds I accept: scalar ε (no vector phase), linearized transfer (breaks
at f ≫ 1, B13's chaotic-scattering domain — order of magnitude only), no
dust→dust propagation (undercounts slow channels, i.e. biased pro-bet),
partner sampling ignores live-live encounters except through saturation.
