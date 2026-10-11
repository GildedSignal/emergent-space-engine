# Predictions — 20261011-1729-scout-6765 (galaxy doll), frozen before the decisive run

Tuned on: case A (rp 1.0, ra 2.0, mid-disc) error-vs-panels; core scaling probe at
(ra/rc) = 0.40, 0.08, 0.04, 0.02; near-circular at r = 0.5, 1, 2, 4. Nothing below
was measured before freezing.

The decisive run is `python3 galaxy_doll.py full` (writes `galaxy-out.json`).

- **P1 (cost class).** Every held-out rosette case — B (rp 0.4, ra 3.0, e 0.76),
  D-with-cut (4.0, 7.5, crossing the Rg band edge), E (nucleus-mixed, rp 0.02) —
  reaches relative error ≤ 1e-6 on BOTH Δφ and Δt at ≤ 32 four-point panels
  (≤ 128 nodes per half-cycle), and ≤ 1e-9 at ≤ 64 panels.
- **P2 (negative control, the band cut).** D without the cut at Rg, at 32 panels,
  is ≥ 10× worse than D with the cut (the C¹ force kink inside a panel degrades
  Gauss–Legendre to algebraic convergence; the plane's band-edge cuts are required
  here too).
- **P3 (core control, held out).** rp 0.0006, ra 0.0024 (ra/rc = 0.048):
  Δφ/π − 1 ≈ 1.4e-4, from the measured quadratic law (9.995e-5 at ra/rc 0.04);
  the harmonic limit Δφ → π (closed centred ellipses) is approached as (ra/rc)².
- **P4 (flat-zone control, held out).** Near-circular at r = 3.0:
  Δφ/π ∈ [1.4139, 1.4141] (monotone approach to √2 = 1.414214 between the
  measured 1.413760 at r = 2 and 1.414091 at r = 4).
- **P5 (error type).** The compiled advance over N = 10⁴ cycles by pure additions
  differs from N·Δφ by machine rounding only (≤ 1e-9 rad total); per-cycle error
  at 32 panels ≤ 1e-9 rad, so the re-key interval for a 1e-4 rad floor is
  ≥ 1e5 cycles. (Linear accumulation, identical every cycle — the r2/B5 error
  type, not a walk.)
- **P6 (scatter transits).** Compiled transit vs leapfrog (independent truth):
  deflection agrees within 1e-4 rad for both β∞ = 0.9 cases, within 1e-3 rad for
  β∞ = 0.3 and the slow case; Δt within 1e-4 relative; the leapfrog's own
  dt-convergence (40k → 80k steps) is below those bars. Known risk: if the
  compiled-vs-leapfrog deflection error comes out ≈ 2× the deflection itself,
  my sign convention for the compiled final velocity is wrong (a code bug, to
  be disclosed and fixed, not a physics result). β∞ = 0.9 bending at b = 0.5 is
  small (~2e-2 rad): at high c the route is nearly straight.
- **P7 (GR seam).** For a Sgr A*-like nucleus (4×10⁶ M_sun, v₀ 220 km/s,
  Θ = 1e-3 rad): seam(H = 1e7 s) ≈ 3×10³ r_s; seam(1e11 s) ≈ 1×10⁵ r_s ≈
  0.04 pc. The seam sits OUTSIDE the Newtonian sphere of influence
  (r_SOI = GM/v₀² ≈ 9×10² r_s with v₀ = 220 km/s) by a factor ~3–130 across
  horizons — i.e. the hole doll's outer edge is set by accumulated GR precession
  (horizon-dependent), not by force dominance — but it stays ≥ 4 orders of
  magnitude below the disc scale (8 kpc ≈ 2×10¹⁰ r_s), so GR is deleted above
  the hole's doll at every playable horizon. Seam/r_SOI scales ≈ M^1.1, so a
  10⁸ M_sun game nucleus pushes the seam to ~10⁶ r_s (tens of pc) — still
  inside the bulge.
- **P8 (frozen disc).** A Milky-Way-like disc (8 kpc, 220 km/s, T ≈ 2.2×10⁸ yr)
  completes < 0.01 orbits per 100-hour session at every rtf ≤ 1e8 (5×10⁻³ at
  rtf 1e8, 5×10⁻⁵ at rtf 1e6). Meanwhile the player's news cone after 100 h at
  rtf 1e6 reaches ~3.5 kpc: at galactic scale, dynamics travel with the player
  and the news, never with the disc.
- **P9 (compile cost).** Python-level compile ~30–300 µs at 32 panels on this
  cloud x86 box (order of magnitude only); the load-bearing number is the panel
  count (P1), which lands in the same class as the plane's measured ~140-panel
  kick compiles.
