# Predictions, r12-seen-flux (written before the run; rung frozen at sha256 a6335a29…89ce)

Cases not tuned on: everything (no exploratory run has happened). Predictions from
1885's published record, my cumulant algebra, and the rung's own definitions.

- **P1 (negative fails hard).** `one-sample` p99_flux_error ≥ 0.30, driven by c2/c3
  (1885: ~40% median sprite error at β 0.9, σ_β 0.03; p99 over a path must exceed its
  median). It must fail the 0.05 license bar — if it passes, the rung is broken.
- **P2 (1885's law reproduces).** At the longitudinal end of c2 the one-sample error's
  spread matches CV(k⁴) = √(e^{16s²}−1), s = γ²σ_β, within ~15% (s = 0.158, CV ≈ 0.70).
  At the transverse end the sensitivity is 1, not γ², so the error collapses ~γ²-fold:
  head-on is where the player sees the failure (blind-spot guard: not exotic — head-on
  approach is a flyby).
- **P3 (candidate passes).** `mix-quad` p99_flux_error ≤ 1e-3 on all 7 cases (quadrature
  of an analytic integrand; c3's e^{4γ²σ≈6} dynamic range is why the node count adapts).
- **P4 (the bulk variant also fails).** The bulk readout N·k(bulk)⁴ errs by
  e^{8γ⁴σ_∥²}−1 ≈ 22% at c2's longitudinal end (under-report: one sample of the mean,
  no tail). Held as a diagnostic; if < 5%, my algebra is wrong somewhere.
- **P5 (moments alone die on shape).** A single-Gaussian moment readout (same Σ, Gaussian
  assumption) on c5 (ring β_rot 0.15) errs ≥ 2× (cumulant estimate ≈ 2.5× over-bright:
  ln I₀(4gβ) = 0.28 vs truncated 4g²β²/2 = 1.24 at the c5 transverse projection) but
  survives c4 (β_rot 0.05, ≈ 0.5%). This is the domain clause: unimodal Gaussian moments
  are licensed only where the 4th-cumulant term (4gσ)⁴·|κ−3|/24 is small; formations
  carry their shape. Diagnostic arm, not a frozen config.
- **P6 (instrument).** two_path_max_rel_diff ≤ 1e-12 (4-vector energy ratio vs the
  1/(γ(1−β⃗·n̂)) form — same algebra, different rounding).
- **P7 (ops).** per-ship ≈ N·(≈20) ≈ 8·10³; one-sample ≈ 20; mix-quad ≤ ~10⁴ worst case
  (c6's two squads) and flat in N — the dossier's cost line, not the fence.

What would make me distrust the run: one-sample passing the license bar (P1 violated),
or the two k paths disagreeing (P6 violated — then every number is instrument noise).
