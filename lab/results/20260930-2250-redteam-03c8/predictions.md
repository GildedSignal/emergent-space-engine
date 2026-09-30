# Predictions (written before the decisive experiment)

The falsifier (`falsifier.c`) compares the frozen r1 Binet-band model —
`u″ + (1 − 6u_k)·u = 1/L̃² − 3u_k²`, u and u′ continuous across bands,
u_k = geometric band centre, bands r_k = 2^(k/m) — against exact GR
(`u″ + u = 1/L̃² + 3u²`), M = 1, float64, RK4 at h_φ = 2×10⁻⁴ (halved-step
convergence checked on the worst case).

Held-out cases = everything outside r1's sampled box, which is
p ∈ [10, 1000] log-uniform, e ∈ [0, 0.7], p ≥ 6.5 + 2e for timelike seeds
and b ∈ [10, 1000] for light deflection. I have not run any of the numbers
below; they are derived from the 1/ω⁵ amplification of the band-midpoint
error near the ISCO/photon-sphere degeneracy (ω_k² = 1 − 6u_k → 0).

- **P-A (control, in-box).** m16 precession error < 1% for every grid point
  inside r1's box. This should reproduce r1's PASS and validate my harness.
- **P-B (timelike, out of box).** The 1%-precession-error contour for m16
  sits at periapsis r_p ≈ 6–7 for e ≤ 0.7 and moves outward to r_p ≈ 7–9 for
  e ∈ {0.9, 0.95}. So gravity-assist products and scattered-belt comets
  (e > 0.7, excluded by r1's sampler) fail the very gate r1 applies, and the
  failure region touches r1's box edge at high e (p ≈ 10, e ≈ 0.7).
- **P-C (light, out of box).** m16 deflection error > 1% for b ≲ 8 and
  > 10% somewhere in b ∈ (5.2, 6.5) (the photon-ring winding region);
  at b = 10 (r1's inner edge) the error lands between 0.2% and 1%,
  i.e. the gate sits just outside the cliff.
- **P-D (plunge quantization).** Near the plunge separatrix, banded and
  exact classifications disagree for some grid points; the banded plunge
  boundary jumps at band edges (≈ 4.4% in r for m16).
- **P-E (scaling).** Precession and deflection errors shrink ≈ ×4 per
  doubling of m (midpoint-rule-like, error ∝ band²).

What I expect to survive: the ring representation's self-similar bound on
the linearization term 3M(u − u_k)² (≤ (2.2%)² relative for m16) — weak-field
timelike behaviour should be robust at the 10⁻³ level, which is why r1 passed.
