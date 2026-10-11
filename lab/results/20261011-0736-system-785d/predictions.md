# Predictions — run 20261011-0736-system-785d (lens: whole system)

Written BEFORE the decisive scans, after only: (i) the cheap-side quadrature (quad.json:
pdot_coh, varpidot_sec, theta_dot per detuning — no truth involved), (ii) instrument
calibration on ONE case (2:1, mu=1e-3: controls printed = outer-detuning bands and the
exact-resonance negative control), (iii) the mu=0 and far controls.
All later cases (2:1 mu=3e-4, 3e-3; 3:2 both) are HELD OUT from everything below.

## The certificate under test (one line, cheap-path only)

    excursion(delta) = 2 * pdot_coh / |theta_dot(delta)|          (circulating)
    T_pump          = kappa * q_e / pdot_coh                      (inside the coherent zone)
    theta_dot = (j+1) n2 - j n1 - varpidot_sec ;  pdot_coh = the slow-phase (resonant)
    amplitude of de/dt from a lambda1-quadrature at fixed resonant angle.

No width constant W, no classification step: the engine's compiled frequencies and kick
quadrature give excursion; a chosen quantum q_e (a design floor, like the spatial floor)
decides the switch and the cadence. This is the same arithmetic as the jet re-anchor
(sqrt(floor/C): time for accumulated drift to reach the quantum) and the slack skin.

## Calibration seen so far (2:1, mu=1e-3)

- band at delta=+0.032 (outer control): 0.037 measured vs certificate 0.050 -> F = 0.74.
- exact resonance: fails (negative control passes), mean drifts.
- mu=0: e bounded, ringing exactly (n1 dt)^2/2, zero drift.
- far controls (2.15, 1.9): no mean drift (positive side).

## Predictions (held-out cases: 2:1 mu=3e-4 and 3e-3; 3:2 mu=3e-4 and 1e-3)

- **P1 (excursion law).** For every (j, mu, delta) whose truth circulates
  (|theta_net| > 2 pi), the running-mean e-band satisfies
  F = band_measured / (2 pdot_coh/|theta_dot|) in [0.3, 3].
- **P2 (no per-case tuning).** The median of F over circulating systems, per (j, mu),
  lies in [0.5, 2] — i.e. one O(1) shape factor, not a new fit per case.
- **P3 (pump time).** At exact resonance, the time for the running mean of e to leave
  the design band q_e = 0.01 is T_pump in [1, 4] x (q_e / pdot_coh), for all four
  held-out (j, mu) — kappa absorbs the phase feedback that r4 measured at ~2x.
  With quad numbers (exact): 2:1 mu=3e-4 pdot=7.31e-4 -> T_pump in [14, 55];
  2:1 mu=3e-3 pdot=7.31e-3 -> [1.4, 5.5]; 3:2 mu=3e-4 pdot=1.98e-3 -> [5, 20];
  3:2 mu=1e-3 pdot=6.58e-3 -> [1.5, 6]. Linearity in q_e is part of P3.
- **P4 (boundary map, per quantum).** For every q_e on the recorded grid:
  (a) NO measured mean-drift failure at any (delta, q_e) where the certificate's
  excursion 2 pdot/|theta_dot| < q_e / 2 (a failure there kills the certificate);
  (b) at delta = 0 the failure time scales linearly in q_e (part of P3);
  (c) the certificate's boundary delta*(q_e) (where excursion = q_e) is within a factor
  3 of the measured outermost failing detuning, whenever delta*(q_e) lies inside the
  scanned range [0.0005, 0.032]. FALSIFIER: if the mean-drift boundary sits at the
  libration-zone edge with a different mu-scaling while the certificate boundary is
  far inside or outside, P4 fails and the excursion law survives only as the wiggle
  amplitude, not the gate.
- **P5 (sign check on varpidot_sec).** The excursion/boundary is asymmetric in +-delta;
  the asymmetry direction implied by the measured bands matches the sign of varpidot_sec
  in theta_dot as computed on the cheap path. If the truth's asymmetry is opposite, the
  cheap-path precession sign is wrong and I report it.

## What would kill the certificate outright

- F leaving [0.3, 3] systematically (not at the chaotic boundary), or scaling with mu
  (it must not: both band and 2pdot/|theta_dot| are linear in mu).
- T_pump uncorrelated with q_e/pdot_coh across the two orders of magnitude in mu.
- The boundary following W = 2.5 mu^(2/3) (the B17 scan convention) rather than the
  certificate's mu-linear map — that would say the convention encodes real physics
  (Hill/overlap scaling) that the kick-quadrature certificate misses.

## Machine

Linux x86, 8 vCPU shared runner, numpy float64; orders of magnitude only (cloud
timings). Each stage < 60 s wall.
