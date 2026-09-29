# predictions.md — written before the decisive run

The case is frozen (no tuning possible), so these are derived, not measured.

Per-step energy error of forward Euler on this orbit, to O(h²):
dE/dstep = h² [ 1/(2r⁴) + |v|²/(2r³) − 3(x·v)²/(2r⁵) ] = h² (r − 0.375)/r⁴
(using v_r² = 2(E + 1/r) − L²/r² with L² = 3/4, E0 = −1/2), which is **positive
everywhere on the orbit** (r ∈ [0.5, 1.5]). Time-averaged: ⟨(r − 0.375)/r⁴⟩ =
(1/L T)∫(1/r − 0.375/r²) dθ ≈ 0.673, so ΔE ≈ 200 · h² · 0.673 ≈ **0.13 per
orbit**, monotonically outward. Predictions:

- **euler unbinds within ~4–15 orbits**: E crosses 0 early, so
  bound_fraction ≈ 4e-4 – 1.5e-3 → **B1 fails** (the kill).
- After escape the bracket turns negative and small; |dE| = E − E0 plateaus
  near its escape value (≥ 0.5) and then barely moves. Since every window
  starts at t ≥ 0.1 t_end = 1000 orbits, all 20 window maxima sit on that
  plateau: **energy_growth_exponent ≈ 0 (E1 passes despite the kill)** — the
  exponent criterion is blind to a drift that has already finished.
- **steps_per_orbit = 200.0 exactly** for both configurations (C1 passes);
  the frozen body is stepped too.
- euler keeps revolving while spiralling out: orbit_closure_count ≈ the
  escape orbit plus a few → **R1 passes**.
- **frozen**: E ≡ −0.5 (dE at the ~1e-16 floor → exponent exactly 0,
  B1/E1/C1 pass) but the position never changes, so the swept angle is 0 →
  **orbit_closure_count = 0, R1 fails**: the control has teeth.

Expected verdict: **KILL** (euler fails B1; frozen fails R1).
