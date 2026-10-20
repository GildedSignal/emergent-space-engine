# Rung r12: the aggregate's seen flux (the dispersion channel, 1885)

Frozen by run 20261019-2339-redteam-7bcf on 19 October 2026, before its run (the 4ff1
pattern: the rung lives in the run folder until the integrator adopts it into
`lab/rungs/`). Design: [docs/representation.md](../../../../docs/representation.md) §2
("An emitter carries a spectral type… beaming k⁴"; "Aggregates are one sample each") —
the flux half of L59, unguarded after 1885's refutation (occlusion is r11's arm).

**Question.** A fleet is seen by the player at bulk β with internal velocity dispersion.
Its seen flux is Σᵢ kᵢ⁴ (exact SR, per member). What must the aggregate readout compute
so the fleet-total flux stays within law tolerance of the exact per-ship sum — and what
does it cost per fleet per frame? The letter's "one sample each" is the negative; the
moment/formation representation (squad Gaussians integrated by quadrature over the full
nonlinear k, formations over their own geometry) is the candidate.

**Configurations.**
- `per-ship` (positive): the truth itself — Σᵢ kᵢ⁴ over all members, computed twice by
  two independent k paths (energy ratio from 4-vectors, and 1/(γ(1−β⃗·n̂))); the reported
  error is path B against path A.
- `one-sample` (negative): the letter's L59 readout — member 0's k⁴ times N.
- `mix-quad` (candidate): the aggregate readout. The fleet carries, per squad, its bulk
  velocity and velocity-dispersion tensor, and per formation its shape; the readout
  integrates k⁴ over that description by Gauss–Hermite quadrature (Gaussian squads) or
  by the periodic trapezoid (a rotating ring formation), against the full nonlinear k.

**Cases** (frozen; members drawn with Python `random.Random(20261019)`; N = 400, equal
emit luminance 1; the observer direction n̂ sweeps θ ∈ [0.02°, 179.98°] over 2001
samples at fixed bulk speed — the transit sweep of r11/c78d, flux channel only):
- c1 Gaussian isotropic σ_β 0.03, bulk β 0.5 (player speed)
- c2 Gaussian σ_β 0.03, β 0.9 (1885's failing case)
- c3 Gaussian σ_β 0.03, β 0.99 (γ 7.1: the amplification 4γ²σ ≈ 6)
- c4 rotating ring formation, tangential β_rot 0.05, bulk β 0.9
- c5 rotating ring, β_rot 0.15, bulk β 0.9
- c6 two squads at δβ_∥ ±0.05 (bimodal), bulk β 0.9
- c7 Gaussian σ_β 0.10, β 0.5 (wide dispersion at player speed)

**Metrics,** one set per configuration:
- `p99_flux_error`: max over the 7 cases of the p99 over the path of |F/F_per-ship − 1|.
- `two_path_max_rel_diff`: max over members and samples of |k_A − k_B|/k_A (instrument).
- `ops_per_fleet_frame`: counted arithmetic operations of the readout at N = 400, worst
  case over the frozen cases (one unit per add/mul/div/sqrt/exp; the anti-absurdity
  fence — the constant-versus-linear scaling is reported in the dossier, not gated).

**Output.** `metrics.json` plus the per-case error table and the 1885 closed-form check
(its CV(k⁴) = √(e^{16s²}−1), s = γ²σ_∥, at the longitudinal end of the sweep).

```configs
per-ship positive
one-sample negative
mix-quad candidate
```

```criteria
instrument type two_path_max_rel_diff <= 1e-9
license type p99_flux_error <= 0.05
fence cost ops_per_fleet_frame <= 20000
```
