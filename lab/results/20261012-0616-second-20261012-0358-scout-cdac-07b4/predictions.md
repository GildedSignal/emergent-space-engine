# Predictions — 20261012-0616-second-20261012-0358-scout-cdac-07b4

Written before the decisive run (`python3 work/hlive_real.py`). A pilot at
N=300/2 orbits and a timing probe at N=1500/2 orbits validated only the
machinery (no crashes, determinism, K scales linearly with surface density,
b spans 1.8e-5..0.06); no quantity below was tuned on them. The toy's
stored metrics (orig-metrics.json) and the checker's refit (alpha = -0.816
over eps in [1e-2,1e-4] at m=1e-10) were read before writing this.

The decisive question: does the scout's live-memory law (memory follows the
surprise rate; s(eps) ~ eps^-0.8; sub-linear inflow; belt no 10^9 risk)
survive real conjunction geometry — real b distribution, Gauss-mapped
correlated (da, de), kick recurrence on the same pair, native stirring —
or does real geometry fatten the escape tail?

- **P1 (headline, matched-rate comparison).** At m=1e-10, eps=1e-3, the
  real-geometry s_part (C1, kicks/body/orbit ~ 59 measured) is within a
  factor 3 of the toy's s_part replayed at the SAME kick rate
  (toy_matched_rate, gamma0 = K_real). If real geometry fatters the tail
  more than 3x, the scout's MB/h line is wrong at its root.
- **P2 (alpha).** alpha_partial (fitted ONLY on rows with D/N < 0.5) at
  m=1e-10 lies in [0.4, 1.6] (the toy's 0.8 inside; the power-law survival
  lever survives real geometry).
- **P3 (inflow exponent).** The D(t) inflow exponent under real geometry
  lies in [0.6, 1.05]: sub-linear accumulation survives; coherent
  same-pair kicks do not make it super-linear.
- **P4 (concentration is real but bounded).** repeat-pair kick fraction
  >= 0.05 and per-body kick-count dispersion (var/mean) > 1.2: the toy's
  independence assumption is false, but its effect on s is bounded (P1).
- **P5 (stirring, the toy's failed P5, now native).** At m=1e-10 sigma_e
  grows < 2x over 20 orbits (no runaway at belt mass); at m=1e-6 it grows
  >= 1.5x within 10 orbits (real viscous stirring at planetary scatterer
  mass).
- **P6 (saturation store vs B18).** At C3 (m=1e-6) D/N >= 0.9 within 10
  orbits, and the honest full store (Elias-Fano map + delta entropy) is
  <= 2x floor + 2 bytes per live body (B18 holds at saturation), total at
  10^9 <= 4.29 GB (the live budget).
- **P7 (10^9 rate line at fixed surface density).** Extrapolated MB per
  play-hour (R1, 16 B) at 10^9 bodies, m=1e-10, eps=1e-3, is <= 50 MB/h
  at every measured surface density (1e4..9e4 /AU).
